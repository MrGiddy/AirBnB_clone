#!/usr/bin/python3
"""Defines User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a user of AirBnB"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""


if __name__ == '__main__':
    User()
