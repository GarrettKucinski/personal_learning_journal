from peewee import *

import datetime

db = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(max_length=150)
    slug = CharField()
    content = TextField()
    date = DateField(formats="%Y-%m-%d")
    time_spent = CharField(max_length=150)
    resources = TextField()
    tags = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-timestamp',)


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()
