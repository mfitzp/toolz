# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\GCAlign\iterate.ui'
#
# Created: Mon Mar 30 10:54:31 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,834,742).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon(":/new/prefix1/Retro Mario World_32.png"))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setIconSize(QtCore.QSize(32,32))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(32,32))
        self.tabWidget.setObjectName("tabWidget")

        self.plotTab = QtGui.QWidget()
        self.plotTab.setObjectName("plotTab")

        self.vboxlayout = QtGui.QVBoxLayout(self.plotTab)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.plotTab)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.indexHSlider = QtGui.QSlider(self.plotTab)
        self.indexHSlider.setOrientation(QtCore.Qt.Horizontal)
        self.indexHSlider.setObjectName("indexHSlider")
        self.hboxlayout1.addWidget(self.indexHSlider)

        self.indexSpinBox = QtGui.QSpinBox(self.plotTab)
        self.indexSpinBox.setObjectName("indexSpinBox")
        self.hboxlayout1.addWidget(self.indexSpinBox)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_2 = QtGui.QLabel(self.plotTab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout3.addWidget(self.label_2)

        self.specNameEdit = QtGui.QLineEdit(self.plotTab)
        self.specNameEdit.setReadOnly(True)
        self.specNameEdit.setObjectName("specNameEdit")
        self.hboxlayout3.addWidget(self.specNameEdit)
        self.hboxlayout2.addLayout(self.hboxlayout3)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_26 = QtGui.QLabel(self.plotTab)
        self.label_26.setObjectName("label_26")
        self.hboxlayout4.addWidget(self.label_26)

        self.mzSIC_SB = QtGui.QSpinBox(self.plotTab)
        self.mzSIC_SB.setMinimum(1)
        self.mzSIC_SB.setMaximum(1000)
        self.mzSIC_SB.setProperty("value",QtCore.QVariant(43))
        self.mzSIC_SB.setObjectName("mzSIC_SB")
        self.hboxlayout4.addWidget(self.mzSIC_SB)

        self.sicGO_Btn = QtGui.QToolButton(self.plotTab)
        self.sicGO_Btn.setObjectName("sicGO_Btn")
        self.hboxlayout4.addWidget(self.sicGO_Btn)
        self.hboxlayout2.addLayout(self.hboxlayout4)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.splitter = QtGui.QSplitter(self.plotTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.plotWidget = MPL_Image_Widget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setMinimumSize(QtCore.QSize(500,250))
        self.plotWidget.setObjectName("plotWidget")

        self.plotWidget2 = MPL_Chrom_Widget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget2.sizePolicy().hasHeightForWidth())
        self.plotWidget2.setSizePolicy(sizePolicy)
        self.plotWidget2.setMinimumSize(QtCore.QSize(500,100))
        self.plotWidget2.setObjectName("plotWidget2")
        self.hboxlayout5.addWidget(self.splitter)

        self.tabWidget_3 = QtGui.QTabWidget(self.plotTab)
        self.tabWidget_3.setMaximumSize(QtCore.QSize(200,16777215))
        self.tabWidget_3.setObjectName("tabWidget_3")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab_4)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.addFileBtn = QtGui.QPushButton(self.tab_4)
        self.addFileBtn.setMaximumSize(QtCore.QSize(100,16777215))
        self.addFileBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.addFileBtn.setObjectName("addFileBtn")
        self.hboxlayout6.addWidget(self.addFileBtn)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout6.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout6)

        self.listWidget = QtGui.QListWidget(self.tab_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(100,0))
        self.listWidget.setMaximumSize(QtCore.QSize(200,16777215))
        self.listWidget.setBaseSize(QtCore.QSize(100,250))
        self.listWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidget.setObjectName("listWidget")
        self.vboxlayout1.addWidget(self.listWidget)
        self.tabWidget_3.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.hboxlayout7 = QtGui.QHBoxLayout(self.tab_5)
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.tableWidget = QtGui.QTableWidget(self.tab_5)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(200,16777215))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setObjectName("tableWidget")
        self.hboxlayout7.addWidget(self.tableWidget)
        self.tabWidget_3.addTab(self.tab_5,"")
        self.hboxlayout5.addWidget(self.tabWidget_3)
        self.vboxlayout.addLayout(self.hboxlayout5)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setHorizontalSpacing(3)
        self.gridlayout.setVerticalSpacing(2)
        self.gridlayout.setObjectName("gridlayout")

        self.cALabelLE = QtGui.QLineEdit(self.plotTab)
        self.cALabelLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cALabelLE.setFont(font)
        self.cALabelLE.setReadOnly(True)
        self.cALabelLE.setObjectName("cALabelLE")
        self.gridlayout.addWidget(self.cALabelLE,0,3,1,1)

        self.cAIndexLE = QtGui.QLineEdit(self.plotTab)
        self.cAIndexLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cAIndexLE.setFont(font)
        self.cAIndexLE.setReadOnly(True)
        self.cAIndexLE.setObjectName("cAIndexLE")
        self.gridlayout.addWidget(self.cAIndexLE,0,5,1,1)

        self.cA_XLE = QtGui.QLineEdit(self.plotTab)
        self.cA_XLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cA_XLE.setFont(font)
        self.cA_XLE.setReadOnly(True)
        self.cA_XLE.setObjectName("cA_XLE")
        self.gridlayout.addWidget(self.cA_XLE,0,7,1,1)

        self.cA_YLE = QtGui.QLineEdit(self.plotTab)
        self.cA_YLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cA_YLE.setFont(font)
        self.cA_YLE.setReadOnly(True)
        self.cA_YLE.setObjectName("cA_YLE")
        self.gridlayout.addWidget(self.cA_YLE,0,9,1,1)

        self.cBLabelLE = QtGui.QLineEdit(self.plotTab)
        self.cBLabelLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cBLabelLE.setFont(font)
        self.cBLabelLE.setReadOnly(True)
        self.cBLabelLE.setObjectName("cBLabelLE")
        self.gridlayout.addWidget(self.cBLabelLE,1,3,1,1)

        self.cBIndexLE = QtGui.QLineEdit(self.plotTab)
        self.cBIndexLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cBIndexLE.setFont(font)
        self.cBIndexLE.setReadOnly(True)
        self.cBIndexLE.setObjectName("cBIndexLE")
        self.gridlayout.addWidget(self.cBIndexLE,1,5,1,1)

        self.cB_XLE = QtGui.QLineEdit(self.plotTab)
        self.cB_XLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cB_XLE.setFont(font)
        self.cB_XLE.setReadOnly(True)
        self.cB_XLE.setObjectName("cB_XLE")
        self.gridlayout.addWidget(self.cB_XLE,1,7,1,1)

        self.cB_YLE = QtGui.QLineEdit(self.plotTab)
        self.cB_YLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cB_YLE.setFont(font)
        self.cB_YLE.setReadOnly(True)
        self.cB_YLE.setObjectName("cB_YLE")
        self.gridlayout.addWidget(self.cB_YLE,1,9,1,1)

        self.label_4 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,0,2,1,1)

        self.label_5 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,1,2,1,1)

        self.label_6 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,0,4,1,1)

        self.label_7 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,0,6,1,1)

        self.label_8 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8,0,8,1,1)

        self.label_9 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridlayout.addWidget(self.label_9,1,4,1,1)

        self.label_10 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridlayout.addWidget(self.label_10,1,6,1,1)

        self.label_11 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridlayout.addWidget(self.label_11,1,8,1,1)

        self.label_12 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridlayout.addWidget(self.label_12,0,10,1,1)

        self.label_13 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridlayout.addWidget(self.label_13,1,10,1,1)

        self.dxLE = QtGui.QLineEdit(self.plotTab)
        self.dxLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.dxLE.setFont(font)
        self.dxLE.setReadOnly(True)
        self.dxLE.setObjectName("dxLE")
        self.gridlayout.addWidget(self.dxLE,0,11,1,1)

        self.dyLE = QtGui.QLineEdit(self.plotTab)
        self.dyLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.dyLE.setFont(font)
        self.dyLE.setReadOnly(True)
        self.dyLE.setObjectName("dyLE")
        self.gridlayout.addWidget(self.dyLE,1,11,1,1)

        self.cursACB = QtGui.QCheckBox(self.plotTab)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.cursACB.setFont(font)
        self.cursACB.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cursACB.setObjectName("cursACB")
        self.gridlayout.addWidget(self.cursACB,0,0,1,1)

        self.cursBCB = QtGui.QCheckBox(self.plotTab)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setWeight(75)
        font.setItalic(True)
        font.setBold(True)
        self.cursBCB.setFont(font)
        self.cursBCB.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cursBCB.setObjectName("cursBCB")
        self.gridlayout.addWidget(self.cursBCB,1,0,1,1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.tabWidget.addTab(self.plotTab,"")

        self.optionsTab = QtGui.QWidget()
        self.optionsTab.setObjectName("optionsTab")

        self.gridlayout1 = QtGui.QGridLayout(self.optionsTab)
        self.gridlayout1.setObjectName("gridlayout1")

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")

        self.plotPkListCB = QtGui.QCheckBox(self.optionsTab)
        self.plotPkListCB.setEnabled(False)
        self.plotPkListCB.setObjectName("plotPkListCB")
        self.gridlayout2.addWidget(self.plotPkListCB,0,0,1,1)

        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setObjectName("gridlayout3")

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setHorizontalSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_3 = QtGui.QLabel(self.optionsTab)
        self.label_3.setEnabled(False)
        self.label_3.setMaximumSize(QtCore.QSize(50,16777215))
        self.label_3.setObjectName("label_3")
        self.gridlayout4.addWidget(self.label_3,0,0,1,1)

        self.sicMZSB = QtGui.QSpinBox(self.optionsTab)
        self.sicMZSB.setEnabled(False)
        self.sicMZSB.setMaximumSize(QtCore.QSize(75,16777215))
        self.sicMZSB.setMinimum(1)
        self.sicMZSB.setMaximum(400)
        self.sicMZSB.setObjectName("sicMZSB")
        self.gridlayout4.addWidget(self.sicMZSB,0,1,1,1)
        self.gridlayout3.addLayout(self.gridlayout4,0,0,1,1)

        self.pltSICBtn = QtGui.QPushButton(self.optionsTab)
        self.pltSICBtn.setEnabled(False)
        self.pltSICBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.pltSICBtn.setObjectName("pltSICBtn")
        self.gridlayout3.addWidget(self.pltSICBtn,1,0,1,1)

        self.plotTICBtn = QtGui.QPushButton(self.optionsTab)
        self.plotTICBtn.setEnabled(False)
        self.plotTICBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.plotTICBtn.setObjectName("plotTICBtn")
        self.gridlayout3.addWidget(self.plotTICBtn,2,0,1,1)

        self.plotBPCBtn = QtGui.QPushButton(self.optionsTab)
        self.plotBPCBtn.setEnabled(False)
        self.plotBPCBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.plotBPCBtn.setObjectName("plotBPCBtn")
        self.gridlayout3.addWidget(self.plotBPCBtn,3,0,1,1)
        self.gridlayout2.addLayout(self.gridlayout3,0,2,2,1)

        self.dendroCB = QtGui.QCheckBox(self.optionsTab)
        self.dendroCB.setEnabled(False)
        self.dendroCB.setObjectName("dendroCB")
        self.gridlayout2.addWidget(self.dendroCB,1,0,1,2)

        self.topHatCB = QtGui.QCheckBox(self.optionsTab)
        self.topHatCB.setEnabled(False)
        self.topHatCB.setObjectName("topHatCB")
        self.gridlayout2.addWidget(self.topHatCB,2,0,1,1)

        self.plotLegendCB = QtGui.QCheckBox(self.optionsTab)
        self.plotLegendCB.setEnabled(False)
        self.plotLegendCB.setChecked(True)
        self.plotLegendCB.setObjectName("plotLegendCB")
        self.gridlayout2.addWidget(self.plotLegendCB,2,1,1,2)

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.label_23 = QtGui.QLabel(self.optionsTab)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.hboxlayout8.addWidget(self.label_23)

        self.chromStyleCB = QtGui.QComboBox(self.optionsTab)
        self.chromStyleCB.setObjectName("chromStyleCB")
        self.hboxlayout8.addWidget(self.chromStyleCB)
        self.gridlayout2.addLayout(self.hboxlayout8,0,1,1,1)
        self.gridlayout1.addLayout(self.gridlayout2,0,0,1,2)

        self.loadDirBtn = QtGui.QPushButton(self.optionsTab)
        self.loadDirBtn.setEnabled(False)
        self.loadDirBtn.setObjectName("loadDirBtn")
        self.gridlayout1.addWidget(self.loadDirBtn,0,2,1,1)

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setObjectName("gridlayout5")

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.label_20 = QtGui.QLabel(self.optionsTab)
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.hboxlayout9.addWidget(self.label_20)

        self.specLengthSB = QtGui.QSpinBox(self.optionsTab)
        self.specLengthSB.setReadOnly(True)
        self.specLengthSB.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.specLengthSB.setMaximum(1000000)
        self.specLengthSB.setProperty("value",QtCore.QVariant(250000))
        self.specLengthSB.setObjectName("specLengthSB")
        self.hboxlayout9.addWidget(self.specLengthSB)
        self.gridlayout5.addLayout(self.hboxlayout9,0,0,1,1)

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_19 = QtGui.QLabel(self.optionsTab)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.hboxlayout10.addWidget(self.label_19)

        self.numSegsSB = QtGui.QSpinBox(self.optionsTab)
        self.numSegsSB.setMaximum(1000000)
        self.numSegsSB.setProperty("value",QtCore.QVariant(500))
        self.numSegsSB.setObjectName("numSegsSB")
        self.hboxlayout10.addWidget(self.numSegsSB)
        self.gridlayout5.addLayout(self.hboxlayout10,1,0,1,1)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.label_14 = QtGui.QLabel(self.optionsTab)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.hboxlayout11.addWidget(self.label_14)

        self.minSNRSB = QtGui.QSpinBox(self.optionsTab)
        self.minSNRSB.setMinimum(2)
        self.minSNRSB.setMaximum(250000)
        self.minSNRSB.setProperty("value",QtCore.QVariant(3))
        self.minSNRSB.setObjectName("minSNRSB")
        self.hboxlayout11.addWidget(self.minSNRSB)
        self.gridlayout5.addLayout(self.hboxlayout11,2,0,1,1)

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.label_15 = QtGui.QLabel(self.optionsTab)
        self.label_15.setEnabled(False)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.hboxlayout12.addWidget(self.label_15)

        self.slopeThreshSB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.slopeThreshSB.setEnabled(False)
        self.slopeThreshSB.setObjectName("slopeThreshSB")
        self.hboxlayout12.addWidget(self.slopeThreshSB)
        self.gridlayout5.addLayout(self.hboxlayout12,3,0,1,1)

        self.hboxlayout13 = QtGui.QHBoxLayout()
        self.hboxlayout13.setObjectName("hboxlayout13")

        self.label_17 = QtGui.QLabel(self.optionsTab)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.hboxlayout13.addWidget(self.label_17)

        self.smthKernSB = QtGui.QSpinBox(self.optionsTab)
        self.smthKernSB.setProperty("value",QtCore.QVariant(15))
        self.smthKernSB.setObjectName("smthKernSB")
        self.hboxlayout13.addWidget(self.smthKernSB)
        self.gridlayout5.addLayout(self.hboxlayout13,4,0,1,1)

        self.hboxlayout14 = QtGui.QHBoxLayout()
        self.hboxlayout14.setObjectName("hboxlayout14")

        self.label_18 = QtGui.QLabel(self.optionsTab)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.hboxlayout14.addWidget(self.label_18)

        self.peakWidthSB = QtGui.QSpinBox(self.optionsTab)
        self.peakWidthSB.setMinimum(3)
        self.peakWidthSB.setMaximum(200000)
        self.peakWidthSB.setProperty("value",QtCore.QVariant(25))
        self.peakWidthSB.setObjectName("peakWidthSB")
        self.hboxlayout14.addWidget(self.peakWidthSB)
        self.gridlayout5.addLayout(self.hboxlayout14,5,0,1,1)

        self.hboxlayout15 = QtGui.QHBoxLayout()
        self.hboxlayout15.setObjectName("hboxlayout15")

        self.showPickedPeaksCB = QtGui.QCheckBox(self.optionsTab)
        self.showPickedPeaksCB.setChecked(True)
        self.showPickedPeaksCB.setObjectName("showPickedPeaksCB")
        self.hboxlayout15.addWidget(self.showPickedPeaksCB)

        self.fndPeaksBtn = QtGui.QPushButton(self.optionsTab)
        self.fndPeaksBtn.setObjectName("fndPeaksBtn")
        self.hboxlayout15.addWidget(self.fndPeaksBtn)
        self.gridlayout5.addLayout(self.hboxlayout15,6,0,1,1)

        self.savePickedPeakBtn = QtGui.QPushButton(self.optionsTab)
        self.savePickedPeakBtn.setObjectName("savePickedPeakBtn")
        self.gridlayout5.addWidget(self.savePickedPeakBtn,7,0,1,1)
        self.gridlayout1.addLayout(self.gridlayout5,1,0,1,1)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setObjectName("gridlayout6")

        self.hboxlayout16 = QtGui.QHBoxLayout()
        self.hboxlayout16.setObjectName("hboxlayout16")

        self.distanceLabel = QtGui.QLabel(self.optionsTab)
        self.distanceLabel.setEnabled(False)
        self.distanceLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.distanceLabel.setObjectName("distanceLabel")
        self.hboxlayout16.addWidget(self.distanceLabel)

        self.maxDistThreshSB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.maxDistThreshSB.setEnabled(False)
        self.maxDistThreshSB.setMinimum(0.01)
        self.maxDistThreshSB.setProperty("value",QtCore.QVariant(10.0))
        self.maxDistThreshSB.setObjectName("maxDistThreshSB")
        self.hboxlayout16.addWidget(self.maxDistThreshSB)
        self.gridlayout6.addLayout(self.hboxlayout16,0,0,1,1)

        self.calcThreshCB = QtGui.QCheckBox(self.optionsTab)
        self.calcThreshCB.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.calcThreshCB.setChecked(True)
        self.calcThreshCB.setObjectName("calcThreshCB")
        self.gridlayout6.addWidget(self.calcThreshCB,1,0,1,1)

        self.hboxlayout17 = QtGui.QHBoxLayout()
        self.hboxlayout17.setObjectName("hboxlayout17")

        self.distCalMethLbl = QtGui.QLabel(self.optionsTab)
        self.distCalMethLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.distCalMethLbl.setObjectName("distCalMethLbl")
        self.hboxlayout17.addWidget(self.distCalMethLbl)

        self.distMethodCB = QtGui.QComboBox(self.optionsTab)
        self.distMethodCB.setObjectName("distMethodCB")
        self.hboxlayout17.addWidget(self.distMethodCB)
        self.gridlayout6.addLayout(self.hboxlayout17,2,0,1,1)

        self.hboxlayout18 = QtGui.QHBoxLayout()
        self.hboxlayout18.setObjectName("hboxlayout18")

        self.clustTypeLbl = QtGui.QLabel(self.optionsTab)
        self.clustTypeLbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.clustTypeLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.clustTypeLbl.setObjectName("clustTypeLbl")
        self.hboxlayout18.addWidget(self.clustTypeLbl)

        self.clusterTypeCB = QtGui.QComboBox(self.optionsTab)
        self.clusterTypeCB.setObjectName("clusterTypeCB")
        self.hboxlayout18.addWidget(self.clusterTypeCB)
        self.gridlayout6.addLayout(self.hboxlayout18,3,0,1,1)

        self.showDendroCB = QtGui.QCheckBox(self.optionsTab)
        self.showDendroCB.setChecked(True)
        self.showDendroCB.setObjectName("showDendroCB")
        self.gridlayout6.addWidget(self.showDendroCB,4,0,1,1)

        self.hboxlayout19 = QtGui.QHBoxLayout()
        self.hboxlayout19.setObjectName("hboxlayout19")

        self.dbScanCB = QtGui.QCheckBox(self.optionsTab)
        self.dbScanCB.setChecked(False)
        self.dbScanCB.setObjectName("dbScanCB")
        self.hboxlayout19.addWidget(self.dbScanCB)

        self.dbAutoCalcCB = QtGui.QCheckBox(self.optionsTab)
        self.dbAutoCalcCB.setEnabled(False)
        self.dbAutoCalcCB.setChecked(True)
        self.dbAutoCalcCB.setObjectName("dbAutoCalcCB")
        self.hboxlayout19.addWidget(self.dbAutoCalcCB)

        self.hboxlayout20 = QtGui.QHBoxLayout()
        self.hboxlayout20.setObjectName("hboxlayout20")

        self.denDistLbl = QtGui.QLabel(self.optionsTab)
        self.denDistLbl.setEnabled(False)
        self.denDistLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.denDistLbl.setObjectName("denDistLbl")
        self.hboxlayout20.addWidget(self.denDistLbl)

        self.densityDistThreshSB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.densityDistThreshSB.setEnabled(False)
        self.densityDistThreshSB.setMinimum(0.01)
        self.densityDistThreshSB.setProperty("value",QtCore.QVariant(15.0))
        self.densityDistThreshSB.setObjectName("densityDistThreshSB")
        self.hboxlayout20.addWidget(self.densityDistThreshSB)
        self.hboxlayout19.addLayout(self.hboxlayout20)
        self.gridlayout6.addLayout(self.hboxlayout19,5,0,1,1)

        self.hboxlayout21 = QtGui.QHBoxLayout()
        self.hboxlayout21.setObjectName("hboxlayout21")

        self.denGrpNum = QtGui.QLabel(self.optionsTab)
        self.denGrpNum.setEnabled(False)
        self.denGrpNum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.denGrpNum.setObjectName("denGrpNum")
        self.hboxlayout21.addWidget(self.denGrpNum)

        self.denGrpNumThresh = QtGui.QDoubleSpinBox(self.optionsTab)
        self.denGrpNumThresh.setEnabled(False)
        self.denGrpNumThresh.setDecimals(0)
        self.denGrpNumThresh.setMinimum(1.0)
        self.denGrpNumThresh.setMaximum(20000.0)
        self.denGrpNumThresh.setProperty("value",QtCore.QVariant(15.0))
        self.denGrpNumThresh.setObjectName("denGrpNumThresh")
        self.hboxlayout21.addWidget(self.denGrpNumThresh)
        self.gridlayout6.addLayout(self.hboxlayout21,6,0,1,1)

        self.hboxlayout22 = QtGui.QHBoxLayout()
        self.hboxlayout22.setObjectName("hboxlayout22")

        self.clusterBtn = QtGui.QPushButton(self.optionsTab)
        self.clusterBtn.setObjectName("clusterBtn")
        self.hboxlayout22.addWidget(self.clusterBtn)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout22.addItem(spacerItem1)
        self.gridlayout6.addLayout(self.hboxlayout22,7,0,1,1)
        self.gridlayout1.addLayout(self.gridlayout6,1,1,1,2)
        self.tabWidget.addTab(self.optionsTab,"")

        self.pkListTab = QtGui.QWidget()
        self.pkListTab.setObjectName("pkListTab")

        self.hboxlayout23 = QtGui.QHBoxLayout(self.pkListTab)
        self.hboxlayout23.setObjectName("hboxlayout23")

        self.tabWidget_2 = QtGui.QTabWidget(self.pkListTab)
        self.tabWidget_2.setObjectName("tabWidget_2")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.hboxlayout24 = QtGui.QHBoxLayout(self.tab)
        self.hboxlayout24.setObjectName("hboxlayout24")

        self.tabPeakTable = CustomTable(self.tab)
        self.tabPeakTable.setObjectName("tabPeakTable")
        self.hboxlayout24.addWidget(self.tabPeakTable)
        self.tabWidget_2.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.hboxlayout25 = QtGui.QHBoxLayout(self.tab_2)
        self.hboxlayout25.setObjectName("hboxlayout25")

        self.tabPeakTable_2 = CustomTable(self.tab_2)
        self.tabPeakTable_2.setObjectName("tabPeakTable_2")
        self.hboxlayout25.addWidget(self.tabPeakTable_2)
        self.tabWidget_2.addTab(self.tab_2,"")
        self.hboxlayout23.addWidget(self.tabWidget_2)
        self.tabWidget.addTab(self.pkListTab,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.hboxlayout26 = QtGui.QHBoxLayout(self.tab_3)
        self.hboxlayout26.setObjectName("hboxlayout26")

        self.gridlayout7 = QtGui.QGridLayout()
        self.gridlayout7.setObjectName("gridlayout7")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout27 = QtGui.QHBoxLayout()
        self.hboxlayout27.setObjectName("hboxlayout27")

        self.label_25 = QtGui.QLabel(self.tab_3)
        self.label_25.setObjectName("label_25")
        self.hboxlayout27.addWidget(self.label_25)

        self.lineEdit = QtGui.QLineEdit(self.tab_3)
        self.lineEdit.setObjectName("lineEdit")
        self.hboxlayout27.addWidget(self.lineEdit)
        self.vboxlayout2.addLayout(self.hboxlayout27)

        self.label_21 = QtGui.QLabel(self.tab_3)
        self.label_21.setObjectName("label_21")
        self.vboxlayout2.addWidget(self.label_21)

        self.listWidget_2 = QtGui.QListWidget(self.tab_3)
        self.listWidget_2.setObjectName("listWidget_2")
        self.vboxlayout2.addWidget(self.listWidget_2)
        self.gridlayout7.addLayout(self.vboxlayout2,1,0,1,1)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.hboxlayout28 = QtGui.QHBoxLayout()
        self.hboxlayout28.setObjectName("hboxlayout28")

        self.label_24 = QtGui.QLabel(self.tab_3)
        self.label_24.setObjectName("label_24")
        self.hboxlayout28.addWidget(self.label_24)

        self.comboBox = QtGui.QComboBox(self.tab_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout28.addWidget(self.comboBox)
        self.vboxlayout3.addLayout(self.hboxlayout28)

        self.label_22 = QtGui.QLabel(self.tab_3)
        self.label_22.setObjectName("label_22")
        self.vboxlayout3.addWidget(self.label_22)

        self.listWidget_3 = QtGui.QListWidget(self.tab_3)
        self.listWidget_3.setObjectName("listWidget_3")
        self.vboxlayout3.addWidget(self.listWidget_3)
        self.gridlayout7.addLayout(self.vboxlayout3,1,2,1,1)

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setObjectName("vboxlayout4")

        spacerItem2 = QtGui.QSpacerItem(20,50,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout4.addItem(spacerItem2)

        self.toolButton = QtGui.QToolButton(self.tab_3)
        self.toolButton.setMinimumSize(QtCore.QSize(32,32))
        self.toolButton.setMaximumSize(QtCore.QSize(32,32))
        self.toolButton.setIcon(QtGui.QIcon(":/new/prefix1/icons/forward.png"))
        self.toolButton.setIconSize(QtCore.QSize(32,32))
        self.toolButton.setObjectName("toolButton")
        self.vboxlayout4.addWidget(self.toolButton)

        self.toolButton_2 = QtGui.QToolButton(self.tab_3)
        self.toolButton_2.setMinimumSize(QtCore.QSize(32,32))
        self.toolButton_2.setMaximumSize(QtCore.QSize(32,32))
        self.toolButton_2.setIcon(QtGui.QIcon(":/new/prefix1/icons/back.png"))
        self.toolButton_2.setIconSize(QtCore.QSize(32,32))
        self.toolButton_2.setObjectName("toolButton_2")
        self.vboxlayout4.addWidget(self.toolButton_2)

        spacerItem3 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout4.addItem(spacerItem3)
        self.gridlayout7.addLayout(self.vboxlayout4,1,1,1,1)

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.label_16 = QtGui.QLabel(self.tab_3)
        self.label_16.setObjectName("label_16")
        self.vboxlayout5.addWidget(self.label_16)

        self.textBrowser = QtGui.QTextBrowser(self.tab_3)
        self.textBrowser.setObjectName("textBrowser")
        self.vboxlayout5.addWidget(self.textBrowser)
        self.gridlayout7.addLayout(self.vboxlayout5,2,0,1,1)

        self.hboxlayout29 = QtGui.QHBoxLayout()
        self.hboxlayout29.setObjectName("hboxlayout29")

        self.pushButton_3 = QtGui.QPushButton(self.tab_3)
        self.pushButton_3.setIcon(QtGui.QIcon(":/new/prefix1/icons/fileopen.png"))
        self.pushButton_3.setObjectName("pushButton_3")
        self.hboxlayout29.addWidget(self.pushButton_3)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout29.addItem(spacerItem4)
        self.gridlayout7.addLayout(self.hboxlayout29,0,0,1,1)
        self.hboxlayout26.addLayout(self.gridlayout7)
        self.tabWidget.addTab(self.tab_3,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,834,21))
        self.menubar.setObjectName("menubar")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menu_Peak_Tools = QtGui.QMenu(self.menubar)
        self.menu_Peak_Tools.setObjectName("menu_Peak_Tools")

        self.menuC_luster = QtGui.QMenu(self.menubar)
        self.menuC_luster.setObjectName("menuC_luster")

        self.menuCluster_Peaks = QtGui.QMenu(self.menuC_luster)
        self.menuCluster_Peaks.setObjectName("menuCluster_Peaks")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)

        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setIcon(QtGui.QIcon(":/new/prefix1/icons/fileopen.png"))
        self.action_Open.setObjectName("action_Open")

        self.actionCursor_A = QtGui.QAction(MainWindow)
        self.actionCursor_A.setObjectName("actionCursor_A")

        self.actionCursor_B = QtGui.QAction(MainWindow)
        self.actionCursor_B.setObjectName("actionCursor_B")

        self.actionClear_Cursors = QtGui.QAction(MainWindow)
        self.actionClear_Cursors.setObjectName("actionClear_Cursors")

        self.actionLabel_Peak = QtGui.QAction(MainWindow)
        self.actionLabel_Peak.setObjectName("actionLabel_Peak")

        self.actionCopy_to_Clipboard = QtGui.QAction(MainWindow)
        self.actionCopy_to_Clipboard.setObjectName("actionCopy_to_Clipboard")

        self.action_Find_Peaks = QtGui.QAction(MainWindow)
        self.action_Find_Peaks.setObjectName("action_Find_Peaks")

        self.actionSave_Peaks_to_CSV = QtGui.QAction(MainWindow)
        self.actionSave_Peaks_to_CSV.setObjectName("actionSave_Peaks_to_CSV")

        self.actionSave_Peaks_to_Data_File = QtGui.QAction(MainWindow)
        self.actionSave_Peaks_to_Data_File.setIcon(QtGui.QIcon(":/new/prefix1/icons/filesave2.png"))
        self.actionSave_Peaks_to_Data_File.setObjectName("actionSave_Peaks_to_Data_File")

        self.actionSave_2D_Peaks_to_CSV = QtGui.QAction(MainWindow)
        self.actionSave_2D_Peaks_to_CSV.setObjectName("actionSave_2D_Peaks_to_CSV")

        self.actionToggle_Peak_Cross_Hairs = QtGui.QAction(MainWindow)
        self.actionToggle_Peak_Cross_Hairs.setObjectName("actionToggle_Peak_Cross_Hairs")

        self.actionDensity_Based_Clustering = QtGui.QAction(MainWindow)
        self.actionDensity_Based_Clustering.setObjectName("actionDensity_Based_Clustering")

        self.actionHierarchical_Method = QtGui.QAction(MainWindow)
        self.actionHierarchical_Method.setObjectName("actionHierarchical_Method")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setIcon(QtGui.QIcon(":/new/prefix1/icons/exitsmall.png"))
        self.actionExit.setObjectName("actionExit")
        self.menuTools.addAction(self.actionCursor_A)
        self.menuTools.addAction(self.actionCursor_B)
        self.menuTools.addAction(self.actionClear_Cursors)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionLabel_Peak)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionCopy_to_Clipboard)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.actionExit)
        self.menu_Peak_Tools.addAction(self.action_Find_Peaks)
        self.menu_Peak_Tools.addAction(self.actionSave_Peaks_to_CSV)
        self.menu_Peak_Tools.addAction(self.actionSave_Peaks_to_Data_File)
        self.menu_Peak_Tools.addAction(self.actionSave_2D_Peaks_to_CSV)
        self.menu_Peak_Tools.addAction(self.actionToggle_Peak_Cross_Hairs)
        self.menuCluster_Peaks.addAction(self.actionDensity_Based_Clustering)
        self.menuCluster_Peaks.addAction(self.actionHierarchical_Method)
        self.menuC_luster.addAction(self.menuCluster_Peaks.menuAction())
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Peak_Tools.menuAction())
        self.menubar.addAction(self.menuC_luster.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.actionSave_Peaks_to_Data_File)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QObject.connect(self.indexHSlider,QtCore.SIGNAL("valueChanged(int)"),self.indexSpinBox.setValue)
        QtCore.QObject.connect(self.indexSpinBox,QtCore.SIGNAL("valueChanged(int)"),self.indexHSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GeeCee", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Data Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Data Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("MainWindow", "SIC m/z:", None, QtGui.QApplication.UnicodeUTF8))
        self.sicGO_Btn.setText(QtGui.QApplication.translate("MainWindow", "GO", None, QtGui.QApplication.UnicodeUTF8))
        self.addFileBtn.setText(QtGui.QApplication.translate("MainWindow", "Add Experiment", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Spectra", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setRowCount(7)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(7)
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "Peak Table", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "dx:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "dy:", None, QtGui.QApplication.UnicodeUTF8))
        self.cursACB.setText(QtGui.QApplication.translate("MainWindow", "Cursor A", None, QtGui.QApplication.UnicodeUTF8))
        self.cursBCB.setText(QtGui.QApplication.translate("MainWindow", "Cursor B", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.plotPkListCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "SIC m/z", None, QtGui.QApplication.UnicodeUTF8))
        self.pltSICBtn.setText(QtGui.QApplication.translate("MainWindow", "Plot SIC", None, QtGui.QApplication.UnicodeUTF8))
        self.plotTICBtn.setText(QtGui.QApplication.translate("MainWindow", "Plot TIC", None, QtGui.QApplication.UnicodeUTF8))
        self.plotBPCBtn.setText(QtGui.QApplication.translate("MainWindow", "Plot BPC", None, QtGui.QApplication.UnicodeUTF8))
        self.dendroCB.setText(QtGui.QApplication.translate("MainWindow", "Show Peak Clustering Dendrogram", None, QtGui.QApplication.UnicodeUTF8))
        self.topHatCB.setText(QtGui.QApplication.translate("MainWindow", "Use TopHat Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.plotLegendCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("MainWindow", "Chromatogram Peak Style:", None, QtGui.QApplication.UnicodeUTF8))
        self.loadDirBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("MainWindow", "Length of Current Spectrum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("MainWindow", "Number of Spectrum Segments:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "Minimum Signal-to-Noise:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("MainWindow", "Slope Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "Smoothing Kernel Length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("MainWindow", "Approximate Peak Width (in points):", None, QtGui.QApplication.UnicodeUTF8))
        self.showPickedPeaksCB.setText(QtGui.QApplication.translate("MainWindow", "Show Picked Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.fndPeaksBtn.setText(QtGui.QApplication.translate("MainWindow", "Find Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.savePickedPeakBtn.setText(QtGui.QApplication.translate("MainWindow", "Save Picked Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.distanceLabel.setText(QtGui.QApplication.translate("MainWindow", "Distance Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.calcThreshCB.setText(QtGui.QApplication.translate("MainWindow", "Determine Distance Threshold by\n"
        " Cluster Tree Inconsistencies", None, QtGui.QApplication.UnicodeUTF8))
        self.distCalMethLbl.setText(QtGui.QApplication.translate("MainWindow", "Distance Calculation Method:", None, QtGui.QApplication.UnicodeUTF8))
        self.clustTypeLbl.setText(QtGui.QApplication.translate("MainWindow", "Clustering Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.showDendroCB.setText(QtGui.QApplication.translate("MainWindow", "Show Clustered Dendrogram", None, QtGui.QApplication.UnicodeUTF8))
        self.dbScanCB.setText(QtGui.QApplication.translate("MainWindow", "Use DBSCAN Clustering", None, QtGui.QApplication.UnicodeUTF8))
        self.dbAutoCalcCB.setText(QtGui.QApplication.translate("MainWindow", "Auto-Calculate Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.denDistLbl.setText(QtGui.QApplication.translate("MainWindow", "Density Distance Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.denGrpNum.setText(QtGui.QApplication.translate("MainWindow", "Minimum Number in a Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.denGrpNumThresh.setToolTip(QtGui.QApplication.translate("MainWindow", "Sets the minimum number of peaks in a group \n"
        "for the first pass of clustering.", None, QtGui.QApplication.UnicodeUTF8))
        self.clusterBtn.setText(QtGui.QApplication.translate("MainWindow", "Cluster Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QtGui.QApplication.translate("MainWindow", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.tabPeakTable.clear()
        self.tabPeakTable.setColumnCount(0)
        self.tabPeakTable.setRowCount(0)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Raw Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.tabPeakTable_2.clear()
        self.tabPeakTable_2.setColumnCount(0)
        self.tabPeakTable_2.setRowCount(0)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Clustered Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pkListTab), QtGui.QApplication.translate("MainWindow", "Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("MainWindow", "Data Folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("MainWindow", "Files in Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("MainWindow", "Master File:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("MainWindow", "Files to Align:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Add File(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove File(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("MainWindow", "Alignment Information:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Select Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Alignment", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "&ChromTools", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Peak_Tools.setTitle(QtGui.QApplication.translate("MainWindow", "&Peak Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuC_luster.setTitle(QtGui.QApplication.translate("MainWindow", "C&luster", None, QtGui.QApplication.UnicodeUTF8))
        self.menuCluster_Peaks.setTitle(QtGui.QApplication.translate("MainWindow", "Cluster Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCursor_A.setText(QtGui.QApplication.translate("MainWindow", "Cursor A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCursor_B.setText(QtGui.QApplication.translate("MainWindow", "Cursor B", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Cursors.setText(QtGui.QApplication.translate("MainWindow", "Clear Cursors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLabel_Peak.setText(QtGui.QApplication.translate("MainWindow", "Label Peak", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy_to_Clipboard.setText(QtGui.QApplication.translate("MainWindow", "Copy to Clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Peaks.setText(QtGui.QApplication.translate("MainWindow", "&Find Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Peaks.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Peaks_to_CSV.setText(QtGui.QApplication.translate("MainWindow", "Save Peaks to CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Peaks_to_Data_File.setText(QtGui.QApplication.translate("MainWindow", "Save Peaks to Data File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_2D_Peaks_to_CSV.setText(QtGui.QApplication.translate("MainWindow", "Save 2D Peaks to CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToggle_Peak_Cross_Hairs.setText(QtGui.QApplication.translate("MainWindow", "Toggle Peak Cross Hairs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDensity_Based_Clustering.setText(QtGui.QApplication.translate("MainWindow", "Density Based Method", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDensity_Based_Clustering.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHierarchical_Method.setText(QtGui.QApplication.translate("MainWindow", "Hierarchical Method", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHierarchical_Method.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+H, Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

from mpl_chrom_widget import MPL_Chrom_Widget
from mpl_image_widget import MPL_Image_Widget
from customTable import CustomTable
import icons_rc
