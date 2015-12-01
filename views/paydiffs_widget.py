from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, \
    QScrollArea, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class PayDiffsWidget(QWidget):

    def __init__(self, diffs, parent=None):
        super(PayDiffsWidget, self).__init__()

        widget = QWidget()
        diffs_layout = QVBoxLayout()
        for employee in sorted(diffs):
            box = self.create_box(employee, diffs[employee])
            diffs_layout.addWidget(box)
        widget.setLayout(diffs_layout)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        widget_layout = QVBoxLayout()
        widget_layout.addWidget(scroll)
        self.setLayout(widget_layout)

    def create_box(self, employee, employee_diffs):
        box = QGroupBox()
        box.setTitle(employee)
        box_layout = QVBoxLayout()
        tbl = self.create_diff_table(employee_diffs)
        box_layout.addWidget(tbl)
        box.setLayout(box_layout)
        return box

    def create_diff_table(self, diffs):
        tbl = QTableWidget()
        tbl.setRowCount(len(diffs))
        tbl.setColumnCount(3)

        tbl.setHorizontalHeaderItem(0, QTableWidgetItem('Field'))
        tbl.setHorizontalHeaderItem(1, QTableWidgetItem('Current'))
        tbl.setHorizontalHeaderItem(2, QTableWidgetItem('Previous'))

        for row, diff in enumerate(diffs):
            tbl.setItem(row, 0, QTableWidgetItem(diff['field_name']))
            tbl.setItem(row, 1, QTableWidgetItem(str(diff['current_amount'])))
            tbl.setItem(row, 2, QTableWidgetItem(str(diff['previous_amount'])))

        tbl.verticalHeader().setVisible(False)
        tbl.resizeColumnsToContents()
        ht = tbl.rowHeight(0) * (tbl.rowCount() + 1)

        tbl.setFixedSize(tbl.horizontalHeader().length() + 20, ht)
        return tbl
