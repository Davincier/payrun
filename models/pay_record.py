class PayRecord(object):

    def __init__(self, dct):
        from models import PayEmployee
        self.employee = PayEmployee(
            dct['EMPLOYEE'],
            dct['GRADE'],
            dct['STEP'],
            dct['FTE']
        )
        self.rec = dct
        del self.rec['EMPLOYEE']
        del self.rec['GRADE']
        del self.rec['STEP']
        del self.rec['FTE']

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
