from peewee import *
from flask_login import UserMixin
from datetime import date


db = SqliteDatabase('user.db')

class User(UserMixin, Model):
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

    def update_status(self):
        today = date.today()
        if self.term < today:
            self.status = 'Expired'
        elif self.status == 'Completed':
            self.status = 'Completed'
        else:
            self.status = 'Active'
        self.save()