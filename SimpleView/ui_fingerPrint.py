# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\SimpleView\fingerPrint.ui'
#
# Created: Mon Feb 16 12:54:58 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_fingerPlotWidget(object):
    def setupUi(self, fingerPlotWidget):
        fingerPlotWidget.setObjectName("fingerPlotWidget")
        fingerPlotWidget.resize(QtCore.QSize(QtCore.QRect(0,0,633,524).size()).expandedTo(fingerPlotWidget.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(fingerPlotWidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tabWidget = QtGui.QTabWidget(fingerPlotWidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.vboxlayout = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout.setObjectName("vboxlayout")

        self.plotWidget = MPL_Widget(self.tab)
        self.plotWidget.setObjectName("plotWidget")
        self.vboxlayout.addWidget(self.plotWidget)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.tab)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.hboxlayout1.addWidget(self.doubleSpinBox)
        self.gridlayout.addLayout(self.hboxlayout1,0,2,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.tab)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.hboxlayout2.addWidget(self.doubleSpinBox_2)
        self.gridlayout.addLayout(self.hboxlayout2,1,2,1,1)

        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,1,1,1,1)

        self.checkBox = QtGui.QCheckBox(self.tab)
        self.checkBox.setObjectName("checkBox")
        self.gridlayout.addWidget(self.checkBox,1,0,1,1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.tabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.tab_3)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.peakTable = CustomTable(self.tab_3)
        self.peakTable.setObjectName("peakTable")
        self.hboxlayout3.addWidget(self.peakTable)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2,"")
        self.hboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(fingerPlotWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(fingerPlotWidget)

    def retranslateUi(self, fingerPlotWidget):
        fingerPlotWidget.setWindowTitle(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("fingerPlotWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("fingerPlotWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("fingerPlotWidget", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("fingerPlotWidget", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.peakTable.clear()
        self.peakTable.setColumnCount(0)
        self.peakTable.setRowCount(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("fingerPlotWidget", "Peak Table", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("fingerPlotWidget", "Options", None, QtGui.QApplication.UnicodeUTF8))

from customTable import CustomTable
from mpl_pyqt4_widget import MPL_Widget
