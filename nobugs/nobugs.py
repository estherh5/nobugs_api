import os
import re
import threading
import time

import google.auth
from flask import make_response, request
from googleapiclient import discovery


# Longest address RFC 5321 allows
MAX_EMAIL_LENGTH = 254

# Sign-ups allowed per client IP per window (app.yaml pins one instance, so
# this in-memory count is the whole count)
RATE_LIMIT = 5
RATE_WINDOW_SECONDS = 60 * 60

_attempts = {}
_attempts_lock = threading.Lock()

EMAIL_PATTERN = re.compile(r'^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)'
    r'*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$')


def text_response(body, status):
    response = make_response(body, status)
    response.mimetype = 'text/plain'
    return response


def client_ip():
    # App Engine puts the caller's address in this header
    return (request.headers.get('X-Appengine-User-Ip')
        or request.remote_addr or 'unknown')


def rate_limited(ip):
    now = time.monotonic()
    with _attempts_lock:
        # Drop expired entries so the table cannot grow without bound
        for key in [k for k, v in _attempts.items()
                if now - v[-1] > RATE_WINDOW_SECONDS]:
            del _attempts[key]
        recent = [t for t in _attempts.get(ip, [])
            if now - t <= RATE_WINDOW_SECONDS]
        if len(recent) >= RATE_LIMIT:
            _attempts[ip] = recent
            return True
        _attempts[ip] = recent + [now]
        return False


def create_email():
    # Request should contain:
    # email <str>
    data = request.get_json(silent=True)

    # Return error if request is missing data
    if (not isinstance(data, dict) or 'email' not in data):
        return text_response('Request must contain email address', 400)

    # Return error if email address is not a string
    if not isinstance(data['email'], str):
        return text_response('Email address must be a string', 400)

    # Remove all whitespace from email address
    email = re.sub(r"\s+", "", data['email'], flags=re.UNICODE)

    # Validate email address format
    if len(email) > MAX_EMAIL_LENGTH or not EMAIL_PATTERN.match(email):
        return text_response('Invalid email address', 400)

    if rate_limited(client_ip()):
        return text_response('Too many requests', 429)

    # Get Google Sheets API credentials from the App Engine service account
    credentials, _ = google.auth.default(
        scopes=['https://www.googleapis.com/auth/spreadsheets'])

    # Initiate Google Sheets service
    service = discovery.build('sheets', 'v4', credentials=credentials,
        cache_discovery=False)

    # The ID of the spreadsheet to update
    spreadsheet_id = os.environ['SPREADSHEET']

    # The A1 notation of a range to search for data in the spreadsheet
    range_ = os.environ['RANGE']

    values_response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_
        ).execute()

    if [email] in values_response.get('values', []):
        return text_response('Email address already on mailing list', 409)

    # RAW stores the text as-is, so an address like "=HYPERLINK(...)"@x.com
    # can never be evaluated as a formula in the owners' spreadsheet
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': [[email]]}
        ).execute()

    return text_response(email, 201)
