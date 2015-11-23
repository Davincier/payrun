# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Nov 23 09:30:52 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tablePayruns = QtWidgets.QTableWidget(self.centralwidget)
        self.tablePayruns.setGeometry(QtCore.QRect(20, 60, 491, 192))
        self.tablePayruns.setColumnCount(3)
        self.tablePayruns.setObjectName("tablePayruns")
        self.tablePayruns.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tablePayruns.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePayruns.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePayruns.setHorizontalHeaderItem(2, item)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(510, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.scrollDetail = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollDetail.setGeometry(QtCore.QRect(20, 270, 761, 281))
        self.scrollDetail.setWidgetResizable(True)
        self.scrollDetail.setObjectName("scrollDetail")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 759, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollDetail.setWidget(self.scrollAreaWidgetContents)
        self.listEmployee = QtWidgets.QListWidget(self.centralwidget)
        self.listEmployee.setGeometry(QtCore.QRect(530, 60, 256, 192))
        self.listEmployee.setObjectName("listEmployee")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "allocat: payruns"))
        item = self.tablePayruns.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Payrun"))
        item = self.tablePayruns.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Records"))
        item = self.tablePayruns.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Differences"))
        self.pushButton.setText(_translate("MainWindow", "Add Payrun"))

