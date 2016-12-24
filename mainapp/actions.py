import json

import flask
import httplib2
import requests

from apiclient import discovery
from apiclient.discovery import build

from oauth2client.client import GoogleCredentials

from mainapp.main import app
import mainapp.views

def list_google_sheets():
    """ Lists all files in Google Drive that are a Google Spreadsheet """
    access_token = json.loads(flask.session['credentials'])['access_token']
    response = requests.get("https://www.googleapis.com/drive/v3/files",
        params={"mimeType": "application%2Fvnd.google-apps.spreadsheet",
        "access_token": access_token})
    sheets_list = [sheet for sheet in response.json()['files'] if sheet['mimeType'] == "application/vnd.google-apps.spreadsheet"]
    return sheets_list

def load_google_sheet(sheet_id):
    """ Returns Google Spreadsheet with given sheet_id """
    try:
        credentials = GoogleCredentials.from_json(flask.session['credentials'])
    except Exception as e:
        return flask.redirect(flask.url_for("index"))

    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    label_range = '1:1'
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=label_range).execute()
    sheet_labels = result.get('values', [])

    if sheet_labels:
        values = sheet_labels

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))

    return values
