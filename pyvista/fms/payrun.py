__author__ = 'Joe'

from pyvista.rpc import DdrLister
from pyvista.rpc.gvv import *


def get_pay_run_ien(cxn, run_id):
    arg = '$O(^PRST(459,"B","%s",1))' % (run_id)
    return get_variable_value(cxn, arg)


def get_pay_period(cxn, ien):
    arg = '$G(^PRST(459,%s,0))' % ien
    response = get_variable_value(cxn, arg)
    parts = response.split('^')
    subparts = parts[0].split('-')
    return {
        'ien': ien,
        'fy': int(subparts[0]),
        'nbr': int(subparts[1]),
        'dt': int(parts[1])
    }


def get_latest_pay_period(cxn):
    hdr = get_global_header(cxn, 'PRST(459')
    return get_pay_period(cxn, hdr['last_ien'])


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

fields = [f[0] for f in fieldDefs]
fieldnames = [f[1] for f in fieldDefs]
fieldnames.insert(0, 'EMPLOYEE UID')

def get_payrun_records(cxn, ien, cp_nbr):
    query = DdrLister()
    query.file = '459.01'
    query.iens = ',%s,' % (ien,)
    query.fields = ';'.join(fields)
    query.index = 'B'
    query.screen = 'I $P(^(0),U,10)="%s"' % (cp_nbr,)
    query.fieldnames = fieldnames
    return query.find(cxn)

def get_multi_payrun_records(cxn, ien, cp_nbrs):
    rex = []
    for cp in cp_nbrs:
        rex += get_payrun_records(cxn, ien, cp)
    return rex

def get_payrun(cxn, cp_nbrs, ien=None):
    if ien is None:
        pp = get_latest_pay_period(cxn)
    else:
        pp = get_pay_period(cxn, ien)
    rex = get_multi_payrun_records(cxn, pp['ien'], cp_nbrs)
    return {
        'pay_period': pp,
        'records': rex
    }
