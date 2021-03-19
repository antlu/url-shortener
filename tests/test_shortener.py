from http import HTTPStatus

import pytest

from url_shortener import create_app, db
from url_shortener.models import Link

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()

@pytest.fixture()
def client(app):
    db.create_all()
    link1 = Link(id='example1', url='http://example1.com')
    link2 = Link(id='example2', url='http://example2.com')
    db.session.add_all([link1, link2])
    db.session.commit()
    yield app.test_client()
    db.session.remove()
    db.drop_all()

@pytest.mark.parametrize(
    'json', [
        {'id': 'example3', 'url': 'http://example3.com'},
        {'url': 'http://example4.com'},
    ],
)
def test_correct_addition(client, json):
    response = client.post('/api/', json=json)
    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json
    json_id = json.get('id')
    response_json_id = response_data['id']
    if json_id:
        assert response_json_id == json_id
    assert response_data['original_url'] == json['url']
    assert response_data['short_url'] == 'http://localhost/{0}'.format(response_json_id)
    assert response_data['api_url'] == 'http://localhost/api/{0}'.format(response_json_id)

@pytest.mark.parametrize(
    'json, http_code, msg', [
        ({'no': 'url'}, HTTPStatus.BAD_REQUEST, 'Invalid URL'),
        ({'url': 'invalid'}, HTTPStatus.BAD_REQUEST, 'Invalid URL'),
        ({'id': 'example1', 'url': 'http://example5.com'}, HTTPStatus.CONFLICT, 'Alias already exists'),
        ({'id': 'example5', 'url': 'http://example1.com'}, HTTPStatus.CONFLICT, 'URL exists'),
    ],
)
def test_incorrect_addition(client, json, http_code, msg):
    response = client.post('/api/', json=json)
    assert response.status_code == http_code
    assert msg in response.json['error']

def test_retrieval_when_posting_existing_one(client):
    existing_record = {'id': 'example1', 'url': 'http://example1.com'}
    response = client.post('/api/', json=existing_record)
    assert response.status_code == HTTPStatus.OK
    assert response.json['id'] == existing_record['id']
    assert response.json['original_url'] == existing_record['url']

def test_retrieval_all(client):
    response = client.get('/api/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 2

def test_retrieval_one(client):
    id_ = 'example1'
    response = client.get('/api/{0}'.format(id_))
    assert response.status_code == HTTPStatus.OK
    assert response.json['id'] == id_

def test_bad_retrieval(client):
    response = client.get('/api/none')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'Not found' in response.json['error']

def test_redirect(client):
    response1 = client.get('/example1')
    assert response1.status_code == HTTPStatus.FOUND
    assert response1.location == 'http://example1.com'

    response2 = client.get('/none')
    assert response2.status_code == HTTPStatus.NOT_FOUND
