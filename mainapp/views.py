import json

import flask
import httplib2

from apiclient import discovery
from apiclient.discovery import build
from oauth2client import client


from mainapp.main import app
from mainapp.auth import get_credentials

@app.route("/")
def index():
    if 'credentials' in flask.session:
        return flask.redirect(flask.url_for('mail_merge'))
    return app.send_static_file("index.html")

@app.route("/auth")
def auth():
    get_credentials()

@app.route("/auth")
def oauth2callback():
    oauth2_call()
    return flask.redirect(flask.url_for('mail_merge'))

@app.route("/mailmerge")
def mail_merge():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()