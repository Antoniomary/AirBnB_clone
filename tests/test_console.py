#!/usr/bin/python3
"""
    Test for console
"""
import unittest
import os
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime


class TestHBNBCommand(unittest.TestCase):
    """A class that tests the console"""

    classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Place": Place,
            "Amenity": Amenity,
            "Review": Review,
        }

    def setUp(self):
        """runs before any test"""
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)
        storage.reload()
        storage._FileStorage__objects = {}

    def test_help(self):
        """Tests the help command"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_help_EOF(self):
        """Tests the help for EOF"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
        s = """EOF (CTRL + D) exits the program
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_all(self):
        """Tests the help for all"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
        s = """Prints all string representation of all instances.

        Usage: all
                   prints the entire instances of the different classes
               all <class name>
                   prints instances of only <class name>
               <class name>.all()
                   also prints instances of only <class name>
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_count(self):
        """Tests the help for count"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help count")
        s = """Counts the number of instances of a class

        Usage: <class name>.count()
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_create(self):
        """Tests the help for create"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
        s = "Creates a class instance, saves it to a JSON file"
        s += """ and prints the id

        Usage: create <class name>
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_destroy(self):
        """Tests the help for destroy"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
        s = """Deletes an instance and saves the change into a JSON file.

        Usage: destroy <class name> <id>
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_help(self):
        """Tests the help for help"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help help")
        s = 'List available commands with "help"'
        s += ''' or detailed help with "help cmd".\n'''
        self.assertEqual(s, f.getvalue())

    def test_help_quit(self):
        """Tests the help for quit"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
        s = """Quit command to exit the program
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_show(self):
        """Tests the help for show"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
        s = """Prints the string representation of an instance

        Usage: show <class name> <instance id>
        \n"""
        self.assertEqual(s, f.getvalue())

    def test_help_update(self):
        """Tests the help for update"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
        s = "Updates/adds instance attribute and"
        s += ''' saves the change to a JSON file

        Usage: update <class name> <id> <attribute name> "<attribute value>"
               <class name>.update(<id>, <attribute name>, <attribute value>)
               <class name>.update(<id>, <dictionary representation>).
        \n'''
        self.assertEqual(s, f.getvalue())

    def test_do_EOF(self):
        """Tests EOF commmand"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        output = f.getvalue()
        self.assertEqual("\n", output)

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("EOF extra argument")
        output = f.getvalue()
        self.assertEqual("\n", output)

    def test_emptyline(self):
        """Tests emptyline method"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("")
        self.assertEqual("", f.getvalue())

    def test_do_quit(self):
        """Tests quit commmand"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        self.assertEqual("", f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("quit extra argument")
        self.assertEqual("", f.getvalue())

    def test_do_create_error(self):
        """Tests the create command errors"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        s = "** class name missing **\n"
        self.assertEqual(s, f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Nothing")
        s = "** class doesn't exist **\n"
        self.assertEqual(s, f.getvalue())

    def test_do_create(self):
        """Tests the create command"""
        storage.reload()
        storage._FileStorage__objects = {}
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        store = storage.all()
        key, value = None, None
        for key in store:
            value = store[key]
            break
        expected = value.__dict__["id"] + '\n'
        self.assertEqual(expected, f.getvalue())

    def test_do_count_error(self):
        """Tests the count command errors"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Dummy.count()")
        s = "** class doesn't exist **\n"
        self.assertEqual(s, f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(".count()")
        s = "** class name missing **\n"
        self.assertEqual(s, f.getvalue())

    def test_do_count(self):
        """Tests the count command"""
        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"{model}.count()")
            self.assertEqual("0\n", f.getvalue())

        for model in self.classes:
            self.classes[model]()
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"{model}.count()")
            self.assertEqual("1\n", f.getvalue())

    def test_do_all_error(self):
        """Tests the all command error"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all MyModel")
        self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_do_all(self):
        """Tests the all command"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        self.assertEqual("[]\n", f.getvalue())

        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {model}")
            self.assertEqual("[]\n", f.getvalue())

        for model in self.classes:
            test_model = self.classes[model]()
            expected = str([str(test_model)])
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {model}")
            self.assertEqual(expected + "\n", f.getvalue())

        self.setUp()

        for model in self.classes:
            test_model = self.classes[model]()
            expected = str([str(test_model)])
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"{model}.all()")
            self.assertEqual(expected + "\n", f.getvalue())

    def test_do_show_error(self):
        """Tests the show command errors"""
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        s = "** class name missing **\n"
        self.assertEqual(s, f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        s = "** class name missing **\n"
        self.assertEqual(s, f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show MyModel")
        s = "** class doesn't exist **\n"
        self.assertEqual(s, f.getvalue())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("MyModel.show()")
        s = "** class doesn't exist **\n"
        self.assertEqual(s, f.getvalue())

        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {model}")
            s = "** instance id missing **\n"
            self.assertEqual(s, f.getvalue())

        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"{model}.show()")
            s = "** instance id missing **\n"
            self.assertEqual(s, f.getvalue())

        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {model} wrong_id")
            s = "** no instance found **\n"
            self.assertEqual(s, f.getvalue())

        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'{model}.show("wrong_id")')
            s = "** no instance found **\n"
            self.assertEqual(s, f.getvalue())

    def test_do_show(self):
        """Tests the show command"""
        id, objs = [], []
        for model in self.classes:
            test_model = self.classes[model]()
            objs.append(test_model)
            id.append(test_model.id)

        i = 0
        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {model} {id[i]}")
            s = f"[{model}] ({id[i]}) {objs[i].__dict__}\n"
            self.assertEqual(s, f.getvalue())
            i += 1

        i = 0
        for model in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd(f'{model}.show("{id[i]}")')
            s = f"[{model}] ({id[i]}) {objs[i].__dict__}\n"
            self.assertEqual(s, f.getvalue())
            i += 1


if __name__ == "__main__":
    unittest.main()
