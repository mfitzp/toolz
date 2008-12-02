# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\GCAlign\iterate.ui'
#
# Created: Mon Dec 01 15:27:29 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,812,710).size()).expandedTo(MainWindow.minimumSizeHint()))
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

        self.label_2 = QtGui.QLabel(self.plotTab)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.specNameEdit = QtGui.QLineEdit(self.plotTab)
        self.specNameEdit.setReadOnly(True)
        self.specNameEdit.setObjectName("specNameEdit")
        self.hboxlayout2.addWidget(self.specNameEdit)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.splitter_2 = QtGui.QSplitter(self.plotTab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(16,16))
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

        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.addFileBtn = QtGui.QPushButton(self.layoutWidget)
        self.addFileBtn.setMaximumSize(QtCore.QSize(100,16777215))
        self.addFileBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.addFileBtn.setObjectName("addFileBtn")
        self.vboxlayout1.addWidget(self.addFileBtn)

        self.listWidget = QtGui.QListWidget(self.layoutWidget)

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
        self.vboxlayout1.addWidget(self.listWidget)

        self.tableWidget = QtGui.QTableWidget(self.layoutWidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(200,16777215))
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setObjectName("tableWidget")
        self.vboxlayout1.addWidget(self.tableWidget)
        self.vboxlayout.addWidget(self.splitter_2)

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
        self.plotPkListCB.setObjectName("plotPkListCB")
        self.gridlayout2.addWidget(self.plotPkListCB,0,0,1,1)

        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setObjectName("gridlayout3")

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setHorizontalSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_3 = QtGui.QLabel(self.optionsTab)
        self.label_3.setMaximumSize(QtCore.QSize(50,16777215))
        self.label_3.setObjectName("label_3")
        self.gridlayout4.addWidget(self.label_3,0,0,1,1)

        self.sicMZSB = QtGui.QSpinBox(self.optionsTab)
        self.sicMZSB.setMaximumSize(QtCore.QSize(75,16777215))
        self.sicMZSB.setMinimum(1)
        self.sicMZSB.setMaximum(400)
        self.sicMZSB.setObjectName("sicMZSB")
        self.gridlayout4.addWidget(self.sicMZSB,0,1,1,1)
        self.gridlayout3.addLayout(self.gridlayout4,0,0,1,1)

        self.pltSICBtn = QtGui.QPushButton(self.optionsTab)
        self.pltSICBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.pltSICBtn.setObjectName("pltSICBtn")
        self.gridlayout3.addWidget(self.pltSICBtn,1,0,1,1)

        self.plotTICBtn = QtGui.QPushButton(self.optionsTab)
        self.plotTICBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.plotTICBtn.setObjectName("plotTICBtn")
        self.gridlayout3.addWidget(self.plotTICBtn,2,0,1,1)

        self.plotBPCBtn = QtGui.QPushButton(self.optionsTab)
        self.plotBPCBtn.setMaximumSize(QtCore.QSize(75,16777215))
        self.plotBPCBtn.setObjectName("plotBPCBtn")
        self.gridlayout3.addWidget(self.plotBPCBtn,3,0,1,1)
        self.gridlayout2.addLayout(self.gridlayout3,0,2,2,1)

        self.dendroCB = QtGui.QCheckBox(self.optionsTab)
        self.dendroCB.setObjectName("dendroCB")
        self.gridlayout2.addWidget(self.dendroCB,1,0,1,2)

        self.topHatCB = QtGui.QCheckBox(self.optionsTab)
        self.topHatCB.setObjectName("topHatCB")
        self.gridlayout2.addWidget(self.topHatCB,2,0,1,1)

        self.plotLegendCB = QtGui.QCheckBox(self.optionsTab)
        self.plotLegendCB.setChecked(True)
        self.plotLegendCB.setObjectName("plotLegendCB")
        self.gridlayout2.addWidget(self.plotLegendCB,2,1,1,2)
        self.gridlayout1.addLayout(self.gridlayout2,0,0,1,1)

        self.loadDirBtn = QtGui.QPushButton(self.optionsTab)
        self.loadDirBtn.setObjectName("loadDirBtn")
        self.gridlayout1.addWidget(self.loadDirBtn,0,1,1,1)

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setObjectName("gridlayout5")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_20 = QtGui.QLabel(self.optionsTab)
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.hboxlayout3.addWidget(self.label_20)

        self.specLengthSB = QtGui.QSpinBox(self.optionsTab)
        self.specLengthSB.setReadOnly(True)
        self.specLengthSB.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.specLengthSB.setMaximum(1000000)
        self.specLengthSB.setProperty("value",QtCore.QVariant(250000))
        self.specLengthSB.setObjectName("specLengthSB")
        self.hboxlayout3.addWidget(self.specLengthSB)
        self.gridlayout5.addLayout(self.hboxlayout3,0,0,1,1)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_19 = QtGui.QLabel(self.optionsTab)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.hboxlayout4.addWidget(self.label_19)

        self.numSegsSB = QtGui.QSpinBox(self.optionsTab)
        self.numSegsSB.setMaximum(1000000)
        self.numSegsSB.setProperty("value",QtCore.QVariant(500))
        self.numSegsSB.setObjectName("numSegsSB")
        self.hboxlayout4.addWidget(self.numSegsSB)
        self.gridlayout5.addLayout(self.hboxlayout4,1,0,1,1)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.label_14 = QtGui.QLabel(self.optionsTab)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.hboxlayout5.addWidget(self.label_14)

        self.minSNRSB = QtGui.QSpinBox(self.optionsTab)
        self.minSNRSB.setMinimum(2)
        self.minSNRSB.setMaximum(250000)
        self.minSNRSB.setProperty("value",QtCore.QVariant(3))
        self.minSNRSB.setObjectName("minSNRSB")
        self.hboxlayout5.addWidget(self.minSNRSB)
        self.gridlayout5.addLayout(self.hboxlayout5,2,0,1,1)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.label_15 = QtGui.QLabel(self.optionsTab)
        self.label_15.setEnabled(False)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.hboxlayout6.addWidget(self.label_15)

        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.optionsTab)
        self.doubleSpinBox_2.setEnabled(False)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.hboxlayout6.addWidget(self.doubleSpinBox_2)
        self.gridlayout5.addLayout(self.hboxlayout6,3,0,1,1)

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.label_17 = QtGui.QLabel(self.optionsTab)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.hboxlayout7.addWidget(self.label_17)

        self.smthKernSB = QtGui.QSpinBox(self.optionsTab)
        self.smthKernSB.setProperty("value",QtCore.QVariant(15))
        self.smthKernSB.setObjectName("smthKernSB")
        self.hboxlayout7.addWidget(self.smthKernSB)
        self.gridlayout5.addLayout(self.hboxlayout7,4,0,1,1)

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.label_18 = QtGui.QLabel(self.optionsTab)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.hboxlayout8.addWidget(self.label_18)

        self.peakWidthSB = QtGui.QSpinBox(self.optionsTab)
        self.peakWidthSB.setMinimum(3)
        self.peakWidthSB.setMaximum(200000)
        self.peakWidthSB.setProperty("value",QtCore.QVariant(25))
        self.peakWidthSB.setObjectName("peakWidthSB")
        self.hboxlayout8.addWidget(self.peakWidthSB)
        self.gridlayout5.addLayout(self.hboxlayout8,5,0,1,1)

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.showPickedPeaksCB = QtGui.QCheckBox(self.optionsTab)
        self.showPickedPeaksCB.setChecked(True)
        self.showPickedPeaksCB.setObjectName("showPickedPeaksCB")
        self.hboxlayout9.addWidget(self.showPickedPeaksCB)

        self.fndPeaksBtn = QtGui.QPushButton(self.optionsTab)
        self.fndPeaksBtn.setObjectName("fndPeaksBtn")
        self.hboxlayout9.addWidget(self.fndPeaksBtn)
        self.gridlayout5.addLayout(self.hboxlayout9,6,0,1,1)

        self.savePickedPeakBtn = QtGui.QPushButton(self.optionsTab)
        self.savePickedPeakBtn.setObjectName("savePickedPeakBtn")
        self.gridlayout5.addWidget(self.savePickedPeakBtn,7,0,1,1)
        self.gridlayout1.addLayout(self.gridlayout5,1,0,1,1)

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setObjectName("gridlayout6")

        self.plotClusterPeakCB = QtGui.QCheckBox(self.optionsTab)
        self.plotClusterPeakCB.setObjectName("plotClusterPeakCB")
        self.gridlayout6.addWidget(self.plotClusterPeakCB,0,0,1,1)

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_16 = QtGui.QLabel(self.optionsTab)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.hboxlayout10.addWidget(self.label_16)

        self.distMethodCB = QtGui.QComboBox(self.optionsTab)
        self.distMethodCB.setObjectName("distMethodCB")
        self.hboxlayout10.addWidget(self.distMethodCB)
        self.gridlayout6.addLayout(self.hboxlayout10,1,0,1,1)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.label_21 = QtGui.QLabel(self.optionsTab)
        self.label_21.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.hboxlayout11.addWidget(self.label_21)

        self.clusterTypeCB = QtGui.QComboBox(self.optionsTab)
        self.clusterTypeCB.setObjectName("clusterTypeCB")
        self.hboxlayout11.addWidget(self.clusterTypeCB)
        self.gridlayout6.addLayout(self.hboxlayout11,2,0,1,1)

        self.showDendroCB = QtGui.QCheckBox(self.optionsTab)
        self.showDendroCB.setChecked(True)
        self.showDendroCB.setObjectName("showDendroCB")
        self.gridlayout6.addWidget(self.showDendroCB,3,0,1,1)

        self.clusterBtn = QtGui.QPushButton(self.optionsTab)
        self.clusterBtn.setObjectName("clusterBtn")
        self.gridlayout6.addWidget(self.clusterBtn,4,0,1,1)
        self.gridlayout1.addLayout(self.gridlayout6,1,1,1,1)
        self.tabWidget.addTab(self.optionsTab,"")

        self.pkListTab = QtGui.QWidget()
        self.pkListTab.setObjectName("pkListTab")

        self.hboxlayout12 = QtGui.QHBoxLayout(self.pkListTab)
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.peakTable = QtGui.QTableWidget(self.pkListTab)
        self.peakTable.setObjectName("peakTable")
        self.hboxlayout12.addWidget(self.peakTable)
        self.tabWidget.addTab(self.pkListTab,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,812,21))
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
        self.menuTools.addAction(self.actionCursor_A)
        self.menuTools.addAction(self.actionCursor_B)
        self.menuTools.addAction(self.actionClear_Cursors)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionLabel_Peak)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionCopy_to_Clipboard)
        self.menu_File.addAction(self.action_Open)
        self.menu_Peak_Tools.addAction(self.action_Find_Peaks)
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
        self.plotClusterPeakCB.setText(QtGui.QApplication.translate("MainWindow", "Show Clustered Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("MainWindow", "Distance Calculation Method:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("MainWindow", "Clustering Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.showDendroCB.setText(QtGui.QApplication.translate("MainWindow", "Show Clutered Dendrogram", None, QtGui.QApplication.UnicodeUTF8))
        self.clusterBtn.setText(QtGui.QApplication.translate("MainWindow", "Cluster Peaks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.peakTable.setRowCount(50)
        self.peakTable.setColumnCount(4)
        self.peakTable.clear()
        self.peakTable.setColumnCount(4)
        self.peakTable.setRowCount(50)
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

from mpl_image_widget import MPL_Image_Widget
from mpl_chrom_widget import MPL_Chrom_Widget
import icons_rc
