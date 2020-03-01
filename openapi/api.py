import json
import os
from pathlib import Path

import connexion

BASE_DIR = Path(__file__).parents[1]
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')


# USER_DATA_DIR = os.path.join(BASE_DIR, 'data')


def write_file_json(user_name, file_name):
    print(connexion.request.files)
    print(bool(connexion.request.files))
    # print(connexion.request.json)
    # print(connexion.request.headers)
    user_dir = os.path.join(UPLOAD_DIR, user_name)
    try:
        os.mkdir(user_dir)
    except FileExistsError:
        pass
    save_dir = os.path.join(user_dir, file_name)
    if bool(connexion.request.files):
        connexion.request.files['file_binary'].save(save_dir)
    # elif connexion.request.json is not None:
    #     print('#'*10)
    #     with open(save_dir, 'w') as outfile:
    #         json.dump(connexion.request.json, outfile)
    else:
        return 'use formData with correct Content-Type HTTP header', 500

    return 'You send the username: {}, file name: {}'.format(user_name, file_name), 201


def set_user_data(user_name, key, value):
    import json
    user_dir = os.path.join(UPLOAD_DIR, user_name)
    # todo: all the data files or just a specific file?
    save_dir = os.path.join(user_dir, 'Data.txt')
    with open(save_dir) as json_file:
        data = json.load(json_file)
        data[key] = value

    with open(save_dir, 'w') as json_file:
        json.dump(data, json_file)

    return 201

def set_global_data(user_name, key, value):
    import json
    user_dir = os.path.join(UPLOAD_DIR, user_name)
    save_dir = os.path.join(user_dir, 'globalData.txt')
    with open(save_dir) as json_file:
        data = json.load(json_file)
        data[key] = value

    with open(save_dir, 'w') as json_file:
        json.dump(data, json_file)
    return 201

def download(user_name, file_name):
    import flask
    user_dir = os.path.join(UPLOAD_DIR, user_name)
    return flask.send_from_directory(user_dir, file_name,
                                     as_attachment=True,
                                     mimetype='application/octet-stream',
                                     attachment_filename=file_name
                                     )


def get_user_data(user_name):
    user_dir = os.path.join(UPLOAD_DIR, user_name)
    os.chdir(user_dir)
    data = []
    for filename in os.listdir(user_dir):
        print(filename)
        with open(filename) as json_file:
            data_json = json.load(json_file)
            data.append(data_json)
    return data
