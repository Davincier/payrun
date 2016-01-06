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

    @staticmethod
    def batch_save(records):
        with BaseModel.database.atomic():
            PayRecord.insert_many()

    @staticmethod
    def get_for_employee(rex, name):
        xx = [x for x in rex if x.employee.name == name]
        return xx[0] if xx else None

    @staticmethod
    def get_diffs(previous_rec, current_rec):
        diffs = []
        for field in current_rec:
            if field in ['_id', 'PAYRUN']:
                continue
            if current_rec[field] != previous_rec[field]:
                diffs.append({
                    'field_name': field,
                    'current_amount': current_rec[field],
                    'previous_amount': previous_rec[field]
                })
        return diffs
