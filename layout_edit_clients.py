# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_edit_clients.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_dlgEditClients(object):
    def setupUi(self, dlgEditClients):
        dlgEditClients.setObjectName(_fromUtf8("dlgEditClients"))
        dlgEditClients.resize(321, 199)
        self.buttonBox = QtGui.QDialogButtonBox(dlgEditClients)
        self.buttonBox.setGeometry(QtCore.QRect(-32, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.inputNewClient = QtGui.QLineEdit(dlgEditClients)
        self.inputNewClient.setGeometry(QtCore.QRect(10, 100, 261, 20))
        self.inputNewClient.setObjectName(_fromUtf8("inputNewClient"))
        self.clientListWidget = QtGui.QListWidget(dlgEditClients)
        self.clientListWidget.setGeometry(QtCore.QRect(10, 10, 261, 81))
        self.clientListWidget.setObjectName(_fromUtf8("clientListWidget"))
        self.btnInsert = QtGui.QToolButton(dlgEditClients)
        self.btnInsert.setGeometry(QtCore.QRect(280, 100, 27, 20))
        self.btnInsert.setCheckable(False)
        self.btnInsert.setObjectName(_fromUtf8("btnInsert"))
        self.btnRemove = QtGui.QToolButton(dlgEditClients)
        self.btnRemove.setGeometry(QtCore.QRect(280, 40, 27, 20))
        self.btnRemove.setCheckable(False)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))

        self.retranslateUi(dlgEditClients)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dlgEditClients.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dlgEditClients.close)
        QtCore.QMetaObject.connectSlotsByName(dlgEditClients)

    def retranslateUi(self, dlgEditClients):
        dlgEditClients.setWindowTitle(_translate("dlgEditClients", "Edit Client List", None))
        self.btnInsert.setText(_translate("dlgEditClients", "+", None))
        self.btnRemove.setText(_translate("dlgEditClients", "X", None))

