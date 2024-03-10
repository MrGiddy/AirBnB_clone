#!/usr/bin/python3
"""Defines class State that derived from BaseModel"""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents the State a user resides in"""
    name = ""
