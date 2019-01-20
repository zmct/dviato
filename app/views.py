import datetime
import flask
from google.auth.transport import requests
import google.oauth2.id_token
from app import app

def get_login():
    id_token = flask.request.cookies.get('token')
    claims = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, requests.Request())
            logged = True
        except ValueError:
            logged = False
    else:
        logged = False
    return logged

@app.route('/')
def index():
   return flask.render_template('index.html', logged=get_login(), header='Driving is better together.')

@app.route('/index')
def index_():
    return flask.redirect(flask.url_for('index'))

@app.route('/login')
def login():
    return flask.render_template('login.html', logged=get_login(), title='login')

@app.route('/terms')
def terms():
    return flask.render_template('terms.html', logged=get_login(), title='terms of service')

@app.route('/privacy')
def privacy():
    return flask.render_template('privacy.html', logged=get_login(), title='privacy policy')
