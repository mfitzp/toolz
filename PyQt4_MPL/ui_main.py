# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\Desktop\PyQt4_MPL\main.ui'
#
# Created: Wed Aug 06 16:50:16 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(QtCore.QSize(QtCore.QRect(0,0,583,443).size()).expandedTo(Form.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(Form)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.plotBtn = QtGui.QPushButton(Form)
        self.plotBtn.setObjectName("plotBtn")
        self.vboxlayout.addWidget(self.plotBtn)

        self.plotWidget = MPL_Widget(Form)
        self.plotWidget.setObjectName("plotWidget")
        self.vboxlayout.addWidget(self.plotWidget)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "matplotlib, PyQt4 and Designer", None, QtGui.QApplication.UnicodeUTF8))
        self.plotBtn.setText(QtGui.QApplication.translate("Form", "Plot", None, QtGui.QApplication.UnicodeUTF8))

from mpl_pyqt4_widget import MPL_Widget
