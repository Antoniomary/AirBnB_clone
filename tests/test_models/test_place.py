#!/usr/bin/python3
"""A test base for Place"""
import unittest
from models.base_model import BaseModel
from models.place import Place
from datetime import datetime
from models import storage


class TestPlace(unittest.TestCase):
    """Tests the Place class"""

    def setUp(self):
        """runs before any test case"""
        self.test_place = Place()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_place = self.test_place
        store = storage.all()
        del store[f"{test_place.__class__.__name__}.{test_place.id}"]
        storage.save()

    def test_documentations(self):
        """checks for Place documentations"""
        from models import place

        self.assertTrue(len(place.__doc__) > 1)
        self.assertTrue(len(Place.__doc__) > 1)

    def test_Place_class_attribute(self):
        """checks the class attribute Place instance have'"""
        self.assertTrue(hasattr(Place, "city_id"))
        self.assertEqual(type(Place.city_id), str)
        self.assertEqual(Place.city_id, "")
        self.assertTrue(hasattr(Place, "user_id"))
        self.assertEqual(type(Place.user_id), str)
        self.assertEqual(Place.user_id, "")
        self.assertTrue(hasattr(Place, "name"))
        self.assertEqual(type(Place.name), str)
        self.assertEqual(Place.name, "")
        self.assertTrue(hasattr(Place, "description"))
        self.assertEqual(type(Place.description), str)
        self.assertEqual(Place.description, "")
        self.assertTrue(hasattr(Place, "number_rooms"))
        self.assertEqual(type(Place.number_rooms), int)
        self.assertEqual(Place.number_rooms, 0)
        self.assertTrue(hasattr(Place, "number_bathrooms"))
        self.assertEqual(type(Place.number_bathrooms), int)
        self.assertEqual(Place.number_bathrooms, 0)
        self.assertTrue(hasattr(Place, "max_guest"))
        self.assertEqual(type(Place.max_guest), int)
        self.assertEqual(Place.max_guest, 0)
        self.assertTrue(hasattr(Place, "price_by_night"))
        self.assertEqual(type(Place.price_by_night), int)
        self.assertEqual(Place.price_by_night, 0)
        self.assertTrue(hasattr(Place, "latitude"))
        self.assertEqual(type(Place.latitude), float)
        self.assertEqual(Place.latitude, 0.0)
        self.assertTrue(hasattr(Place, "longitude"))
        self.assertEqual(type(Place.longitude), float)
        self.assertEqual(Place.longitude, 0.0)
        self.assertTrue(hasattr(Place, "amenity_ids"))
        self.assertEqual(type(Place.amenity_ids), list)
        self.assertEqual(Place.amenity_ids, [])

    def test_attributes(self):
        """checks the attributes of Place instance"""
        test_place = self.test_place
        self.assertTrue(hasattr(test_place, "id"))
        self.assertTrue(hasattr(test_place, "created_at"))
        self.assertTrue(hasattr(test_place, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the Place instance attributes"""
        test_place = self.test_place
        self.assertEqual(type(test_place.id), str)
        self.assertEqual(type(test_place.created_at), datetime)
        self.assertEqual(type(test_place.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_place = self.test_place
        str_repr = str(test_place)
        self.assertEqual(type(str_repr), str)
        class_name = test_place.__class__.__name__
        id, dict = test_place.id, test_place.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if Place class is a sub-class of BaseModel"""
        self.assertTrue(issubclass(Place, BaseModel))

    def test_methods(self):
        """checks the methods of Place"""
        namespace = dir(Place)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_place = self.test_place
        self.assertTrue(test_place.created_at == test_place.updated_at)
        test_place.save()
        self.assertFalse(test_place.created_at == test_place.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_place = self.test_place
        ret = test_place.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "Place")
        self.assertTrue(type(test_place.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_place.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_place.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_place.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_place.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_place = self.test_place
        test_place_dict = test_place.to_dict()
        self.assertIn("__class__", test_place_dict.keys())
        new_instance = Place(**test_place_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_place))
        self.assertEqual(new_instance.__dict__, test_place.__dict__)
        self.assertFalse(new_instance == test_place)


if __name__ == "__main__":
    unittest.main()
