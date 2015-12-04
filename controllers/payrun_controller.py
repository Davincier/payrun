from PyQt5.QtWidgets import QListWidgetItem
from models import PayRun, PayRecord
from views import PayrunWidget, PayDiffsWidget


class PayrunController(object):
    def __init__(self, db):
        self.widget = PayrunWidget()
        self.ui = self.widget.ui
        self.db = db
        self.load_payruns(self.ui.payrunList)
        self.payrun_selected(self.ui.payrunList.item(0))
        self.ui.payrunList.clicked.connect(self.payrun_selected)
        self.ui.employeeList.clicked.connect(self.employee_selected)
        # self.ui.addRunButton.clicked.connect(self.add_next_run)

    def load_payruns(self, lst):
        self.payruns = PayRun.get_runs(self.db)
        for payrun in self.payruns:
            lst.addItem(QListWidgetItem(payrun.tag))
        lst.item(0).setSelected(True)

    def payrun_selected(self, item):
        if type(item) is QListWidgetItem:
            run_tag = item.text()
        else:
            run_tag = str(item.data())

        self.run = self.get_run(run_tag)
        self.run.get_children()

        self.load_employees()
        self.ui.payrunGrid.addWidget(PayDiffsWidget(self.run.diffs), 1, 1, 4, 1)

    def get_run(self, tag):
        xx = [x for x in self.payruns if x.tag == tag]
        return xx[0] if xx else None

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

        from controllers import PayrecController
        controller = PayrecController(self.run.tag, rec)
        controller.runit()

    def runit(self):
        self.widget.show()

    # def add_next_run(self, db):
    #     latest_run_tag = self.ui.payrunList.item(0).text()
    #     tmp = self.parse_payrun_str(latest_run)
    #     run_id = PayRun.get_next_payrun_id(tmp['fy'], tmp['pp'])
    #
    #     vc = VistaController()
    #     run = vc.get_payrun(run_id)
    #
    #     PayRun.save_run(db, run_id, run)
