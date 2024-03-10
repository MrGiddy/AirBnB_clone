#!/usr/bin/python3
"""Defines unittests for Place class"""
import os
import unittest
from datetime import datetime
from models.place import Place
from models import storage


class TestPlaceInstantiation(unittest.TestCase):
    """unittest cases for Place class"""

    def test_place_city_id_str_public(self):
        place = Place()
        self.assertEqual(str, type(place.city_id))

    def test_place_user_id_str_public(self):
        place = Place()
        self.assertEqual(str, type(place.user_id))

    def test_place_name_str_public(self):
        place = Place()
        self.assertEqual(str, type(place.name))

    def test_place_description_str_public(self):
        place = Place()
        self.assertEqual(str, type(place.description))

    def test_place_number_rooms_int_public(self):
        place = Place()
        self.assertEqual(int, type(place.number_rooms))

    def test_place_number_bathrooms_int_public(self):
        place = Place()
        self.assertEqual(int, type(place.number_bathrooms))

    def test_place_max_guest_int_public(self):
        place = Place()
        self.assertEqual(int, type(place.max_guest))

    def test_place_price_by_night_int_public(self):
        place = Place()
        self.assertEqual(int, type(place.price_by_night))

    def test_place_latitude_float_public(self):
        place = Place()
        self.assertEqual(float, type(place.latitude))

    def test_place_longitude_float_public(self):
        place = Place()
        self.assertEqual(float, type(place.longitude))

    def test_place_amenity_ids_list_public(self):
        place = Place()
        self.assertEqual(list, type(place.amenity_ids))

    def test_created_at_datetime_public(self):
        place = Place()
        self.assertEqual(datetime, type(place.created_at))

    def test_updated_at_datetime_public(self):
        place = Place()
        self.assertEqual(datetime, type(place.updated_at))

    def test_place_arg_passed_unused(self):
        place = Place('arg')
        self.assertFalse('arg' in place.__dict__.values())

    def test_place_initializes_no_arg(self):
        place = Place()
        self.assertEqual(Place, type(place))

    def test_new_place_in_objects(self):
        place = Place()
        self.assertTrue(place in storage.all().values())

    def test_place_id_unique(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_place_created_at_unique(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.created_at, place2.created_at)

    def test_place_updated_at_unique(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.updated_at, place2.updated_at)

    def test_place_kwargs(self):
        time_now = datetime.now()
        kwargs = {
            'id': '123',
            'created_at': time_now.isoformat(),
            'updated_at': time_now.isoformat()
        }
        place = Place(**kwargs)
        self.assertEqual(kwargs['id'], place.id)
        self.assertEqual(time_now, place.created_at)
        self.assertEqual(time_now, place.updated_at)


class TestPlaceInheritedMethods(unittest.TestCase):
    """unittest cases for place on methods inherited from BaseModel"""

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
    def test_place_save_updated_at_changes(self):
        place = Place()
        update1 = place.updated_at
        place.save()
        update2 = place.updated_at
        self.assertLess(update1, update2)

    def test_place_save_arg_passed(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def test_place_save_file_updated(self):
        place = Place()
        place.save()
        place_key = f'Place.{place.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            storage.reload()
            reloaded_objs = storage.all()
            self.assertTrue(place_key in reloaded_objs.keys())

    # to_dict() method
    def test_place_to_dict_type(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(dict, type(place_dict))

    def test_place_to_dict_expected_keys(self):
        place = Place()
        keys = ['id', 'created_at', 'updated_at', '__class_']
        self.assertTrue(key in place.to_dict() for key in keys)

    def test_place_to_dict_custom_attribs(self):
        place = Place()
        place.building_type = "duplex"
        place.balcony = "True"
        self.assertTrue('duplex' in place.to_dict().values())
        self.assertTrue('balcony' in place.to_dict().keys())

    def test_place_to_dict_created_at_isoformat_str(self):
        place = Place()
        self.assertTrue(str, type(place.to_dict()['created_at']))

    def test_place_to_dict_updated_at_isoformat_str(self):
        place = Place()
        self.assertTrue(str, type(place.to_dict()['updated_at']))

    def test_to_dict_arg_passed(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict('arg')

    def test_place_to_dict_length(self):
        my_model = Place()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    # __str__() method
    def test_place_str_(self):
        place = Place()
        place.id = '123'
        time_now = datetime.now()
        place.created_at = place.updated_at = time_now
        place_dict = {
            'id': '123',
            'created_at': time_now,
            'updated_at': time_now
        }
        expected = f'[Place] (123) {place_dict}'
        self.assertEqual(expected, place.__str__())


if __name__ == '__main__':
    unittest.main()
