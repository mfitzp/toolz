# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/clowers/workspace/SimpleView/example_main.ui'
#
# Created: Tue Feb 10 20:05:54 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.vboxlayout = QtGui.QVBoxLayout(Form)
        self.vboxlayout.setObjectName("vboxlayout")
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.vboxlayout.addWidget(self.pushButton)
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName("widget")
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Plot", None, QtGui.QApplication.UnicodeUTF8))

