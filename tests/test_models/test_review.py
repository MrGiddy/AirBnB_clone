#!/usr/bin/python3
"""Defines unittests for Review class"""
import os
import unittest
from datetime import datetime
from models.review import Review
from models import storage


class TestReviewInstantiation(unittest.TestCase):
    """unittest cases for Review class"""

    def test_review_place_id_str_public(self):
        review = Review()
        self.assertEqual(str, type(review.place_id))

    def test_review_user_id_str_public(self):
        review = Review()
        self.assertEqual(str, type(review.user_id))

    def test_review_text_str_public(self):
        review = Review()
        self.assertEqual(str, type(review.text))

    def test_created_at_datetime_public(self):
        review = Review()
        self.assertEqual(datetime, type(review.created_at))

    def test_updated_at_datetime_public(self):
        review = Review()
        self.assertEqual(datetime, type(review.updated_at))

    def test_review_arg_passed_unused(self):
        review = Review('arg')
        self.assertFalse('arg' in review.__dict__.values())

    def test_review_initializes_no_arg(self):
        review = Review()
        self.assertEqual(Review, type(review))

    def test_new_review_in_objects(self):
        review = Review()
        self.assertTrue(review in storage.all().values())

    def test_review_id_unique(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_review_created_at_unique(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.created_at, review2.created_at)

    def test_review_updated_at_unique(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.updated_at, review2.updated_at)

    def test_review_kwargs(self):
        time_now = datetime.now()
        kwargs = {
            'id': '123',
            'created_at': time_now.isoformat(),
            'updated_at': time_now.isoformat(),
        }
        review = Review(**kwargs)
        self.assertEqual(kwargs['id'], review.id)
        self.assertEqual(time_now, review.created_at)
        self.assertEqual(time_now, review.updated_at)


class TestReviewInheritedMethods(unittest.TestCase):
    """unittest cases for review on methods inherited from BaseModel"""

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
    def test_review_save_updated_at_changes(self):
        review = Review()
        update1 = review.updated_at
        review.save()
        update2 = review.updated_at
        self.assertLess(update1, update2)

    def test_review_save_arg_passed(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_review_save_file_updated(self):
        review = Review()
        review.save()
        review_id = f'Review.{review.id}'
        with open('file.json', 'r', encoding='utf-8') as f:
            storage.reload()
            reloaded_objs = storage.all()
            self.assertTrue(review_id in reloaded_objs.keys())

    # to_dict() method
    def test_review_to_dict_type(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(dict, type(review_dict))

    def test_review_to_dict_expected_keys(self):
        review = Review()
        keys = ['id', 'created_at', 'updated_at', '__class_']
        self.assertTrue(key in review.to_dict() for key in keys)

    def test_review_to_dict_custom_attribs(self):
        review = Review()
        review.first_name = "Ademy"
        review.fav_color = "Purple"
        self.assertTrue('Ademy' in review.to_dict().values())
        self.assertTrue('fav_color' in review.to_dict().keys())

    def test_review_to_dict_created_at_isoformat_str(self):
        review = Review()
        self.assertTrue(str, type(review.to_dict()['created_at']))

    def test_review_to_dict_updated_at_isoformat_str(self):
        review = Review()
        self.assertTrue(str, type(review.to_dict()['updated_at']))

    def test_to_dict_arg_passed(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict('arg')

    def test_review_to_dict_length(self):
        my_model = Review()
        prev_len = len(my_model.__dict__)
        len_after = len(my_model.to_dict())
        self.assertEqual(len_after - 1, prev_len)

    # __str__() method
    def test_review_str_(self):
        review = Review()
        review.id = '123'
        time_now = datetime.now()
        review.created_at = review.updated_at = time_now
        review_dict = {
            'id': '123',
            'created_at': time_now,
            'updated_at': time_now
        }
        expected = f'[Review] (123) {review_dict}'
        self.assertEqual(expected, review.__str__())


if __name__ == '__main__':
    unittest.main()
