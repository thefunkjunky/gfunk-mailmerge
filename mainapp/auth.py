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

def get_credentials():
    """ Obtains user's OAuth credentials """

    flow = client.flow_from_clientsecrets(
        CLIENT_SECRET_FILE,
        scope=SCOPES,
        redirect_uri='http://localhost:8081/')


