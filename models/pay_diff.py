from peewee import *
from .base_model import BaseModel
from models import PayRun, PayRecord


class PayDiff(BaseModel):

    payrun = ForeignKeyField(PayRun, related_name='diffs_query')
    record = ForeignKeyField(PayRecord, related_name='diffs')
    field_name = CharField()
    previous_amount = FloatField()
    current_amount = FloatField()
    notes = TextField()

    class Meta:
        db_table = 'paydiffs'

    def __str__(self):
        return '%s: %d, %d' % \
               (self.field_name,
                self.previous_amount,
                self.current_amount)
