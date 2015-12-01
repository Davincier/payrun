from PyQt5.QtWidgets import QWidget, QListWidgetItem
from views.payrun_widget_ui import Ui_payrunWidget


class PayrunWidget(QWidget):
    def __init__(self):
        super(PayrunWidget, self).__init__()
        self.ui = Ui_payrunWidget()
        self.ui.setupUi(self)
