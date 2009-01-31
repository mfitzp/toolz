# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\pyXCMS\main.ui'
#
# Created: Fri Jan 30 16:37:53 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,987,731).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon(":/new/prefix1/icons/games.png"))
        MainWindow.setIconSize(QtCore.QSize(30,30))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
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
        self.runXCMSBtn.setIcon(QtGui.QIcon(":/new/prefix1/icons/applications.png"))
        self.runXCMSBtn.setIconSize(QtCore.QSize(32,32))
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

        self.hboxlayout6 = QtGui.QHBoxLayout(self.tab_2)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.vboxlayout6 = QtGui.QVBoxLayout()
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.hboxlayout8.addWidget(self.label_6)

        self.eicIndexSlider = QtGui.QSlider(self.tab_2)
        self.eicIndexSlider.setMaximum(150)
        self.eicIndexSlider.setOrientation(QtCore.Qt.Horizontal)
        self.eicIndexSlider.setObjectName("eicIndexSlider")
        self.hboxlayout8.addWidget(self.eicIndexSlider)

        self.eicIndexSB = QtGui.QSpinBox(self.tab_2)
        self.eicIndexSB.setMaximum(150)
        self.eicIndexSB.setObjectName("eicIndexSB")
        self.hboxlayout8.addWidget(self.eicIndexSB)
        self.vboxlayout6.addLayout(self.hboxlayout8)

        self.plotWidget = MPL_Widget(self.tab_2)
        self.plotWidget.setObjectName("plotWidget")
        self.vboxlayout6.addWidget(self.plotWidget)
        self.hboxlayout7.addLayout(self.vboxlayout6)

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.vboxlayout7 = QtGui.QVBoxLayout()
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.hboxlayout10.addWidget(self.label_7)

        self.eicCurFolderLE = QtGui.QLineEdit(self.tab_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eicCurFolderLE.sizePolicy().hasHeightForWidth())
        self.eicCurFolderLE.setSizePolicy(sizePolicy)
        self.eicCurFolderLE.setReadOnly(True)
        self.eicCurFolderLE.setObjectName("eicCurFolderLE")
        self.hboxlayout10.addWidget(self.eicCurFolderLE)
        self.vboxlayout7.addLayout(self.hboxlayout10)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.hboxlayout11.addWidget(self.label_5)

        self.mzStartSB = QtGui.QDoubleSpinBox(self.tab_2)
        self.mzStartSB.setDecimals(4)
        self.mzStartSB.setMaximum(100000.0)
        self.mzStartSB.setSingleStep(0.05)
        self.mzStartSB.setProperty("value",QtCore.QVariant(515.15))
        self.mzStartSB.setObjectName("mzStartSB")
        self.hboxlayout11.addWidget(self.mzStartSB)
        self.vboxlayout7.addLayout(self.hboxlayout11)

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.hboxlayout12.addWidget(self.label_4)

        self.mzStopSB = QtGui.QDoubleSpinBox(self.tab_2)
        self.mzStopSB.setDecimals(4)
        self.mzStopSB.setMaximum(100000.0)
        self.mzStopSB.setSingleStep(0.05)
        self.mzStopSB.setProperty("value",QtCore.QVariant(517.15))
        self.mzStopSB.setObjectName("mzStopSB")
        self.hboxlayout12.addWidget(self.mzStopSB)
        self.vboxlayout7.addLayout(self.hboxlayout12)

        self.getEICBtn = QtGui.QPushButton(self.tab_2)
        self.getEICBtn.setObjectName("getEICBtn")
        self.vboxlayout7.addWidget(self.getEICBtn)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout7.addItem(spacerItem2)
        self.hboxlayout9.addLayout(self.vboxlayout7)
        self.hboxlayout7.addLayout(self.hboxlayout9)
        self.hboxlayout6.addLayout(self.hboxlayout7)
        self.tabWidget.addTab(self.tab_2,"")
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
        self.menu_File.addAction(self.action_Open)
        self.menuF_unctions.addAction(self.actionSave_Results_Table)
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
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "m/z Stop:", None, QtGui.QApplication.UnicodeUTF8))
        self.getEICBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Do It!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.getEICBtn.setText(QtGui.QApplication.translate("MainWindow", "Fetch EIC", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "EIC", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuF_unctions.setTitle(QtGui.QApplication.translate("MainWindow", "F&unctions", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Results_Table.setText(QtGui.QApplication.translate("MainWindow", "Save Results Table", None, QtGui.QApplication.UnicodeUTF8))

from customTable import CustomTable
from mpl_pyqt4_widget import MPL_Widget
import resource_rc
