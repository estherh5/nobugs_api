[![Build Status](https://travis-ci.org/estherh5/nobugs_api.svg?branch=master)](https://travis-ci.org/estherh5/nobugs_api)
[![codecov](https://codecov.io/gh/estherh5/nobugs_api/branch/master/graph/badge.svg)](https://codecov.io/gh/estherh5/nobugs_api)

# NoBugs API
NoBugs! is a pest control supply company in Philadelphia, PA. My father founded the company in 1983, inspired by his father's pest control supply business founded in 1935. My parents now co-own the company and have largely kept their business off of the internet, advertising through paper and word of mouth. This API is built for customers to add their email addresses to the NoBugs! mailing list, which is stored on a Google Sheets spreadsheet.

## Setup
1. Create a project on Google Cloud Platform's App Engine.
2. Create a Google Sheets spreadsheet to store email addresses and share it (Editor) with the App Engine default service account (`<project>@appspot.gserviceaccount.com`). The API authenticates as that account, so no key file is needed.
3. Enable the [Google Sheets API](https://console.developers.google.com/apis/api/sheets) for your Cloud project.
4. Copy `app.yaml` to `app.prod.yaml` (gitignored) and fill in:
    * `ENV_TYPE` for the environment status (set this to "Dev" for testing or "Prod" for live)
    * `SPREADSHEET` for the Google Sheets spreadsheet ID (found in the spreadsheet URL; i.e., "https://docs.google.com/spreadsheets/d/<ID\>")
    * `RANGE` for the Google Sheets spreadsheet range where email addresses are stored (e.g., "A:A")
5. Deploy with `gcloud app deploy app.prod.yaml --version <name> --no-promote`, check it at `https://<name>-dot-<project>.<region>.r.appspot.com/api/email`, then move traffic with `gcloud app services set-traffic default --splits <name>=1`.

Tests: `pip install -r requirements.txt && ENV_TYPE=Dev SPREADSHEET=x RANGE=A:A python -m unittest discover`.

## API
To post an email address to the NoBugs Google Sheets spreadsheet, a client can send a request to the following endpoint:

\
**POST** /api/email
* Post email address by sending the jsonified email address in the request body. Note that email addresses that are already included on the spreadsheet will not get added again (409), addresses are stored as plain text (never evaluated as formulas), each IP may sign up 5 times an hour (429), and browsers may call it only from https://nobugsphilly.com.
* Example request body:
```javascript
{
    "email": "test@test.com"
}
```
