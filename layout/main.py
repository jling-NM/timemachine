# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './layout/main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(242, 307)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/timemachine_16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 221, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 184, 221, 81))
        self.textEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 168, 71, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 242, 19))
        self.menubar.setObjectName("menubar")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.actionEdit_Clients = QtWidgets.QAction(MainWindow)
        self.actionEdit_Clients.setObjectName("actionEdit_Clients")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionReport = QtWidgets.QAction(MainWindow)
        self.actionReport.setObjectName("actionReport")
        self.menuSetting.addAction(self.actionReport)
        self.menuSetting.addAction(self.actionEdit_Clients)
        self.menuSetting.addAction(self.actionExit)
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Time Machine"))
        self.label.setText(_translate("MainWindow", "Day Notes:"))
        self.menuSetting.setTitle(_translate("MainWindow", "&File"))
        self.actionEdit_Clients.setText(_translate("MainWindow", "&Client List"))
        self.actionEdit_Clients.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionReport.setText(_translate("MainWindow", "&Report"))
        self.actionReport.setShortcut(_translate("MainWindow", "Ctrl+R"))

import timemachine_rc
