#!/usr/bin/python3
"""
    Test for the FileStorage class
"""
import unittest
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """A class that tests the FileStorage class"""

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
