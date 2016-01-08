from PyQt5.QtWidgets import QWidget, QListWidgetItem
from views.payrun_widget_ui import Ui_payrunWidget


class PayrunWidget(QWidget):
    def __init__(self, controller):
        super(PayrunWidget, self).__init__()
        self.ui = Ui_payrunWidget()
        self.ui.setupUi(self)
        self.controller = controller
        self.ui.payrunList.clicked.connect(self.payrun_selected)
        self.ui.employeeList.clicked.connect(self.employee_selected)
        self.ui.addRunButton.clicked.connect(self.add_run_clicked)

    def load_payruns(self, payruns):
        self.ui.payrunList.clear()
        for payrun in payruns:
            self.ui.payrunList.addItem(QListWidgetItem(str(payrun)))

    def select_payrun(self, index):
        self.ui.payrunList.item(index).setSelected(True)
        self.payrun_selected(self.ui.payrunList.item(index))

    def payrun_selected(self, item):
        if type(item) is QListWidgetItem:
            tag_str = item.text()
        else:
            tag_str = str(item.data())
        self.controller.payrun_selected(tag_str)

    def load_employees(self, employee_names):
        self.ui.employeeList.clear()
        for employee in employee_names:
            self.ui.employeeList.addItem(QListWidgetItem(employee))

    def employee_selected(self, item):
        self.controller.employee_selected(str(item.data()))

    def add_run_clicked(self):
        latest_run_tag = self.ui.payrunList.item(0).text()
        self.controller.add_run_clicked(latest_run_tag)

    def add_diffs_widget(self, diffs_widget):
        self.ui.payrunGrid.addWidget(diffs_widget, 1, 1, 4, 1)