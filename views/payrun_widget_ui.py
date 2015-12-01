# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'payrun_widget.ui'
#
# Created: Tue Dec  1 14:10:46 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_payrunWidget(object):
    def setupUi(self, payrunWidget):
        payrunWidget.setObjectName("payrunWidget")
        payrunWidget.resize(711, 626)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(payrunWidget.sizePolicy().hasHeightForWidth())
        payrunWidget.setSizePolicy(sizePolicy)
        payrunWidget.setBaseSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/greencat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        payrunWidget.setWindowIcon(icon)
        payrunWidget.setAutoFillBackground(False)
        self.gridLayout = QtWidgets.QGridLayout(payrunWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.payrunGrid = QtWidgets.QGridLayout()
        self.payrunGrid.setObjectName("payrunGrid")
        self.label_2 = QtWidgets.QLabel(payrunWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.payrunGrid.addWidget(self.label_2, 3, 0, 1, 1)
        self.payrunList = QtWidgets.QListWidget(payrunWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.payrunList.sizePolicy().hasHeightForWidth())
        self.payrunList.setSizePolicy(sizePolicy)
        self.payrunList.setObjectName("payrunList")
        self.payrunGrid.addWidget(self.payrunList, 2, 0, 1, 1)
        self.employeeList = QtWidgets.QListWidget(payrunWidget)
        self.employeeList.setObjectName("employeeList")
        self.payrunGrid.addWidget(self.employeeList, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(payrunWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.payrunGrid.addWidget(self.label, 0, 0, 1, 1)
        self.addRunButton = QtWidgets.QPushButton(payrunWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addRunButton.setFont(font)
        self.addRunButton.setObjectName("addRunButton")
        self.payrunGrid.addWidget(self.addRunButton, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(payrunWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.payrunGrid.addWidget(self.label_3, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.payrunGrid, 0, 0, 1, 1)

        self.retranslateUi(payrunWidget)
        QtCore.QMetaObject.connectSlotsByName(payrunWidget)

    def retranslateUi(self, payrunWidget):
        _translate = QtCore.QCoreApplication.translate
        payrunWidget.setWindowTitle(_translate("payrunWidget", "allocat: payruns"))
        self.label_2.setText(_translate("payrunWidget", "Employees"))
        self.label.setText(_translate("payrunWidget", "Pay Runs"))
        self.addRunButton.setText(_translate("payrunWidget", "Add Next Run"))
        self.label_3.setText(_translate("payrunWidget", "Differences"))

