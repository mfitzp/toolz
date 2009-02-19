# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\pyXCMS\main.ui'
#
# Created: Thu Feb 19 11:01:03 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,987,673).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon("games.png"))
        MainWindow.setIconSize(QtCore.QSize(30,30))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.vboxlayout = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.getFolderBtn = QtGui.QPushButton(self.tab)
        self.getFolderBtn.setObjectName("getFolderBtn")
        self.hboxlayout2.addWidget(self.getFolderBtn)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout2)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_25 = QtGui.QLabel(self.tab)
        self.label_25.setObjectName("label_25")
        self.hboxlayout3.addWidget(self.label_25)

        self.curFolderLE = QtGui.QLineEdit(self.tab)
        self.curFolderLE.setReadOnly(True)
        self.curFolderLE.setObjectName("curFolderLE")
        self.hboxlayout3.addWidget(self.curFolderLE)
        self.vboxlayout2.addLayout(self.hboxlayout3)

        self.label_21 = QtGui.QLabel(self.tab)
        self.label_21.setObjectName("label_21")
        self.vboxlayout2.addWidget(self.label_21)

        self.dirListWidget = QtGui.QListWidget(self.tab)
        self.dirListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.dirListWidget.setObjectName("dirListWidget")
        self.vboxlayout2.addWidget(self.dirListWidget)
        self.vboxlayout1.addLayout(self.vboxlayout2)
        self.hboxlayout1.addLayout(self.vboxlayout1)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.hboxlayout4.addWidget(self.label)

        self.xcmsMethodCB = QtGui.QComboBox(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xcmsMethodCB.sizePolicy().hasHeightForWidth())
        self.xcmsMethodCB.setSizePolicy(sizePolicy)
        self.xcmsMethodCB.setObjectName("xcmsMethodCB")
        self.hboxlayout4.addWidget(self.xcmsMethodCB)
        self.vboxlayout3.addLayout(self.hboxlayout4)

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.vboxlayout4.addWidget(self.label_2)

        self.paramTableWidget = CustomTable(self.tab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paramTableWidget.sizePolicy().hasHeightForWidth())
        self.paramTableWidget.setSizePolicy(sizePolicy)
        self.paramTableWidget.setObjectName("paramTableWidget")
        self.vboxlayout4.addWidget(self.paramTableWidget)
        self.vboxlayout3.addLayout(self.vboxlayout4)
        self.hboxlayout1.addLayout(self.vboxlayout3)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout5.addItem(spacerItem1)

        self.runXCMSBtn = QtGui.QToolButton(self.tab)
        self.runXCMSBtn.setIcon(QtGui.QIcon("applications.png"))
        self.runXCMSBtn.setIconSize(QtCore.QSize(30,30))
        self.runXCMSBtn.setObjectName("runXCMSBtn")
        self.hboxlayout5.addWidget(self.runXCMSBtn)
        self.vboxlayout5.addLayout(self.hboxlayout5)

        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.vboxlayout5.addWidget(self.label_3)

        self.RoutputTE = QtGui.QTextEdit(self.tab)
        self.RoutputTE.setReadOnly(True)
        self.RoutputTE.setObjectName("RoutputTE")
        self.vboxlayout5.addWidget(self.RoutputTE)
        self.vboxlayout.addLayout(self.vboxlayout5)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout = QtGui.QGridLayout(self.tab_2)
        self.gridlayout.setObjectName("gridlayout")

        self.vboxlayout6 = QtGui.QVBoxLayout()
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.hboxlayout6.addWidget(self.label_6)

        self.eicIndexSlider = QtGui.QSlider(self.tab_2)
        self.eicIndexSlider.setMaximum(10000)
        self.eicIndexSlider.setOrientation(QtCore.Qt.Horizontal)
        self.eicIndexSlider.setObjectName("eicIndexSlider")
        self.hboxlayout6.addWidget(self.eicIndexSlider)

        self.eicIndexSB = QtGui.QSpinBox(self.tab_2)
        self.eicIndexSB.setMaximum(10000)
        self.eicIndexSB.setObjectName("eicIndexSB")
        self.hboxlayout6.addWidget(self.eicIndexSB)
        self.vboxlayout6.addLayout(self.hboxlayout6)

        self.plotWidget = MPL_Widget(self.tab_2)
        self.plotWidget.setObjectName("plotWidget")
        self.vboxlayout6.addWidget(self.plotWidget)
        self.gridlayout.addLayout(self.vboxlayout6,0,0,1,1)

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.vboxlayout7 = QtGui.QVBoxLayout()
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.hboxlayout8.addWidget(self.label_7)

        self.eicCurFolderLE = QtGui.QLineEdit(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eicCurFolderLE.sizePolicy().hasHeightForWidth())
        self.eicCurFolderLE.setSizePolicy(sizePolicy)
        self.eicCurFolderLE.setReadOnly(True)
        self.eicCurFolderLE.setObjectName("eicCurFolderLE")
        self.hboxlayout8.addWidget(self.eicCurFolderLE)
        self.vboxlayout7.addLayout(self.hboxlayout8)

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.hboxlayout9.addWidget(self.label_5)

        self.mzStartSB = QtGui.QDoubleSpinBox(self.tab_2)
        self.mzStartSB.setDecimals(4)
        self.mzStartSB.setMaximum(100000.0)
        self.mzStartSB.setSingleStep(0.05)
        self.mzStartSB.setProperty("value",QtCore.QVariant(215.15))
        self.mzStartSB.setObjectName("mzStartSB")
        self.hboxlayout9.addWidget(self.mzStartSB)
        self.vboxlayout7.addLayout(self.hboxlayout9)

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.hboxlayout10.addWidget(self.label_4)

        self.mzStopSB = QtGui.QDoubleSpinBox(self.tab_2)
        self.mzStopSB.setDecimals(4)
        self.mzStopSB.setMaximum(100000.0)
        self.mzStopSB.setSingleStep(0.05)
        self.mzStopSB.setProperty("value",QtCore.QVariant(227.15))
        self.mzStopSB.setObjectName("mzStopSB")
        self.hboxlayout10.addWidget(self.mzStopSB)
        self.vboxlayout7.addLayout(self.hboxlayout10)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.hboxlayout11.addWidget(self.label_11)

        self.rtWidthSB = QtGui.QDoubleSpinBox(self.tab_2)
        self.rtWidthSB.setDecimals(1)
        self.rtWidthSB.setMinimum(1.0)
        self.rtWidthSB.setMaximum(100000.0)
        self.rtWidthSB.setSingleStep(1.0)
        self.rtWidthSB.setProperty("value",QtCore.QVariant(200.0))
        self.rtWidthSB.setObjectName("rtWidthSB")
        self.hboxlayout11.addWidget(self.rtWidthSB)
        self.vboxlayout7.addLayout(self.hboxlayout11)

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.hboxlayout12.addWidget(self.label_12)

        self.rtWidthSB_Stop = QtGui.QDoubleSpinBox(self.tab_2)
        self.rtWidthSB_Stop.setDecimals(1)
        self.rtWidthSB_Stop.setMinimum(-1.0)
        self.rtWidthSB_Stop.setMaximum(100000.0)
        self.rtWidthSB_Stop.setSingleStep(1.0)
        self.rtWidthSB_Stop.setProperty("value",QtCore.QVariant(-1.0))
        self.rtWidthSB_Stop.setObjectName("rtWidthSB_Stop")
        self.hboxlayout12.addWidget(self.rtWidthSB_Stop)
        self.vboxlayout7.addLayout(self.hboxlayout12)

        self.rtTypeCB = QtGui.QCheckBox(self.tab_2)
        self.rtTypeCB.setChecked(True)
        self.rtTypeCB.setObjectName("rtTypeCB")
        self.vboxlayout7.addWidget(self.rtTypeCB)

        self.fillPeaks_CB = QtGui.QCheckBox(self.tab_2)
        self.fillPeaks_CB.setChecked(False)
        self.fillPeaks_CB.setObjectName("fillPeaks_CB")
        self.vboxlayout7.addWidget(self.fillPeaks_CB)

        self.plotLegendCB = QtGui.QCheckBox(self.tab_2)
        self.plotLegendCB.setChecked(False)
        self.plotLegendCB.setObjectName("plotLegendCB")
        self.vboxlayout7.addWidget(self.plotLegendCB)

        self.getEICBtn = QtGui.QPushButton(self.tab_2)
        self.getEICBtn.setObjectName("getEICBtn")
        self.vboxlayout7.addWidget(self.getEICBtn)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout7.addItem(spacerItem2)
        self.hboxlayout7.addLayout(self.vboxlayout7)
        self.gridlayout.addLayout(self.hboxlayout7,0,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.vboxlayout8 = QtGui.QVBoxLayout(self.tab_4)
        self.vboxlayout8.setObjectName("vboxlayout8")

        self.hboxlayout13 = QtGui.QHBoxLayout()
        self.hboxlayout13.setObjectName("hboxlayout13")

        self.loadRPY2BatchBtn = QtGui.QPushButton(self.tab_4)
        self.loadRPY2BatchBtn.setEnabled(False)
        self.loadRPY2BatchBtn.setObjectName("loadRPY2BatchBtn")
        self.hboxlayout13.addWidget(self.loadRPY2BatchBtn)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout13.addItem(spacerItem3)
        self.vboxlayout8.addLayout(self.hboxlayout13)

        self.batchScriptTE = QtGui.QTextEdit(self.tab_4)
        self.batchScriptTE.setEnabled(False)
        self.batchScriptTE.setObjectName("batchScriptTE")
        self.vboxlayout8.addWidget(self.batchScriptTE)

        self.hboxlayout14 = QtGui.QHBoxLayout()
        self.hboxlayout14.setObjectName("hboxlayout14")

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout14.addItem(spacerItem4)

        self.runBatchBtn = QtGui.QPushButton(self.tab_4)
        self.runBatchBtn.setEnabled(False)
        self.runBatchBtn.setObjectName("runBatchBtn")
        self.hboxlayout14.addWidget(self.runBatchBtn)
        self.vboxlayout8.addLayout(self.hboxlayout14)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.killRBtn = QtGui.QPushButton(self.tab_3)
        self.killRBtn.setEnabled(False)
        self.killRBtn.setGeometry(QtCore.QRect(20,10,121,21))
        self.killRBtn.setObjectName("killRBtn")
        self.tabWidget.addTab(self.tab_3,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,987,21))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menuF_unctions = QtGui.QMenu(self.menubar)
        self.menuF_unctions.setObjectName("menuF_unctions")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")

        self.actionSave_Results_Table = QtGui.QAction(MainWindow)
        self.actionSave_Results_Table.setObjectName("actionSave_Results_Table")

        self.actionTest_XCMS = QtGui.QAction(MainWindow)
        self.actionTest_XCMS.setObjectName("actionTest_XCMS")

        self.actionSave_HDF5 = QtGui.QAction(MainWindow)
        self.actionSave_HDF5.setObjectName("actionSave_HDF5")

        self.actionLoad_HDF5 = QtGui.QAction(MainWindow)
        self.actionLoad_HDF5.setObjectName("actionLoad_HDF5")

        self.actionRun_XCMS = QtGui.QAction(MainWindow)
        self.actionRun_XCMS.setObjectName("actionRun_XCMS")
        self.menu_File.addAction(self.actionSave_HDF5)
        self.menu_File.addAction(self.actionLoad_HDF5)
        self.menuF_unctions.addAction(self.actionSave_Results_Table)
        self.menuF_unctions.addSeparator()
        self.menuF_unctions.addAction(self.actionRun_XCMS)
        self.menuF_unctions.addSeparator()
        self.menuF_unctions.addAction(self.actionTest_XCMS)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuF_unctions.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.eicIndexSlider,QtCore.SIGNAL("valueChanged(int)"),self.eicIndexSB.setValue)
        QtCore.QObject.connect(self.eicIndexSB,QtCore.SIGNAL("valueChanged(int)"),self.eicIndexSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pyXCMS", None, QtGui.QApplication.UnicodeUTF8))
        self.getFolderBtn.setText(QtGui.QApplication.translate("MainWindow", "Select Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("MainWindow", "Data Folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("MainWindow", "Files in Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Grouping Method:", None, QtGui.QApplication.UnicodeUTF8))
        self.xcmsMethodCB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select XCMS Processing Method</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Parameters:", None, QtGui.QApplication.UnicodeUTF8))
        self.paramTableWidget.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Adjust XCMS Parameters</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.paramTableWidget.setRowCount(0)
        self.paramTableWidget.setColumnCount(0)
        self.paramTableWidget.clear()
        self.paramTableWidget.setColumnCount(0)
        self.paramTableWidget.setRowCount(0)
        self.runXCMSBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Make it happen!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.runXCMSBtn.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "R output:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "xcms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "EIC Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Current Folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "m/z Start:", None, QtGui.QApplication.UnicodeUTF8))
        self.mzStartSB.setToolTip(QtGui.QApplication.translate("MainWindow", "Upper bound of the EIC extraction range", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "m/z Stop:", None, QtGui.QApplication.UnicodeUTF8))
        self.mzStopSB.setToolTip(QtGui.QApplication.translate("MainWindow", "Low bound of the EIC extraction range", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "RT Start:", None, QtGui.QApplication.UnicodeUTF8))
        self.rtWidthSB.setToolTip(QtGui.QApplication.translate("MainWindow", "Retention time window of the EIC", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "RT Stop:", None, QtGui.QApplication.UnicodeUTF8))
        self.rtWidthSB_Stop.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Set to -1 for the entire spectrum</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.rtTypeCB.setToolTip(QtGui.QApplication.translate("MainWindow", "Do you want the corrected EIC or the raw values?", None, QtGui.QApplication.UnicodeUTF8))
        self.rtTypeCB.setText(QtGui.QApplication.translate("MainWindow", "Retrieve Corrected EIC?", None, QtGui.QApplication.UnicodeUTF8))
        self.fillPeaks_CB.setToolTip(QtGui.QApplication.translate("MainWindow", "Do you want the corrected EIC or the raw values?", None, QtGui.QApplication.UnicodeUTF8))
        self.fillPeaks_CB.setText(QtGui.QApplication.translate("MainWindow", "Fill Missing Peaks?", None, QtGui.QApplication.UnicodeUTF8))
        self.plotLegendCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Legend?", None, QtGui.QApplication.UnicodeUTF8))
        self.getEICBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Do It!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.getEICBtn.setText(QtGui.QApplication.translate("MainWindow", "Fetch EIC", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "EIC", None, QtGui.QApplication.UnicodeUTF8))
        self.loadRPY2BatchBtn.setText(QtGui.QApplication.translate("MainWindow", "Load rpy2 Batch Script", None, QtGui.QApplication.UnicodeUTF8))
        self.runBatchBtn.setText(QtGui.QApplication.translate("MainWindow", "Do It!", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Batch Processing", None, QtGui.QApplication.UnicodeUTF8))
        self.killRBtn.setText(QtGui.QApplication.translate("MainWindow", "Kill R Process", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuF_unctions.setTitle(QtGui.QApplication.translate("MainWindow", "F&unctions", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Results_Table.setText(QtGui.QApplication.translate("MainWindow", "Save Results Table", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest_XCMS.setText(QtGui.QApplication.translate("MainWindow", "Test XCMS", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest_XCMS.setToolTip(QtGui.QApplication.translate("MainWindow", "Needs faakho package", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest_XCMS.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Needs faakho package", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_HDF5.setText(QtGui.QApplication.translate("MainWindow", "Save HDF5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_HDF5.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_HDF5.setText(QtGui.QApplication.translate("MainWindow", "Load HDF5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_HDF5.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun_XCMS.setText(QtGui.QApplication.translate("MainWindow", "Run XCMS", None, QtGui.QApplication.UnicodeUTF8))

from customTable import CustomTable
from mpl_pyqt4_widget import MPL_Widget
import icons_rc
