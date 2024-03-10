#!/usr/bin/python3
"""Defines unittests for User class"""
import os
import unittest
from datetime import datetime
from models.user import User
from models import storage


class TestUserInstantiation(unittest.TestCase):
    """unittest cases for User class"""

    def test_user_email_str_public(self):
        user = User()
        self.assertEqual(str, type(user.email))

    def test_user_password_str_public(self):
        user = User()
        self.assertEqual(str, type(user.password))

    def test_user_first_name_str_public(self):
        user = User()
        self.assertEqual(str, type(user.first_name))

    def test_user_last_name_str_public(self):
        user = User()
        self.assertEqual(str, type(user.last_name))

    def test_created_at_datetime_public(self):
        user = User()
        self.assertEqual(datetime, type(user.created_at))

    def test_updated_at_datetime_public(self):
        user = User()
        self.assertEqual(datetime, type(user.updated_at))

    def test_user_arg_passed_unused(self):
        user = User('arg')
        self.assertFalse('arg' in user.__dict__.values())

    def test_user_initializes_no_arg(self):
        user = User()
        self.assertEqual(User, type(user))

    def test_new_user_in_objects(self):
        user = User()
        self.assertTrue(user in storage.all().values())

    def test_user_id_unique(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_user_created_at_unique(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.created_at, user2.created_at)

    def test_user_updated_at_unique(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.updated_at, user2.updated_at)

    def test_user_kwargs(self):
        time_now = datetime.now()
        kwargs = {
            'id': '123',
            'created_at': time_now.isoformat(),
            'updated_at': time_now.isoformat(),
            'first_name': 'Ademy',
            'last_name': 'Grace',
            'email': 'ademy.grace@gmail.com'
        }
        user = User(**kwargs)
        self.assertEqual(kwargs['id'], user.id)
        self.assertEqual(time_now, user.created_at)
        self.assertEqual(time_now, user.updated_at)
        self.assertEqual(kwargs['first_name'], user.first_name)
        self.assertEqual(kwargs['last_name'], user.last_name)
        self.assertEqual(kwargs['email'], user.email)

    # def test_user_None_kwargs(self):
    #     with self.assertRaises(TypeError):
    #         User(id=None, created_at=None, updated_at=None)


class TestUserInheritedMethods(unittest.TestCase):
    """unittest cases for user on methods inherited from BaseModel"""

    def setUp(self):
        try:
            os.rename('file.json', 'tmp_file')
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

        try:
            os.rename('tmp_file', 'file.json')
        except FileNotFoundError:
            pass

    # save() method
    def test_user_save_updated_at_unique(self):
        user = User()
        update1 = user.updated_at
        user.save()
        update2 = user.updated_at
        self.assertLess(update1, update2)

    def test_user_save_arg_passed(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_user_save_file_updated(self):
        user = User()
        user.save()
        user_id = f'User.{user.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            storage.reload()
            reloaded_objs = storage.all()
            self.assertTrue(user_id in reloaded_objs.keys())

    # to_dict() method
    def test_user_to_dict_type(self):
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(dict, type(user_dict))

    def test_user_to_dict_expected_keys(self):
        user = User()
        keys = ['id', 'created_at', 'updated_at', '__class_']
        self.assertTrue(key in user.to_dict() for key in keys)

    def test_user_to_dict_custom_attribs(self):
        user = User()
        user.first_name = "Ademy"
        user.fav_color = "Purple"
        self.assertTrue('Ademy' in user.to_dict().values())
        self.assertTrue('fav_color' in user.to_dict().keys())

    def test_user_to_dict_created_at_isoformat_str(self):
        user = User()
        self.assertTrue(str, type(user.to_dict()['created_at']))

    def test_user_to_dict_updated_at_isoformat_str(self):
        user = User()
        self.assertTrue(str, type(user.to_dict()['updated_at']))

    def test_to_dict_arg_passed(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict('arg')

    def test_user_to_dict_length(self):
        my_model = User()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    # __str__() method
    def test_user_str_(self):
        user = User()
        user.id = '123'
        time_now = datetime.now()
        user.created_at = user.updated_at = time_now
        user_dict = {
            'id': '123',
            'created_at': time_now,
            'updated_at': time_now
        }
        expected = f'[User] (123) {user_dict}'
        self.assertEqual(expected, user.__str__())


if __name__ == '__main__':
    unittest.main()
