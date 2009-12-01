# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\DaQueue\mainwindow.ui'
#
# Created: Tue Dec 01 13:00:46 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(562, 745)
        MainWindow.setCursor(QtCore.Qt.ArrowCursor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Retro Question Block.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtUrl = QtGui.QLineEdit(self.centralWidget)
        self.txtUrl.setObjectName("txtUrl")
        self.horizontalLayout.addWidget(self.txtUrl)
        self.btnNavigate = QtGui.QPushButton(self.centralWidget)
        self.btnNavigate.setObjectName("btnNavigate")
        self.horizontalLayout.addWidget(self.btnNavigate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webView = QtWebKit.QWebView(self.centralWidget)
        self.webView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.verticalLayout.addWidget(self.webView)
        self.taskTable = CustomTable(self.centralWidget)
        self.taskTable.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.taskTable.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.taskTable.setGridStyle(QtCore.Qt.SolidLine)
        self.taskTable.setRowCount(5)
        self.taskTable.setColumnCount(5)
        self.taskTable.setObjectName("taskTable")
        self.taskTable.setColumnCount(5)
        self.taskTable.setRowCount(5)
        self.verticalLayout.addWidget(self.taskTable)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 562, 21))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtGui.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menuFunctions = QtGui.QMenu(self.menuBar)
        self.menuFunctions.setObjectName("menuFunctions")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionTestAction = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/Service Manager.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTestAction.setIcon(icon1)
        self.actionTestAction.setIconVisibleInMenu(True)
        self.actionTestAction.setObjectName("actionTestAction")
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menuFunctions.menuAction())
        self.toolBar.addAction(self.actionTestAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DaQueue", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNavigate.setText(QtGui.QApplication.translate("MainWindow", "Navigate", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFunctions.setTitle(QtGui.QApplication.translate("MainWindow", "Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTestAction.setText(QtGui.QApplication.translate("MainWindow", "TestAction", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
from tableClass import CustomTable
