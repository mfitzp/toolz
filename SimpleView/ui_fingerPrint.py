# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\SimpleView\fingerPrint.ui'
#
# Created: Tue Mar 31 13:33:02 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_fingerPlotWidget(object):
    def setupUi(self, fingerPlotWidget):
        fingerPlotWidget.setObjectName("fingerPlotWidget")
        fingerPlotWidget.resize(QtCore.QSize(QtCore.QRect(0,0,633,524).size()).expandedTo(fingerPlotWidget.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(fingerPlotWidget)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(fingerPlotWidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setObjectName("gridlayout1")

        self.plotWidget = MPL_Widget(self.tab)
        self.plotWidget.setObjectName("plotWidget")
        self.gridlayout1.addWidget(self.plotWidget,0,0,1,1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(self.tab)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.mzTol_SB = QtGui.QDoubleSpinBox(self.tab)
        self.mzTol_SB.setDecimals(3)
        self.mzTol_SB.setMinimum(0.001)
        self.mzTol_SB.setMaximum(50000.0)
        self.mzTol_SB.setSingleStep(0.5)
        self.mzTol_SB.setProperty("value",QtCore.QVariant(500.0))
        self.mzTol_SB.setObjectName("mzTol_SB")
        self.hboxlayout.addWidget(self.mzTol_SB)
        self.gridlayout2.addLayout(self.hboxlayout,0,2,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout1.addWidget(self.label_2)

        self.stdDev_SB = QtGui.QDoubleSpinBox(self.tab)
        self.stdDev_SB.setMaximum(500.0)
        self.stdDev_SB.setProperty("value",QtCore.QVariant(3.0))
        self.stdDev_SB.setObjectName("stdDev_SB")
        self.hboxlayout1.addWidget(self.stdDev_SB)
        self.gridlayout2.addLayout(self.hboxlayout1,1,2,1,1)

        self.showRaw_CB = QtGui.QCheckBox(self.tab)
        self.showRaw_CB.setChecked(False)
        self.showRaw_CB.setObjectName("showRaw_CB")
        self.gridlayout2.addWidget(self.showRaw_CB,1,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.hboxlayout2.addWidget(self.label_3)

        self.fpName_LE = QtGui.QLineEdit(self.tab)
        self.fpName_LE.setObjectName("fpName_LE")
        self.hboxlayout2.addWidget(self.fpName_LE)
        self.gridlayout2.addLayout(self.hboxlayout2,0,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.hboxlayout3.addWidget(self.label_4)

        self.sigLvl_SB = QtGui.QDoubleSpinBox(self.tab)
        self.sigLvl_SB.setDecimals(2)
        self.sigLvl_SB.setMinimum(0.01)
        self.sigLvl_SB.setMaximum(1.0)
        self.sigLvl_SB.setSingleStep(0.05)
        self.sigLvl_SB.setProperty("value",QtCore.QVariant(0.05))
        self.sigLvl_SB.setObjectName("sigLvl_SB")
        self.hboxlayout3.addWidget(self.sigLvl_SB)
        self.gridlayout2.addLayout(self.hboxlayout3,2,2,1,1)

        self.fingerPrint_Btn = QtGui.QPushButton(self.tab)
        self.fingerPrint_Btn.setObjectName("fingerPrint_Btn")
        self.gridlayout2.addWidget(self.fingerPrint_Btn,0,1,1,1)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.hboxlayout4.addWidget(self.label_7)

        self.minSpectra_SB = QtGui.QSpinBox(self.tab)
        self.minSpectra_SB.setEnabled(False)
        self.minSpectra_SB.setMinimum(1)
        self.minSpectra_SB.setProperty("value",QtCore.QVariant(3))
        self.minSpectra_SB.setObjectName("minSpectra_SB")
        self.hboxlayout4.addWidget(self.minSpectra_SB)
        self.gridlayout2.addLayout(self.hboxlayout4,2,1,1,1)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.hboxlayout5.addWidget(self.label_5)

        self.freqCutoff_SB = QtGui.QDoubleSpinBox(self.tab)
        self.freqCutoff_SB.setDecimals(2)
        self.freqCutoff_SB.setMinimum(0.01)
        self.freqCutoff_SB.setMaximum(1.0)
        self.freqCutoff_SB.setSingleStep(0.05)
        self.freqCutoff_SB.setProperty("value",QtCore.QVariant(0.5))
        self.freqCutoff_SB.setObjectName("freqCutoff_SB")
        self.hboxlayout5.addWidget(self.freqCutoff_SB)
        self.gridlayout2.addLayout(self.hboxlayout5,2,0,1,1)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.commitFP_Btn = QtGui.QPushButton(self.tab)
        self.commitFP_Btn.setObjectName("commitFP_Btn")
        self.hboxlayout6.addWidget(self.commitFP_Btn)

        self.saveFP_Btn = QtGui.QPushButton(self.tab)
        self.saveFP_Btn.setObjectName("saveFP_Btn")
        self.hboxlayout6.addWidget(self.saveFP_Btn)
        self.gridlayout2.addLayout(self.hboxlayout6,1,1,1,1)
        self.gridlayout1.addLayout(self.gridlayout2,1,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.hboxlayout7 = QtGui.QHBoxLayout(self.tab_3)
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.peakTable = CustomTable(self.tab_3)
        self.peakTable.setObjectName("peakTable")
        self.hboxlayout7.addWidget(self.peakTable)
        self.tabWidget.addTab(self.tab_3,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.saveFP_Btn_4 = QtGui.QPushButton(self.tab_2)
        self.saveFP_Btn_4.setGeometry(QtCore.QRect(20,20,131,31))
        self.saveFP_Btn_4.setObjectName("saveFP_Btn_4")

        self.commitFP_Btn_4 = QtGui.QPushButton(self.tab_2)
        self.commitFP_Btn_4.setGeometry(QtCore.QRect(20,70,131,31))
        self.commitFP_Btn_4.setObjectName("commitFP_Btn_4")
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)

        self.retranslateUi(fingerPlotWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(fingerPlotWidget)

    def retranslateUi(self, fingerPlotWidget):
        fingerPlotWidget.setWindowTitle(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("fingerPlotWidget", "ppm Tolerance:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("fingerPlotWidget", "Min # of Standard Deviations:", None, QtGui.QApplication.UnicodeUTF8))
        self.showRaw_CB.setText(QtGui.QApplication.translate("fingerPlotWidget", "Show FP Spectra?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.fpName_LE.setText(QtGui.QApplication.translate("fingerPlotWidget", "Rename me!", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("fingerPlotWidget", "Significance Level:", None, QtGui.QApplication.UnicodeUTF8))
        self.fingerPrint_Btn.setText(QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("fingerPlotWidget", "Min # of Spectra:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("fingerPlotWidget", "Freq Cutoff:", None, QtGui.QApplication.UnicodeUTF8))
        self.commitFP_Btn.setToolTip(QtGui.QApplication.translate("fingerPlotWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Commits fingerprint to main window for future comparison with user selected spectra.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.commitFP_Btn.setText(QtGui.QApplication.translate("fingerPlotWidget", "Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFP_Btn.setToolTip(QtGui.QApplication.translate("fingerPlotWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Saves Fingerprint to Disk</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFP_Btn.setText(QtGui.QApplication.translate("fingerPlotWidget", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("fingerPlotWidget", "Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.peakTable.clear()
        self.peakTable.setColumnCount(0)
        self.peakTable.setRowCount(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("fingerPlotWidget", "Peak Table", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFP_Btn_4.setToolTip(QtGui.QApplication.translate("fingerPlotWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Saves Fingerprint to Disk</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveFP_Btn_4.setText(QtGui.QApplication.translate("fingerPlotWidget", "Save Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.commitFP_Btn_4.setToolTip(QtGui.QApplication.translate("fingerPlotWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Commits fingerprint to main window for future comparison with user selected spectra.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.commitFP_Btn_4.setText(QtGui.QApplication.translate("fingerPlotWidget", "Commit Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("fingerPlotWidget", "Options", None, QtGui.QApplication.UnicodeUTF8))

from customTable import CustomTable
from mpl_pyqt4_widget import MPL_Widget
