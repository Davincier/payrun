from peewee import *
from .base_model import BaseModel


class PayRun(BaseModel):

    ien = CharField()
    cp = CharField()
    fy = IntegerField()
    pp = IntegerField()
    notes = TextField()
    # Has many PayRecord (records)
    # Has many PayRunDiff (diffs)

    class Meta:
        db_table = 'payruns'

    def __str__(self):
        return '%s-%s-%s' % (self.fy, self.pp, self.cp)

    @staticmethod
    def get_all():
        return [
            rec for rec in PayRun.select().order_by(
                PayRun.fy.desc(), PayRun.pp.desc(), PayRun.cp
            )
        ]

    @staticmethod
    def get_one(run_id):
        return PayRun.get(PayRun.id == run_id)

    @staticmethod
    def get_id(ien):
        qry = PayRun.select().where(PayRun.ien == ien)
        return qry.get().id if qry.exists() else None

    def add_records(self, records):
        for rec in records:
            rec.payrun = self.id
        with self._meta.database.atomic():
            PayRecord.insert_many(records)

    @staticmethod
    def make_tag(fy, pp, cp):
        return '%02d-%02d-%s' % (fy, pp, cp)

    def next_tag(self):
        fy = self.fy
        pp = self.pp + 1
        if pp > 26:
            pp = 1
            fy += 1
        return PayRun.make_tag(fy, pp, self.cp)

    def previous_tag(self):
        fy = self.fy
        pp = self.pp - 1
        if pp == 0:
            pp = 26
            fy -= 1
        return PayRun.make_tag(fy, pp, self.cp)

    @staticmethod
    def pay_period(tag):
        parts = tag.split('-')
        return '%02d-%02d' % (parts[0], parts[1])

    def make_diffs(self, ):
        pass
        # from models import PayRecord
        # prev_rex = self._get_previous_records()
        # self.diffs = {}
        # if not prev_rex:
        #     return
        # for current_rec in self.rex:
        #     key = current_rec['EMPLOYEE UID']
        #     if not key in prev_rex:
        #         continue
        #     prev_rec = prev_rex[key]
        #     rec_diffs = PayRecord.get_diffs(prev_rec, current_rec)
        #     if rec_diffs:
        #         self.diffs[current_rec['EMPLOYEE']] = rec_diffs

    def _get_previous_records(self):
        pass
        # query = {'PAYRUN': self.previous_tag()}
        # rex = self.db.payrun_records.find(query)
        # result = {}
        # for rec in rex:
        #     result[rec['EMPLOYEE UID']] = rec
        # return result

    # def save(self):
        # self.db.payruns.insert({'tag': self.tag, 'diffs': self.diffs})
