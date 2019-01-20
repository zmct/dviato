import flask
import flask_restful
import config

app = flask.Flask(__name__)
app.config.from_object(config.Config)
api = flask_restful.Api(app)

from app import views
