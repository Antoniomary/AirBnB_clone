#!/usr/bin/python3
"""
    Test for console
"""
import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


class TestHBNBCommand(unittest.TestCase):
    """A class that tests the console"""

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


if __name__ == "__main__":
    unittest.main()
