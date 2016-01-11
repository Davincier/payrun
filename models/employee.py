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

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return '%s: GRADE %02d, STEP %02d, FTE %d%%' % \
               (self.name, self.grade, self.step, self.fte)

    @staticmethod
    def get_all():
        return [
            rec for rec in
            Employee.select().where(
                Employee.active == True).order_by(Employee.name)
        ]

    @staticmethod
    def get_one(record_id):
        return Employee.get(Employee.id == record_id)

    @staticmethod
    def get_by_name(name):
        return Employee.get(Employee.name == name)

    @staticmethod
    def has_payrecord(name):
        return Employee.select().where(Employee.name == name).exists()
