from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

import datetime

db = SqliteDatabase('journal.db')


class BaseModel(Model):
    class Meta:
        database = db


class Entry(BaseModel):
    title = CharField(max_length=150)
    slug = CharField()
    content = TextField()
    date = DateField(formats="%Y-%m-%d")
    time_spent = CharField(max_length=150)
    resources = TextField()
    tags = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-timestamp',)


class User(UserMixin, BaseModel):
    username = CharField(max_length=150)
    password = CharField(max_length=150)

    @classmethod
    def create_user(cls, username, password):
        try:
            with db.transaction():
                cls.create(username=username,
                           password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists!")


def initialize():
    db.connect()
    db.create_tables([Entry, User], safe=True)
    db.close()
