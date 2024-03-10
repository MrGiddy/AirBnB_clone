#!/usr/bin/python3
"""Defines Review class that inherits from BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a Review"""
    place_id = ""
    user_id = ""
    text = ""


if __name__ == '__main__':
    Review()
