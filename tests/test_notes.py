import pytest
from api.models.user import UserModel
from api.models.note import NoteModel
from tests.init_test import client, application, auth_headers


@pytest.fixture()
def user():
    user_data = {"username": "testuser", "password": "1234"}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def note(user):
    note_data = {"author_id": user.id, "text": "Quote for testuser"}
    note = NoteModel(**note_data)
    note.save()
    return note






def test_note_get_by_id(client, note, auth_headers):
    response = client.get('/notes/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json["text"] == note.text


def test_note_not_found(client, note, auth_headers):
    response = client.get('/notes/2', headers=auth_headers)
    assert response.status_code == 404


def test_note_creation(client, auth_headers):
    note_data = {
        "text": "Quote for auth user",
        "private": False
    }
    response = client.post('/notes',
                           json=note_data,
                           headers=auth_headers,
                           )
    data = response.json
    assert response.status_code == 201
    assert note_data["text"] == data["text"]
    assert note_data["private"] == data["private"]


def test_note_edit(client, note_admin, auth_headers):
    note_edit_data = {
        "text": "Edited note"
    }
    response = client.put(f'/notes/{note_admin.id}',
                          json=note_edit_data,
                          headers=auth_headers,
                          )
    data = response.json
    assert response.status_code == 200
    assert data["text"] == note_edit_data["text"]


def test_note_delete(client, note_admin, auth_headers):

    response = client.delete(f'/notes/{note_admin.id}', headers=auth_headers)
    note = NoteModel.query.get(note_admin.id)
    assert response.status_code == 204
    assert note is None;
