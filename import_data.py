__author__ = 'Joe'

flds = {
    'employee_id': 'EMPLOYEE',
    'grade': 'GRADE',
    'step': 'STEP',
    'fte_equivalent': 'FTE',
    'normal_hours_8b': '8B NORMAL HOURS',
    'normal_hours': 'NORMAL HOURS',
    'oasdi_tax_va_share_cppd': 'OASDI TAX VA SHARE CPPD',
    'fegli_va_share_cppd': 'FEGLI VA SHARE CPPD',
    'health_benefits_va_share_cppd': 'HEALTH BENEFITS VA SHARE CPPD',
    'retirement_va_share_cppd': 'RETIREMENT VA SHARE CPPD',
    'tsp_csf_gov_basic_contrib': 'TSP CSF GOV BASIC CONTRIB',
    'tsp_gsf_gov_basic_contrib': 'TSP GSF GOV BASIC CONTRIB',
    'tsp_csf_gov_match_contrib': 'TSP CSF GOV MATCH CONTRIB',
    'tsp_gsf_gov_match_contrib': 'TSP GSF GOV MATCH CONTRIB',
    'base_pay_cppd': 'BASE PAY CPPD',
    'holiday_amt': 'HOLIDAY AMT',
    'overtime_amt_cppd': 'OVERTIME AMT CPPD',
    'gross_pay_plus_benefits_cppd': 'GROSS PAY PLUS BENEFITS CPPD',
    'overtime_hours_wk_1': 'OVERTIME HOURS WK 1',
    'overtime_hours_wk_2': 'OVERTIME HOURS WK 2',
    'overtime_amt_wk_1': 'OVERTIME AMT WK 1',
    'overtime_amt_wk_2': 'OVERTIME AMT WK 2',
    'hrs_excess_8_day_wk_1': 'HRS EXCESS 8 DAY WK 1',
    'hrs_excess_8_day_wk_2': 'HRS EXCESS 8 DAY WK 2',
    'hrs_excess_8_day_amt_wk_1': 'HRS EXCESS 8 DAY AMT WK 1',
    'hrs_excess_8_day_amt_wk_2': 'HRS EXCESS 8 DAY AMT WK 2'
}

def import_data(sql_db, mongo_db):
    tbl = 'efms_pay_runs'
    sql = 'select * from ' + tbl
    sql_payruns = get_sql_data(sql_db, tbl, sql)

    employees = {}
    for employee in sql_db.execute_sql('select id,name from staff'):
        employees[employee[0]] = employee[1]

    for sql_run in sql_payruns:
        json_run = {
            'fy': sql_run['fy'],
            'pp': sql_run['pay_period'],
            'cp': sql_run['cp_nbr'],
            'rex': [],
            'diffs': []
        }

        tbl = 'efms_pay_run_records'
        sql = 'select * from ' + tbl + ' where payrun_id=' + str(sql_run['id'])
        rex = get_sql_data(sql_db, tbl, sql)
        newrex = []
        for rec in rex:
            newrec = {}
            for sqlname in flds:
                newrec[flds[sqlname]] = rec[sqlname]
            newrec['EMPLOYEE'] = employees[newrec['EMPLOYEE']]
            newrex.append(newrec)
        json_run['rex'] = newrex

        tbl = 'efms_pay_run_diffs'
        sql = 'select * from ' + tbl + ' where payrun_id=' + str(sql_run['id'])
        diffs = {}
        diff_data = get_sql_data(sql_db, tbl, sql)
        for diff in diff_data:
            if not diff['field_name'] in flds:
                continue
            employee = employees[diff['employee_id']]
            diff['field_name'] = flds[diff['field_name']]
            del diff['id']
            del diff['employee_id']
            del diff['payrun_id']
            if not employee in diffs:
                diffs[employee] = []
            diffs[employee].append(diff)
        json_run['diffs'] = diffs

        mongo_db.payruns.insert(json_run)


def get_sql_data(db, table, sql):
    fldnames = [f.name for f in db.get_columns(table)]
    rex = db.execute_sql(sql).fetchall()
    return [dict(zip(fldnames, rec)) for rec in rex]


if __name__ == '__main__':
    from peewee import *
    from pymongo import MongoClient

    sql_db = SqliteDatabase('rdt.db')
    mongo_db = MongoClient('localhost', 3001).meteor

    import_data(sql_db, mongo_db)

    print('Done')
