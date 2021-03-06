'''models auth interacts with'''
__author__ = 'dturner'

import uuid
from portfolio.common.mongo import Mongo
from flask import session

class User(object):
    '''User model {email, password, name, _id}'''

    def __init__(self, email, password, name=None, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    @classmethod
    def get_by_email(cls, email):
        data = Mongo.find_one('users', {'email': email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls, _id):
        data = Mongo.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)


    @staticmethod
    def validate_credentials(email, password):
        user = User.get_by_email(email)
        if user is not None:
            # need to add in the salt algorithm here
            return user.password == password
        return False


    @staticmethod
    def login_user(email, password):
        if User.validate_credentials(email, password) is True:
            session['email'] = email
        else:
            # do something else
            session['email'] = None


    @staticmethod
    def logout_user():
        session['email'] = None


    @classmethod
    def register_user(cls, email, password, name=None):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password, name)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False


    @classmethod
    def register_user_successful(self):
        pass


    def json(self):
        return {'name' : self.name,
                'password' : self.password,
                'email' : self.email,
                '_id' : self._id}


    @classmethod
    def from_mongo(cls, _id):
        user = Mongo.find_one(collection='users',
                              query={'_id': _id})
        # cls(** object) is the same as
        # name=user['name'],
        # password=user['password'],
        # email=user['email'],
        # _id=user['_id']
        return cls(**user)


    def save_to_mongo(self):
        Mongo.insert(collection='users',
                     json=self.json())
