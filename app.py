__author__ = 'Joe'

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from forms.main_window import Ui_MainWindow


db = None


class PayrunApp(QMainWindow):
    def __init__(self):
        super(PayrunApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_payruns(self.ui.tablePayruns)

    def load_payruns(self, tbl):
        global db
        payruns = db.payruns.find({}, {'rex':0, 'diffs':0})

        for row, payrun in enumerate(payruns):
            run = '%02d-%02d:%s' % (payrun['fy'], payrun['pay_period'], payrun['cp_nbr'])
            tbl.insertRow(row)
            tbl.setItem(row, 0, QTableWidgetItem(run))
            self.rex_button = self.create_button('rex', tbl, payrun['_id'])
            tbl.setCellWidget(row, 1, self.rex_button)
            self.diffs_button = self.create_button('diffs', tbl, payrun['_id'])
            tbl.setCellWidget(row, 2, self.diffs_button)

    def create_button(self, name, tbl, run_id):
        btn = QPushButton(name, tbl)
        btn.setObjectName(name + '_' + str(run_id))
        btn.clicked.connect(self.cell_button_click)
        return btn

    def cell_button_click(self):
        from bson import ObjectId

        caller = self.sender().objectName()
        parts = caller.split('_')
        option = parts[0]
        run_id = ObjectId(parts[1])

        global db
        rec = db.payruns.find_one({'_id': run_id}, {option: 1})
        print(len(rec[option]))


def main():
    import sys
    from pymongo import MongoClient

    global db
    db = MongoClient('localhost', 3001).meteor

    app = QApplication(sys.argv)
    widget = PayrunApp()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
