# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\SimpleView\fingerPrint.ui'
#
# Created: Tue Feb 17 09:56:13 2009
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

        self.gridlayout = QtGui.QGridLayout(self.tab)
        self.gridlayout.setObjectName("gridlayout")

        self.plotWidget = MPL_Widget(self.tab)
        self.plotWidget.setObjectName("plotWidget")
        self.gridlayout.addWidget(self.plotWidget,0,0,1,1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.tab)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.mzTol_SB = QtGui.QDoubleSpinBox(self.tab)
        self.mzTol_SB.setDecimals(3)
        self.mzTol_SB.setMinimum(0.001)
        self.mzTol_SB.setMaximum(50000.0)
        self.mzTol_SB.setSingleStep(0.5)
        self.mzTol_SB.setProperty("value",QtCore.QVariant(500.0))
        self.mzTol_SB.setObjectName("mzTol_SB")
        self.hboxlayout1.addWidget(self.mzTol_SB)
        self.gridlayout1.addLayout(self.hboxlayout1,0,2,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.tab)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.hboxlayout2.addWidget(self.doubleSpinBox_2)
        self.gridlayout1.addLayout(self.hboxlayout2,1,2,1,1)

        self.fingerPrint_Btn = QtGui.QPushButton(self.tab)
        self.fingerPrint_Btn.setObjectName("fingerPrint_Btn")
        self.gridlayout1.addWidget(self.fingerPrint_Btn,1,1,1,1)

        self.showRaw_CB = QtGui.QCheckBox(self.tab)
        self.showRaw_CB.setChecked(True)
        self.showRaw_CB.setObjectName("showRaw_CB")
        self.gridlayout1.addWidget(self.showRaw_CB,1,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.hboxlayout3.addWidget(self.label_3)

        self.fpName_LE = QtGui.QLineEdit(self.tab)
        self.fpName_LE.setObjectName("fpName_LE")
        self.hboxlayout3.addWidget(self.fpName_LE)
        self.gridlayout1.addLayout(self.hboxlayout3,0,0,1,1)
        self.gridlayout.addLayout(self.gridlayout1,1,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.hboxlayout4 = QtGui.QHBoxLayout(self.tab_3)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.peakTable = CustomTable(self.tab_3)
        self.peakTable.setObjectName("peakTable")
        self.hboxlayout4.addWidget(self.peakTable)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.saveFP_Btn = QtGui.QPushButton(self.tab_2)
        self.saveFP_Btn.setGeometry(QtCore.QRect(20,20,131,31))
        self.saveFP_Btn.setObjectName("saveFP_Btn")

        self.commitFP_Btn = QtGui.QPushButton(self.tab_2)
        self.commitFP_Btn.setGeometry(QtCore.QRect(20,70,131,31))
        self.commitFP_Btn.setObjectName("commitFP_Btn")
        self.tabWidget.addTab(self.tab_2,"")
        self.hboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(fingerPlotWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(fingerPlotWidget)

    def retranslateUi(self, fingerPlotWidget):
        fingerPlotWidget.setWindowTitle(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("fingerPlotWidget", "ppm Tolerance:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("fingerPlotWidget", "Misc:", None, QtGui.QApplication.UnicodeUTF8))
        self.fingerPrint_Btn.setText(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.showRaw_CB.setText(QtGui.QApplication.translate("fingerPlotWidget", "Show FP Spectra?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.fpName_LE.setText(QtGui.QApplication.translate("fingerPlotWidget", "Change me if you want to commit fingerprint!", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.peakTable.clear()
        self.peakTable.setColumnCount(0)
        self.peakTable.setRowCount(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("fingerPlotWidget", "Peak Table", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFP_Btn.setToolTip(QtGui.QApplication.translate("fingerPlotWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Saves Fingerprint to Disk</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFP_Btn.setText(QtGui.QApplication.translate("fingerPlotWidget", "Save Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.commitFP_Btn.setToolTip(QtGui.QApplication.translate("fingerPlotWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Commits fingerprint to main window for future comparison with user selected spectra.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.commitFP_Btn.setText(QtGui.QApplication.translate("fingerPlotWidget", "Commit Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("fingerPlotWidget", "Options", None, QtGui.QApplication.UnicodeUTF8))

from customTable import CustomTable
from mpl_pyqt4_widget import MPL_Widget
