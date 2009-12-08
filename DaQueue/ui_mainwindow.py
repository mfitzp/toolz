# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/clowers/workspace/DaQueue/mainwindow.ui'
#
# Created: Tue Dec  8 09:21:46 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        MainWindow.setCursor(QtCore.Qt.ArrowCursor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Retro Question Block.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.tab)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.taskTable = CustomTable(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskTable.sizePolicy().hasHeightForWidth())
        self.taskTable.setSizePolicy(sizePolicy)
        self.taskTable.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.taskTable.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.taskTable.setGridStyle(QtCore.Qt.SolidLine)
        self.taskTable.setRowCount(3)
        self.taskTable.setColumnCount(6)
        self.taskTable.setObjectName("taskTable")
        self.taskTable.setColumnCount(6)
        self.taskTable.setRowCount(3)
        self.verticalLayout_2.addWidget(self.taskTable)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.serverStatusBtn = QtGui.QToolButton(self.layoutWidget)
        self.serverStatusBtn.setObjectName("serverStatusBtn")
        self.horizontalLayout_2.addWidget(self.serverStatusBtn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.deleteQueueRowBtn = QtGui.QPushButton(self.layoutWidget)
        self.deleteQueueRowBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.deleteQueueRowBtn.setObjectName("deleteQueueRowBtn")
        self.horizontalLayout_2.addWidget(self.deleteQueueRowBtn)
        self.updateQueueBtn = QtGui.QPushButton(self.layoutWidget)
        self.updateQueueBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.updateQueueBtn.setObjectName("updateQueueBtn")
        self.horizontalLayout_2.addWidget(self.updateQueueBtn)
        self.submitQueueBtn = QtGui.QPushButton(self.layoutWidget)
        self.submitQueueBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.submitQueueBtn.setObjectName("submitQueueBtn")
        self.horizontalLayout_2.addWidget(self.submitQueueBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editServerCB = QtGui.QCheckBox(self.tab_2)
        self.editServerCB.setObjectName("editServerCB")
        self.horizontalLayout.addWidget(self.editServerCB)
        self.line = QtGui.QFrame(self.tab_2)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.serverAddressLE = QtGui.QLineEdit(self.tab_2)
        self.serverAddressLE.setEnabled(False)
        self.serverAddressLE.setObjectName("serverAddressLE")
        self.horizontalLayout_3.addWidget(self.serverAddressLE)
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.portSB = QtGui.QSpinBox(self.tab_2)
        self.portSB.setEnabled(False)
        self.portSB.setMaximum(20000)
        self.portSB.setProperty("value", 5984)
        self.portSB.setObjectName("portSB")
        self.horizontalLayout_3.addWidget(self.portSB)
        self.resetServerBtn = QtGui.QPushButton(self.tab_2)
        self.resetServerBtn.setEnabled(False)
        self.resetServerBtn.setObjectName("resetServerBtn")
        self.horizontalLayout_3.addWidget(self.resetServerBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtGui.QSpacerItem(20, 78, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtGui.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menuFunctions = QtGui.QMenu(self.menuBar)
        self.menuFunctions.setObjectName("menuFunctions")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DaQueue", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Server Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.serverStatusBtn.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteQueueRowBtn.setText(QtGui.QApplication.translate("MainWindow", "Delete Job", None, QtGui.QApplication.UnicodeUTF8))
        self.updateQueueBtn.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.submitQueueBtn.setText(QtGui.QApplication.translate("MainWindow", "Submit Queue", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Queue", None, QtGui.QApplication.UnicodeUTF8))
        self.editServerCB.setText(QtGui.QApplication.translate("MainWindow", "Edit Server Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Server Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.serverAddressLE.setToolTip(QtGui.QApplication.translate("MainWindow", "Address of the CouchDB server used to store queue jobs.", None, QtGui.QApplication.UnicodeUTF8))
        self.serverAddressLE.setInputMask(QtGui.QApplication.translate("MainWindow", "999.999.999.999; ", None, QtGui.QApplication.UnicodeUTF8))
        self.serverAddressLE.setText(QtGui.QApplication.translate("MainWindow", "127.0.0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.resetServerBtn.setText(QtGui.QApplication.translate("MainWindow", "Reset Server", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFunctions.setTitle(QtGui.QApplication.translate("MainWindow", "Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTestAction.setText(QtGui.QApplication.translate("MainWindow", "TestAction", None, QtGui.QApplication.UnicodeUTF8))

from tableClass import CustomTable
