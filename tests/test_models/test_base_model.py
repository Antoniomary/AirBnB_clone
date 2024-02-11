#!/usr/bin/python3
"""A test base for BaseModel"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
from models import storage


class TestBaseModel(unittest.TestCase):
    """Tests the BaseModel class"""

    def setUp(self):
        """runs before any test case"""
        self.test_model = BaseModel()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_model = self.test_model
        store = storage.all()
        del store[f"{test_model.__class__.__name__}.{test_model.id}"]
        storage.save()

    def test_documentations(self):
        """checks for BaseModel documentations"""
        from models import base_model

        self.assertTrue(len(base_model.__doc__) > 1)
        self.assertTrue(len(BaseModel.__doc__) > 1)
        self.assertTrue(len(BaseModel.__init__.__doc__) > 1)
        self.assertTrue(len(BaseModel.__str__.__doc__) > 1)
        self.assertTrue(len(BaseModel.save.__doc__) > 1)
        self.assertTrue(len(BaseModel.to_dict.__doc__) > 1)
        # self.assertTrue(len(BaseModel.) > 1)

    def test_attributes(self):
        """checks the attributes of BaseModel"""
        test_model = self.test_model
        self.assertTrue(hasattr(test_model, "id"))
        self.assertTrue(hasattr(test_model, "created_at"))
        self.assertTrue(hasattr(test_model, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the attributes"""
        test_model = self.test_model
        self.assertEqual(type(test_model.id), str)
        self.assertEqual(type(test_model.created_at), datetime)
        self.assertEqual(type(test_model.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_model = self.test_model
        str_repr = str(test_model)
        self.assertEqual(type(str_repr), str)
        class_name = test_model.__class__.__name__
        id, dict = test_model.id, test_model.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if Model class is the same class"""
        self.assertTrue(issubclass(BaseModel, BaseModel))

    def test_methods(self):
        """checks the methods of BaseModel"""
        namespace = dir(BaseModel)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_model = self.test_model
        self.assertTrue(test_model.created_at == test_model.updated_at)
        test_model.save()
        self.assertFalse(test_model.created_at == test_model.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_model = self.test_model
        ret = test_model.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "BaseModel")
        self.assertTrue(type(test_model.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_model.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_model.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_model.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_model.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_model = self.test_model
        test_model_dict = test_model.to_dict()
        self.assertIn("__class__", test_model_dict.keys())
        new_instance = BaseModel(**test_model_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_model))
        self.assertEqual(new_instance.__dict__, test_model.__dict__)
        self.assertFalse(new_instance == test_model)


if __name__ == "__main__":
    unittest.main()
