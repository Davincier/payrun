__author__ = 'Joe'

from pyvista.rpc import DdrLister
from pyvista.rpc.gvv import *


class FmsPayrun(object):

    def __init__(self, cxn, pay_period):
        self.cxn = cxn
        self.pay_period = pay_period
        if cxn:
            self.ien = self._get_ien()
        self.fieldDefs = [
            ('.01E', 'EMPLOYEE', self._no_convert),
            ('3', 'GRADE', self._convert_to_int),
            ('4', 'STEP', self._convert_to_int),
            ('10', 'FTE', self._fte_convert),
            ('6', '8B NORMAL HOURS', self._convert_to_int),
            ('11', 'NORMAL HOURS', self._convert_to_int),
            ('29', 'OASDI TAX VA SHARE CPPD', self._convert_to_float),
            ('34', 'FEGLI VA SHARE CPPD', self._convert_to_float),
            ('37', 'HEALTH BENEFITS VA SHARE CPPD', self._convert_to_float),
            ('40', 'RETIREMENT VA SHARE CPPD', self._convert_to_float),
            ('61', 'TSP CSF GOV BASIC CONTRIB', self._convert_to_float),
            ('63', 'TSP GSF GOV BASIC CONTRIB', self._convert_to_float),
            ('64', 'TSP CSF GOV MATCH CONTRIB', self._convert_to_float),
            ('66', 'TSP GSF GOV MATCH CONTRIB', self._convert_to_float),
            ('85', 'BASE PAY CPPD', self._convert_to_float),
            ('88', 'HOLIDAY AMT', self._convert_to_float),
            ('94', 'OVERTIME AMT CPPD', self._convert_to_float),
            ('118', 'GROSS PAY PLUS BENEFITS CPPD', self._convert_to_float),
            ('131', 'OVERTIME HOURS WK 1', self._convert_to_float),
            ('132', 'OVERTIME HOURS WK 2', self._convert_to_float),
            ('133', 'OVERTIME AMT WK 1', self._convert_to_float),
            ('134', 'OVERTIME AMT WK 2', self._convert_to_float),
            ('135', 'HRS EXCESS 8 DAY WK 1', self._convert_to_int),
            ('136', 'HRS EXCESS 8 DAY WK 2', self._convert_to_int),
            ('137', 'HRS EXCESS 8 DAY AMT WK 1', self._convert_to_float),
            ('138', 'HRS EXCESS 8 DAY AMT WK 2', self._convert_to_float)
        ]

    def __str__(self):
        return self.pay_period

    def _get_ien(self):
        arg = '$O(^PRST(459,"B","%s",1))' % (self.pay_period)
        return get_variable_value(self.cxn, arg)

    def _build_query(self, cp):
        query = DdrLister()
        query.file = '459.01'
        query.iens = ',%s,' % (self.ien,)
        query.fields = self._get_vista_field_str()
        query.index = 'B'
        query.screen = 'I $P(^(0),U,10)="%s"' % (cp,)
        query.fieldnames = self._get_fieldnames()
        return query

    def get_records(self, cps):
        rex = {}
        for cp in cps:
            query = self._build_query(cp)
            rex[cp] = query.find(self.cxn)
            for rec in rex[cp]:
                self._convert_fields(rec)
        return rex

    def _get_vista_field_str(self):
        return ';'.join([f[0] for f in self.fieldDefs])

    def _get_fieldnames(self):
        fieldnames = [f[1] for f in self.fieldDefs]
        fieldnames.insert(0, 'EMPLOYEE UID')
        return fieldnames

    def _convert_fields(self, rec):
        for field in self.fieldDefs:
            rec[field[1]] = field[2](rec[field[1]])

    def _no_convert(self, field):
        return field

    def _fte_convert(self, field):
        return int(float(field) * 100)

    def _convert_to_int(self, field):
        return int(field) if field else None

    def _convert_to_float(self, field):
        return float(field) if field else None

    # def get_pay_period(self):
    #     arg = '$G(^PRST(459,%s,0))' % self.ien
    #     response = get_variable_value(self.cxn, arg)
    #     parts = response.split('^')
    #     subparts = parts[0].split('-')
    #     return {
    #         'ien': self.ien,
    #         'fy': int(subparts[0]),
    #         'nbr': int(subparts[1]),
    #         'dt': int(parts[1])
    #     }
    #
    # def get_latest_pay_period(self):
    #     hdr = get_global_header(self.cxn, 'PRST(459')
    #     return self.get_pay_period(self.cxn, hdr['last_ien'])
