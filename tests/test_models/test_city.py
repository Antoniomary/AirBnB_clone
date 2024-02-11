#!/usr/bin/python3
"""A test base for City"""
import unittest
from models.base_model import BaseModel
from models.city import City
from datetime import datetime
from models import storage


class TestCity(unittest.TestCase):
    """Tests the City class"""

    def setUp(self):
        """runs before any test case"""
        self.test_city = City()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_city = self.test_city
        store = storage.all()
        del store[f"{test_city.__class__.__name__}.{test_city.id}"]
        storage.save()

    def test_documentations(self):
        """checks for City documentations"""
        from models import city

        self.assertTrue(len(city.__doc__) > 1)
        self.assertTrue(len(City.__doc__) > 1)

    def test_City_class_attribute(self):
        """checks the class attribute City instance have'"""
        self.assertTrue(hasattr(City, "state_id"))
        self.assertEqual(type(City.state_id), str)
        self.assertEqual(City.state_id, "")
        self.assertTrue(hasattr(City, "name"))
        self.assertEqual(type(City.name), str)
        self.assertEqual(City.name, "")

    def test_attributes(self):
        """checks the attributes of City instance"""
        test_city = self.test_city
        self.assertTrue(hasattr(test_city, "id"))
        self.assertTrue(hasattr(test_city, "created_at"))
        self.assertTrue(hasattr(test_city, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the City instance attributes"""
        test_city = self.test_city
        self.assertEqual(type(test_city.id), str)
        self.assertEqual(type(test_city.created_at), datetime)
        self.assertEqual(type(test_city.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_city = self.test_city
        str_repr = str(test_city)
        self.assertEqual(type(str_repr), str)
        class_name = test_city.__class__.__name__
        id, dict = test_city.id, test_city.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if City class is a sub-class of BaseModel"""
        self.assertTrue(issubclass(City, BaseModel))

    def test_methods(self):
        """checks the methods of City"""
        namespace = dir(City)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_city = self.test_city
        self.assertTrue(test_city.created_at == test_city.updated_at)
        test_city.save()
        self.assertFalse(test_city.created_at == test_city.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_city = self.test_city
        ret = test_city.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "City")
        self.assertTrue(type(test_city.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_city.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_city.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_city.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_city.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_city = self.test_city
        test_city_dict = test_city.to_dict()
        self.assertIn("__class__", test_city_dict.keys())
        new_instance = City(**test_city_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_city))
        self.assertEqual(new_instance.__dict__, test_city.__dict__)
        self.assertFalse(new_instance == test_city)


if __name__ == "__main__":
    unittest.main()
