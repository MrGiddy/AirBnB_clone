#!/usr/bin/python3
"""Defines Amenity class deriving from BaseModel"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an Amenity"""
    name = ""


if __name__ == '__main__':
    Amenity()
