#!/usr/bin/python3
"""Defines City class that derives from BaseModel"""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a City"""
    state_id = ""
    name = ""


if __name__ == '__main__':
    City()
