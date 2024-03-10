#!/usr/bin/python3
"""Defines unittests for State class"""
import os
import unittest
from datetime import datetime
from models.state import State
from models import storage


class TestStateInstantiation(unittest.TestCase):
    """unittest cases for State class"""

    def test_state_name_str_public(self):
        state = State()
        self.assertEqual(str, type(state.name))

    def test_state_name_attrib_set(self):
        state = State()
        state.name = 'Nairobi'
        self.assertTrue('name' in state.__dict__)
        self.assertTrue('Nairobi' in state.__dict__.values())

    def test_state_created_at_datetime_public(self):
        state = State()
        self.assertEqual(datetime, type(state.created_at))

    def test_state_updated_at_datetime_public(self):
        state = State()
        self.assertEqual(datetime, type(state.updated_at))

    def test_state_arg_passed_unused(self):
        state = State('arg')
        self.assertFalse('arg' in state.__dict__.values())

    def test_state_initializes_no_arg(self):
        state = State()
        self.assertEqual(State, type(state))

    def test_new_state_in_objects(self):
        state = State()
        self.assertTrue(state in storage.all().values())

    def test_state_id_unique(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_state_created_at_unique(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.created_at, state2.created_at)

    def test_state_updated_at_unique(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.updated_at, state2.updated_at)

    def test_state_kwargs(self):
        time_now = datetime.now()
        kwargs = {
            'id': '254',
            'created_at': time_now.isoformat(),
            'updated_at': time_now.isoformat(),
            'name': 'Kenya'
        }
        state = State(**kwargs)
        self.assertEqual(kwargs['id'], state.id)
        self.assertEqual(time_now, state.created_at)
        self.assertEqual(time_now, state.updated_at)
        self.assertEqual(kwargs['name'], state.name)


class TestStateInheritedMethods(unittest.TestCase):
    """unittest cases for state on methods inherited from BaseModel"""

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
    def test_state_save_updated_at_changes(self):
        state = State()
        update1 = state.updated_at
        state.save()
        update2 = state.updated_at
        self.assertLess(update1, update2)

    def test_state_save_arg_passed(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_state_save_file_updated(self):
        state = State()
        state.save()
        state_id = f'State.{state.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            storage.reload()
            reloaded_objs = storage.all()
            self.assertTrue(state_id in reloaded_objs.keys())

    # to_dict() method
    def test_state_to_dict_type(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(dict, type(state_dict))

    def test_state_to_dict_expected_keys(self):
        state = State()
        keys = ['id', 'created_at', 'updated_at', '__class_']
        self.assertTrue(key in state.to_dict() for key in keys)

    def test_state_to_dict_custom_attribs(self):
        state = State()
        state.name = "Kenya"
        state.continent = "Africa"
        self.assertTrue('Kenya' in state.to_dict().values())
        self.assertTrue('continent' in state.to_dict().keys())

    def test_state_to_dict_created_at_isoformat_str(self):
        state = State()
        self.assertTrue(str, type(state.to_dict()['created_at']))

    def test_state_to_dict_updated_at_isoformat_str(self):
        state = State()
        self.assertTrue(str, type(state.to_dict()['updated_at']))

    def test_state_to_dict_arg_passed(self):
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict('arg')

    def test_state_to_dict_length(self):
        my_model = State()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    # __str__() method
    def test_state_str_(self):
        state = State()
        state.id = '123'
        time_now = datetime.now()
        state.created_at = state.updated_at = time_now
        state_dict = {
            'id': '123',
            'created_at': time_now,
            'updated_at': time_now
        }
        expected = f'[State] (123) {state_dict}'
        self.assertEqual(expected, state.__str__())


if __name__ == '__main__':
    unittest.main()
