from PyQt5.QtWidgets import QListWidgetItem
from views.payrun_widget import PayrunWidget
from views.paydiffs_widget import PayDiffsWidget
from models.pay_run import PayRun
from models.pay_record import PayRecord
from controllers.payrec_controller import PayrecController


class PayrunController(object):
    def __init__(self, db):
        self.widget = PayrunWidget()
        self.ui = self.widget.ui
        self.db = db
        self.load_payruns(self.ui.payrunList)
        self.payrun_selected(self.ui.payrunList.item(0))
        self.ui.payrunList.clicked.connect(self.payrun_selected)
        self.ui.employeeList.clicked.connect(self.employee_selected)

    def load_payruns(self, lst):
        for payrun in PayRun.get_runs(self.db):
            lst.addItem(QListWidgetItem(payrun.__str__()))

        lst.item(0).setSelected(True)

    def payrun_selected(self, item):
        if type(item) is QListWidgetItem:
            run_ids = self.parse_payrun_str(item.text())
        else:
            run_ids = self.parse_payrun_str(str(item.data()))

        self.run = PayRun.get_run(self.db, run_ids)
        self.load_employees()
        self.ui.payrunGrid.addWidget(PayDiffsWidget(self.run.diffs), 1, 1, 4, 1)

    def parse_payrun_str(self, s):
        parts = s.split(':')
        cp_nbr = parts[1].strip(' ')
        parts = parts[0].split('-')
        fy = int(parts[0])
        pay_period = int(parts[1])
        return {
            'fy': fy, 'pp': pay_period, 'cp': cp_nbr
        }

    def load_employees(self):
        if not self.run:
            return

        lst = self.ui.employeeList
        lst.clear()

        for rec in self.run.rex:
            lst.addItem(QListWidgetItem(rec.employee.name))
        lst.item(0).setSelected(True)

    def employee_selected(self, item):
        rec = PayRecord.get_for_employee(self.run.rex, str(item.data()))
        if not rec:
            return

        controller = PayrecController(self.parse_payrun_str(str(self.run)), rec)
        controller.runit()

    def runit(self):
        self.widget.show()