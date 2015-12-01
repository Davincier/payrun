from models.pay_employee import PayEmployee


class PayRecord(object):

    def __init__(self, dct):
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
