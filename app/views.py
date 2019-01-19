import flask
from app import app

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/index')
def index_():
    return flask.redirect(flask.url_for('index'))
