import pytest

from pathlib import Path
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
BASE_DIR = Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'main.db'}"
    # TEST_DATABASE = f"sqlite:///{BASE_DIR / 'test.db'}"
    TEST_DATABASE = f"sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "supeR secret KeyS"
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
    security_definitions = {
        "basicAuth": {
            "type": "basic"
        }
    }

    APISPEC = {
        'APISPEC_SPEC': APISpec(
            title='Notes Project',
            version='v1',
            plugins=[MarshmallowPlugin()],
            securityDefinitions=security_definitions,
            securitu=[],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger',  # URI API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui'  # URI UI of API Doc
    }
