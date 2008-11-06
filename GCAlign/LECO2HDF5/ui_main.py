# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\GCAlign\LECO2HDF5\main.ui'
#
# Created: Wed Nov 05 10:55:37 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,500,446).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon(":/new/prefix1/Clone_32.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.selLECODataBtn = QtGui.QPushButton(self.centralwidget)
        self.selLECODataBtn.setObjectName("selLECODataBtn")
        self.hboxlayout.addWidget(self.selLECODataBtn)

        self.LECOFolderLE = QtGui.QLineEdit(self.centralwidget)
        self.LECOFolderLE.setObjectName("LECOFolderLE")
        self.hboxlayout.addWidget(self.LECOFolderLE)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.singleFileCB = QtGui.QCheckBox(self.centralwidget)
        self.singleFileCB.setChecked(True)
        self.singleFileCB.setObjectName("singleFileCB")
        self.hboxlayout1.addWidget(self.singleFileCB)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout1.addWidget(self.line)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.outputBtn = QtGui.QPushButton(self.centralwidget)
        self.outputBtn.setObjectName("outputBtn")
        self.hboxlayout2.addWidget(self.outputBtn)

        self.outputFileLE = QtGui.QLineEdit(self.centralwidget)
        self.outputFileLE.setObjectName("outputFileLE")
        self.hboxlayout2.addWidget(self.outputFileLE)
        self.vboxlayout1.addLayout(self.hboxlayout2)

        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.vboxlayout1.addWidget(self.line_2)
        self.vboxlayout.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.vboxlayout2.addWidget(self.label_3)

        self.outputTE = QtGui.QTextEdit(self.centralwidget)
        self.outputTE.setObjectName("outputTE")
        self.vboxlayout2.addWidget(self.outputTE)
        self.vboxlayout.addLayout(self.vboxlayout2)

        self.cnvrtLECOBtn = QtGui.QPushButton(self.centralwidget)
        self.cnvrtLECOBtn.setObjectName("cnvrtLECOBtn")
        self.vboxlayout.addWidget(self.cnvrtLECOBtn)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,500,21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        self.actionConvert2HDF5 = QtGui.QAction(MainWindow)
        self.actionConvert2HDF5.setObjectName("actionConvert2HDF5")

        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.menuFile.addAction(self.actionClose)
        self.menuTools.addAction(self.actionConvert2HDF5)
        self.menuTools.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.LECOFolderLE,self.outputFileLE)
        MainWindow.setTabOrder(self.outputFileLE,self.cnvrtLECOBtn)
        MainWindow.setTabOrder(self.cnvrtLECOBtn,self.outputTE)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "LECO2HDF5", None, QtGui.QApplication.UnicodeUTF8))
        self.selLECODataBtn.setText(QtGui.QApplication.translate("MainWindow", "LECO netCDF File:", None, QtGui.QApplication.UnicodeUTF8))
        self.singleFileCB.setText(QtGui.QApplication.translate("MainWindow", "Single File Conversion?", None, QtGui.QApplication.UnicodeUTF8))
        self.outputBtn.setText(QtGui.QApplication.translate("MainWindow", "&Output File:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Output Message:", None, QtGui.QApplication.UnicodeUTF8))
        self.cnvrtLECOBtn.setText(QtGui.QApplication.translate("MainWindow", "&Convert to HDF5", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert2HDF5.setText(QtGui.QApplication.translate("MainWindow", "&Convert2HDF5", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
