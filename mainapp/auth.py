from __future__ import print_function
import os
import httplib2

import flask

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'static/client_secret.json'
APPLICATION_NAME = 'GFunk\'s Mail Merger'
REDIRECT_URI = 'http://www.example.com/oauth2callback'

def get_credentials():
    """ Obtains user's OAuth credentials """
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())


def oauth2_call():
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRET_FILE,
        scope=SCOPES,
        redirect_uri=flask.url_for('oauth2callback', _external=True),
        include_granted_scopes=True)

    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()



