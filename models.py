from peewee import *

db = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(max_length=150)
    description = TextField()
    time_spent = IntegerField(default=0)
    resources = CharField(max_length=250)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()
