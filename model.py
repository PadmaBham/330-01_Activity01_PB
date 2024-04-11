# All TODOs are updated to TODONEs after the corresponding task is completed!

from peewee import Model, CharField, DateTimeField, ForeignKeyField, TextField
import os

from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class User(Model):
    # TODONE: Added model fields here
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = db


class Task(Model):
    # TODONE: Added model fields here
    task = TextField()
    performed = DateTimeField(null=True)
    performed_by = ForeignKeyField(model=User, null=True)

    class Meta:
        database = db
