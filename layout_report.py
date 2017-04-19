# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout_report.ui'
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

class Ui_dlgReport(object):
    def setupUi(self, dlgReport):
        dlgReport.setObjectName(_fromUtf8("dlgReport"))
        dlgReport.resize(380, 379)
        self.buttonBox = QtGui.QDialogButtonBox(dlgReport)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.plainTextEdit = QtGui.QPlainTextEdit(dlgReport)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 180, 271, 191))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.frame = QtGui.QFrame(dlgReport)
        self.frame.setGeometry(QtCore.QRect(10, 10, 271, 161))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.calendarWidget = QtGui.QCalendarWidget(self.frame)
        self.calendarWidget.setGeometry(QtCore.QRect(3, 5, 264, 148))
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))

        self.retranslateUi(dlgReport)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dlgReport.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dlgReport.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgReport)

    def retranslateUi(self, dlgReport):
        dlgReport.setWindowTitle(_translate("dlgReport", "Dialog", None))

