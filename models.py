from peewee import *

import datetime

db = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(max_length=150)
    content = TextField()
    date = CharField(max_length=150)
    time_spent = CharField(max_length=150)
    resources = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-title',)


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()
