from app import db
from models import PayRun, PayRecord, PayDiff, Employee


def import_data():
    path = 'c:\\bench\\payrun\\pyvista\\fms\\tests\\run'
    runs = [
        {'ien': '559', 'fy': 13, 'pp': 15, 'cp': '015'},
        {'ien': '559', 'fy': 13, 'pp': 15, 'cp': '016'},
        {'ien': '560', 'fy': 13, 'pp': 16, 'cp': '015'},
        {'ien': '560', 'fy': 13, 'pp': 16, 'cp': '016'},
        {'ien': '616', 'fy': 15, 'pp': 20, 'cp': '015'},
        {'ien': '616', 'fy': 15, 'pp': 20, 'cp': '016'},
        {'ien': '617', 'fy': 15, 'pp': 21, 'cp': '015'},
        {'ien': '617', 'fy': 15, 'pp': 21, 'cp': '016'},
        {'ien': '618', 'fy': 15, 'pp': 22, 'cp': '015'},
        {'ien': '618', 'fy': 15, 'pp': 22, 'cp': '016'},
        {'ien': '619', 'fy': 15, 'pp': 23, 'cp': '015'},
        {'ien': '619', 'fy': 15, 'pp': 23, 'cp': '016'}
    ]
    with db.atomic():
        PayRun.insert_many(runs).execute()

    for run in PayRun.select():

        filename = path + run.ien + '_' + run.cp + '.txt'
        f = open(filename)
        dta = f.readlines()
        f.close()

        for line in dta:
            if line[0].isdigit():
                emp = make_emp(line, run.cp)
                rec = make_rec(line.rstrip(), run.id, emp.id)
                prev_run_id = run.get_previous_run_id()
                if prev_run_id:
                    rec.make_diffs(prev_run_id)


def make_emp(line, cp):
    flds = line.split('^')
    if Employee.has_record(flds[1]):
        return Employee.get_by_name(flds[1])
    return Employee.create(
        dfn=flds[0],
        name=flds[1],
        grade=int(flds[2]),
        step=int(flds[3]),
        fte=int(float(flds[4]) * 100),
        cp=cp
    )


def make_rec(line, payrun_id, employee_id):
    flds = line.split('^')
    return PayRecord.create(
        payrun=payrun_id,
        employee=employee_id,
        normal_hours_8b=int(flds[5]),
        normal_hours=int(flds[6]),
        oasdi_tax_va_share_cppd=to_float(flds[7]),
        fegli_va_share_cppd=to_float(flds[8]),
        health_benefits_va_share_cppd=to_float(flds[9]),
        retirement_va_share_cppd=to_float(flds[10]),
        tsp_csf_gov_basic_contrib=to_float(flds[11]),
        tsp_gsf_gov_basic_contrib=to_float(flds[12]),
        tsp_csf_gov_match_contrib=to_float(flds[13]),
        tsp_gsf_gov_match_contrib=to_float(flds[14]),
        base_pay_cppd=to_float(flds[15]),
        holiday_amt=to_float(flds[16]),
        overtime_amt_cppd=to_float(flds[17]),
        gross_pay_plus_benefits_cppd=to_float(flds[18]),
        overtime_hours_wk_1=to_float(flds[19]),
        overtime_hours_wk_2=to_float(flds[20]),
        overtime_amt_wk_1=to_float(flds[21]),
        overtime_amt_wk_2=to_float(flds[22]),
        hrs_excess_8_day_wk_1=to_float(flds[23]),
        hrs_excess_8_day_wk_2=to_float(flds[24]),
        hrs_excess_8_day_amt_wk_1=to_float(flds[25]),
        hrs_excess_8_day_amt_wk_2=to_float(flds[26])
    )


def to_float(value):
    if value == '':
        return None
    return float(value)


if __name__ == '__main__':
    import_data()
    print('Done')
