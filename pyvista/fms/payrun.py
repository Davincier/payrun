__author__ = 'Joe'

from pyvista.rpc import DdrLister
from pyvista.rpc.gvv import *


class FmsPayrun(object):

    def __init__(self, cxn, pay_period):
        self.cxn = cxn
        self.pay_period = pay_period
        if cxn:
            self.ien = self._get_ien()

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
        return query

    def get(self, cps):
        rex = {}
        for cp in cps:
            query = self._build_query(cp)
            rex[cp] = query.find(self.cxn)
        return rex

    def _get_vista_field_str(self):
        return ';'.join([f[0] for f in fieldDefs])

    def _get_fieldnames(self):
        fieldnames = [f[1] for f in fieldDefs]
        fieldnames.insert(0, 'EMPLOYEE UID')
        return fieldnames

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


fieldDefs = [
    ('.01E', 'EMPLOYEE'),
    ('3', 'GRADE'),
    ('4', 'STEP'),
    ('10', 'FTE'),
    ('6', '8B NORMAL HOURS'),
    ('11', 'NORMAL HOURS'),
    ('29', 'OASDI TAX VA SHARE CPPD'),
    ('34', 'FEGLI VA SHARE CPPD'),
    ('37', 'HEALTH BENEFITS VA SHARE CPPD'),
    ('40', 'RETIREMENT VA SHARE CPPD'),
    ('61', 'TSP CSF GOV BASIC CONTRIB'),
    ('63', 'TSP GSF GOV BASIC CONTRIB'),
    ('64', 'TSP CSF GOV MATCH CONTRIB'),
    ('66', 'TSP GSF GOV MATCH CONTRIB'),
    ('85', 'BASE PAY CPPD'),
    ('88', 'HOLIDAY AMT'),
    ('94', 'OVERTIME AMT CPPD'),
    ('118', 'GROSS PAY PLUS BENEFITS CPPD'),
    ('131', 'OVERTIME HOURS WK 1'),
    ('132', 'OVERTIME HOURS WK 2'),
    ('133', 'OVERTIME AMT WK 1'),
    ('134', 'OVERTIME AMT WK 2'),
    ('135', 'HRS EXCESS 8 DAY WK 1'),
    ('136', 'HRS EXCESS 8 DAY WK 2'),
    ('137', 'HRS EXCESS 8 DAY AMT WK 1'),
    ('138', 'HRS EXCESS 8 DAY AMT WK 2')
]
