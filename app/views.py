import datetime
import flask
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from app import app

client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=client.key('visit'))
    entity.update({
        'timestamp': dt
    })
    client.put(entity)

def fetch_times(limit):
    return
    query = client.query(kind='visit')
    query.order = ['-timestamp']
    return query.fetch(limit=limit)

@app.route('/')
def index():
    # id_token = flask.request.cookies.get('token')
    return flask.render_template('index.html', header='Driving is better together.')

@app.route('/index')
def index_():
    return flask.redirect(flask.url_for('index'))

@app.route('/payment')
def payment():
    return flask.render_template('payment.html', header='Please make a payment')

@app.route('/login')
def login():
    id_token = flask.request.cookies.get('token')
    error = None
    claims = None
    times = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, requests.Request())
        except ValueError as exc:
            error = str(exc)
        store_time(datetime.datetime.now())
        times = fetch_times(10)
    return flask.render_template('login.html', title='login')

@app.route('/terms')
def terms():
    return flask.render_template('terms.html', title='terms of service')

@app.route('/privacy')
def privacy():
    return flask.render_template('privacy.html', title='privacy policy')
