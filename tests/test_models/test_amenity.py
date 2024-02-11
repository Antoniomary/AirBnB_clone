#!/usr/bin/python3
"""A test base for Amenity"""
import unittest
from models.base_model import BaseModel
from models.amenity import Amenity
from datetime import datetime
from models import storage


class TestAmenity(unittest.TestCase):
    """Tests the Amenity class"""

    def setUp(self):
        """runs before any test case"""
        self.test_amenity = Amenity()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_amenity = self.test_amenity
        store = storage.all()
        del store[f"{test_amenity.__class__.__name__}.{test_amenity.id}"]
        storage.save()

    def test_documentations(self):
        """checks for Amenity documentations"""
        from models import amenity

        self.assertTrue(len(amenity.__doc__) > 1)
        self.assertTrue(len(Amenity.__doc__) > 1)

    def test_Amenity_class_attribute(self):
        """checks the class attribute Amenity has"""
        self.assertTrue(hasattr(Amenity, "name"))
        self.assertEqual(type(Amenity.name), str)
        self.assertEqual(Amenity.name, "")

    def test_attributes(self):
        """checks the attributes of Amenity instance"""
        test_amenity = self.test_amenity
        self.assertTrue(hasattr(test_amenity, "id"))
        self.assertTrue(hasattr(test_amenity, "created_at"))
        self.assertTrue(hasattr(test_amenity, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the Amenity instance attributes"""
        test_amenity = self.test_amenity
        self.assertEqual(type(test_amenity.id), str)
        self.assertEqual(type(test_amenity.created_at), datetime)
        self.assertEqual(type(test_amenity.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_amenity = self.test_amenity
        str_repr = str(test_amenity)
        self.assertEqual(type(str_repr), str)
        class_name = test_amenity.__class__.__name__
        id, dict = test_amenity.id, test_amenity.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if Amenity class is a sub-class of BaseModel"""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_methods(self):
        """checks the methods of Amenity"""
        namespace = dir(Amenity)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_amenity = self.test_amenity
        self.assertTrue(test_amenity.created_at == test_amenity.updated_at)
        test_amenity.save()
        self.assertFalse(test_amenity.created_at == test_amenity.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_amenity = self.test_amenity
        ret = test_amenity.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "Amenity")
        self.assertTrue(type(test_amenity.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_amenity.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_amenity.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_amenity.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_amenity.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_amenity = self.test_amenity
        test_amenity_dict = test_amenity.to_dict()
        self.assertIn("__class__", test_amenity_dict.keys())
        new_instance = Amenity(**test_amenity_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_amenity))
        self.assertEqual(new_instance.__dict__, test_amenity.__dict__)
        self.assertFalse(new_instance == test_amenity)


if __name__ == "__main__":
    unittest.main()
