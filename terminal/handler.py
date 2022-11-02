# load modules
import logging, os
from .api.myip import blueprint_myip
from .api.url import blueprint_url

# import Flask app from main
from __main__ import app

# we load the secrets here, outside the handler

# register blueprints
app.register_blueprint(blueprint_myip, url_prefix="/v1/myip")
app.register_blueprint(blueprint_url, url_prefix="/v1/url")

try:
    app.config.update(#redis-master.openfaas-fn.svc.cluster.local
        URL_MAX_LENGTH=os.getenv('URL_MAX_LENGTH', default=100000),
        REDIS_HOST=os.getenv('REDIS_HOST', default='redis'),
        REDIRECT_BASE_URL=os.getenv('REDIRECT_BASE_URL', default='https://api.codref.org/function/terminal/v1'),
    )

except Exception as ex:
    logging.fatal(f'Cannot access credentials storage, or not all secrets found. [{ex}]')
    raise
