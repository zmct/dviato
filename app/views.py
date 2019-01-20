import random
import datetime
import flask
import flask_restful
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from app import app, api

def get_login():
    id_token = flask.request.cookies.get('token')
    claims = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, requests.Request())
            uid = claims['user_id']
        except ValueError:
            uid = None
    else:
        uid = None
    return uid

client = datastore.Client()

class UserInfo(flask_restful.Resource):
    def get(self, uid):
        if uid == get_login():
            entity = client.get(client.key('user', uid))
            return {key:entity[key] for key in entity}
        else:
            return {}
    def put(self, uid, *args, **kwargs):
        print(flask.request.get_json())
        if uid == get_login():
            entity = datastore.Entity(client.key('user', uid))
            entity.update(flask.request.get_json())
            client.put(entity)
    def patch(self, uid, **kwargs):
        if uid == get_login():
            entity = client.get(client.key('user', uid))
            for arg in kwargs:
                entity[arg] = kwargs[arg]
            client.put(entity)
    def delete(self, uid, **kwargs):
        if uid == get_login():
            client.delete(client.key('user', uid))

api.add_resource(UserInfo, '/user/<string:uid>')

@app.route('/')
def index():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('index.html', logged=logged)

@app.route('/index')
def index_():
    return flask.redirect(flask.url_for('index'))

@app.route('/login')
def login():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('login.html', logged=logged, title='Login')

@app.route('/drive')
def drive():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('drive.html', logged=logged, title='Drive')

@app.route('/pool')
def pool():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('pool.html', logged=logged, title='Carpool', random=random)

@app.route('/poolresult')
def poolresult():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('poolresult.html', logged=logged, title='Carpool', random=random)

@app.route('/mapsearch')
def mapsearch():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('mapsearch.html', logged=logged, title='Map search', random=random)

@app.route('/mapsearchdrive')
def mapsearchdrive():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('mapsearchdrive.html', logged=logged, title='Map search', random=random)

@app.route('/terms')
def terms():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('terms.html', logged=logged, title='terms of service')

@app.route('/privacy')
def privacy():
    uid = get_login()
    logged = uid is not None
    return flask.render_template('privacy.html', logged=logged, title='privacy policy')
