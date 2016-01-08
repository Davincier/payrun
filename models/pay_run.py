from collections import namedtuple
from peewee import *
from .base_model import BaseModel

PayRunTag = namedtuple('PayRunTag', ['fy', 'pp', 'cp'])


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
        return PayRun.select().order_by(
            PayRun.fy.desc(), PayRun.pp.desc(), PayRun.cp
        )

    @staticmethod
    def get_one(run_id):
        return PayRun.get(PayRun.id == run_id)

    @staticmethod
    def get_id(ien):
        qry = PayRun.select().where(PayRun.ien == ien)
        return qry.get().id if qry.exists() else None

    def previous_tag(self):
        fy = self.fy
        pp = self.pp - 1
        if pp == 0:
            pp = 26
            fy -= 1
        return PayRunTag(fy=fy, pp=pp, cp=self.cp)

    @staticmethod
    def pay_period(tag_str):
        tag = PayRun.get_tag(tag_str)
        return '%02d-%02d' % (tag.fy, tag.pp)

    @staticmethod
    def get_tag(tag_str):
        parts = tag_str.split('-')
        return PayRunTag(fy=parts[0], pp=parts[1], cp=parts[2])

    def make_diffs(self):
        from models import PayRecord, PayDiff
        from app import db
        prev_rex = self._get_previous_records()
        diffs = {}
        if not prev_rex:
            return
        print(str(self))
        for current_rec in self.records:
            # print(current_rec.employee.name)
            qry = prev_rex.select().where(PayRecord.employee == current_rec.employee)
            if not qry.exists():
                continue
            rec_diffs = PayRecord.make_diffs(prev_rex.get(), current_rec)
            if rec_diffs:
                # with db.atomic():
                #     PayDiff.insert_many(rec_diffs).execute()
                diffs[current_rec.employee.id] = rec_diffs
        pass

    def get_previous_run_id(self):
        prev_tag = self.previous_tag()
        qry = PayRun.select().where(
            (PayRun.fy == prev_tag.fy) &
            (PayRun.pp == prev_tag.pp) &
            (PayRun.cp == prev_tag.cp)
        )
        if not qry.exists():
            return None
        return qry.get().id

    def _get_previous_records(self):
        prev_ien = int(self.ien) - 1
        qry = PayRun.select().where((PayRun.ien == prev_ien) & (PayRun.cp == self.cp))
        if not qry.exists():
            return None
        prev_run = qry.get()
        return prev_run.records

    # def save(self):
        # self.db.payruns.insert({'tag': self.tag, 'diffs': self.diffs})
