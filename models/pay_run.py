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
        return '%02d-%02d: %s' % (self.fy, self.pp, self.cp)

    @staticmethod
    def get_runs(db):
        return [PayRun(r) for r in db.payruns.find({}, {'rex':0, 'diffs':0}).sort('_id', -1)]

    @staticmethod
    def get_run(db, run_ids):
        rec = PayRun(db.payruns.find_one(run_ids))
        rec.rex = sorted(rec.rex, key=lambda rec: rec.employee.name)
        return rec
