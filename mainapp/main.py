from flask import Flask
import os

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "tuneful.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import api
from . import routes
from . import views
