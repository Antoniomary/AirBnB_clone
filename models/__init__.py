#!/usr/bin/python3
"""
    It makes this current directory where it is located a package.
    It creates a unique FileStorage instance.
"""
from models.engine import file_storage


storage = file_storage.FileStorage()
storage.reload()
