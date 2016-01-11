from peewee import *
from .base_model import BaseModel
from models import PayRun, Employee


class PayRecord(BaseModel):

    payrun = ForeignKeyField(PayRun, related_name='records_query')
    employee = ForeignKeyField(Employee, related_name='payrecords')
    normal_hours_8b = IntegerField()
    normal_hours = IntegerField()
    oasdi_tax_va_share_cppd = FloatField()
    fegli_va_share_cppd = FloatField()
    health_benefits_va_share_cppd = FloatField()
    retirement_va_share_cppd = FloatField()
    tsp_csf_gov_basic_contrib = FloatField()
    tsp_gsf_gov_basic_contrib = FloatField()
    tsp_csf_gov_match_contrib = FloatField()
    tsp_gsf_gov_match_contrib = FloatField()
    base_pay_cppd = FloatField()
    holiday_amt = FloatField()
    overtime_amt_cppd = FloatField()
    gross_pay_plus_benefits_cppd = FloatField()
    overtime_hours_wk_1 = FloatField()
    overtime_hours_wk_2 = FloatField()
    overtime_amt_wk_1 = FloatField()
    overtime_amt_wk_2 = FloatField()
    hrs_excess_8_day_wk_1 = FloatField()
    hrs_excess_8_day_wk_2 = FloatField()
    hrs_excess_8_day_amt_wk_1 = FloatField()
    hrs_excess_8_day_amt_wk_2 = FloatField()
    notes = TextField()
    # Has many PayDiff (diffs)

    class Meta:
        db_table = 'payrecords'

    def __str__(self):
        return '%s: %s' % (str(self.payrun), self.employee.name)

    def make_diffs(self, prev_run_id):
        from app import db, diff_fields
        from models import PayDiff

        prev_rec = self._get_previous_record(prev_run_id)
        if not prev_rec:
            return

        diffs = []
        for field in diff_fields[3:]:
            curval = getattr(self, field)
            preval = getattr(prev_rec, field)
            if curval != preval:
                diffs.append({
                    'payrun': self.payrun,
                    'record': self,
                    'field_name': field,
                    'current_amount': curval,
                    'previous_amount': preval
                })
        if diffs:
            with db.atomic():
                PayDiff.insert_many(diffs).execute()

    def _get_previous_record(self, prev_run_id):
        qry = PayRecord.select().where(
            (PayRecord.payrun == prev_run_id) &
            (PayRecord.employee == self.employee)
        )
        if not qry.exists():
            return None
        return qry.get()
