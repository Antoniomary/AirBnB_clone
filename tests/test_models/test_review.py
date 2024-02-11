#!/usr/bin/python3
"""A test base for Review"""
import unittest
from models.base_model import BaseModel
from models.review import Review
from datetime import datetime
from models import storage


class TestReview(unittest.TestCase):
    """Tests the Review class"""

    def setUp(self):
        """runs before any test case"""
        self.test_review = Review()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_review = self.test_review
        store = storage.all()
        del store[f"{test_review.__class__.__name__}.{test_review.id}"]
        storage.save()

    def test_documentations(self):
        """checks for Review documentations"""
        from models import review

        self.assertTrue(len(review.__doc__) > 1)
        self.assertTrue(len(Review.__doc__) > 1)

    def test_Review_class_attribute(self):
        """checks the class attribute Review instance have'"""
        self.assertTrue(hasattr(Review, "place_id"))
        self.assertEqual(type(Review.place_id), str)
        self.assertEqual(Review.place_id, "")
        self.assertTrue(hasattr(Review, "user_id"))
        self.assertEqual(type(Review.user_id), str)
        self.assertEqual(Review.user_id, "")
        self.assertTrue(hasattr(Review, "text"))
        self.assertEqual(type(Review.text), str)
        self.assertEqual(Review.text, "")

    def test_attributes(self):
        """checks the attributes of Review instance"""
        test_review = self.test_review
        self.assertTrue(hasattr(test_review, "id"))
        self.assertTrue(hasattr(test_review, "created_at"))
        self.assertTrue(hasattr(test_review, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the Review instance attributes"""
        test_review = self.test_review
        self.assertEqual(type(test_review.id), str)
        self.assertEqual(type(test_review.created_at), datetime)
        self.assertEqual(type(test_review.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_review = self.test_review
        str_repr = str(test_review)
        self.assertEqual(type(str_repr), str)
        class_name = test_review.__class__.__name__
        id, dict = test_review.id, test_review.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if Review class is a sub-class of BaseModel"""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_methods(self):
        """checks the methods of Review"""
        namespace = dir(Review)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_review = self.test_review
        self.assertTrue(test_review.created_at == test_review.updated_at)
        test_review.save()
        self.assertFalse(test_review.created_at == test_review.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_review = self.test_review
        ret = test_review.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "Review")
        self.assertTrue(type(test_review.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_review.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_review.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_review.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_review.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_review = self.test_review
        test_review_dict = test_review.to_dict()
        self.assertIn("__class__", test_review_dict.keys())
        new_instance = Review(**test_review_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_review))
        self.assertEqual(new_instance.__dict__, test_review.__dict__)
        self.assertFalse(new_instance == test_review)


if __name__ == "__main__":
    unittest.main()
