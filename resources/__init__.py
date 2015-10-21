import os 
from flask import Flask, make_response
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from flask.ext.assets import Environment, Bundle
from bson.json_util import dumps
import jinja2

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/junks"

ASSETS_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__)
app._static_folder = ASSETS_DIR
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
app.jinja_loader=jinja2.FileSystemLoader('templates')


# compass config
assets = Environment(app)
app.config['ASSETS_DEBUG'] = True

main_scss = Bundle('scss/style.scss', 'scss/media.scss', filters='compass', output='css/style.css', depends='scss/includes/*.scss')
assets.register('main_scss', main_scss)

bootstrap_css = Bundle('scss/bootstrap/bootstrap-cyborg.css', output='css/bootstrap.css')
assets.register('bootstrap_css', bootstrap_css)

dashboard_css = Bundle('scss/dashboard.scss', filters='compass', output='css/dashboard.css', depends='*.scss')
assets.register('dashboard_css', dashboard_css)

print_css = Bundle('scss/print.scss', filters='compass', output='css/print.css', depends='*.sass')
assets.register('print_css', print_css)

terminal_css = Bundle('scss/includes/terminal.scss', filters='compass', output='css/terminal.css', depends='*.scss')
assets.register('terminal_css', terminal_css)

junk_index_css = Bundle('scss/junks.scss', filters='compass', output='css/junks.css', depends='includes/*.scss')
assets.register('junks_css', junk_index_css)

# mongo db
app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

import resources.routes
