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
            run.save()

            filename = path + ien + '_' + cp + '.txt'
            f = open(filename)
            dta = f.readlines()
            f.close()

            emp = None
            rex = []
            for line in dta:
                if line[0].isdigit():
                    emp = make_emp(line)
                    emp.cp = cp
                    emp.save()
                    rex.append(make_rec(line.rstrip()))
            emp.add_records(rex)
            run.add_records(rex)
    pass


def make_run(ien, pp, cp):
    run = PayRun()
    run.ien = ien
    parts = pp.split('-')
    run.fy = parts[0]
    run.pp = parts[1]
    run.cp = cp
    run.id = PayRecord.get_id(ien)
    return run


def make_emp(line):
    flds = line.split('^')
    emp = Employee()
    emp.dfn = flds[0]
    emp.name = flds[1]
    emp.grade = int(flds[2])
    emp.step = int(flds[3])
    emp.fte = int(float(flds[4]) * 100)
    emp.id = Employee.get_id(emp.name)
    return emp


def make_rec(line):
    flds = line.split('^')
    rec = PayRecord()
    rec.normal_hours_8b = int(flds[5])
    rec.normal_hours = int(flds[6])
    rec.oasdi_tax_va_share_cppd = to_float(flds[7])
    rec.fegli_va_share_cppd = to_float(flds[8])
    rec.health_benefits_va_share_cppd = to_float(flds[9])
    rec.retirement_va_share_cppd = to_float(flds[10])
    rec.tsp_csf_gov_basic_contrib = to_float(flds[11])
    rec.tsp_gsf_gov_basic_contrib = to_float(flds[12])
    rec.tsp_csf_gov_match_contrib = to_float(flds[13])
    rec.tsp_gsf_gov_match_contrib = to_float(flds[14])
    rec.base_pay_cppd = to_float(flds[15])
    rec.holiday_amt = to_float(flds[16])
    rec.overtime_amt_cppd = to_float(flds[17])
    rec.gross_pay_plus_benefits_cppd = to_float(flds[18])
    rec.overtime_hours_wk_1 = to_float(flds[19])
    rec.overtime_hours_wk_2 = to_float(flds[20])
    rec.overtime_amt_wk_1 = to_float(flds[21])
    rec.overtime_amt_wk_2 = to_float(flds[22])
    rec.hrs_excess_8_day_wk_1 = to_float(flds[23])
    rec.hrs_excess_8_day_wk_2 = to_float(flds[24])
    rec.hrs_excess_8_day_amt_wk_1 = to_float(flds[25])
    rec.hrs_excess_8_day_amt_wk_2 = to_float(flds[26])
    return rec


def to_float(value):
    if value == '':
        return None
    return float(value)


if __name__ == '__main__':
    import_data()
    print('Done')
