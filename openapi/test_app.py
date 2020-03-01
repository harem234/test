import json
import os
from pathlib import Path
import unittest
from io import BytesIO

import connexion
from connexion import RestyResolver

BASE_URL = 'http://127.0.0.1:5000/api'
BASE_DIR = Path(__file__).parents[1]
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('swagger.yaml', resolver=RestyResolver('api'))

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        flask_app.app.config['DEBUG'] = False
        flask_app.app.config['TESTING'] = True
        self.client = flask_app.app.test_client()

    # def test_upload(self):
    #     import io
    #     test_file_binary = b'ABCDE{FG.}.?!@#()*^&*(\n\n\r\t\n h'
    #     data = {'file_binary': (io.BytesIO(test_file_binary), 'test_file_binary')}
    #     response = self.client.post(
    #         ('/api/upload?user_name=mahdi&file_name=test_file_binary'),
    #         data=data,
    #         content_type='multipart/form-data'
    #     )
    #     assert response.status_code == 201
    #     assert response.content_type == 'application/json'
    #     data = {}
    #     stream = b'{"test name": "test value","test name2": "test value2"}'
    #     data['file_binary'] = (BytesIO(stream), 'Data.txt')
    #     response = self.client.post(BASE_URL + '/upload?user_name=mahdi&file_name=globalData.txt',
    #                                 data=data,
    #                                 content_type='multipart/form-data')
    #     assert response.status_code == 201

    def test_get_user_data(self):
        response = self.client.get('/api/getUserData?user_name=mahdi')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.data == b'[\n  {\n    "test name": "test value",\n    "test name2": "test value2"\n  },\n  {\n    ' \
                                b'"test": "2",\n    "test name": "test value",\n    "test name2": "test value2"\n  }\n]\n '

    def test_download(self):
        response = self.client.get('/api/download?user_name=mahdi&file_name=Data.txt')
        assert response.status_code == 200
        assert response.content_type == 'application/octet-stream'
        assert response.data == b'{  \r\n\t"test name": "test value",  \r\n\t"test name2": "test value2"\r\n\t\r\n}'

    def test_upload(self):
        """Test audio upload endpoint works"""
        import io
        test_file_binary = b'ABCDE{FG.}.?!@#()*^&*(\n\n\r\t\n h'
        data = {'file_binary': (io.BytesIO(test_file_binary), 'test_file_binary')}
        response = self.client.post(
            ('/api/upload?user_name=mahdi&file_name=test_file_binary'),
            data=data,
            content_type='multipart/form-data'
        )
        assert response.status_code == 201
        assert response.content_type == 'application/json'

    def test_set_user_data(self):
        """test set a value for user data in Data.txt file of the specific user"""
        response = self.client.post('/api/setUserData?user_name=mahdi&key=test4&value=test_value_4')
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

    def test_set_global_data(self):
        """test set a value for user data in Data.txt file of the specific user"""
        response = self.client.post('/api/setGlobalData?user_name=mahdi&key=test5&value=test_value_5')
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

if __name__ == "__main__":
    unittest.main()
