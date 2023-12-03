from flask import Flask
from flask_smorest import Api
import os
from dotenv import load_dotenv
from lots import bp as lots_bp


load_dotenv()

class Config:
    API_TITLE = "Inrix Hack 2023"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "docs"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    APP_ID = os.getenv('appId')
    HASH_TOKEN = os.getenv('hashToken')
    GOOGLE_API_KEY = os.getenv('googleAPIKey')


app = Flask(__name__)
app.config.from_object(Config)

api = Api()
api.init_app(app)
api.register_blueprint(lots_bp)