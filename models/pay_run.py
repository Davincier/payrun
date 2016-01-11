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

    # Has many PayRecord (records_query)
    records = None

    # Has many PayDiff (diffs_query)
    diffs = None

    class Meta:
        db_table = 'payruns'

    def __str__(self):
        return '%s-%s-%s' % (self.fy, self.pp, self.cp)

    @staticmethod
    def get_all():
        return [run for run in PayRun.select().order_by(
            PayRun.fy.desc(), PayRun.pp.desc(), PayRun.cp
        )]

    @staticmethod
    def get_one(run_id):
        run = PayRun.get(PayRun.id == run_id)
        run.add_manys()
        return run

    @staticmethod
    def get_by_tag(tag_str):
        tag = PayRun.get_tag(tag_str)
        try:
            run = PayRun.get(
                (PayRun.fy == tag.fy) &
                (PayRun.pp == tag.pp) &
                (PayRun.cp == tag.cp)
            )
            run.add_manys()
        except PayRun.DoesNotExist:
            run = None
        return run

    def get_record_for_employee(self, name):
        from models import Employee
        qry = self.records_query.select().join(Employee).where(Employee.name == name)
        if not qry.exists():
            return None
        return qry.get()

    def add_manys(self):
        self.records = [rec for rec in self.records_query]
        self.diffs = self._build_diffs()

    def _build_diffs(self):
        from collections import OrderedDict
        diff_list = [diff for diff in self.diffs_query]
        diff_dict = {}
        for diff in diff_list:
            if diff.record.employee.name not in diff_dict:
                diff_dict[diff.record.employee.name] = []
            diff_dict[diff.record.employee.name].append(diff)
        od = OrderedDict(sorted(diff_dict.items()))
        return od

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
        return PayRunTag(fy=int(parts[0]), pp=int(parts[1]), cp=parts[2])

    def make_diffs(self):
        from models import PayRecord, PayDiff
        from app import db
        prev_rex = self._get_previous_records()
        if not prev_rex:
            return
        for current_rec in self.records:
            qry = prev_rex.select().where(PayRecord.employee == current_rec.employee)
            if not qry.exists():
                continue
            rec_diffs = PayRecord.get_diffs(prev_rex.get(), current_rec)
            if rec_diffs:
                with db.atomic():
                    PayDiff.insert_many(rec_diffs).execute()

    def get_previous_run_id(self):
        prev_tag = self.previous_tag()
        try:
            run_id = PayRun.get(
                (PayRun.fy == prev_tag.fy) &
                (PayRun.pp == prev_tag.pp) &
                (PayRun.cp == prev_tag.cp)
            ).id
        except PayRun.DoesNotExist:
            run_id = None
        return run_id

    def _get_previous_records(self):
        from models import PayRecord
        prev_id = self.get_previous_run_id()
        return [PayRecord(r)
                for r in PayRecord.select().where(
                PayRecord.payrun == prev_id)
                ] or None

    # def save(self):
        # self.db.payruns.insert({'tag': self.tag, 'diffs': self.diffs})
