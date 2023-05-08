#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Calls the parent class with initializer"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.encrypt_password(value)

    def encrypt_password(self, pwd):
        """Encrypts password"""
        _pwd = hashlib.md5(pwd.encode("utf-8")).hexdigest()
        return _pwd
