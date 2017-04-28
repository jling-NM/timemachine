# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './layout/edit_clients.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgEditClients(object):
    def setupUi(self, dlgEditClients):
        dlgEditClients.setObjectName("dlgEditClients")
        dlgEditClients.resize(321, 199)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgEditClients)
        self.buttonBox.setGeometry(QtCore.QRect(-32, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.inputNewClient = QtWidgets.QLineEdit(dlgEditClients)
        self.inputNewClient.setGeometry(QtCore.QRect(10, 100, 261, 20))
        self.inputNewClient.setObjectName("inputNewClient")
        self.clientListWidget = QtWidgets.QListWidget(dlgEditClients)
        self.clientListWidget.setGeometry(QtCore.QRect(10, 10, 261, 81))
        self.clientListWidget.setObjectName("clientListWidget")
        self.btnInsert = QtWidgets.QToolButton(dlgEditClients)
        self.btnInsert.setGeometry(QtCore.QRect(280, 100, 27, 20))
        self.btnInsert.setCheckable(False)
        self.btnInsert.setObjectName("btnInsert")
        self.btnRemove = QtWidgets.QToolButton(dlgEditClients)
        self.btnRemove.setGeometry(QtCore.QRect(280, 40, 27, 20))
        self.btnRemove.setCheckable(False)
        self.btnRemove.setObjectName("btnRemove")

        self.retranslateUi(dlgEditClients)
        self.buttonBox.accepted.connect(dlgEditClients.accept)
        self.buttonBox.rejected.connect(dlgEditClients.close)
        QtCore.QMetaObject.connectSlotsByName(dlgEditClients)

    def retranslateUi(self, dlgEditClients):
        _translate = QtCore.QCoreApplication.translate
        dlgEditClients.setWindowTitle(_translate("dlgEditClients", "Edit Client List"))
        self.btnInsert.setText(_translate("dlgEditClients", "+"))
        self.btnRemove.setText(_translate("dlgEditClients", "X"))

