from peewee import *

import datetime

db = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(max_length=150)
    description = TextField()
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = CharField(max_length=150)
    resources = TextField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()
