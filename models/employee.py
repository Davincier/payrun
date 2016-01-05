from peewee import *
from .base_model import BaseModel


class Employee(BaseModel):
    dfn = CharField()
    name = CharField()
    grade = IntegerField()
    step = IntegerField()
    fte = IntegerField()
    cp = CharField()
    notes = TextField()
    active = BooleanField()
    # Has many PayRecord ('payrecords')
    # Has many PayDiff ('paydiffs')

    class Meta:
        db_table = 'employees'

    @staticmethod
    def get_all():
        return [
            rec for rec in
            Employee.select().where(Employee.active == True).order_by(Employee.name)
        ]

    @staticmethod
    def get_one(record_id):
        return Employee.get(Employee.id == record_id)

    @staticmethod
    def get_by_name(name):
        return Employee.get(Employee.name == name)

    @staticmethod
    def has_record(name):
        return Employee.select().where(Employee.name == name).exists()

    @staticmethod
    def get_id(name):
        qry = Employee.select().where(Employee.name == name)
        return qry.get().id if qry.exists() else None

    def add_records(self, records):
        for rec in records:
            rec.employee = self.id
        with self._meta.database.atomic():
            PayRecord.insert_many(records)
