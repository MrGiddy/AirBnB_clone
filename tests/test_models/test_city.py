#!/usr/bin/python3
"""Defines unittests for City class"""
import os
import unittest
from datetime import datetime
from models.city import City
from models import storage


class TestCityInstantiation(unittest.TestCase):
    """unittest cases for City class"""

    def test_city_state_id_str_public(self):
        city = City()
        self.assertEqual(str, type(city.state_id))

    def test_city_name_str_public(self):
        city = City()
        self.assertEqual(str, type(city.name))

    def test_created_at_datetime_public(self):
        city = City()
        self.assertEqual(datetime, type(city.created_at))

    def test_updated_at_datetime_public(self):
        city = City()
        self.assertEqual(datetime, type(city.updated_at))

    def test_city_arg_passed_unused(self):
        city = City('arg')
        self.assertFalse('arg' in city.__dict__.values())

    def test_city_initializes_no_arg(self):
        city = City()
        self.assertEqual(City, type(city))

    def test_new_city_in_objects(self):
        city = City()
        self.assertTrue(city in storage.all().values())

    def test_city_id_unique(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_city_created_at_unique(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.created_at, city2.created_at)

    def test_city_updated_at_unique(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.updated_at, city2.updated_at)

    def test_city_kwargs(self):
        time_now = datetime.now()
        kwargs = {
            'id': '254',
            'created_at': time_now.isoformat(),
            'updated_at': time_now.isoformat(),
            'state_id': '00100',
            'name': 'Nairobi'
        }
        city = City(**kwargs)
        self.assertEqual(kwargs['id'], city.id)
        self.assertEqual(time_now, city.created_at)
        self.assertEqual(time_now, city.updated_at)
        self.assertEqual(kwargs['state_id'], city.state_id)
        self.assertEqual(kwargs['name'], city.name)


class TestCityInheritedMethods(unittest.TestCase):
    """unittest cases for city on methods inherited from BaseModel"""

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
    def test_city_save_updated_at_changes(self):
        city = City()
        update1 = city.updated_at
        city.save()
        update2 = city.updated_at
        self.assertLess(update1, update2)

    def test_city_save_arg_passed(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_city_save_file_updated(self):
        city = City()
        city.save()
        city_id = f'City.{city.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            storage.reload()
            reloaded_objs = storage.all()
            self.assertTrue(city_id in reloaded_objs.keys())

    # to_dict() method
    def test_city_to_dict_type(self):
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(dict, type(city_dict))

    def test_city_to_dict_expected_keys(self):
        city = City()
        keys = ['id', 'created_at', 'updated_at', '__class_']
        self.assertTrue(key in city.to_dict() for key in keys)

    def test_city_to_dict_custom_attribs(self):
        city = City()
        city.name = "Nairobi"
        city.code = "00100"
        self.assertTrue('Nairobi' in city.to_dict().values())
        self.assertTrue('code' in city.to_dict().keys())

    def test_city_to_dict_created_at_isoformat_str(self):
        city = City()
        self.assertTrue(str, type(city.to_dict()['created_at']))

    def test_city_to_dict_updated_at_isoformat_str(self):
        city = City()
        self.assertTrue(str, type(city.to_dict()['updated_at']))

    def test_to_dict_arg_passed(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict('arg')

    def test_city_to_dict_length(self):
        my_model = City()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    # __str__() method
    def test_city_str_(self):
        city = City()
        city.id = '123'
        time_now = datetime.now()
        city.created_at = city.updated_at = time_now
        city_dict = {
            'id': '123',
            'created_at': time_now,
            'updated_at': time_now
        }
        expected = f'[City] (123) {city_dict}'
        self.assertEqual(expected, city.__str__())


if __name__ == '__main__':
    unittest.main()
