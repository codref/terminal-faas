import hashlib
from datetime import timedelta, date
from flask import Blueprint, request, redirect
from ..db.redis import get_db

# import Flask app from main
from __main__ import app

# define the blueprint
blueprint_url = Blueprint(
    name="blueprint_url", import_name=__name__)


@blueprint_url.route('/minify', methods=['POST'])
def put_minify_url():
    '''
    Return a minified URL which lasts for 3 days in
    Redis cache
    '''

    if request.content_length > app.config["URL_MAX_LENGTH"]:
        return {
            'error': 'The length of the provided URL is too big. Max allowed size is 10Kb'
        }, 413

    url = request.get_json()["url"]
    url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()

    r = get_db()
    r.set(url_hash, url)
    expiration_date = timedelta(days=3)
    r.expire(url_hash, int(expiration_date.total_seconds()))

    return {
        'minifiedURL': f'{app.config["REDIRECT_BASE_URL"]}/url/to/{url_hash}',
        'expirationDate': date.today() + expiration_date
    }, 200

@blueprint_url.route('/to/<string:url_hash>', methods=['GET'])
def get_minify_url_and_redirect(url_hash):
    '''
    Retrieves regular URL from minified and reply with a 301 redirect
    and deletes it
    '''

    r = get_db()
    url = r.getdel(url_hash)

    if url is None:
        return {
            'error': 'URL is expired or does not exist'
        }, 404

    return redirect(url.decode('utf-8'), code=301)

@blueprint_url.route('/minify/<string:url_hash>', methods=['GET'])
def get_minify_url(url_hash):
    '''
    Retrieves regular URL from minified hash and deletes it
    '''

    r = get_db()
    url = r.getdel(url_hash)

    if url is None:
        return {
            'error': 'URL is expired or does not exist'
        }, 404    

    return {
        'url': url.decode('utf-8')
    }, 200