[![Build Status](https://travis-ci.org/estherh5/nobugs_api.svg?branch=master)](https://travis-ci.org/estherh5/nobugs_api)
[![codecov](https://codecov.io/gh/estherh5/nobugs_api/branch/master/graph/badge.svg)](https://codecov.io/gh/estherh5/nobugs_api)

# NoBugs API
NoBugs! is a pest control supply company in Philadelphia, PA. My father founded the company in 1983, inspired by his father's pest control supply business founded in 1935. My parents now co-own the company and have largely kept their business off of the internet, advertising through paper and word of mouth. This API is built for customers to add their email addresses to the NoBugs! mailing list, which is stored on a Google Sheets spreadsheet.

## Setup
1. Create a project on Google Cloud Platform's App Engine.
2. Clone this repository on your Cloud instance.
3. Enter a virtual environment on your Cloud instance (`virtualenv env`) and install dependencies into a lib folder that will be used during deployment (`pip install -t lib -r requirements.txt`).
4. Create a Google Sheets spreadsheet to store email addresses.
5. Enable the [Google Sheets API](https://console.developers.google.com/apis/api/sheets) and the [Google Drive API](https://console.developers.google.com/apis/api/drive) for your Cloud project.
6. Create a [service account key](https://console.cloud.google.com/apis/credentials) for your App Engine default service account.
7. Set the following environment variables for the API in the app.yaml file:
    * `ENV_TYPE` for the environment status (set this to "Dev" for testing or "Prod" for live)
    * `SPREADSHEET` for the Google Sheets spreadsheet ID (found in the spreadsheet URL; i.e., "https://docs.google.com/spreadsheets/d/<ID\>")
    * `RANGE` for the Google Sheets spreadsheet range where email addresses are stored (e.g., "A:A")
8. Start your server by running `gcloud app deploy` on the Cloud CLI.

## API
To post an email address to the NoBugs Google Sheets spreadsheet, a client can send a request to the following endpoint:

\
**POST** /api/email
* Post email address by sending the jsonified email address in the request body. Note that email addresses that are already included on the spreadsheet will not get added again.
* Example request body:
```javascript
{
    "email": "test@test.com"
}
```
