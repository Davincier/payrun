from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFont
from views.payrec_widget_ui import Ui_PayrecWidget


class PayrecWidget(QDialog):
    def __init__(self):
        super(PayrecWidget, self).__init__()
        self.ui = Ui_PayrecWidget()
        self.ui.setupUi(self)
        font = QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ui.rec_label.setFont(font)
        self.ui.gsf_label.setFont(font)

    def load_record(self, payrun, payrec, fields):
        self._load_employee_label(str(payrec.employee))
        self._load_run_label(payrun)
        self._load_table(payrec, fields)

    def _load_employee_label(self, text):
        self.ui.rec_label.setText(text)

    def _load_run_label(self, text):
        self.ui.gsf_label.setText(text)

    def _load_table(self, payrec, fields):
        from PyQt5.QtWidgets import QTableWidgetItem

        # I have no fucking idea why setItem needs a -1 row,
        # but this "works"
        for row, field in enumerate(fields):
            s = str(getattr(payrec, field))
            if s == 'None':
                s = ''
            self.ui.rec_table.setItem(row - 1, 1, QTableWidgetItem(s))


# fields = [
#     '8B NORMAL HOURS',
#     'NORMAL HOURS',
#     'OASDI TAX VA SHARE CPPD',
#     'FEGLI VA SHARE CPPD',
#     'HEALTH BENEFITS VA SHARE CPPD',
#     'RETIREMENT VA SHARE CPPD',
#     'TSP CSF GOV BASIC CONTRIB',
#     'TSP GSF GOV BASIC CONTRIB',
#     'TSP CSF GOV MATCH CONTRIB',
#     'TSP GSF GOV MATCH CONTRIB',
#     'BASE PAY CPPD',
#     'HOLIDAY AMT',
#     'OVERTIME AMT CPPD',
#     'GROSS PAY PLUS BENEFITS CPPD',
#     'OVERTIME HOURS WK 1',
#     'OVERTIME HOURS WK 2',
#     'OVERTIME AMT WK 1',
#     'OVERTIME AMT WK 2',
#     'HRS EXCESS 8 DAY WK 1',
#     'HRS EXCESS 8 DAY WK 2',
#     'HRS EXCESS 8 DAY AMT WK 1',
#     'HRS EXCESS 8 DAY AMT WK 2'
# ]
