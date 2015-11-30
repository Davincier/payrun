from models.pay_run import PayRun


class PayRecord(object):

    def __init__(self, dct):
        self.employee = dct['EMPLOYEE']
        self.run = PayRun({
            '_id': dct['_id'],
            'fy': dct['fy'],
            'pp': dct['pp'],
            'cp': dct['cp']
        })
        self.rec = rec

    def __str__(self):
        return '%s, PAY PERIOD: %s, FCP: %s' % \
               (self.employee, self.run, self.run.cp)
