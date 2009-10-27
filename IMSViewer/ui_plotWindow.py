# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\NoiseProject\plotWindow.ui'
#
# Created: Tue May 12 09:23:56 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_plotWindow(object):
    def setupUi(self, plotWindow):
        plotWindow.setObjectName("plotWindow")
        plotWindow.resize(650, 600)
        self.gridlayout = QtGui.QGridLayout(plotWindow)
        self.gridlayout.setObjectName("gridlayout")
        self.tabWidget = QtGui.QTabWidget(plotWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.plotWidget = MPL_Widget(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setObjectName("plotWidget")
        self.gridLayout.addWidget(self.plotWidget, 0, 0, 1, 1)
        self._2 = QtGui.QGridLayout()
        self._2.setObjectName("_2")
        self.label_3 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self._2.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self._2.addWidget(self.label_4, 0, 2, 1, 1)
        self.min_label = QtGui.QLabel(self.tab)
        self.min_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.min_label.setObjectName("min_label")
        self._2.addWidget(self.min_label, 1, 0, 1, 1)
        self.xmin_lineEdit = QtGui.QLineEdit(self.tab)
        self.xmin_lineEdit.setObjectName("xmin_lineEdit")
        self._2.addWidget(self.xmin_lineEdit, 1, 1, 1, 1)
        self.ymin_lineEdit = QtGui.QLineEdit(self.tab)
        self.ymin_lineEdit.setObjectName("ymin_lineEdit")
        self._2.addWidget(self.ymin_lineEdit, 1, 2, 1, 1)
        self.max_label = QtGui.QLabel(self.tab)
        self.max_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_label.setObjectName("max_label")
        self._2.addWidget(self.max_label, 2, 0, 1, 1)
        self.xmax_lineEdit = QtGui.QLineEdit(self.tab)
        self.xmax_lineEdit.setObjectName("xmax_lineEdit")
        self._2.addWidget(self.xmax_lineEdit, 2, 1, 1, 1)
        self.ymax_lineEdit = QtGui.QLineEdit(self.tab)
        self.ymax_lineEdit.setObjectName("ymax_lineEdit")
        self._2.addWidget(self.ymax_lineEdit, 2, 2, 1, 1)
        self.gridLayout.addLayout(self._2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.hboxlayout = QtGui.QHBoxLayout(self.tab_3)
        self.hboxlayout.setObjectName("hboxlayout")
        self.peakTable = CustomTable(self.tab_3)
        self.peakTable.setObjectName("peakTable")
        self.peakTable.setColumnCount(0)
        self.peakTable.setRowCount(0)
        self.hboxlayout.addWidget(self.peakTable)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(plotWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(plotWindow)

    def retranslateUi(self, plotWindow):
        plotWindow.setWindowTitle(QtGui.QApplication.translate("plotWindow", "Plot Window", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("plotWindow", "X Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("plotWindow", "Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.min_label.setText(QtGui.QApplication.translate("plotWindow", "Minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.max_label.setText(QtGui.QApplication.translate("plotWindow", "Maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("plotWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("plotWindow", "Data Table", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("plotWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))

from customTable import CustomTable
from mpl_pyqt4_widget import MPL_Widget