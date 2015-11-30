from PyQt5.QtWidgets import QWidget, QListWidgetItem
from forms.payrun_widget import Ui_payrunWidget
from forms.paydiffs_widget import PayDiffsWidget


class PayrunController(QWidget):
    def __init__(self, db):
        super(PayrunController, self).__init__()
        self.ui = Ui_payrunWidget()
        self.ui.setupUi(self)

        self.db = db

        self.load_payruns(self.ui.payrunList)
        self.payrun_selected(self.ui.payrunList.item(0))

    def load_payruns(self, lst):
        payruns = self.db.payruns.find({}, {'rex':0, 'diffs':0}).sort('_id', -1)

        for payrun in payruns:
            run = '%02d-%02d:%s' % (payrun['fy'], payrun['pp'], payrun['cp'])
            lst.addItem(QListWidgetItem(run))

        lst.item(0).setSelected(True)
        lst.clicked.connect(self.payrun_selected)

    def payrun_selected(self, item):
        if type(item) is QListWidgetItem:
            run_ids = self.parse_payrun_str(item.text())
        else:
            run_ids = self.parse_payrun_str(str(item.data()))

        self.run = self.db.payruns.find_one(run_ids)
        self.load_employees()
        self.ui.payrunGrid.addWidget(PayDiffsWidget(self.run['diffs']), 1, 1, 3, 1)

    def parse_payrun_str(self, s):
        parts = s.split(':')
        cp_nbr = parts[1]
        parts = parts[0].split('-')
        fy = int(parts[0])
        pay_period = int(parts[1])
        return {
            'fy': fy, 'pp': pay_period, 'cp': cp_nbr
        }

    def load_employees(self):
        if not self.run:
            return
        employees = self.run['rex']
        from operator import itemgetter
        employees = sorted(employees, key=itemgetter('EMPLOYEE'))
        lst = self.ui.employeeList
        lst.clear()
        for employee in employees:
            lst.addItem(QListWidgetItem(str(employee['EMPLOYEE'])))
        lst.item(0).setSelected(True)
        lst.clicked.connect(self.employee_selected)

    def employee_selected(self, item):
        employee_name = str(item.data())
        rec = next((r for r in self.run['rex'] if r['EMPLOYEE'] == employee_name), None)
        if not rec:
            return

        # from models.pay_employee import PayEmployee
        # payemp = PayEmployee(employee_name, 12, 3, '015')
        #
        # from models.pay_record import PayRecord
        # from models.pay_run import PayRun
        # payrec = PayRecord(self.run, rec)

        from controllers.payrec_controller import PayrecController
        controller = PayrecController(self.run, rec)
        controller.show_widget()