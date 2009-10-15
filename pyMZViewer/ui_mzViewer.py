# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\pyMZViewer\mzViewer.ui'
#
# Created: Thu Oct 15 11:14:26 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(647, 744)
        MainWindow.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(50)
        font.setBold(False)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/games.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.chromTabWidget = QtGui.QTabWidget(self.splitter)
        self.chromTabWidget.setObjectName("chromTabWidget")
        self.chromTab = QtGui.QWidget()
        self.chromTab.setObjectName("chromTab")
        self.verticalLayout = QtGui.QVBoxLayout(self.chromTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.chromTab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spectra_CB = QtGui.QComboBox(self.chromTab)
        self.spectra_CB.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.spectra_CB.setObjectName("spectra_CB")
        self.horizontalLayout_2.addWidget(self.spectra_CB)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.chromTab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.scanSBox = QtGui.QSpinBox(self.chromTab)
        self.scanSBox.setFrame(False)
        self.scanSBox.setReadOnly(True)
        self.scanSBox.setMaximum(10000000)
        self.scanSBox.setObjectName("scanSBox")
        self.horizontalLayout.addWidget(self.scanSBox)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.chromWidget = MPL_Widget(self.chromTab)
        self.chromWidget.setObjectName("chromWidget")
        self.verticalLayout.addWidget(self.chromWidget)
        self.chromTabWidget.addTab(self.chromTab, "")
        self.scanInfoTab = QtGui.QWidget()
        self.scanInfoTab.setObjectName("scanInfoTab")
        self.hboxlayout = QtGui.QHBoxLayout(self.scanInfoTab)
        self.hboxlayout.setObjectName("hboxlayout")
        self.tableWidget = QtGui.QTableWidget(self.scanInfoTab)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(20)
        self.hboxlayout.addWidget(self.tableWidget)
        self.chromTabWidget.addTab(self.scanInfoTab, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.widget = QtGui.QWidget(self.tab)
        self.widget.setGeometry(QtCore.QRect(10, 20, 187, 164))
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self._3 = QtGui.QHBoxLayout()
        self._3.setObjectName("_3")
        self.label_13 = QtGui.QLabel(self.widget)
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setObjectName("label_13")
        self._3.addWidget(self.label_13)
        self.mzLo_SB = QtGui.QDoubleSpinBox(self.widget)
        self.mzLo_SB.setDecimals(3)
        self.mzLo_SB.setMinimum(1.0)
        self.mzLo_SB.setMaximum(100000.0)
        self.mzLo_SB.setSingleStep(0.05)
        self.mzLo_SB.setProperty("value", QtCore.QVariant(650.0))
        self.mzLo_SB.setObjectName("mzLo_SB")
        self._3.addWidget(self.mzLo_SB)
        self.verticalLayout_4.addLayout(self._3)
        self._4 = QtGui.QHBoxLayout()
        self._4.setObjectName("_4")
        self.label_14 = QtGui.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self._4.addWidget(self.label_14)
        self.mzHi_SB = QtGui.QDoubleSpinBox(self.widget)
        self.mzHi_SB.setDecimals(3)
        self.mzHi_SB.setMinimum(1.0)
        self.mzHi_SB.setMaximum(100000.0)
        self.mzHi_SB.setSingleStep(0.05)
        self.mzHi_SB.setProperty("value", QtCore.QVariant(750.0))
        self.mzHi_SB.setObjectName("mzHi_SB")
        self._4.addWidget(self.mzHi_SB)
        self.verticalLayout_4.addLayout(self._4)
        self._5 = QtGui.QHBoxLayout()
        self._5.setObjectName("_5")
        self.getXIC_Btn = QtGui.QPushButton(self.widget)
        self.getXIC_Btn.setObjectName("getXIC_Btn")
        self._5.addWidget(self.getXIC_Btn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self._5.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self._5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.xicList_CB = QtGui.QComboBox(self.widget)
        self.xicList_CB.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.xicList_CB.setObjectName("xicList_CB")
        self.xicList_CB.addItem(QtCore.QString())
        self.horizontalLayout_4.addWidget(self.xicList_CB)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.chromTabWidget.addTab(self.tab, "")
        self.spectrumTabWidget = QtGui.QTabWidget(self.splitter)
        self.spectrumTabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.spectrumTabWidget.setObjectName("spectrumTabWidget")
        self.mzTab = QtGui.QWidget()
        self.mzTab.setObjectName("mzTab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.mzTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mzWidget = MPL_Widget(self.mzTab)
        self.mzWidget.setEnabled(True)
        self.mzWidget.setObjectName("mzWidget")
        self.verticalLayout_3.addWidget(self.mzWidget)
        self.spectrumTabWidget.addTab(self.mzTab, "")
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 647, 22))
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
        self.toolBar.setMinimumSize(QtCore.QSize(12, 25))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Edit = QtGui.QAction(MainWindow)
        self.action_Edit.setObjectName("action_Edit")
        self.action_Tools = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/Service Manager.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Tools.setIcon(icon1)
        self.action_Tools.setObjectName("action_Tools")
        self.actionFileOpen = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/fileopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFileOpen.setIcon(icon2)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.actionFileSave = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/filesave2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFileSave.setIcon(icon3)
        self.actionFileSave.setObjectName("actionFileSave")
        self.actionFileSaveAs = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/filesaveas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFileSaveAs.setIcon(icon4)
        self.actionFileSaveAs.setObjectName("actionFileSaveAs")
        self.actionNewFile = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/filenew.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFile.setIcon(icon5)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionTools = QtGui.QAction(MainWindow)
        self.actionTools.setIcon(icon1)
        self.actionTools.setObjectName("actionTools")
        self.action_getSelection = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/kspread_ksp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_getSelection.setIcon(icon6)
        self.action_getSelection.setObjectName("action_getSelection")
        self.actionClear = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/cleanlarge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear.setIcon(icon7)
        self.actionClear.setObjectName("actionClear")
        self.action_New = QtGui.QAction(MainWindow)
        self.action_New.setIcon(icon5)
        self.action_New.setObjectName("action_New")
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setIcon(icon2)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setIcon(icon3)
        self.action_Save.setObjectName("action_Save")
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setIcon(icon4)
        self.actionSave_As.setObjectName("actionSave_As")
        self.action_Exit = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Exit.setIcon(icon8)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Clear = QtGui.QAction(MainWindow)
        self.action_Clear.setIcon(icon7)
        self.action_Clear.setObjectName("action_Clear")
        self.action_Table_Selection = QtGui.QAction(MainWindow)
        self.action_Table_Selection.setIcon(icon6)
        self.action_Table_Selection.setObjectName("action_Table_Selection")
        self.action_Cut = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/editcut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Cut.setIcon(icon9)
        self.action_Cut.setObjectName("action_Cut")
        self.action_Paste = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/editpaste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Paste.setIcon(icon10)
        self.action_Paste.setObjectName("action_Paste")
        self.actionRunScript = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/software-development.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRunScript.setIcon(icon11)
        self.actionRunScript.setObjectName("actionRunScript")
        self.actionAbout = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon12)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPlot = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/120px-Icon_Mathematical_Plot.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlot.setIcon(icon13)
        self.actionPlot.setObjectName("actionPlot")
        self.actionDelete = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/xkill.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon14)
        self.actionDelete.setObjectName("actionDelete")
        self.actionDeleteAll = QtGui.QAction(MainWindow)
        self.actionDeleteAll.setIcon(icon14)
        self.actionDeleteAll.setObjectName("actionDeleteAll")
        self.actionPlotItem = QtGui.QAction(MainWindow)
        self.actionPlotItem.setIcon(icon13)
        self.actionPlotItem.setObjectName("actionPlotItem")
        self.actionHints = QtGui.QAction(MainWindow)
        self.actionHints.setObjectName("actionHints")
        self.menuFile.addAction(self.action_Open)
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
        self.toolBar.addAction(self.actionRunScript)

        self.retranslateUi(MainWindow)
        self.chromTabWidget.setCurrentIndex(0)
        self.spectrumTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "mzViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Spectra:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Scan #:", None, QtGui.QApplication.UnicodeUTF8))
        self.chromTabWidget.setTabText(self.chromTabWidget.indexOf(self.chromTab), QtGui.QApplication.translate("MainWindow", "Chromatogram", None, QtGui.QApplication.UnicodeUTF8))
        self.chromTabWidget.setTabText(self.chromTabWidget.indexOf(self.scanInfoTab), QtGui.QApplication.translate("MainWindow", "Scan Info", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "m/z Lo:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "m/z Hi:", None, QtGui.QApplication.UnicodeUTF8))
        self.mzHi_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "If this value is set to -1 then a TIC starting from m/z Lo will be returned", None, QtGui.QApplication.UnicodeUTF8))
        self.getXIC_Btn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Create an EIC for all members within a selected group.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.getXIC_Btn.setText(QtGui.QApplication.translate("MainWindow", "Fetch XIC", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Current XIC:", None, QtGui.QApplication.UnicodeUTF8))
        self.xicList_CB.setItemText(0, QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.chromTabWidget.setTabText(self.chromTabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.spectrumTabWidget.setTabText(self.spectrumTabWidget.indexOf(self.mzTab), QtGui.QApplication.translate("MainWindow", "MS", None, QtGui.QApplication.UnicodeUTF8))
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

from mpl_pyqt4_widget import MPL_Widget
import SubPlot_rc
