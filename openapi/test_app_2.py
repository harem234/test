import json
import os
from pathlib import Path

import pytest
import connexion
from connexion import RestyResolver

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('swagger.yaml', resolver=RestyResolver('api'))

BASE_DIR = Path(__file__).parents[1]


# todo what is this?
@pytest.fixture(scope='module')
def client():
    # fetch underlying flask app from the connexion app
    # flask_app = flask_app.app
    flask_app.app.config['DEBUG'] = False
    flask_app.app.config['TESTING'] = True
    with flask_app.app.test_client() as c:
        yield c


def test_get_user_data(client):
    response = client.get('/api/getUserData?user_name=mahdi')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    user_dir = os.path.join(UPLOAD_DIR, 'mahdi')
    os.chdir(user_dir)
    data = []
    for filename in os.listdir(user_dir):
        print(filename)
        with open(filename) as json_file:
            data_json = json.load(json_file)
            data.append(data_json)

    assert response.data == data


def test_download(client):
    response = client.get('/api/download?user_name=mahdi&file_name=Data.txt')
    assert response.status_code == 200
    assert response.content_type == 'application/octet-stream'
    assert response.data == b'{  \r\n\t"test name": "test value",  \r\n\t"test name2": "test value2"\r\n\t\r\n}'


def test_upload(client):
    """Test audio upload endpoint works"""
    import io
    test_file_binary = b'ABCDE{FG.}.?!@#()*^&*(\n\n\r\t\n h'
    data = {'file_binary': (io.BytesIO(test_file_binary), 'test_file_binary')}
    response = client.post(
        ('/api/upload?user_name=mahdi&file_name=test_file_binary'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201
    assert response.content_type == 'application/json'


def test_set_user_data(client):
    """test set a value for user data in Data.txt file of the specific user"""
    response = client.post('/api/setUserData?user_name=mahdi&key=test4&value=test_value_4')
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    user_dir = os.path.join(UPLOAD_DIR, 'mahdi')
    # todo: all the data files or just a specific file?
    data_file = os.path.join(user_dir, 'Data.txt')
    with open(data_file) as json_file:
        data = json.load(json_file)
        data['test4'] = 'test_value_4'

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    with open(data_file) as json_file:
        data = json.load(json_file)
        assert data['test4'] == 'test_value_4'


def test_set_global_data(client):
    """test set a value for user data in Data.txt file of the specific user"""
    response = client.post('/api/setGlobalData?user_name=mahdi&key=test5&value=test_value_5')
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    user_dir = os.path.join(UPLOAD_DIR, 'mahdi')
    # todo: all the data files or just a specific file?
    data_file = os.path.join(user_dir, 'globalData.txt')
    with open(data_file) as json_file:
        data = json.load(json_file)
        data['test5'] = 'test_value_5'

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    with open(data_file) as json_file:
        data = json.load(json_file)
        assert data['test5'] == 'test_value_5'
