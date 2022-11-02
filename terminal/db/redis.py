import redis
from flask import g
# import Flask app from main
from __main__ import app


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = redis.Redis(host=app.config['REDIS_HOST'], port=6379, db=0)
    return db