#!/usr/bin/python3
"""Defines FileStorage class"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage():
    """
       An abstracted file storage engine.
       Serializes instances to a JSON file and desirializes
       JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary; `__objects`"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to `__objects` dictionary.
           The key of the object is: `<obj class name>.id`"""
        key = f'{obj.__class__.__name__}.{obj.id}'
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes `__objects` dictionary to
           the JSON file `__file_path`"""
        serializable_dict = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
            }
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_dict, f)

    def reload(self):
        """Deserializes JSON file `__file_path` to
          `__objects` dictionary if file exists"""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                loaded_dict = json.load(f)

            for key, obj_dict in loaded_dict.items():
                class_name = obj_dict['__class__']
                del obj_dict['__class__']
                instance = eval(class_name)(**obj_dict)
                FileStorage.__objects[key] = instance

        except FileNotFoundError:
            pass


if __name__ == '__main__':
    FileStorage()
