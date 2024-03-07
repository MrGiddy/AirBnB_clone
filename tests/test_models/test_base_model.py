#!/usr/bin/python3
"""Defines unittest cases for BaseModel"""
from datetime import datetime
import io
import contextlib
from models.base_model import BaseModel
import unittest
import uuid


class testInstantiation(unittest.TestCase):
    """unittest cases for initialized instance variables"""

    def test_id_unique(self):
        my_model = BaseModel()
        my_model2 = BaseModel()
        self.assertNotEqual(my_model.id, my_model2.id)

    def test_id_string(self):
        my_model = BaseModel()
        self.assertEqual(str, type(my_model.id))

    def test_id_uuid4(self):
        my_model = BaseModel()
        uuid_obj = uuid.UUID(my_model.id, version=4)
        self.assertEqual(uuid_obj.version, 4)

    def test_created_at_is_datetime(self):
        my_model = BaseModel()
        time_created = my_model.created_at
        self.assertEqual(datetime, type(time_created))

    def test_updated_at_is_datetime(self):
        my_model = BaseModel()
        time_updated = my_model.updated_at
        self.assertEqual(datetime, type(time_updated))


class testStr(unittest.TestCase):
    """unittests for overidden __str__ method"""

    @staticmethod
    def captured_stdout(my_model):
        captured_stdout = io.StringIO()
        with contextlib.redirect_stdout(captured_stdout):
            print(my_model, end='')
        return captured_stdout.getvalue()

    def test_str_equal(self):
        my_model = BaseModel()
        expected = f'[BaseModel] ({my_model.id}) {my_model.__dict__}'
        self.assertEqual(expected, self.captured_stdout(my_model))


class testSave(unittest.TestCase):
    """unittest cases for save method"""

    def test_save_works(self):
        my_model = BaseModel()
        update1 = my_model.updated_at
        my_model.save()
        update2 = my_model.updated_at
        self.assertNotEqual(update1, update2)

    def test_save_datetime(self):
        my_model = BaseModel()
        my_model.save
        self.assertEqual(datetime, type(my_model.updated_at))


class testToDict(unittest.TestCase):
    """unittest cases for to_dict method"""

    def test_to_dict_returns_dict(self):
        my_model = BaseModel()
        ret_dict = my_model.to_dict()
        self.assertEqual(dict, type(ret_dict))

    def test_to_dict_classname_added(self):
        my_model = BaseModel()
        ret_dict = my_model.to_dict()
        self.assertEqual(ret_dict['__class__'], "BaseModel")

    def test_to_dict_length(self):
        my_model = BaseModel()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    @staticmethod
    def is_isoformat(datetime_string):
        """Tests if a datetime string is in isoformat()"""
        try:
            datetime.fromisoformat(datetime_string)
            return True
        except ValueError:
            return False

    def test_to_dict_created_at_isoformat(self):
        my_model = BaseModel()
        ret_dict = my_model.to_dict()
        isoformat_string = ret_dict['created_at']
        self.assertTrue(self.is_isoformat(isoformat_string))

    def test_to_dict_updated_at_isoformat(self):
        my_model = BaseModel()
        ret_dict = my_model.to_dict()
        isoformat_string = ret_dict['updated_at']
        self.assertTrue(self.is_isoformat(isoformat_string))
