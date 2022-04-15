import os
import json
import uuid as uuid_lib
import importlib
from .action import Action

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w+') as f:
        json.dump(data, f, indent=4)

def stringify(data):
    return json.dumps(data, indent=4)

def uuid():
    return str(uuid_lib.uuid1())

def create_folder(folder):
    if not os.path.exists(folder):
        print(f'Creating folder: {folder}')
        os.makedirs(folder)

def import_actions():
    for file in os.listdir(os.path.abspath('./data/repository/actions')):
        if file[0] == '_':
            continue

        mod_name = file[:-3]   # strip .py at the end
        package_name = 'data.repository.actions'
        cls = importlib.import_module('.' + mod_name, package=package_name)
        
        for attr in dir(cls):
            if attr[0] == '_':
                continue

            obj = getattr(cls, attr)
            if isinstance(obj, type) and issubclass(obj, Action) and obj != Action:
                obj()