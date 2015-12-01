from PyQt5.QtWidgets import QDialog
from views.payrec_widget_ui import Ui_PayrecWidget


class PayrecWidget(QDialog):
    def __init__(self):
        super(PayrecWidget, self).__init__()
        self.ui = Ui_PayrecWidget()
        self.ui.setupUi(self)
