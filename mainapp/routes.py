import json

import flask
import httplib2

from apiclient import discovery
from apiclient.discovery import build
from oauth2client import client

from .auth import get_credentials, oauth2_call

@app.route('/')
def index():
    get_credentials()
    return flask.render_template("templates/index.html")

@app.route('/oauth2callback')
def oauth2callback():
    oauth2_call()
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()