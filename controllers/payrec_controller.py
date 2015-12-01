from views.payrec_widget import PayrecWidget


fields = [
    '8B NORMAL HOURS',
    'NORMAL HOURS',
    'OASDI TAX VA SHARE CPPD',
    'FEGLI VA SHARE CPPD',
    'HEALTH BENEFITS VA SHARE CPPD',
    'RETIREMENT VA SHARE CPPD',
    'TSP CSF GOV BASIC CONTRIB',
    'TSP GSF GOV BASIC CONTRIB',
    'TSP CSF GOV MATCH CONTRIB',
    'TSP GSF GOV MATCH CONTRIB',
    'BASE PAY CPPD',
    'HOLIDAY AMT',
    'OVERTIME AMT CPPD',
    'GROSS PAY PLUS BENEFITS CPPD',
    'OVERTIME HOURS WK 1',
    'OVERTIME HOURS WK 2',
    'OVERTIME AMT WK 1',
    'OVERTIME AMT WK 2',
    'HRS EXCESS 8 DAY WK 1',
    'HRS EXCESS 8 DAY WK 2',
    'HRS EXCESS 8 DAY AMT WK 1',
    'HRS EXCESS 8 DAY AMT WK 2'
]


class PayrecController(object):
    def __init__(self, payrun, payrec):
        self.widget = PayrecWidget()
        self.ui = self.widget.ui
        self.payrun = payrun
        self.payrec = payrec
        self.load_record()

    def load_record(self):
        self.load_rec_label()
        self.load_gsf_label()
        self.load_table()

    def load_rec_label(self):
        self.ui.rec_label.setText(str(self.payrec.employee))

    def load_gsf_label(self):
        s = 'PAY PERIOD: %02d-%02d, FCP: %s' % \
            (self.payrun['fy'], self.payrun['pp'], self.payrun['cp'])
        self.ui.gsf_label.setText(s)

    def load_table(self):
        from PyQt5.QtWidgets import QTableWidgetItem

        # I have no fucking idea why setItem needs a -1 row,
        # but this "works"
        for row, field in enumerate(fields):
            self.ui.rec_table.setItem(row-1, 1, QTableWidgetItem(str(self.payrec.rec[field])))

    def runit(self):
        self.widget.exec_()
