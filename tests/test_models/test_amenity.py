#!/usr/bin/python3
"""Defines unittests for Amenity class"""
import os
import unittest
from datetime import datetime
from models.amenity import Amenity
from models import storage


class TestAmenityInstantiation(unittest.TestCase):
    """unittest cases for Amenity class"""

    def test_amenity_name_str_public(self):
        amenity = Amenity()
        self.assertEqual(str, type(amenity.name))

    def test_amenity_name_attrib_set(self):
        amenity = Amenity()
        amenity.name = 'free wifi'
        self.assertTrue('name' in amenity.__dict__)
        self.assertTrue('free wifi' in amenity.__dict__.values())

    def test_amenity_created_at_datetime_public(self):
        amenity = Amenity()
        self.assertEqual(datetime, type(amenity.created_at))

    def test_amenity_updated_at_datetime_public(self):
        amenity = Amenity()
        self.assertEqual(datetime, type(amenity.updated_at))

    def test_amenity_arg_passed_unused(self):
        amenity = Amenity('arg')
        self.assertFalse('arg' in amenity.__dict__.values())

    def test_amenity_initializes_no_arg(self):
        amenity = Amenity()
        self.assertEqual(Amenity, type(amenity))

    def test_new_amenity_in_objects(self):
        amenity = Amenity()
        self.assertTrue(amenity in storage.all().values())

    def test_amenity_id_unique(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_amenity_created_at_unique(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.created_at, amenity2.created_at)

    def test_amenity_updated_at_unique(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.updated_at, amenity2.updated_at)

    def test_amenity_kwargs(self):
        time_now = datetime.now()
        kwargs = {
            'id': '254',
            'created_at': time_now.isoformat(),
            'updated_at': time_now.isoformat(),
            'name': 'free wifi'
        }
        amenity = Amenity(**kwargs)
        self.assertEqual(kwargs['id'], amenity.id)
        self.assertEqual(time_now, amenity.created_at)
        self.assertEqual(time_now, amenity.updated_at)
        self.assertEqual(kwargs['name'], amenity.name)


class TestAmenityInheritedMethods(unittest.TestCase):
    """unittest cases for amenity on methods inherited from BaseModel"""

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
    def test_amenity_save_updated_at_changes(self):
        amenity = Amenity()
        update1 = amenity.updated_at
        amenity.save()
        update2 = amenity.updated_at
        self.assertLess(update1, update2)

    def test_amenity_save_arg_passed(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def test_amenity_save_file_updated(self):
        amenity = Amenity()
        amenity.save()
        amenity_key = f'Amenity.{amenity.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            storage.reload()
            reloaded_objs = storage.all()
            self.assertTrue(amenity_key in reloaded_objs.keys())

    # to_dict() method
    def test_amenity_to_dict_type(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(dict, type(amenity_dict))

    def test_amenity_to_dict_expected_keys(self):
        amenity = Amenity()
        keys = ['id', 'created_at', 'updated_at', '__class_']
        self.assertTrue(key in amenity.to_dict() for key in keys)

    def test_amenity_to_dict_custom_attribs(self):
        amenity = Amenity()
        amenity.name = "free wifi"
        amenity.count = 1
        self.assertTrue('free wifi' in amenity.to_dict().values())
        self.assertTrue('count' in amenity.to_dict().keys())

    def test_amenity_to_dict_created_at_isoformat_str(self):
        amenity = Amenity()
        self.assertTrue(str, type(amenity.to_dict()['created_at']))

    def test_amenity_to_dict_updated_at_isoformat_str(self):
        amenity = Amenity()
        self.assertTrue(str, type(amenity.to_dict()['updated_at']))

    def test_amenity_to_dict_arg_passed(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict('arg')

    def test_amenity_to_dict_length(self):
        my_model = Amenity()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    # __str__() method
    def test_amenity_str_(self):
        amenity = Amenity()
        amenity.id = '123'
        time_now = datetime.now()
        amenity.created_at = amenity.updated_at = time_now
        amenity_dict = {
            'id': '123',
            'created_at': time_now,
            'updated_at': time_now
        }
        expected = f'[Amenity] (123) {amenity_dict}'
        self.assertEqual(expected, amenity.__str__())


if __name__ == '__main__':
    unittest.main()
