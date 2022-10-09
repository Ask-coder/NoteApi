import pytest
from api.models.tag import TagModel
from api.models.note import NoteModel
from tests.init_test import client, application, user_admin, note_admin, auth_headers


@pytest.fixture
def tag_data():
    return {
        "name": "tag-1"
    }


@pytest.fixture
def tag(tag_data):
    tag_data = {**tag_data}
    tag = TagModel(**tag_data)
    tag.save()
    return tag


@pytest.fixture
def tag_for_note(user_admin, note, tag):
    return


def test_tag_get_by_id(client, tag):
    response = client.get('/tags/1')
    assert response.status_code == 200
    assert response.json["name"] == tag.name


def test_tag_creation(client, tag_data):
    response = client.post('/tags', json=tag_data)
    data = response.json
    assert response.status_code == 201
    assert tag_data["name"] == data["name"]


def test_add_tag_to_note(client, note_admin, tag):
    tags_data = {
        "tags": [
            f'{tag.id}'
        ]
    }
    response = client.put(f'/notes/{note_admin.id}/tags',
                          json = tags_data,
                          )

    data = response.json
    note_admin.tags.append(tag)
    assert response.status_code == 200
    assert data["tags"][0]['name'] == tag.name
