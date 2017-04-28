# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './layout/report.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgReport(object):
    def setupUi(self, dlgReport):
        dlgReport.setObjectName("dlgReport")
        dlgReport.resize(380, 379)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/timemachine_16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgReport.setWindowIcon(icon)
        dlgReport.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgReport)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtWidgets.QFrame(dlgReport)
        self.frame.setGeometry(QtCore.QRect(10, 10, 271, 161))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.frame)
        self.calendarWidget.setGeometry(QtCore.QRect(3, 5, 264, 151))
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setObjectName("calendarWidget")
        self.frame_2 = QtWidgets.QFrame(dlgReport)
        self.frame_2.setGeometry(QtCore.QRect(10, 180, 271, 181))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.lblReport = QtWidgets.QLabel(self.frame_2)
        self.lblReport.setGeometry(QtCore.QRect(10, 10, 251, 161))
        self.lblReport.setAutoFillBackground(True)
        self.lblReport.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lblReport.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lblReport.setText("")
        self.lblReport.setTextFormat(QtCore.Qt.AutoText)
        self.lblReport.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblReport.setWordWrap(True)
        self.lblReport.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.lblReport.setObjectName("lblReport")

        self.retranslateUi(dlgReport)
        self.buttonBox.accepted.connect(dlgReport.accept)
        QtCore.QMetaObject.connectSlotsByName(dlgReport)

    def retranslateUi(self, dlgReport):
        _translate = QtCore.QCoreApplication.translate
        dlgReport.setWindowTitle(_translate("dlgReport", "Report"))

import timemachine_rc
