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

