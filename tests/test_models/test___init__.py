#!/usr/bin/python3
"""
    Test for the __init__ file
"""
import unittest
import models
import inspect
from models.engine.file_storage import FileStorage


class Test__init__(unittest.TestCase):
    """A test suite for the __init__ file in this directory"""

    def test_file_storage(self):
        """checks if file_storage was imported"""
        self.assertIn("file_storage", dir(models))
        self.assertTrue(inspect.ismodule(models.file_storage))

    def test_storage(self):
        """checks that the variable storage exists"""
        self.assertIn("storage", models.__dict__.keys())

    def test_storage_class(self):
        """checks the class that storage belongs to"""
        self.assertTrue(type(models.storage) is FileStorage)
