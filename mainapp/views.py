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
# from mainapp.auth import get_credentials, oauth2_call

@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        # return str(json.loads(flask.session['credentials']))
        access_token = json.loads(flask.session['credentials'])['token_response']['access_token']
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http_auth,
                                discoveryServiceUrl=discoveryUrl)

        # Get a list of spreadsheets using Google Drive REST API
        response = requests.get("https://www.googleapis.com/drive/v3/files",
            params={"mimeType": "application%2Fvnd.google-apps.spreadsheet",
            "access_token": access_token})

        sheets_list = [sheet for sheet in response.json()['files'] if sheet['mimeType'] == "application/vnd.google-apps.spreadsheet"]

        return str(sheets_list)


@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
            CLIENT_SECRET_FILE,
            scope=SCOPES,
            redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))


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