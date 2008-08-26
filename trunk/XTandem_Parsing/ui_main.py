# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\SVN\toolz\XTandem_Parsing\main.ui'
#
# Created: Tue Aug 26 10:53:40 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,1085,853).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setMinimumSize(QtCore.QSize(0,25))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(50)
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setWindowIcon(QtGui.QIcon(":/new/prefix1/icons/games.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.plotTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.plotTabWidget.setObjectName("plotTabWidget")

        self.plotTab = QtGui.QWidget()
        self.plotTab.setObjectName("plotTab")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.plotTab)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.plotWidget = MPL_Widget(self.plotTab)
        self.plotWidget.setObjectName("plotWidget")
        self.hboxlayout2.addWidget(self.plotWidget)
        self.plotTabWidget.addTab(self.plotTab,"")

        self.configTab = QtGui.QWidget()
        self.configTab.setObjectName("configTab")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.configTab)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label_4 = QtGui.QLabel(self.configTab)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,0,0,1,1)

        self.label_5 = QtGui.QLabel(self.configTab)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,0,1,1,1)

        self.db_TableList = QtGui.QListWidget(self.configTab)
        self.db_TableList.setObjectName("db_TableList")
        self.gridlayout.addWidget(self.db_TableList,1,0,1,1)

        self.db_XCols = QtGui.QListWidget(self.configTab)
        self.db_XCols.setObjectName("db_XCols")
        self.gridlayout.addWidget(self.db_XCols,1,1,1,1)

        self.addPlotButton = QtGui.QPushButton(self.configTab)
        self.addPlotButton.setObjectName("addPlotButton")
        self.gridlayout.addWidget(self.addPlotButton,2,0,1,1)

        self.label_6 = QtGui.QLabel(self.configTab)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,2,1,1,1)

        self.db_YCols = QtGui.QListWidget(self.configTab)
        self.db_YCols.setObjectName("db_YCols")
        self.gridlayout.addWidget(self.db_YCols,3,1,1,1)

        self.cb_logx = QtGui.QCheckBox(self.configTab)
        self.cb_logx.setObjectName("cb_logx")
        self.gridlayout.addWidget(self.cb_logx,5,0,1,1)

        self.cb_logy = QtGui.QCheckBox(self.configTab)
        self.cb_logy.setObjectName("cb_logy")
        self.gridlayout.addWidget(self.cb_logy,5,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.openDBButton = QtGui.QPushButton(self.configTab)
        self.openDBButton.setObjectName("openDBButton")
        self.hboxlayout4.addWidget(self.openDBButton)

        self.curDBPathName = QtGui.QLineEdit(self.configTab)
        self.curDBPathName.setObjectName("curDBPathName")
        self.hboxlayout4.addWidget(self.curDBPathName)

        self.dbConnectRB = QtGui.QRadioButton(self.configTab)
        self.dbConnectRB.setObjectName("dbConnectRB")
        self.hboxlayout4.addWidget(self.dbConnectRB)
        self.vboxlayout1.addLayout(self.hboxlayout4)

        self.checkBox = QtGui.QCheckBox(self.configTab)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.vboxlayout1.addWidget(self.checkBox)
        self.vboxlayout.addLayout(self.vboxlayout1)
        self.hboxlayout3.addLayout(self.vboxlayout)
        self.plotTabWidget.addTab(self.configTab,"")
        self.hboxlayout1.addWidget(self.plotTabWidget)

        self.SelectInfoWidget = QtGui.QTableWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectInfoWidget.sizePolicy().hasHeightForWidth())
        self.SelectInfoWidget.setSizePolicy(sizePolicy)
        self.SelectInfoWidget.setObjectName("SelectInfoWidget")
        self.hboxlayout1.addWidget(self.SelectInfoWidget)
        self.hboxlayout.addLayout(self.hboxlayout1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,1085,22))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(50)
        font.setBold(False)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")

        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")

        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")

        self.menuData = QtGui.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(12,25))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)

        self.action_Edit = QtGui.QAction(MainWindow)
        self.action_Edit.setObjectName("action_Edit")

        self.action_Tools = QtGui.QAction(MainWindow)
        self.action_Tools.setIcon(QtGui.QIcon(":/new/prefix1/icons/Service Manager.png"))
        self.action_Tools.setObjectName("action_Tools")

        self.actionFileOpen = QtGui.QAction(MainWindow)
        self.actionFileOpen.setIcon(QtGui.QIcon(":/new/prefix1/icons/fileopen.png"))
        self.actionFileOpen.setObjectName("actionFileOpen")

        self.actionFileSave = QtGui.QAction(MainWindow)
        self.actionFileSave.setIcon(QtGui.QIcon(":/new/prefix1/icons/filesave2.png"))
        self.actionFileSave.setObjectName("actionFileSave")

        self.actionFileSaveAs = QtGui.QAction(MainWindow)
        self.actionFileSaveAs.setIcon(QtGui.QIcon(":/new/prefix1/icons/filesaveas.png"))
        self.actionFileSaveAs.setObjectName("actionFileSaveAs")

        self.actionNewFile = QtGui.QAction(MainWindow)
        self.actionNewFile.setIcon(QtGui.QIcon(":/new/prefix1/icons/filenew.png"))
        self.actionNewFile.setObjectName("actionNewFile")

        self.actionTools = QtGui.QAction(MainWindow)
        self.actionTools.setIcon(QtGui.QIcon(":/new/prefix1/icons/Service Manager.png"))
        self.actionTools.setObjectName("actionTools")

        self.action_getSelection = QtGui.QAction(MainWindow)
        self.action_getSelection.setIcon(QtGui.QIcon(":/new/prefix1/icons/kspread_ksp.png"))
        self.action_getSelection.setObjectName("action_getSelection")

        self.actionClear = QtGui.QAction(MainWindow)
        self.actionClear.setIcon(QtGui.QIcon(":/new/prefix1/icons/cleanlarge.png"))
        self.actionClear.setObjectName("actionClear")

        self.action_New = QtGui.QAction(MainWindow)
        self.action_New.setIcon(QtGui.QIcon(":/new/prefix1/icons/filenew.png"))
        self.action_New.setObjectName("action_New")

        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setIcon(QtGui.QIcon(":/new/prefix1/icons/fileopen.png"))
        self.action_Open.setObjectName("action_Open")

        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setIcon(QtGui.QIcon(":/new/prefix1/icons/filesave2.png"))
        self.action_Save.setObjectName("action_Save")

        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setIcon(QtGui.QIcon(":/new/prefix1/icons/filesaveas.png"))
        self.actionSave_As.setObjectName("actionSave_As")

        self.action_Exit = QtGui.QAction(MainWindow)
        self.action_Exit.setIcon(QtGui.QIcon(":/new/prefix1/icons/exit.png"))
        self.action_Exit.setObjectName("action_Exit")

        self.action_Clear = QtGui.QAction(MainWindow)
        self.action_Clear.setIcon(QtGui.QIcon(":/new/prefix1/icons/cleanlarge.png"))
        self.action_Clear.setObjectName("action_Clear")

        self.action_Table_Selection = QtGui.QAction(MainWindow)
        self.action_Table_Selection.setIcon(QtGui.QIcon(":/new/prefix1/icons/kspread_ksp.png"))
        self.action_Table_Selection.setObjectName("action_Table_Selection")

        self.action_Cut = QtGui.QAction(MainWindow)
        self.action_Cut.setIcon(QtGui.QIcon(":/new/prefix1/icons/editcut.png"))
        self.action_Cut.setObjectName("action_Cut")

        self.action_Paste = QtGui.QAction(MainWindow)
        self.action_Paste.setIcon(QtGui.QIcon(":/new/prefix1/icons/editpaste.png"))
        self.action_Paste.setObjectName("action_Paste")

        self.actionRunScript = QtGui.QAction(MainWindow)
        self.actionRunScript.setIcon(QtGui.QIcon(":/new/prefix1/icons/software-development.png"))
        self.actionRunScript.setObjectName("actionRunScript")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setIcon(QtGui.QIcon(":/new/prefix1/icons/help.png"))
        self.actionAbout.setObjectName("actionAbout")

        self.actionPlot = QtGui.QAction(MainWindow)
        self.actionPlot.setIcon(QtGui.QIcon(":/new/prefix1/icons/120px-Icon_Mathematical_Plot.svg.png"))
        self.actionPlot.setObjectName("actionPlot")

        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setIcon(QtGui.QIcon(":/new/prefix1/icons/xkill.png"))
        self.actionDelete.setObjectName("actionDelete")

        self.actionDeleteAll = QtGui.QAction(MainWindow)
        self.actionDeleteAll.setIcon(QtGui.QIcon(":/new/prefix1/icons/xkill.png"))
        self.actionDeleteAll.setObjectName("actionDeleteAll")

        self.actionPlotItem = QtGui.QAction(MainWindow)
        self.actionPlotItem.setIcon(QtGui.QIcon(":/new/prefix1/icons/120px-Icon_Mathematical_Plot.svg.png"))
        self.actionPlotItem.setObjectName("actionPlotItem")

        self.actionHints = QtGui.QAction(MainWindow)
        self.actionHints.setObjectName("actionHints")
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.action_Exit)
        self.menu_Edit.addAction(self.action_Cut)
        self.menu_Edit.addAction(self.action_Paste)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionHints)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionFileOpen)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addAction(self.actionRunScript)

        self.retranslateUi(MainWindow)
        self.plotTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "X!Tandem Results Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.plotTabWidget.setTabText(self.plotTabWidget.indexOf(self.plotTab), QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Database Tables:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "X-Axis:", None, QtGui.QApplication.UnicodeUTF8))
        self.addPlotButton.setText(QtGui.QApplication.translate("MainWindow", "Add Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Y-Axis:", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_logx.setText(QtGui.QApplication.translate("MainWindow", "Log X", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_logy.setText(QtGui.QApplication.translate("MainWindow", "Log Y", None, QtGui.QApplication.UnicodeUTF8))
        self.openDBButton.setText(QtGui.QApplication.translate("MainWindow", "Select Database", None, QtGui.QApplication.UnicodeUTF8))
        self.dbConnectRB.setText(QtGui.QApplication.translate("MainWindow", "DB Connected?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Append New Files to Database?", None, QtGui.QApplication.UnicodeUTF8))
        self.plotTabWidget.setTabText(self.plotTabWidget.indexOf(self.configTab), QtGui.QApplication.translate("MainWindow", "Define Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.SelectInfoWidget.setRowCount(20)
        self.SelectInfoWidget.setColumnCount(2)
        self.SelectInfoWidget.clear()
        self.SelectInfoWidget.setColumnCount(2)
        self.SelectInfoWidget.setRowCount(20)
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Tools.setTitle(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuData.setTitle(QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Edit.setText(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Tools.setText(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileOpen.setText(QtGui.QApplication.translate("MainWindow", "fileOpen", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileOpen.setToolTip(QtGui.QApplication.translate("MainWindow", "Open File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileSave.setText(QtGui.QApplication.translate("MainWindow", "fileSave", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileSave.setToolTip(QtGui.QApplication.translate("MainWindow", "Save File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFileSaveAs.setText(QtGui.QApplication.translate("MainWindow", "fileSaveAs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFile.setText(QtGui.QApplication.translate("MainWindow", "newFile", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNewFile.setToolTip(QtGui.QApplication.translate("MainWindow", "New File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTools.setText(QtGui.QApplication.translate("MainWindow", "Transfer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTools.setIconText(QtGui.QApplication.translate("MainWindow", "Transfer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTools.setToolTip(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.action_getSelection.setText(QtGui.QApplication.translate("MainWindow", "getSelection", None, QtGui.QApplication.UnicodeUTF8))
        self.action_getSelection.setToolTip(QtGui.QApplication.translate("MainWindow", "Get Table Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("MainWindow", "clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear Data and Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setText(QtGui.QApplication.translate("MainWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save &As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Exit.setText(QtGui.QApplication.translate("MainWindow", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Exit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear.setText(QtGui.QApplication.translate("MainWindow", "Clea&r", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Table_Selection.setText(QtGui.QApplication.translate("MainWindow", "&Table Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Cut.setText(QtGui.QApplication.translate("MainWindow", "&Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Cut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Paste.setText(QtGui.QApplication.translate("MainWindow", "&Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Paste.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRunScript.setText(QtGui.QApplication.translate("MainWindow", "runScript", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRunScript.setToolTip(QtGui.QApplication.translate("MainWindow", "Run Python Script", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlot.setText(QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteAll.setText(QtGui.QApplication.translate("MainWindow", "DeleteAll", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotItem.setText(QtGui.QApplication.translate("MainWindow", "PlotItem", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotItem.setIconText(QtGui.QApplication.translate("MainWindow", "Plot Item", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotItem.setToolTip(QtGui.QApplication.translate("MainWindow", "Plot Item", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHints.setText(QtGui.QApplication.translate("MainWindow", "Hints", None, QtGui.QApplication.UnicodeUTF8))

from mpl_custom_widget import MPL_Widget
import SubPlot_rc
