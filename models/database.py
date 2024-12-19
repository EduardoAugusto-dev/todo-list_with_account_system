from peewee import *

db = SqliteDatabase('user.db')

class User(Model):
    id = AutoField()
    password = CharField()
    email = CharField(unique=True)
    username = CharField()

    class Meta:
        database = db

class Task(Model):
    id = AutoField()
    title = CharField()
    description = CharField()
    term = DateField()
    status = CharField(default='Pending')
    user = ForeignKeyField(User, backref='tasks')

    class Meta:
        database = db