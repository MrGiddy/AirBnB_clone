#!/usr/bin/python3
"""Defines BaseModel class"""
import models
import uuid
from datetime import datetime


class BaseModel():
    """Defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Instantiates BaseModel"""
        if kwargs and kwargs['id']:
            for key in kwargs:
                if key in ('created_at', 'updated_at'):
                    kwargs[key] = datetime.fromisoformat(kwargs[key])

            keys_list = [key for key in kwargs if key != '__class__']
            for key in keys_list:
                setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary of key/values of instance __dict__"""
        ret_dict = {key: getattr(self, key) for key in self.__dict__}
        ret_dict['__class__'] = self.__class__.__name__
        ret_dict['created_at'] = ret_dict['created_at'].isoformat()
        ret_dict['updated_at'] = ret_dict['updated_at'].isoformat()

        return ret_dict

    def __str__(self):
        """Displays custom output if str() or print() is called
           on an instance of BaseModel
        """
        class_name = self.__class__.__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)


if __name__ == '__main__':
    BaseModel()
