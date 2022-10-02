# load modules
from .api.myip import blueprint_myip

# import Flask app from main
from __main__ import app

# we load the secrets here, outside the handler

# register blueprints
app.register_blueprint(blueprint_myip, url_prefix="/v1/myip")

