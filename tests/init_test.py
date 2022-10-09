from api import db
from app import app
from config import Config
from base64 import b64encode
from api.models.user import UserModel
from api.models.note import NoteModel
import pytest


@pytest.fixture()
def application():
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE
    })
    db.create_all()
    yield app
    db.drop_all()


@pytest.fixture()
def client(application):
    return application.test_client()

@pytest.fixture()
def user_admin():
    user_data = {"username": "admin", "password": "admin", "role": "admin"}
    user = UserModel(**user_data)
    user.save()
    return user

@pytest.fixture()
def auth_headers(user_admin):
    user_data = {"username": "admin", "password": "admin", "role": "admin"}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers

@pytest.fixture()
def user_admin():
    user_data = {"username": "admin", "password": "admin"}
    user = UserModel(**user_data)
    user.save()
    return user

@pytest.fixture()
def note_admin(user_admin):
    note_data = {"author_id": user_admin.id, "text": "Note for admin"}
    note = NoteModel(**note_data)
    note.save()
    return note


