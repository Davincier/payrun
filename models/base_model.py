import peewee
from app import db


class BaseModel(peewee.Model):
    class Meta:
        database = db
