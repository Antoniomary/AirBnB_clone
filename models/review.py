#!/usr/bin/python3
"""
    A module that defines a Review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """a class that defines a review"""
    place_id = ""
    user_id = ""
    text = ""
