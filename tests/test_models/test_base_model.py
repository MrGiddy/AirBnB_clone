#!/usr/bin/python3
"""Defines unittest cases for BaseModel"""
import contextlib
import io
import os
import unittest
import uuid
from datetime import datetime
from models.base_model import BaseModel


# 1. Test BaseModel Instantiation


class test_BaseModel_Instantiation(unittest.TestCase):
    """unittest cases for initialized instance variables"""

    def test_init_id_unique(self):
        my_model = BaseModel()
        my_model2 = BaseModel()
        self.assertNotEqual(my_model.id, my_model2.id)

    def test_init_id_string(self):
        my_model = BaseModel()
        self.assertEqual(str, type(my_model.id))

    def test_init_id_uuid4(self):
        my_model = BaseModel()
        uuid_obj = uuid.UUID(my_model.id, version=4)
        self.assertEqual(uuid_obj.version, 4)

    def test_init_created_at_is_datetime(self):
        my_model = BaseModel()
        time_created = my_model.created_at
        self.assertEqual(datetime, type(time_created))

    def test_init_updated_at_is_datetime(self):
        my_model = BaseModel()
        time_updated = my_model.updated_at
        self.assertEqual(datetime, type(time_updated))

    def test_init_kwargs_works(self):
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual("My_First_Model", my_new_model.name)
        self.assertEqual(89, my_new_model.my_number)
        self.assertIsNotNone(my_new_model.id)
        self.assertEqual(type(my_new_model.created_at), datetime)
        self.assertEqual(type(my_new_model.updated_at), datetime)

    def test_init_kwargs_empty(self):
        empty_dict = {}
        my_model = BaseModel(**empty_dict)
        self.assertEqual(3, len(my_model.__dict__))
        self.assertIsNotNone(my_model.id)
        self.assertIsNotNone(my_model.created_at)
        self.assertIsNotNone(my_model.updated_at)
        self.assertEqual(type(my_model.id), str)
        self.assertEqual(type(my_model.created_at), datetime)
        self.assertEqual(type(my_model.updated_at), datetime)

    def test_init_kwargs_custom_dict(self):
        custom_dict = {
            'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
            'created_at': '2022-01-01T00:00:00',
            'updated_at': '2022-01-01T01:00:00',
            'custom_attr': [90, 100]
        }
        my_model = BaseModel(**custom_dict)
        created_at = my_model.created_at.isoformat()
        updated_at = my_model.updated_at.isoformat()
        self.assertEqual(my_model.id, '56d43177-cc5f-4d6c-a0c1-e167f8c27337')
        self.assertEqual(created_at, '2022-01-01T00:00:00')
        self.assertEqual(updated_at, '2022-01-01T01:00:00')
        self.assertEqual(my_model.custom_attr, [90, 100])


# 2. Test BaseModel methods

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

    @classmethod
    def setUp(self):
        try:
            os.rename('file.json', 'tmp_file')
        except FileNotFoundError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

        try:
            os.rename('tmp_file', 'file.json')
        except FileNotFoundError:
            pass

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

    def test_save_updates_file(self):
        my_model = BaseModel()
        my_model.save()
        key = f'BaseModel.{my_model.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            self.assertTrue(key in f.read())


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


if __name__ == '__main__':
    unittest.main()
