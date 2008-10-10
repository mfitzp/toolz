# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\SVN\Bruker2mzXML\main.ui'
#
# Created: Thu Oct 09 12:18:10 2008
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

        self.selBrukerDataBtn = QtGui.QPushButton(self.centralwidget)
        self.selBrukerDataBtn.setObjectName("selBrukerDataBtn")
        self.hboxlayout.addWidget(self.selBrukerDataBtn)

        self.brukerFolderLE = QtGui.QLineEdit(self.centralwidget)
        self.brukerFolderLE.setObjectName("brukerFolderLE")
        self.hboxlayout.addWidget(self.brukerFolderLE)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.singleFileCB = QtGui.QCheckBox(self.centralwidget)
        self.singleFileCB.setObjectName("singleFileCB")
        self.vboxlayout.addWidget(self.singleFileCB)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.autoXFileBtn = QtGui.QPushButton(self.centralwidget)
        self.autoXFileBtn.setEnabled(False)
        self.autoXFileBtn.setObjectName("autoXFileBtn")
        self.hboxlayout1.addWidget(self.autoXFileBtn)

        self.autoExecuteLE = QtGui.QLineEdit(self.centralwidget)
        self.autoExecuteLE.setEnabled(False)
        self.autoExecuteLE.setObjectName("autoExecuteLE")
        self.hboxlayout1.addWidget(self.autoExecuteLE)
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

        self.cnvrtBrukerBtn = QtGui.QPushButton(self.centralwidget)
        self.cnvrtBrukerBtn.setObjectName("cnvrtBrukerBtn")
        self.vboxlayout.addWidget(self.cnvrtBrukerBtn)
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

        self.actionConvert2XML = QtGui.QAction(MainWindow)
        self.actionConvert2XML.setObjectName("actionConvert2XML")

        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.menuFile.addAction(self.actionClose)
        self.menuTools.addAction(self.actionConvert2XML)
        self.menuTools.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.brukerFolderLE,self.autoExecuteLE)
        MainWindow.setTabOrder(self.autoExecuteLE,self.outputFileLE)
        MainWindow.setTabOrder(self.outputFileLE,self.cnvrtBrukerBtn)
        MainWindow.setTabOrder(self.cnvrtBrukerBtn,self.outputTE)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bruker2mzXML", None, QtGui.QApplication.UnicodeUTF8))
        self.selBrukerDataBtn.setText(QtGui.QApplication.translate("MainWindow", "&Bruker Data:", None, QtGui.QApplication.UnicodeUTF8))
        self.singleFileCB.setText(QtGui.QApplication.translate("MainWindow", "Single File Conversion?", None, QtGui.QApplication.UnicodeUTF8))
        self.autoXFileBtn.setText(QtGui.QApplication.translate("MainWindow", "&AutoExecute File:", None, QtGui.QApplication.UnicodeUTF8))
        self.outputBtn.setText(QtGui.QApplication.translate("MainWindow", "&Output File:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Output Message:", None, QtGui.QApplication.UnicodeUTF8))
        self.cnvrtBrukerBtn.setText(QtGui.QApplication.translate("MainWindow", "&Convert to mzXML", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert2XML.setText(QtGui.QApplication.translate("MainWindow", "&Convert2XML", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))

import qrc_icons
