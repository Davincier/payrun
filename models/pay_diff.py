from peewee import *
from .base_model import BaseModel
from models import PayRun, Employee


class PayDiff(BaseModel):

    payrun = ForeignKeyField(PayRun, related_name='diffs')
    employee = ForeignKeyField(Employee, related_name='paydiffs')
    field_name = CharField()
    previous_amount = DecimalField()
    current_amount = DecimalField()
    notes = TextField()

    class Meta:
        db_table = 'paydiffs'
