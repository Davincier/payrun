# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'payrun_widget.ui'
#
# Created: Fri Nov 27 14:26:02 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_payrunWidget(object):
    def setupUi(self, payrunWidget):
        payrunWidget.setObjectName("payrunWidget")
        payrunWidget.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(payrunWidget.sizePolicy().hasHeightForWidth())
        payrunWidget.setSizePolicy(sizePolicy)
        payrunWidget.setBaseSize(QtCore.QSize(0, 0))
        self.gridLayout = QtWidgets.QGridLayout(payrunWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.payrunGrid = QtWidgets.QGridLayout()
        self.payrunGrid.setObjectName("payrunGrid")
        self.label = QtWidgets.QLabel(payrunWidget)
        self.label.setObjectName("label")
        self.payrunGrid.addWidget(self.label, 0, 0, 1, 1)
        self.employeeList = QtWidgets.QListWidget(payrunWidget)
        self.employeeList.setObjectName("employeeList")
        self.payrunGrid.addWidget(self.employeeList, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(payrunWidget)
        self.label_2.setObjectName("label_2")
        self.payrunGrid.addWidget(self.label_2, 2, 0, 1, 1)
        self.payrunList = QtWidgets.QListWidget(payrunWidget)
        self.payrunList.setObjectName("payrunList")
        self.payrunGrid.addWidget(self.payrunList, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(payrunWidget)
        self.label_3.setObjectName("label_3")
        self.payrunGrid.addWidget(self.label_3, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.payrunGrid, 0, 0, 1, 1)

        self.retranslateUi(payrunWidget)
        QtCore.QMetaObject.connectSlotsByName(payrunWidget)

    def retranslateUi(self, payrunWidget):
        _translate = QtCore.QCoreApplication.translate
        payrunWidget.setWindowTitle(_translate("payrunWidget", "allocat: payruns"))
        self.label.setText(_translate("payrunWidget", "Pay Runs"))
        self.label_2.setText(_translate("payrunWidget", "Employees"))
        self.label_3.setText(_translate("payrunWidget", "Differences"))

