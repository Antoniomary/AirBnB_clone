#!/usr/bin/python3
"""
    Test for the FileStorage class
"""
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
import os
import json


class TestFileStorage(unittest.TestCase):
    """A class that tests the FileStorage class"""

    def setUp(self):
        """runs before any test case"""
        self.test_model = BaseModel()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_model = self.test_model
        store = storage.all()
        del store[f"{test_model.__class__.__name__}.{test_model.id}"]
        storage.save()

    def test_documentation(self):
        """checks the documentation of FileStorage"""
        from models.engine import file_storage

        self.assertTrue(len(file_storage.__doc__) > 1)
        self.assertTrue(len(FileStorage.all.__doc__) > 1)
        self.assertTrue(len(FileStorage.new.__doc__) > 1)
        self.assertTrue(len(FileStorage.save.__doc__) > 1)
        self.assertTrue(len(FileStorage.reload.__doc__) > 1)

    def test_attributes(self):
        """checks if attribute is private"""
        cls_attrs = FileStorage.__dict__
        self.assertFalse(hasattr(FileStorage, "file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertFalse(hasattr(FileStorage, "objects"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))

    def test_methods(self):
        """checks to see the methods in FileStorage"""
        cls_methods = dir(FileStorage)
        self.assertIn("all", cls_methods)
        self.assertIn("new", cls_methods)
        self.assertIn("save", cls_methods)
        self.assertIn("reload", cls_methods)

    def test___file_path(self):
        """test the __file_path"""
        test_model = self.test_model
        self.assertTrue(type(FileStorage._FileStorage__file_path) is str)
        self.assertEqual(FileStorage._FileStorage__file_path, "file.json")
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test___objects(self):
        """test the __object"""
        test_model = self.test_model
        self.assertTrue(type(FileStorage._FileStorage__objects) is dict)
        key = f"BaseModel.{test_model.id}"
        value = test_model
        expected = {key: value}
        objects = storage.all()
        self.assertTrue(len(objects) >= 1)
        self.assertIn(key, objects.keys())
        self.assertEqual(value, objects[key])

    def test_all(self):
        """test the all method"""
        test_model = self.test_model
        key = f"BaseModel.{test_model.id}"
        value = test_model
        storage._FileStorage__objects = {key: value}
        expected = {key: value}
        objects = storage.all()
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects, expected)

    def test_new(self):
        """test the new method"""
        test_model = self.test_model
        key = f"BaseModel.{test_model.id}"
        value = test_model
        expected = {key: value}
        storage._FileStorage__objects = {}
        storage.new(test_model)
        objects = storage.all()
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects, expected)

    def test_save(self):
        """test the save method"""
        test_model = self.test_model
        key = f"BaseModel.{test_model.id}"
        value = test_model
        storage._FileStorage__objects = {key: value}
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            content = json.load(f)
            self.assertIn(key, content.keys())
            new_model = BaseModel(**content[key])
            self.assertEqual(value.__dict__, new_model.__dict__)

    def test_reload(self):
        """test the reload method"""
        temp = storage._FileStorage__objects
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)
        storage._FileStorage__objects = {}
        storage.save()
        storage.reload()
        objects = storage.all()
        self.assertTrue(objects == {})

        test_model = BaseModel()
        storage.save()
        key = f"BaseModel.{test_model.id}"
        value = test_model
        storage.reload()
        objects = storage.all()
        self.assertEqual(len(objects), 1)
        expected = {key: value}
        self.assertEqual(objects.keys(), expected.keys())
        self.assertEqual(str(objects[key]), str(expected[key]))
        storage._FileStorage__objects = temp
