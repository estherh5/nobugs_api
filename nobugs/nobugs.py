import httplib2
import os
import re

from flask import make_response, request
from googleapiclient import discovery
from google.auth import app_engine


def create_email():
    # Request should contain:
    # email <str>
    data = request.get_json()

    # Return error if request is missing data
    if (not data or 'email' not in data):
        return make_response('Request must contain email address', 400)

    # Return error if email address is not a string
    if not isinstance(data['email'], str):
        return make_response('Email address must be a string', 400)

    # Remove all whitespace from email address
    email = re.sub(r"\s+", "", data['email'], flags=re.UNICODE)

    # Validate email address format
    pattern = re.compile(r'^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)'
        r'*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$')

    if not pattern.match(email):
        return make_response('Invalid email address', 400)

    # Get Google Sheets API credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive']

    credentials = app_engine.Credentials(scopes=scope)

    # Initiate Google Sheets service
    service = discovery.build('sheets', 'v4', credentials=credentials)

    # The ID of the spreadsheet to update
    spreadsheet_id = os.environ['SPREADSHEET']

    # The A1 notation of a range to search for data in the spreadsheet
    range_ = os.environ['RANGE']

    # How the input data should be interpreted (as though a user entered it)
    value_input_option = 'USER_ENTERED'

    # How the input data should be inserted (at the end of the data range)
    insert_data_option = 'INSERT_ROWS'

    # Value to be added to spreadsheet (email address)
    value_range_body = {
        "values": [
            [email]
        ]
    }

    gs_request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body
        )

    response = gs_request.execute()

    return make_response(email, 201)
