import json

import flask
import httplib2
import requests

from apiclient import discovery
from apiclient.discovery import build


from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
'https://www.googleapis.com/auth/drive.readonly']
CLIENT_SECRET_FILE = 'mainapp/static/client_id.json'
REDIRECT_URI = 'http://www.example.com/oauth2callback'
APPLICATION_NAME = 'GFunk\'s Mail Merger'


from mainapp.main import app
import mainapp.auth
from mainapp.actions import *


@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for("get_credentials"))
    access_token = json.loads(flask.session['credentials'])['access_token']
    response = requests.get("https://www.googleapis.com/drive/v3/files",
        params={"mimeType": "application%2Fvnd.google-apps.spreadsheet",
        "access_token": access_token})
    sheets_list = [sheet for sheet in response.json()['files'] if sheet['mimeType'] == "application/vnd.google-apps.spreadsheet"]
    sheet_labels = load_google_sheet("1Nc4ja07OY6XCD3HTC6YnrapL_ks1418RSQXy6kY5HHo")
    return str(sheets_list) + "\n\n\n" + str(sheet_labels)

@app.route("/mailmerge")
def mail_merge():
    if 'credentials' in flask.session:
        flask.send_static_file("mailmerge.html")
    else:
        return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
        import uuid
        app.secret_key = str(uuid.uuid4())
        app.debug = False
        app.run()