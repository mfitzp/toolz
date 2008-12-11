# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\GCAlign\iterate.ui'
#
# Created: Thu Dec 11 14:46:04 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,793,674).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon(":/new/prefix1/Retro Mario World_32.png"))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.plotTab = QtGui.QWidget()
        self.plotTab.setObjectName("plotTab")

        self.gridlayout = QtGui.QGridLayout(self.plotTab)
        self.gridlayout.setObjectName("gridlayout")

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
        self.gridlayout.addLayout(self.hboxlayout1,0,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_2 = QtGui.QLabel(self.plotTab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.specNameEdit = QtGui.QLineEdit(self.plotTab)
        self.specNameEdit.setReadOnly(True)
        self.specNameEdit.setObjectName("specNameEdit")
        self.hboxlayout2.addWidget(self.specNameEdit)
        self.gridlayout.addLayout(self.hboxlayout2,1,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.splitter = QtGui.QSplitter(self.plotTab)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.plotWidget = MPL_Image_Widget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setMinimumSize(QtCore.QSize(500,250))
        self.plotWidget.setObjectName("plotWidget")

        self.plotWidget2 = MPL_Chrom_Widget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget2.sizePolicy().hasHeightForWidth())
        self.plotWidget2.setSizePolicy(sizePolicy)
        self.plotWidget2.setMinimumSize(QtCore.QSize(500,100))
        self.plotWidget2.setObjectName("plotWidget2")
        self.hboxlayout3.addWidget(self.splitter)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.addFileBtn = QtGui.QPushButton(self.plotTab)
        self.addFileBtn.setMaximumSize(QtCore.QSize(100,16777215))
        self.addFileBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.addFileBtn.setObjectName("addFileBtn")
        self.vboxlayout.addWidget(self.addFileBtn)

        self.listWidget = QtGui.QListWidget(self.plotTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(100,0))
        self.listWidget.setMaximumSize(QtCore.QSize(200,16777215))
        self.listWidget.setBaseSize(QtCore.QSize(100,250))
        self.listWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidget.setObjectName("listWidget")
        self.vboxlayout.addWidget(self.listWidget)

        self.tableWidget = QtGui.QTableWidget(self.plotTab)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(200,16777215))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setObjectName("tableWidget")
        self.vboxlayout.addWidget(self.tableWidget)
        self.hboxlayout3.addLayout(self.vboxlayout)
        self.gridlayout.addLayout(self.hboxlayout3,2,0,1,1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setHorizontalSpacing(3)
        self.gridlayout1.setVerticalSpacing(2)
        self.gridlayout1.setObjectName("gridlayout1")

        self.cALabelLE = QtGui.QLineEdit(self.plotTab)
        self.cALabelLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cALabelLE.setFont(font)
        self.cALabelLE.setReadOnly(True)
        self.cALabelLE.setObjectName("cALabelLE")
        self.gridlayout1.addWidget(self.cALabelLE,0,3,1,1)

        self.cAIndexLE = QtGui.QLineEdit(self.plotTab)
        self.cAIndexLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cAIndexLE.setFont(font)
        self.cAIndexLE.setReadOnly(True)
        self.cAIndexLE.setObjectName("cAIndexLE")
        self.gridlayout1.addWidget(self.cAIndexLE,0,5,1,1)

        self.cA_XLE = QtGui.QLineEdit(self.plotTab)
        self.cA_XLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cA_XLE.setFont(font)
        self.cA_XLE.setReadOnly(True)
        self.cA_XLE.setObjectName("cA_XLE")
        self.gridlayout1.addWidget(self.cA_XLE,0,7,1,1)

        self.cA_YLE = QtGui.QLineEdit(self.plotTab)
        self.cA_YLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cA_YLE.setFont(font)
        self.cA_YLE.setReadOnly(True)
        self.cA_YLE.setObjectName("cA_YLE")
        self.gridlayout1.addWidget(self.cA_YLE,0,9,1,1)

        self.cBLabelLE = QtGui.QLineEdit(self.plotTab)
        self.cBLabelLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cBLabelLE.setFont(font)
        self.cBLabelLE.setReadOnly(True)
        self.cBLabelLE.setObjectName("cBLabelLE")
        self.gridlayout1.addWidget(self.cBLabelLE,1,3,1,1)

        self.cBIndexLE = QtGui.QLineEdit(self.plotTab)
        self.cBIndexLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cBIndexLE.setFont(font)
        self.cBIndexLE.setReadOnly(True)
        self.cBIndexLE.setObjectName("cBIndexLE")
        self.gridlayout1.addWidget(self.cBIndexLE,1,5,1,1)

        self.cB_XLE = QtGui.QLineEdit(self.plotTab)
        self.cB_XLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cB_XLE.setFont(font)
        self.cB_XLE.setReadOnly(True)
        self.cB_XLE.setObjectName("cB_XLE")
        self.gridlayout1.addWidget(self.cB_XLE,1,7,1,1)

        self.cB_YLE = QtGui.QLineEdit(self.plotTab)
        self.cB_YLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.cB_YLE.setFont(font)
        self.cB_YLE.setReadOnly(True)
        self.cB_YLE.setObjectName("cB_YLE")
        self.gridlayout1.addWidget(self.cB_YLE,1,9,1,1)

        self.label_4 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,0,2,1,1)

        self.label_5 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,1,2,1,1)

        self.label_6 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,0,4,1,1)

        self.label_7 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridlayout1.addWidget(self.label_7,0,6,1,1)

        self.label_8 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridlayout1.addWidget(self.label_8,0,8,1,1)

        self.label_9 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridlayout1.addWidget(self.label_9,1,4,1,1)

        self.label_10 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridlayout1.addWidget(self.label_10,1,6,1,1)

        self.label_11 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridlayout1.addWidget(self.label_11,1,8,1,1)

        self.label_12 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridlayout1.addWidget(self.label_12,0,10,1,1)

        self.label_13 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridlayout1.addWidget(self.label_13,1,10,1,1)

        self.dxLE = QtGui.QLineEdit(self.plotTab)
        self.dxLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.dxLE.setFont(font)
        self.dxLE.setReadOnly(True)
        self.dxLE.setObjectName("dxLE")
        self.gridlayout1.addWidget(self.dxLE,0,11,1,1)

        self.dyLE = QtGui.QLineEdit(self.plotTab)
        self.dyLE.setMaximumSize(QtCore.QSize(16777215,17))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.dyLE.setFont(font)
        self.dyLE.setReadOnly(True)
        self.dyLE.setObjectName("dyLE")
        self.gridlayout1.addWidget(self.dyLE,1,11,1,1)

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
        self.gridlayout1.addWidget(self.cursACB,0,0,1,1)

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
        self.gridlayout1.addWidget(self.cursBCB,1,0,1,1)
        self.gridlayout.addLayout(self.gridlayout1,3,0,1,1)
        self.tabWidget.addTab(self.plotTab,"")

        self.optionsTab = QtGui.QWidget()
        self.optionsTab.setObjectName("optionsTab")

        self.gridlayout2 = QtGui.QGridLayout(self.optionsTab)
        self.gridlayout2.setObjectName("gridlayout2")

        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setObjectName("gridlayout3")

        self.plotPkListCB = QtGui.QCheckBox(self.optionsTab)
        self.plotPkListCB.setObjectName("plotPkListCB")
        self.gridlayout3.addWidget(self.plotPkListCB,0,0,1,1)

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setObjectName("gridlayout4")

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setHorizontalSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.label_3 = QtGui.QLabel(self.optionsTab)
        self.label_3.setMaximumSize(QtCore.QSize(50,16777215))
        self.label_3.setObjectName("label_3")
        self.gridlayout5.addWidget(self.label_3,0,0,1,1)

        self.sicMZSB = QtGui.QSpinBox(self.optionsTab)
        self.sicMZSB.setMaximumSize(QtCore.QSize(75,16777215))
        self.sicMZSB.setMinimum(1)
        self.sicMZSB.setMaximum(400)
        self.sicMZSB.setObjectName("sicMZSB")
        self.gridlayout5.addWidget(self.sicMZSB,0,1,1,1)
        self.gridlayout4.addLayout(self.gridlayout5,0,0,1,1)

        self.pltSICBtn = QtGui.QPushButton(self.optionsTab)
        self.pltSICBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.pltSICBtn.setObjectName("pltSICBtn")
        self.gridlayout4.addWidget(self.pltSICBtn,1,0,1,1)

        self.plotTICBtn = QtGui.QPushButton(self.optionsTab)
        self.plotTICBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.plotTICBtn.setObjectName("plotTICBtn")
        self.gridlayout4.addWidget(self.plotTICBtn,2,0,1,1)

        self.plotBPCBtn = QtGui.QPushButton(self.optionsTab)
        self.plotBPCBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.plotBPCBtn.setObjectName("plotBPCBtn")
        self.gridlayout4.addWidget(self.plotBPCBtn,3,0,1,1)
        self.gridlayout3.addLayout(self.gridlayout4,0,2,2,1)

        self.dendroCB = QtGui.QCheckBox(self.optionsTab)
        self.dendroCB.setObjectName("dendroCB")
        self.gridlayout3.addWidget(self.dendroCB,1,0,1,2)

        self.topHatCB = QtGui.QCheckBox(self.optionsTab)
        self.topHatCB.setObjectName("topHatCB")
        self.gridlayout3.addWidget(self.topHatCB,2,0,1,1)

        self.plotLegendCB = QtGui.QCheckBox(self.optionsTab)
        self.plotLegendCB.setChecked(True)
        self.plotLegendCB.setObjectName("plotLegendCB")
        self.gridlayout3.addWidget(self.plotLegendCB,2,1,1,2)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_23 = QtGui.QLabel(self.optionsTab)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.hboxlayout4.addWidget(self.label_23)

        self.chromStyleCB = QtGui.QComboBox(self.optionsTab)
        self.chromStyleCB.setObjectName("chromStyleCB")
        self.hboxlayout4.addWidget(self.chromStyleCB)
        self.gridlayout3.addLayout(self.hboxlayout4,0,1,1,1)
        self.gridlayout2.addLayout(self.gridlayout3,0,0,1,2)

        self.loadDirBtn = QtGui.QPushButton(self.optionsTab)
        self.loadDirBtn.setObjectName("loadDirBtn")
        self.gridlayout2.addWidget(self.loadDirBtn,0,2,1,1)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setObjectName("gridlayout6")

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.label_20 = QtGui.QLabel(self.optionsTab)
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.hboxlayout5.addWidget(self.label_20)

        self.specLengthSB = QtGui.QSpinBox(self.optionsTab)
        self.specLengthSB.setReadOnly(True)
        self.specLengthSB.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.specLengthSB.setMaximum(1000000)
        self.specLengthSB.setProperty("value",QtCore.QVariant(250000))
        self.specLengthSB.setObjectName("specLengthSB")
        self.hboxlayout5.addWidget(self.specLengthSB)
        self.gridlayout6.addLayout(self.hboxlayout5,0,0,1,1)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.label_19 = QtGui.QLabel(self.optionsTab)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.hboxlayout6.addWidget(self.label_19)

        self.numSegsSB = QtGui.QSpinBox(self.optionsTab)
        self.numSegsSB.setMaximum(1000000)
        self.numSegsSB.setProperty("value",QtCore.QVariant(500))
        self.numSegsSB.setObjectName("numSegsSB")
        self.hboxlayout6.addWidget(self.numSegsSB)
        self.gridlayout6.addLayout(self.hboxlayout6,1,0,1,1)

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.label_14 = QtGui.QLabel(self.optionsTab)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.hboxlayout7.addWidget(self.label_14)

        self.minSNRSB = QtGui.QSpinBox(self.optionsTab)
        self.minSNRSB.setMinimum(2)
        self.minSNRSB.setMaximum(250000)
        self.minSNRSB.setProperty("value",QtCore.QVariant(3))
        self.minSNRSB.setObjectName("minSNRSB")
        self.hboxlayout7.addWidget(self.minSNRSB)
        self.gridlayout6.addLayout(self.hboxlayout7,2,0,1,1)

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.label_15 = QtGui.QLabel(self.optionsTab)
        self.label_15.setEnabled(False)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.hboxlayout8.addWidget(self.label_15)

        self.slopeThreshSB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.slopeThreshSB.setEnabled(False)
        self.slopeThreshSB.setObjectName("slopeThreshSB")
        self.hboxlayout8.addWidget(self.slopeThreshSB)
        self.gridlayout6.addLayout(self.hboxlayout8,3,0,1,1)

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.label_17 = QtGui.QLabel(self.optionsTab)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.hboxlayout9.addWidget(self.label_17)

        self.smthKernSB = QtGui.QSpinBox(self.optionsTab)
        self.smthKernSB.setProperty("value",QtCore.QVariant(15))
        self.smthKernSB.setObjectName("smthKernSB")
        self.hboxlayout9.addWidget(self.smthKernSB)
        self.gridlayout6.addLayout(self.hboxlayout9,4,0,1,1)

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_18 = QtGui.QLabel(self.optionsTab)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.hboxlayout10.addWidget(self.label_18)

        self.peakWidthSB = QtGui.QSpinBox(self.optionsTab)
        self.peakWidthSB.setMinimum(3)
        self.peakWidthSB.setMaximum(200000)
        self.peakWidthSB.setProperty("value",QtCore.QVariant(25))
        self.peakWidthSB.setObjectName("peakWidthSB")
        self.hboxlayout10.addWidget(self.peakWidthSB)
        self.gridlayout6.addLayout(self.hboxlayout10,5,0,1,1)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.showPickedPeaksCB = QtGui.QCheckBox(self.optionsTab)
        self.showPickedPeaksCB.setChecked(True)
        self.showPickedPeaksCB.setObjectName("showPickedPeaksCB")
        self.hboxlayout11.addWidget(self.showPickedPeaksCB)

        self.fndPeaksBtn = QtGui.QPushButton(self.optionsTab)
        self.fndPeaksBtn.setObjectName("fndPeaksBtn")
        self.hboxlayout11.addWidget(self.fndPeaksBtn)
        self.gridlayout6.addLayout(self.hboxlayout11,6,0,1,1)

        self.savePickedPeakBtn = QtGui.QPushButton(self.optionsTab)
        self.savePickedPeakBtn.setObjectName("savePickedPeakBtn")
        self.gridlayout6.addWidget(self.savePickedPeakBtn,7,0,1,1)
        self.gridlayout2.addLayout(self.gridlayout6,1,0,1,1)

        self.gridlayout7 = QtGui.QGridLayout()
        self.gridlayout7.setObjectName("gridlayout7")

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.distanceLabel = QtGui.QLabel(self.optionsTab)
        self.distanceLabel.setEnabled(False)
        self.distanceLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.distanceLabel.setObjectName("distanceLabel")
        self.hboxlayout12.addWidget(self.distanceLabel)

        self.maxDistThreshSB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.maxDistThreshSB.setEnabled(False)
        self.maxDistThreshSB.setMinimum(0.01)
        self.maxDistThreshSB.setProperty("value",QtCore.QVariant(10.0))
        self.maxDistThreshSB.setObjectName("maxDistThreshSB")
        self.hboxlayout12.addWidget(self.maxDistThreshSB)
        self.gridlayout7.addLayout(self.hboxlayout12,0,0,1,1)

        self.calcThreshCB = QtGui.QCheckBox(self.optionsTab)
        self.calcThreshCB.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.calcThreshCB.setChecked(True)
        self.calcThreshCB.setObjectName("calcThreshCB")
        self.gridlayout7.addWidget(self.calcThreshCB,1,0,1,1)

        self.hboxlayout13 = QtGui.QHBoxLayout()
        self.hboxlayout13.setObjectName("hboxlayout13")

        self.distCalMethLbl = QtGui.QLabel(self.optionsTab)
        self.distCalMethLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.distCalMethLbl.setObjectName("distCalMethLbl")
        self.hboxlayout13.addWidget(self.distCalMethLbl)

        self.distMethodCB = QtGui.QComboBox(self.optionsTab)
        self.distMethodCB.setObjectName("distMethodCB")
        self.hboxlayout13.addWidget(self.distMethodCB)
        self.gridlayout7.addLayout(self.hboxlayout13,2,0,1,1)

        self.hboxlayout14 = QtGui.QHBoxLayout()
        self.hboxlayout14.setObjectName("hboxlayout14")

        self.clustTypeLbl = QtGui.QLabel(self.optionsTab)
        self.clustTypeLbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.clustTypeLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.clustTypeLbl.setObjectName("clustTypeLbl")
        self.hboxlayout14.addWidget(self.clustTypeLbl)

        self.clusterTypeCB = QtGui.QComboBox(self.optionsTab)
        self.clusterTypeCB.setObjectName("clusterTypeCB")
        self.hboxlayout14.addWidget(self.clusterTypeCB)
        self.gridlayout7.addLayout(self.hboxlayout14,3,0,1,1)

        self.showDendroCB = QtGui.QCheckBox(self.optionsTab)
        self.showDendroCB.setChecked(True)
        self.showDendroCB.setObjectName("showDendroCB")
        self.gridlayout7.addWidget(self.showDendroCB,4,0,1,1)

        self.hboxlayout15 = QtGui.QHBoxLayout()
        self.hboxlayout15.setObjectName("hboxlayout15")

        self.dbScanCB = QtGui.QCheckBox(self.optionsTab)
        self.dbScanCB.setObjectName("dbScanCB")
        self.hboxlayout15.addWidget(self.dbScanCB)

        self.dbAutoCalcCB = QtGui.QCheckBox(self.optionsTab)
        self.dbAutoCalcCB.setEnabled(False)
        self.dbAutoCalcCB.setChecked(True)
        self.dbAutoCalcCB.setObjectName("dbAutoCalcCB")
        self.hboxlayout15.addWidget(self.dbAutoCalcCB)

        self.hboxlayout16 = QtGui.QHBoxLayout()
        self.hboxlayout16.setObjectName("hboxlayout16")

        self.denDistLbl = QtGui.QLabel(self.optionsTab)
        self.denDistLbl.setEnabled(False)
        self.denDistLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.denDistLbl.setObjectName("denDistLbl")
        self.hboxlayout16.addWidget(self.denDistLbl)

        self.densityDistThreshSB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.densityDistThreshSB.setEnabled(False)
        self.densityDistThreshSB.setMinimum(0.01)
        self.densityDistThreshSB.setProperty("value",QtCore.QVariant(10.0))
        self.densityDistThreshSB.setObjectName("densityDistThreshSB")
        self.hboxlayout16.addWidget(self.densityDistThreshSB)
        self.hboxlayout15.addLayout(self.hboxlayout16)
        self.gridlayout7.addLayout(self.hboxlayout15,5,0,1,1)

        self.clusterBtn = QtGui.QPushButton(self.optionsTab)
        self.clusterBtn.setObjectName("clusterBtn")
        self.gridlayout7.addWidget(self.clusterBtn,6,0,1,1)
        self.gridlayout2.addLayout(self.gridlayout7,1,1,1,2)
        self.tabWidget.addTab(self.optionsTab,"")

        self.pkListTab = QtGui.QWidget()
        self.pkListTab.setObjectName("pkListTab")

        self.hboxlayout17 = QtGui.QHBoxLayout(self.pkListTab)
        self.hboxlayout17.setObjectName("hboxlayout17")

        self.tabPeakTable = CustomTable(self.pkListTab)
        self.tabPeakTable.setObjectName("tabPeakTable")
        self.hboxlayout17.addWidget(self.tabPeakTable)
        self.tabWidget.addTab(self.pkListTab,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,793,21))
        self.menubar.setObjectName("menubar")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menu_Peak_Tools = QtGui.QMenu(self.menubar)
        self.menu_Peak_Tools.setObjectName("menu_Peak_Tools")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_Open = QtGui.QAction(MainWindow)
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
        self.actionSave_Peaks_to_Data_File.setObjectName("actionSave_Peaks_to_Data_File")

        self.actionSave_Raw_Peaks_to_CSV = QtGui.QAction(MainWindow)
        self.actionSave_Raw_Peaks_to_CSV.setObjectName("actionSave_Raw_Peaks_to_CSV")
        self.menuTools.addAction(self.actionCursor_A)
        self.menuTools.addAction(self.actionCursor_B)
        self.menuTools.addAction(self.actionClear_Cursors)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionLabel_Peak)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionCopy_to_Clipboard)
        self.menu_File.addAction(self.action_Open)
        self.menu_Peak_Tools.addAction(self.action_Find_Peaks)
        self.menu_Peak_Tools.addAction(self.actionSave_Peaks_to_CSV)
        self.menu_Peak_Tools.addAction(self.actionSave_Peaks_to_Data_File)
        self.menu_Peak_Tools.addAction(self.actionSave_Raw_Peaks_to_CSV)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Peak_Tools.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.indexHSlider,QtCore.SIGNAL("valueChanged(int)"),self.indexSpinBox.setValue)
        QtCore.QObject.connect(self.indexSpinBox,QtCore.SIGNAL("valueChanged(int)"),self.indexHSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "GeeCee", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Data Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Data Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.addFileBtn.setText(QtGui.QApplication.translate("MainWindow", "Add Experiment", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setRowCount(7)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(7)
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
        self.clusterBtn.setText(QtGui.QApplication.translate("MainWindow", "Cluster Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.tabPeakTable.clear()
        self.tabPeakTable.setColumnCount(0)
        self.tabPeakTable.setRowCount(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pkListTab), QtGui.QApplication.translate("MainWindow", "Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "&ChromTools", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Peak_Tools.setTitle(QtGui.QApplication.translate("MainWindow", "&Peak Tools", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionSave_Raw_Peaks_to_CSV.setText(QtGui.QApplication.translate("MainWindow", "Save Raw Peaks to CSV", None, QtGui.QApplication.UnicodeUTF8))

from mpl_chrom_widget import MPL_Chrom_Widget
from mpl_image_widget import MPL_Image_Widget
from customTable import CustomTable
import icons_rc
