from models.pay_record import PayRecord


class PayRun(object):

    def __init__(self, dct):
        self.id = dct['_id']
        self.fy = dct['fy']
        self.pp = dct['pp']
        self.cp = dct['cp']
        if 'rex' in dct:
            self.rex = [PayRecord(rec) for rec in dct['rex']]
        if 'diffs' in dct:
            self.diffs = dct['diffs']

    def __str__(self):
        return '%02d-%02d' % (self.fy, self.pp)