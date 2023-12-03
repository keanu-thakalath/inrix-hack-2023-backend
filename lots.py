from flask import current_app
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from datetime import datetime
import requests
from auth import get_token

def refresh_auth_token():
    if not current_app.config.get('token'):
        current_app.config['token'] = get_token()
        return
    if datetime.now() > current_app.config['token']['expiry']:
        current_app.config['token'] = get_token()

bp = Blueprint("lots", "lots", url_prefix="/lots", description="Gets lot information")

LOTS_URL = 'https://api.iq.inrix.com/lots/v3'
DISTANCE_MATRIX_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

def get_lots(point, radius):
    refresh_auth_token()
    try:
        headers = {"Authorization": f"Bearer {current_app.config['token']['token']}"}
        response = requests.get(LOTS_URL, params={'point': point, 'radius': radius}, headers=headers)
        response.raise_for_status()
        return response.json()['result']

    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}'
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}'

def get_walking_distance(office_point, lots):
    origin_string = '|'.join([f"{lot['point']['coordinates'][1]},{lot['point']['coordinates'][0]}" for lot in lots])
    try:
        response = requests.get(DISTANCE_MATRIX_URL, params={'destinations': office_point.replace('|', ','),
                                                             'origins': origin_string, 'mode': 'WALKING',
                                                             'key': current_app.config['GOOGLE_API_KEY']})
        response.raise_for_status()
        return list(map(lambda row: row['elements'][0]['duration']['value'], response.json()['rows']))
    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}', None, None
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}', None, None


class LotsQueryArgSchema(ma.Schema):
    point = ma.fields.String(load_only=True)
    radius = ma.fields.Integer(load_only=True)

class LotsSchema(ma.Schema):
    result = ma.fields.String(dump_only=True)

@bp.route("/lots")
class Lots(MethodView):
    @bp.arguments(LotsQueryArgSchema, location="query")
    @bp.response(200)
    def get(self, args):
        refresh_auth_token()    
        lots = get_lots(args['point'], args['radius'])
        return get_walking_distance(args['point'], lots)

'''
given points, radius
'''

@bp.route("/test")
class WalkingDistance(MethodView):
    @bp.arguments(LotsQueryArgSchema, location="query")
    @bp.response(200)
    def get(self, args):
        refresh_auth_token()
        response = get_lots(args['point'], args['radius'])
        return get_walking_distance(args['point'], response)
        