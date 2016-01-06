from models import PayRun, PayRecord, PayDiff, Employee


def import_data():
    path = 'c:\\bench\\payrun\\pyvista\\fms\\tests\\run'
    runs = {
        '559': '13-15',
        '560': '13-16',
        '616': '15-20',
        '617': '15-21',
        '618': '15-22',
        '619': '15-23'
    }

    for ien, pp in runs.items():
        for cp in ['015', '016']:
            run = make_run(ien, pp, cp)

            filename = path + ien + '_' + cp + '.txt'
            f = open(filename)
            dta = f.readlines()
            f.close()

            for line in dta:
                if line[0].isdigit():
                    emp = make_emp(line, cp)
                    make_rec(line.rstrip(), run.id, emp.id)


def make_run(ien, pp, cp):
    parts = pp.split('-')
    run = PayRun.create(
        ien=ien,
        fy=int(parts[0]),
        pp=int(parts[1]),
        cp=cp
    )
    return run


def make_emp(line, cp):
    flds = line.split('^')
    if Employee.has_record(flds[1]):
        return Employee.get_by_name(flds[1])
    emp = Employee.create(
        dfn=flds[0],
        name=flds[1],
        grade=int(flds[2]),
        step=int(flds[3]),
        fte=int(float(flds[4])),
        cp=cp
    )
    return emp


def make_rec(line, payrun_id, employee_id):
    flds = line.split('^')
    rec = PayRecord.create(
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
