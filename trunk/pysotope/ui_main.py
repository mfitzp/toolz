# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/clowers/workspace/pysotope/main.ui'
#
# Created: Wed Nov 11 20:58:12 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 754)
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
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.mainTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.mainTabWidget.setObjectName("mainTabWidget")
        self.periodTab = QtGui.QWidget()
        self.periodTab.setObjectName("periodTab")
        self.elemTableWidget = QtGui.QTableWidget(self.periodTab)
        self.elemTableWidget.setEnabled(True)
        self.elemTableWidget.setGeometry(QtCore.QRect(730, 10, 256, 584))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elemTableWidget.sizePolicy().hasHeightForWidth())
        self.elemTableWidget.setSizePolicy(sizePolicy)
        self.elemTableWidget.setShowGrid(False)
        self.elemTableWidget.setRowCount(13)
        self.elemTableWidget.setColumnCount(2)
        self.elemTableWidget.setObjectName("elemTableWidget")
        self.elemTableWidget.setColumnCount(2)
        self.elemTableWidget.setRowCount(13)
        self.mainTabWidget.addTab(self.periodTab, "")
        self.calcTab = QtGui.QWidget()
        self.calcTab.setObjectName("calcTab")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.calcTab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formulaA_CB = QtGui.QCheckBox(self.calcTab)
        self.formulaA_CB.setChecked(True)
        self.formulaA_CB.setObjectName("formulaA_CB")
        self.horizontalLayout_2.addWidget(self.formulaA_CB)
        self.formulaInputA = QtGui.QLineEdit(self.calcTab)
        self.formulaInputA.setObjectName("formulaInputA")
        self.horizontalLayout_2.addWidget(self.formulaInputA)
        self.calcFormulaA_Btn = QtGui.QToolButton(self.calcTab)
        self.calcFormulaA_Btn.setObjectName("calcFormulaA_Btn")
        self.horizontalLayout_2.addWidget(self.calcFormulaA_Btn)
        self.formulaA_MW_LE = QtGui.QLineEdit(self.calcTab)
        self.formulaA_MW_LE.setReadOnly(True)
        self.formulaA_MW_LE.setObjectName("formulaA_MW_LE")
        self.horizontalLayout_2.addWidget(self.formulaA_MW_LE)
        self.label = QtGui.QLabel(self.calcTab)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.line = QtGui.QFrame(self.calcTab)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.label_7 = QtGui.QLabel(self.calcTab)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.chargeA = QtGui.QSpinBox(self.calcTab)
        self.chargeA.setMinimum(-99)
        self.chargeA.setObjectName("chargeA")
        self.horizontalLayout_2.addWidget(self.chargeA)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formulaB_CB = QtGui.QCheckBox(self.calcTab)
        self.formulaB_CB.setChecked(True)
        self.formulaB_CB.setObjectName("formulaB_CB")
        self.horizontalLayout_4.addWidget(self.formulaB_CB)
        self.formulaInputB = QtGui.QLineEdit(self.calcTab)
        self.formulaInputB.setObjectName("formulaInputB")
        self.horizontalLayout_4.addWidget(self.formulaInputB)
        self.calcFormulaB_Btn = QtGui.QToolButton(self.calcTab)
        self.calcFormulaB_Btn.setObjectName("calcFormulaB_Btn")
        self.horizontalLayout_4.addWidget(self.calcFormulaB_Btn)
        self.formulaB_MW_LE = QtGui.QLineEdit(self.calcTab)
        self.formulaB_MW_LE.setReadOnly(True)
        self.formulaB_MW_LE.setObjectName("formulaB_MW_LE")
        self.horizontalLayout_4.addWidget(self.formulaB_MW_LE)
        self.label_2 = QtGui.QLabel(self.calcTab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.line_2 = QtGui.QFrame(self.calcTab)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_4.addWidget(self.line_2)
        self.label_10 = QtGui.QLabel(self.calcTab)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.chargeB = QtGui.QSpinBox(self.calcTab)
        self.chargeB.setMinimum(-99)
        self.chargeB.setObjectName("chargeB")
        self.horizontalLayout_4.addWidget(self.chargeB)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        self.plotWidget = MPL_Widget(self.calcTab)
        self.plotWidget.setObjectName("plotWidget")
        self.verticalLayout_7.addWidget(self.plotWidget)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.mainTabWidget.addTab(self.calcTab, "")
        self.configTab = QtGui.QWidget()
        self.configTab.setObjectName("configTab")
        self.gridLayout = QtGui.QGridLayout(self.configTab)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtGui.QLabel(self.configTab)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.db_TableList = QtGui.QListWidget(self.configTab)
        self.db_TableList.setObjectName("db_TableList")
        self.verticalLayout_4.addWidget(self.db_TableList)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtGui.QLabel(self.configTab)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.db_XCols = QtGui.QListWidget(self.configTab)
        self.db_XCols.setObjectName("db_XCols")
        self.verticalLayout_5.addWidget(self.db_XCols)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtGui.QLabel(self.configTab)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.db_YCols = QtGui.QListWidget(self.configTab)
        self.db_YCols.setObjectName("db_YCols")
        self.verticalLayout_6.addWidget(self.db_YCols)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtGui.QLabel(self.configTab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.isoResCalc_SB = QtGui.QDoubleSpinBox(self.configTab)
        self.isoResCalc_SB.setDecimals(1)
        self.isoResCalc_SB.setMinimum(10.0)
        self.isoResCalc_SB.setMaximum(10000000.0)
        self.isoResCalc_SB.setSingleStep(500.0)
        self.isoResCalc_SB.setProperty("value", QtCore.QVariant(10000.0))
        self.isoResCalc_SB.setObjectName("isoResCalc_SB")
        self.horizontalLayout.addWidget(self.isoResCalc_SB)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(856, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.sizeModSpinBox = QtGui.QDoubleSpinBox(self.configTab)
        self.sizeModSpinBox.setMinimum(0.0)
        self.sizeModSpinBox.setSingleStep(0.5)
        self.sizeModSpinBox.setProperty("value", QtCore.QVariant(1.5))
        self.sizeModSpinBox.setObjectName("sizeModSpinBox")
        self.gridlayout.addWidget(self.sizeModSpinBox, 0, 1, 1, 1)
        self.sizeArrayComboB = QtGui.QComboBox(self.configTab)
        self.sizeArrayComboB.setObjectName("sizeArrayComboB")
        self.gridlayout.addWidget(self.sizeArrayComboB, 1, 1, 1, 1)
        self.updatePlotBtn = QtGui.QPushButton(self.configTab)
        self.updatePlotBtn.setObjectName("updatePlotBtn")
        self.gridlayout.addWidget(self.updatePlotBtn, 3, 1, 1, 1)
        self.clearPlotBtn = QtGui.QPushButton(self.configTab)
        self.clearPlotBtn.setObjectName("clearPlotBtn")
        self.gridlayout.addWidget(self.clearPlotBtn, 5, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.configTab)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.configTab)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridlayout.addWidget(self.label_9, 1, 0, 1, 1)
        self.clearPlotCB = QtGui.QCheckBox(self.configTab)
        self.clearPlotCB.setChecked(True)
        self.clearPlotCB.setObjectName("clearPlotCB")
        self.gridlayout.addWidget(self.clearPlotCB, 4, 1, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.cb_logx = QtGui.QCheckBox(self.configTab)
        self.cb_logx.setObjectName("cb_logx")
        self.hboxlayout1.addWidget(self.cb_logx)
        self.cb_logy = QtGui.QCheckBox(self.configTab)
        self.cb_logy.setObjectName("cb_logy")
        self.hboxlayout1.addWidget(self.cb_logy)
        self.gridlayout.addLayout(self.hboxlayout1, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridlayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout, 2, 1, 1, 1)
        self.mainTabWidget.addTab(self.configTab, "")
        self.hboxlayout.addWidget(self.mainTabWidget)
        self.verticalLayout_2.addLayout(self.hboxlayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1150, 23))
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
        self.toolBar.setEnabled(True)
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
        self.actionLoad_Folder = QtGui.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/fileimport.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Folder.setIcon(icon15)
        self.actionLoad_Folder.setObjectName("actionLoad_Folder")
        self.actionSave_All_Tables = QtGui.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/new/prefix1/icons/kchart_chrt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_All_Tables.setIcon(icon16)
        self.actionSave_All_Tables.setObjectName("actionSave_All_Tables")
        self.actionCopy_Current_Database = QtGui.QAction(MainWindow)
        self.actionCopy_Current_Database.setIcon(icon10)
        self.actionCopy_Current_Database.setObjectName("actionCopy_Current_Database")
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.actionLoad_Folder)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.action_Exit)
        self.menu_Edit.addAction(self.action_Cut)
        self.menu_Edit.addAction(self.action_Paste)
        self.menu_Tools.addAction(self.actionSave_All_Tables)
        self.menu_Tools.addAction(self.actionCopy_Current_Database)
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
        self.toolBar.addAction(self.actionTools)

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pysotope", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.periodTab), QtGui.QApplication.translate("MainWindow", "Periodic Table", None, QtGui.QApplication.UnicodeUTF8))
        self.formulaA_CB.setToolTip(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Plot the isotope pattern for formula A.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.formulaA_CB.setText(QtGui.QApplication.translate("MainWindow", "Forumla A:", None, QtGui.QApplication.UnicodeUTF8))
        self.calcFormulaA_Btn.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "g/mol", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Charge:", None, QtGui.QApplication.UnicodeUTF8))
        self.formulaB_CB.setToolTip(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Plot the isotope pattern for formula B.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.formulaB_CB.setText(QtGui.QApplication.translate("MainWindow", "Formula B:", None, QtGui.QApplication.UnicodeUTF8))
        self.calcFormulaB_Btn.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "g/mol", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Charge:", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.calcTab), QtGui.QApplication.translate("MainWindow", "MW Calculator", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Database Tables:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "X-Axis:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Y-Axis:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Isotope Calculation Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.updatePlotBtn.setText(QtGui.QApplication.translate("MainWindow", "Update Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPlotBtn.setText(QtGui.QApplication.translate("MainWindow", "Clear Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Size Modifier:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Size Array:", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPlotCB.setText(QtGui.QApplication.translate("MainWindow", "Clear on Update?", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_logx.setText(QtGui.QApplication.translate("MainWindow", "Log X", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_logy.setText(QtGui.QApplication.translate("MainWindow", "Log Y", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.configTab), QtGui.QApplication.translate("MainWindow", "Define Plot", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionLoad_Folder.setText(QtGui.QApplication.translate("MainWindow", "Load Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_All_Tables.setText(QtGui.QApplication.translate("MainWindow", "Save All Tables to CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy_Current_Database.setText(QtGui.QApplication.translate("MainWindow", "Copy Current Database", None, QtGui.QApplication.UnicodeUTF8))

from mpl_custom_widget import MPL_Widget
import SubPlot_rc