from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFont
from app import rec_fields
from views.payrec_widget_ui import Ui_PayrecWidget
from .helpers import *


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
        for row, field in enumerate(rec_fields):
            s = self._format_amount(field, getattr(payrec, field))
            self.ui.rec_table.setItem(row - 1, 1, QTableWidgetItem(s))

    def _format_amount(self, fldname, value):
        if fldname in [
            'normal_hours_8b',
            'normal_hours',
            'overtime_hrs_wk_1',
            'overtime_hrs_wk_2',
            'hrs_excess_8_day_wk1',
            'hrs_excess_8_day_wk2'
        ]:
            return str(value)
        # elif fldname in []:
        #     return to_money(value)
        # else:
        return to_money(value)
