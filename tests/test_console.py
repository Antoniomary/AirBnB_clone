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


if __name__ == "__main__":
    unittest.main()
