projections = {
    'no_diffs': {'diffs': 0},
    'just_diffs': {'diffs': 1}
}


class PayRun(object):

    def __init__(self, db, dct):
        self.db = db
        if '_id' in dct:
            self.id = dct['_id']
        self.tag = dct['tag']
        if 'diffs' in dct:
            self.diffs = dct['diffs']
        self.split_tag()

    def __str__(self):
        return self.tag

    def split_tag(self):
        parts = self.tag.split('-')
        self.fy = int(parts[0])
        self.pp = int(parts[1])
        self.cp = parts[2]

    @staticmethod
    def make_tag(fy, pp, cp):
        return '%02d-%02d-%s' % (fy, pp, cp)

    @staticmethod
    def get_runs(db):
        return [PayRun(db, r) for r in db.payruns.find({}, projections['no_diffs']).sort('_id', -1)]

    def get_diffs(self):
        self.diffs = self.db.payruns.find_one({'_id': self.id})['diffs']

    def get_rex(self):
        from models import PayRecord
        query = {'PAYRUN': self.tag}
        self.rex = [PayRecord(rec) for rec in self.db.payrun_records.find(query).sort('EMPLOYEE')]

    def get_children(self):
        self.get_rex()
        self.get_diffs()

    def next_tag(self):
        fy = self.fy
        pp = self.pp + 1
        if pp > 26:
            pp = 1
            fy += 1
        return PayRun.make_tag(fy, pp, self.cp)

    def previous_tag(self):
        fy = self.fy
        pp = self.pp - 1
        if pp == 0:
            pp = 26
            fy -= 1
        return PayRun.make_tag(fy, pp, self.cp)

    @staticmethod
    def pay_period(tag):
        parts = tag.split('-')
        return '%02d-%02d' % (parts[0], parts[1])

    def make_diffs(self, ):
        from models import PayRecord
        prev_rex = self._get_previous_records()
        self.diffs = {}
        if not prev_rex:
            return
        for current_rec in self.rex:
            key = current_rec['EMPLOYEE UID']
            if not key in prev_rex:
                continue
            prev_rec = prev_rex[key]
            rec_diffs = PayRecord.get_diffs(prev_rec, current_rec)
            if rec_diffs:
                self.diffs[current_rec['EMPLOYEE']] = rec_diffs

    def _get_previous_records(self):
        query = {'PAYRUN': self.previous_tag()}
        rex = self.db.payrun_records.find(query)
        result = {}
        for rec in rex:
            result[rec['EMPLOYEE UID']] = rec
        return result

    def save(self):
        self.db.payruns.insert({'tag': self.tag, 'diffs': self.diffs})
