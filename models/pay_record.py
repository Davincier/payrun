from peewee import *
from .base_model import BaseModel
from models import PayRun, Employee


class PayRecord(BaseModel):

    payrun = ForeignKeyField(PayRun, related_name='records')
    employee = ForeignKeyField(Employee, related_name='payrecords')
    normal_hours_8b = IntegerField()
    normal_hours = IntegerField()
    oasdi_tax_va_share_cppd = DecimalField()
    fegli_va_share_cppd = DecimalField()
    health_benefits_va_share_cppd = DecimalField()
    retirement_va_share_cppd = DecimalField()
    tsp_csf_gov_basic_contrib = DecimalField()
    tsp_gsf_gov_basic_contrib = DecimalField()
    tsp_csf_gov_match_contrib = DecimalField()
    tsp_gsf_gov_match_contrib = DecimalField()
    base_pay_cppd = DecimalField()
    holiday_amt = DecimalField()
    overtime_amt_cppd = DecimalField()
    gross_pay_plus_benefits_cppd = DecimalField()
    overtime_hours_wk_1 = DecimalField()
    overtime_hours_wk_2 = DecimalField()
    overtime_amt_wk_1 = DecimalField()
    overtime_amt_wk_2 = DecimalField()
    hrs_excess_8_day_wk_1 = DecimalField()
    hrs_excess_8_day_wk_2 = DecimalField()
    hrs_excess_8_day_amt_wk_1 = DecimalField()
    hrs_excess_8_day_amt_wk_2 = DecimalField()
    notes = TextField()

    class Meta:
        db_table = 'payrecords'

    def __str__(self):
        return '%s: %s' % (str(self.payrun), self.employee.name)

    @staticmethod
    def batch_save(records):
        with BaseModel.database.atomic():
            PayRecord.insert_many()

    @staticmethod
    def get_for_employee(rex, name):
        xx = [x for x in rex if x.employee.name == name]
        return xx[0] if xx else None

    def make_diffs(self, prev_run_id):
        from app import db, diff_fields
        from models import PayDiff

        qry = PayRecord.select().where(PayRecord.payrun == prev_run_id)
        if not qry.exists():
            return
        diffs = []
        prev_rec = qry.get()
        for field in diff_fields[3:]:
            curval = getattr(self, field)
            preval = getattr(prev_rec, field)
            if curval != preval:
                diffs.append({
                    'payrun': self.payrun,
                    'employee': self.employee,
                    'field_name': field,
                    'current_amount': curval,
                    'previous_amount': preval
                })
        with db.atomic():
            PayDiff.insert_many(diffs).execute()
