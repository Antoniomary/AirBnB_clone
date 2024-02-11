#!/usr/bin/python3
"""A test base for User"""
import unittest
from models.base_model import BaseModel
from models.user import User
from datetime import datetime
from models import storage


class TestUser(unittest.TestCase):
    """Tests the User class"""

    def setUp(self):
        """runs before any test case"""
        self.test_user = User()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_user = self.test_user
        store = storage.all()
        del store[f"{test_user.__class__.__name__}.{test_user.id}"]
        storage.save()

    def test_documentations(self):
        """checks for User documentations"""
        from models import user

        self.assertTrue(len(user.__doc__) > 1)
        self.assertTrue(len(User.__doc__) > 1)

    def test_User_class_attribute(self):
        """checks the class attribute User instance have'"""
        self.assertTrue(hasattr(User, "email"))
        self.assertEqual(type(User.email), str)
        self.assertEqual(User.email, "")
        self.assertTrue(hasattr(User, "password"))
        self.assertEqual(type(User.password), str)
        self.assertEqual(User.password, "")
        self.assertTrue(hasattr(User, "first_name"))
        self.assertEqual(type(User.first_name), str)
        self.assertEqual(User.first_name, "")
        self.assertTrue(hasattr(User, "last_name"))
        self.assertEqual(type(User.last_name), str)
        self.assertEqual(User.last_name, "")

    def test_attributes(self):
        """checks the attributes of User instance"""
        test_user = self.test_user
        self.assertTrue(hasattr(test_user, "id"))
        self.assertTrue(hasattr(test_user, "created_at"))
        self.assertTrue(hasattr(test_user, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the User instance attributes"""
        test_user = self.test_user
        self.assertEqual(type(test_user.id), str)
        self.assertEqual(type(test_user.created_at), datetime)
        self.assertEqual(type(test_user.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_user = self.test_user
        str_repr = str(test_user)
        self.assertEqual(type(str_repr), str)
        class_name = test_user.__class__.__name__
        id, dict = test_user.id, test_user.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if User class is a sub-class of BaseModel"""
        self.assertTrue(issubclass(User, BaseModel))

    def test_methods(self):
        """checks the methods of User"""
        namespace = dir(User)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_user = self.test_user
        self.assertTrue(test_user.created_at == test_user.updated_at)
        test_user.save()
        self.assertFalse(test_user.created_at == test_user.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_user = self.test_user
        ret = test_user.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "User")
        self.assertTrue(type(test_user.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_user.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_user.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_user.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_user.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_user = self.test_user
        test_user_dict = test_user.to_dict()
        self.assertIn("__class__", test_user_dict.keys())
        new_instance = User(**test_user_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_user))
        self.assertEqual(new_instance.__dict__, test_user.__dict__)
        self.assertFalse(new_instance == test_user)


if __name__ == "__main__":
    unittest.main()
