#!/usr/bin/python3
"""A test base for State"""
import unittest
from models.base_model import BaseModel
from models.state import State
from datetime import datetime
from models import storage


class TestState(unittest.TestCase):
    """Tests the State class"""

    def setUp(self):
        """runs before any test case"""
        self.test_state = State()

    def tearDown(self):
        """runs if SetUp succeeded"""
        test_state = self.test_state
        store = storage.all()
        del store[f"{test_state.__class__.__name__}.{test_state.id}"]
        storage.save()

    def test_documentations(self):
        """checks for State documentations"""
        from models import state

        self.assertTrue(len(state.__doc__) > 1)
        self.assertTrue(len(State.__doc__) > 1)

    def test_State_class_attribute(self):
        """checks the class attribute State has"""
        self.assertTrue(hasattr(State, "name"))
        self.assertEqual(type(State.name), str)
        self.assertEqual(State.name, "")

    def test_attributes(self):
        """checks the attributes of State instance"""
        test_state = self.test_state
        self.assertTrue(hasattr(test_state, "id"))
        self.assertTrue(hasattr(test_state, "created_at"))
        self.assertTrue(hasattr(test_state, "updated_at"))

    def test_attribute_type(self):
        """checks the type of the State instance attributes"""
        test_state = self.test_state
        self.assertEqual(type(test_state.id), str)
        self.assertEqual(type(test_state.created_at), datetime)
        self.assertEqual(type(test_state.updated_at), datetime)

    def test___str__(self):
        """checks the __str__ method"""
        test_state = self.test_state
        str_repr = str(test_state)
        self.assertEqual(type(str_repr), str)
        class_name = test_state.__class__.__name__
        id, dict = test_state.id, test_state.__dict__
        expected = f"[{class_name}] ({id}) {dict}"
        self.assertEqual(str_repr, expected)

    def test_inheritance(self):
        """checks if State class is a sub-class of BaseModel"""
        self.assertTrue(issubclass(State, BaseModel))

    def test_methods(self):
        """checks the methods of State"""
        namespace = dir(State)
        self.assertIn("save", namespace)
        self.assertIn("to_dict", namespace)

    def test_save(self):
        """checks the working of the save method"""
        test_state = self.test_state
        self.assertTrue(test_state.created_at == test_state.updated_at)
        test_state.save()
        self.assertFalse(test_state.created_at == test_state.updated_at)

    def test_to_dict(self):
        """checks the working of the to_dict method"""
        test_state = self.test_state
        ret = test_state.to_dict()
        self.assertTrue(type(ret) is dict)
        self.assertIn("__class__", ret.keys())
        self.assertTrue(ret["__class__"] == "State")
        self.assertTrue(type(test_state.__dict__["created_at"]) is datetime)
        self.assertTrue(type(test_state.__dict__["updated_at"]) is datetime)
        self.assertTrue(type(ret["created_at"]) is str)
        self.assertTrue(type(ret["updated_at"]) is str)
        strf = test_state.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["created_at"])
        strf = test_state.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(strf, ret["updated_at"])
        self.assertFalse(ret == test_state.__dict__)

    def test_create_from_dictionary(self):
        """checks how creating instance from a dictionary works"""
        test_state = self.test_state
        test_state_dict = test_state.to_dict()
        self.assertIn("__class__", test_state_dict.keys())
        new_instance = State(**test_state_dict)
        self.assertIsInstance(new_instance, BaseModel)
        self.assertTrue(type(new_instance) is type(test_state))
        self.assertEqual(new_instance.__dict__, test_state.__dict__)
        self.assertFalse(new_instance == test_state)


if __name__ == "__main__":
    unittest.main()
