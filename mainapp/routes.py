import json

import flask
import httplib2

from apiclient import discovery
from apiclient.discovery import build
from oauth2client import client

from . import auth

@app.route('/')
def index():
    return flask.render_template("templates/index.html")

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
            'client_secrets.json',
            scope='https://www.googleapis.com/auth/drive.metadata.readonly',
            redirect_uri=flask.url_for('oauth2callback', _external=True),
            include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()