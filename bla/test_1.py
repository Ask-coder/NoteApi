
def test_list_append():
    l = [2, 5]
    l.append(7)
    assert len(l) == 3
    assert l[-1] == 7


def test_slice():
    s = 'hello'
    res = s[2:4]
    assert res == "ll"

from app import app

def test_user_get_by_id():
    test_client = app.test_client()
    response = test_client.get('/users/1')
    assert response.status_code == 200
    assert response.json.get("username")
    assert response.json.get("username") == "test-user"
    assert response.json.get('id') == 1


def test_create_user():
    pass


def test_delete_user():
    pass