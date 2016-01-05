import peewee
from peewee import SqliteDatabase

sqlite_db = SqliteDatabase('c:\\bench\\allocat\\allocat.db')


class BaseModel(peewee.Model):
    class Meta:
        database = sqlite_db
