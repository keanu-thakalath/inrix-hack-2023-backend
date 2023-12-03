from flask import current_app
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint, abort
from datetime import datetime
import requests

TOKEN_URL = 'https://api.iq.inrix.com/auth/v1/appToken'

def get_token():
    # Make the request to the INRIX token endpoint
    try:
        response = requests.get(TOKEN_URL, params={'appId': current_app.config['APP_ID'], 'hashToken': current_app.config['HASH_TOKEN']})
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()
        # Extract the token from the response
        # For more info on how to parse the response, see the json_parser_example.py file
        return {'token': data['result']['token'], 'expiry': datetime.strptime(data['result']['expiry'], "%Y-%m-%dT%H:%M:%S.%fZ")}

    except requests.exceptions.RequestException as e:
        return f'Request failed with error: {e}', None, None
    except (KeyError, ValueError) as e:
        return f'Error parsing JSON: {e}', None, None