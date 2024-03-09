"""Defines unittest cases for file_storage module"""
import models
import os
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

# 1. Test FileStorage Instantiation


class TestFileStorageInstantiation(unittest.TestCase):
    """unittest cases for the instantiation of the FileStorage class"""

    def test_FileStorageInstantiation_no_args(self):
        self.assertEqual(FileStorage, type(FileStorage()))

    def test_FileStorageInstantiation_arg_passed(self):
        with self.assertRaises(TypeError):
            FileStorage("arg")

    def test_FileStorage_file_path_is_private(self):
        my_storage = FileStorage()
        with self.assertRaises(AttributeError):
            print(my_storage.__file_path)

    def test_FileStorage_file_path_is_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_FileStorage_objects_is_private(self):
        my_storage = FileStorage()
        with self.assertRaises(AttributeError):
            print(my_storage.__objects)

    def test_FileStorage_objects_is_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_initialization_of_storage(self):
        self.assertEqual(FileStorage, type(models.storage))

# 2. Test FileStorage methods


class TestFileStorageMethods(unittest.TestCase):
    """unittest cases for methods of FileStorage class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", 'tmp_file')
        except FileNotFoundError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

        try:
            os.rename("tmp_file", "file.json")
        except FileNotFoundError:
            pass

        FileStorage._FileStorage__objects = {}

    # all() method
    def test_all_returns_dict(self):
        my_storage = FileStorage()
        self.assertEqual(dict, type(my_storage.all()))

    def test_all_arg_passed(self):
        my_storage = FileStorage()
        with self.assertRaises(TypeError):
            my_storage.all('arg')

    # new() method
    def test_new_sets_objs(self):
        my_model = BaseModel()
        models.storage.new(my_model)
        key = f'BaseModel.{my_model.id}'
        self.assertTrue(key in models.storage.all().keys())

    def test_new_two_args(self):
        my_model = BaseModel()
        with self.assertRaises(TypeError):
            models.storage.new(my_model, 'arg2')

    def test_new_None_passed(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    # save() method
    def test_save_serializes_to_file(self):
        my_model = BaseModel()
        models.storage.new(my_model)  # add a new object in __objects
        models.storage.save()  # save __objects in file.json
        with open('file.json', 'r', encoding='utf-8') as f:
            text = f.read()
            self.assertTrue(f'BaseModel.{my_model.id}' in text)

    def test_save_arg_passed(self):
        with self.assertRaises(TypeError):
            models.storage.save('arg')

    # reload() method
    def test_reload_deserializes(self):
        my_model = BaseModel()
        models.storage.new(my_model)
        models.storage.save()
        models.storage.reload()
        loaded_objs = FileStorage._FileStorage__objects
        self.assertTrue(f'BaseModel.{my_model.id}' in loaded_objs)

    # def test_reload_file_dne(self):
    #     with self.assertRaises(FileNotFoundError):
    #         models.storage.reload()

    def test_reload_arg_passed(self):
        with self.assertRaises(TypeError):
            models.storage.reload('arg')


if __name__ == '__main__':
    unittest.main()
