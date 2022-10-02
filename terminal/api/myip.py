from flask import Blueprint, request

# import Flask app from main
from __main__ import app

# define the blueprint
blueprint_myip = Blueprint(
    name="blueprint_myip", import_name=__name__)


@blueprint_myip.route('', methods=['GET'])
def get_my_ip():
    '''
    Return IP and ISO2 country from cloudflare header
    '''

    return {
        'ip': 'n/a' if 'Cf-Connecting-Ip' not in request.headers else  request.headers['Cf-Connecting-Ip'],
        'country': 'n/a' if 'Cf-Ipcountry' not in request.headers else request.headers['Cf-Ipcountry'],
    }, 200
