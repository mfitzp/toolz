# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\SimpleView\main.ui'
#
# Created: Tue Feb 10 11:56:44 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,831,731).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon(":/new/prefix1/Retro Mario World_32.png"))

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

        self.splitter = QtGui.QSplitter(self.plotTab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.indexHSlider = QtGui.QSlider(self.layoutWidget)
        self.indexHSlider.setOrientation(QtCore.Qt.Horizontal)
        self.indexHSlider.setObjectName("indexHSlider")
        self.hboxlayout1.addWidget(self.indexHSlider)

        self.indexSpinBox = QtGui.QSpinBox(self.layoutWidget)
        self.indexSpinBox.setObjectName("indexSpinBox")
        self.hboxlayout1.addWidget(self.indexSpinBox)
        self.vboxlayout1.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.specNameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.specNameEdit.setReadOnly(True)
        self.specNameEdit.setObjectName("specNameEdit")
        self.hboxlayout2.addWidget(self.specNameEdit)
        self.vboxlayout1.addLayout(self.hboxlayout2)

        self.plotWidget = MPL_Widget(self.layoutWidget)
        self.plotWidget.setObjectName("plotWidget")
        self.vboxlayout1.addWidget(self.plotWidget)

        self.specListWidget = QtGui.QListWidget(self.splitter)
        self.specListWidget.setMaximumSize(QtCore.QSize(200,16777215))
        self.specListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.specListWidget.setObjectName("specListWidget")
        self.vboxlayout.addWidget(self.splitter)

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

        self.label_3 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,0,2,1,1)

        self.label_4 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,1,2,1,1)

        self.label_5 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,0,4,1,1)

        self.label_6 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,0,6,1,1)

        self.label_7 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,0,8,1,1)

        self.label_8 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8,1,4,1,1)

        self.label_9 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridlayout.addWidget(self.label_9,1,6,1,1)

        self.label_10 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridlayout.addWidget(self.label_10,1,8,1,1)

        self.label_11 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridlayout.addWidget(self.label_11,0,10,1,1)

        self.label_12 = QtGui.QLabel(self.plotTab)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridlayout.addWidget(self.label_12,1,10,1,1)

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

        self.hboxlayout3 = QtGui.QHBoxLayout(self.optionsTab)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,1,0,1,1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")

        self.loadmzXMLCB = QtGui.QCheckBox(self.optionsTab)
        self.loadmzXMLCB.setChecked(True)
        self.loadmzXMLCB.setObjectName("loadmzXMLCB")
        self.gridlayout2.addWidget(self.loadmzXMLCB,0,0,1,1)

        self.plotPkListCB = QtGui.QCheckBox(self.optionsTab)
        self.plotPkListCB.setObjectName("plotPkListCB")
        self.gridlayout2.addWidget(self.plotPkListCB,0,1,1,1)

        self.plotLegendCB = QtGui.QCheckBox(self.optionsTab)
        self.plotLegendCB.setChecked(True)
        self.plotLegendCB.setObjectName("plotLegendCB")
        self.gridlayout2.addWidget(self.plotLegendCB,1,0,1,1)

        self.excludeLIFTCB = QtGui.QCheckBox(self.optionsTab)
        self.excludeLIFTCB.setObjectName("excludeLIFTCB")
        self.gridlayout2.addWidget(self.excludeLIFTCB,2,0,1,1)

        self.invertCompCB = QtGui.QCheckBox(self.optionsTab)
        self.invertCompCB.setChecked(True)
        self.invertCompCB.setObjectName("invertCompCB")
        self.gridlayout2.addWidget(self.invertCompCB,2,1,1,1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_13 = QtGui.QLabel(self.optionsTab)
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.hboxlayout4.addWidget(self.label_13)

        self.mzLo_SB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.mzLo_SB.setDecimals(3)
        self.mzLo_SB.setMinimum(1.0)
        self.mzLo_SB.setMaximum(100000.0)
        self.mzLo_SB.setSingleStep(0.05)
        self.mzLo_SB.setProperty("value",QtCore.QVariant(1295.0))
        self.mzLo_SB.setObjectName("mzLo_SB")
        self.hboxlayout4.addWidget(self.mzLo_SB)
        self.vboxlayout2.addLayout(self.hboxlayout4)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.label_14 = QtGui.QLabel(self.optionsTab)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.hboxlayout5.addWidget(self.label_14)

        self.mzHi_SB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.mzHi_SB.setDecimals(3)
        self.mzHi_SB.setMinimum(-1.0)
        self.mzHi_SB.setMaximum(100000.0)
        self.mzHi_SB.setSingleStep(0.05)
        self.mzHi_SB.setProperty("value",QtCore.QVariant(1297.0))
        self.mzHi_SB.setObjectName("mzHi_SB")
        self.hboxlayout5.addWidget(self.mzHi_SB)
        self.vboxlayout2.addLayout(self.hboxlayout5)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.getEIC_Btn = QtGui.QPushButton(self.optionsTab)
        self.getEIC_Btn.setObjectName("getEIC_Btn")
        self.hboxlayout6.addWidget(self.getEIC_Btn)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout6.addItem(spacerItem1)
        self.vboxlayout2.addLayout(self.hboxlayout6)
        self.gridlayout2.addLayout(self.vboxlayout2,3,1,1,1)

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.loadDirBtn = QtGui.QPushButton(self.optionsTab)
        self.loadDirBtn.setObjectName("loadDirBtn")
        self.hboxlayout7.addWidget(self.loadDirBtn)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout7.addItem(spacerItem2)
        self.gridlayout2.addLayout(self.hboxlayout7,1,1,1,1)
        self.gridlayout1.addLayout(self.gridlayout2,0,0,1,1)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.label_17 = QtGui.QLabel(self.optionsTab)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.hboxlayout8.addWidget(self.label_17)

        self.comboBox = QtGui.QComboBox(self.optionsTab)
        self.comboBox.setEnabled(False)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout8.addWidget(self.comboBox)
        self.vboxlayout3.addLayout(self.hboxlayout8)

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.label_21 = QtGui.QLabel(self.optionsTab)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.hboxlayout9.addWidget(self.label_21)

        self.minRow_SB = QtGui.QSpinBox(self.optionsTab)
        self.minRow_SB.setMinimum(1)
        self.minRow_SB.setMaximum(100)
        self.minRow_SB.setProperty("value",QtCore.QVariant(1))
        self.minRow_SB.setObjectName("minRow_SB")
        self.hboxlayout9.addWidget(self.minRow_SB)
        self.vboxlayout3.addLayout(self.hboxlayout9)

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_22 = QtGui.QLabel(self.optionsTab)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.hboxlayout10.addWidget(self.label_22)

        self.minClust_SB = QtGui.QSpinBox(self.optionsTab)
        self.minClust_SB.setMinimum(1)
        self.minClust_SB.setMaximum(100)
        self.minClust_SB.setProperty("value",QtCore.QVariant(4))
        self.minClust_SB.setObjectName("minClust_SB")
        self.hboxlayout10.addWidget(self.minClust_SB)
        self.vboxlayout3.addLayout(self.hboxlayout10)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setObjectName("hboxlayout11")

        self.label_23 = QtGui.QLabel(self.optionsTab)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.hboxlayout11.addWidget(self.label_23)

        self.dbscanEPS_SB = QtGui.QSpinBox(self.optionsTab)
        self.dbscanEPS_SB.setMinimum(-1)
        self.dbscanEPS_SB.setMaximum(1000)
        self.dbscanEPS_SB.setProperty("value",QtCore.QVariant(-1))
        self.dbscanEPS_SB.setObjectName("dbscanEPS_SB")
        self.hboxlayout11.addWidget(self.dbscanEPS_SB)
        self.vboxlayout3.addLayout(self.hboxlayout11)

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setObjectName("hboxlayout12")

        self.label_15 = QtGui.QLabel(self.optionsTab)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.hboxlayout12.addWidget(self.label_15)

        self.noiseFactor_SB = QtGui.QSpinBox(self.optionsTab)
        self.noiseFactor_SB.setMinimum(1)
        self.noiseFactor_SB.setMaximum(100)
        self.noiseFactor_SB.setProperty("value",QtCore.QVariant(10))
        self.noiseFactor_SB.setObjectName("noiseFactor_SB")
        self.hboxlayout12.addWidget(self.noiseFactor_SB)
        self.vboxlayout3.addLayout(self.hboxlayout12)

        self.hboxlayout13 = QtGui.QHBoxLayout()
        self.hboxlayout13.setObjectName("hboxlayout13")

        self.label_16 = QtGui.QLabel(self.optionsTab)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.hboxlayout13.addWidget(self.label_16)

        self.snrNoiseEst_SB = QtGui.QDoubleSpinBox(self.optionsTab)
        self.snrNoiseEst_SB.setDecimals(1)
        self.snrNoiseEst_SB.setMinimum(1.0)
        self.snrNoiseEst_SB.setMaximum(5000.0)
        self.snrNoiseEst_SB.setProperty("value",QtCore.QVariant(3.0))
        self.snrNoiseEst_SB.setObjectName("snrNoiseEst_SB")
        self.hboxlayout13.addWidget(self.snrNoiseEst_SB)
        self.vboxlayout3.addLayout(self.hboxlayout13)

        self.plotNoiseEst_CB = QtGui.QCheckBox(self.optionsTab)
        self.plotNoiseEst_CB.setChecked(False)
        self.plotNoiseEst_CB.setObjectName("plotNoiseEst_CB")
        self.vboxlayout3.addWidget(self.plotNoiseEst_CB)

        self.hboxlayout14 = QtGui.QHBoxLayout()
        self.hboxlayout14.setObjectName("hboxlayout14")

        self.showNoise_Btn = QtGui.QPushButton(self.optionsTab)
        self.showNoise_Btn.setObjectName("showNoise_Btn")
        self.hboxlayout14.addWidget(self.showNoise_Btn)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout14.addItem(spacerItem3)
        self.vboxlayout3.addLayout(self.hboxlayout14)

        spacerItem4 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout3.addItem(spacerItem4)
        self.gridlayout1.addLayout(self.vboxlayout3,2,0,1,1)

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.useDefaultScale_CB = QtGui.QCheckBox(self.optionsTab)
        self.useDefaultScale_CB.setChecked(False)
        self.useDefaultScale_CB.setObjectName("useDefaultScale_CB")
        self.vboxlayout4.addWidget(self.useDefaultScale_CB)

        self.hboxlayout15 = QtGui.QHBoxLayout()
        self.hboxlayout15.setObjectName("hboxlayout15")

        self.scaleStartLbl = QtGui.QLabel(self.optionsTab)
        self.scaleStartLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scaleStartLbl.setObjectName("scaleStartLbl")
        self.hboxlayout15.addWidget(self.scaleStartLbl)

        self.scaleStart_SB = QtGui.QSpinBox(self.optionsTab)
        self.scaleStart_SB.setMinimum(1)
        self.scaleStart_SB.setMaximum(10000)
        self.scaleStart_SB.setProperty("value",QtCore.QVariant(2))
        self.scaleStart_SB.setObjectName("scaleStart_SB")
        self.hboxlayout15.addWidget(self.scaleStart_SB)
        self.vboxlayout4.addLayout(self.hboxlayout15)

        self.hboxlayout16 = QtGui.QHBoxLayout()
        self.hboxlayout16.setObjectName("hboxlayout16")

        self.scaleEndLbl = QtGui.QLabel(self.optionsTab)
        self.scaleEndLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scaleEndLbl.setObjectName("scaleEndLbl")
        self.hboxlayout16.addWidget(self.scaleEndLbl)

        self.scaleStop_SB = QtGui.QSpinBox(self.optionsTab)
        self.scaleStop_SB.setMinimum(1)
        self.scaleStop_SB.setMaximum(10000)
        self.scaleStop_SB.setProperty("value",QtCore.QVariant(64))
        self.scaleStop_SB.setObjectName("scaleStop_SB")
        self.hboxlayout16.addWidget(self.scaleStop_SB)
        self.vboxlayout4.addLayout(self.hboxlayout16)

        self.hboxlayout17 = QtGui.QHBoxLayout()
        self.hboxlayout17.setObjectName("hboxlayout17")

        self.scaleFactorLbl = QtGui.QLabel(self.optionsTab)
        self.scaleFactorLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scaleFactorLbl.setObjectName("scaleFactorLbl")
        self.hboxlayout17.addWidget(self.scaleFactorLbl)

        self.scaleFactor_SB = QtGui.QSpinBox(self.optionsTab)
        self.scaleFactor_SB.setMinimum(1)
        self.scaleFactor_SB.setMaximum(100)
        self.scaleFactor_SB.setProperty("value",QtCore.QVariant(4))
        self.scaleFactor_SB.setObjectName("scaleFactor_SB")
        self.hboxlayout17.addWidget(self.scaleFactor_SB)
        self.vboxlayout4.addLayout(self.hboxlayout17)

        self.hboxlayout18 = QtGui.QHBoxLayout()
        self.hboxlayout18.setObjectName("hboxlayout18")

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.makeScales_Btn = QtGui.QPushButton(self.optionsTab)
        self.makeScales_Btn.setObjectName("makeScales_Btn")
        self.vboxlayout5.addWidget(self.makeScales_Btn)

        spacerItem5 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout5.addItem(spacerItem5)
        self.hboxlayout18.addLayout(self.vboxlayout5)

        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout18.addItem(spacerItem6)
        self.vboxlayout4.addLayout(self.hboxlayout18)
        self.gridlayout1.addLayout(self.vboxlayout4,2,1,1,1)

        self.hboxlayout19 = QtGui.QHBoxLayout()
        self.hboxlayout19.setObjectName("hboxlayout19")

        self.vboxlayout6 = QtGui.QVBoxLayout()
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.scalesTable = QtGui.QTableWidget(self.optionsTab)
        self.scalesTable.setFrameShape(QtGui.QFrame.StyledPanel)
        self.scalesTable.setObjectName("scalesTable")
        self.vboxlayout6.addWidget(self.scalesTable)

        spacerItem7 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout6.addItem(spacerItem7)
        self.hboxlayout19.addLayout(self.vboxlayout6)

        spacerItem8 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout19.addItem(spacerItem8)
        self.gridlayout1.addLayout(self.hboxlayout19,2,2,1,1)
        self.hboxlayout3.addLayout(self.gridlayout1)
        self.tabWidget.addTab(self.optionsTab,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,831,21))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")

        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
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

        self.actionLabel_Peak = QtGui.QAction(MainWindow)
        self.actionLabel_Peak.setObjectName("actionLabel_Peak")

        self.actionCopy_to_Clipboard = QtGui.QAction(MainWindow)
        self.actionCopy_to_Clipboard.setObjectName("actionCopy_to_Clipboard")

        self.actionClear_Cursors = QtGui.QAction(MainWindow)
        self.actionClear_Cursors.setObjectName("actionClear_Cursors")

        self.actionRead_Me = QtGui.QAction(MainWindow)
        self.actionRead_Me.setObjectName("actionRead_Me")

        self.actionPeak_Picking = QtGui.QAction(MainWindow)
        self.actionPeak_Picking.setObjectName("actionPeak_Picking")
        self.menu_File.addAction(self.action_Open)
        self.menuTools.addAction(self.actionCursor_A)
        self.menuTools.addAction(self.actionCursor_B)
        self.menuTools.addAction(self.actionClear_Cursors)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionLabel_Peak)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionCopy_to_Clipboard)
        self.menu_Help.addAction(self.actionRead_Me)
        self.menu_Help.addAction(self.actionPeak_Picking)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.indexHSlider,QtCore.SIGNAL("valueChanged(int)"),self.indexSpinBox.setValue)
        QtCore.QObject.connect(self.indexSpinBox,QtCore.SIGNAL("valueChanged(int)"),self.indexHSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SpectrumViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Spectrum Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Spectrum Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Label:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "dx:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "dy:", None, QtGui.QApplication.UnicodeUTF8))
        self.cursACB.setText(QtGui.QApplication.translate("MainWindow", "Cursor A", None, QtGui.QApplication.UnicodeUTF8))
        self.cursBCB.setText(QtGui.QApplication.translate("MainWindow", "Cursor B", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.loadmzXMLCB.setText(QtGui.QApplication.translate("MainWindow", "Load mzXML", None, QtGui.QApplication.UnicodeUTF8))
        self.plotPkListCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.plotLegendCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.excludeLIFTCB.setText(QtGui.QApplication.translate("MainWindow", "Exclude LIFT MS/MS Files", None, QtGui.QApplication.UnicodeUTF8))
        self.invertCompCB.setText(QtGui.QApplication.translate("MainWindow", "Invert Single Comparison", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "m/z Lo:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "m/z Hi:", None, QtGui.QApplication.UnicodeUTF8))
        self.mzHi_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "If this value is set to -1 then a TIC starting from m/z Lo will be returned", None, QtGui.QApplication.UnicodeUTF8))
        self.getEIC_Btn.setText(QtGui.QApplication.translate("MainWindow", "Fetch EIC", None, QtGui.QApplication.UnicodeUTF8))
        self.loadDirBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "Wavelet Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Default to Mexican Hat</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">More later...</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("MainWindow", "End of Wavelet Noise Rows:", None, QtGui.QApplication.UnicodeUTF8))
        self.minRow_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Last row of the wavelet to be considered noise.</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Must be less than the number of scales.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">A smaller number means more peaks,</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">but not necessarily better results.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("MainWindow", "Minimum Wavelet Cluster Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.minClust_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "Minimum number of peaks to be found during the wavelet transform for each MS peak.\n"
        "Must be less than the number of scales.\n"
        "Half the number of scales appears to be a good approximation.\n"
        "Higher numbers mean fewer peaks.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("MainWindow", "Clustering Distance Threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.dbscanEPS_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Distance to be used for a clustering cutoff.</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Set to -1 for auto-calculation.  </p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">A smaller number means fewer peaks while a larger</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">number includes more surrounding neighbors.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Be careful...</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("MainWindow", "Noise Split Factor:", None, QtGui.QApplication.UnicodeUTF8))
        self.noiseFactor_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Factor by which the spectrum will be split in order to estimate local noise.  More is better but slower. For example:</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">if the lenght of a MS spectrum = 10000</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">and Noise Split Factor = 10</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">the number of segments used = 1000</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setToolTip(QtGui.QApplication.translate("MainWindow", "SNR value used for noise estimate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("MainWindow", "SNR Noise Estimation:", None, QtGui.QApplication.UnicodeUTF8))
        self.snrNoiseEst_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "SNR value used for noise estimate", None, QtGui.QApplication.UnicodeUTF8))
        self.plotNoiseEst_CB.setText(QtGui.QApplication.translate("MainWindow", "Show Noise Estimate", None, QtGui.QApplication.UnicodeUTF8))
        self.showNoise_Btn.setText(QtGui.QApplication.translate("MainWindow", "Calculate and Show Noise (without Peak Picking)", None, QtGui.QApplication.UnicodeUTF8))
        self.useDefaultScale_CB.setText(QtGui.QApplication.translate("MainWindow", "Used Default Scales for CWT", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleStartLbl.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleStartLbl.setText(QtGui.QApplication.translate("MainWindow", "Scale Start:", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleStart_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Starting point for scales</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleEndLbl.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleEndLbl.setText(QtGui.QApplication.translate("MainWindow", "Scale End:", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleStop_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">End point for scales.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleFactorLbl.setToolTip(QtGui.QApplication.translate("MainWindow", "Factor by which the spectrum will be split in order to estimate local noise", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleFactorLbl.setText(QtGui.QApplication.translate("MainWindow", "Scale Factor:", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleFactor_SB.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Don\'t Mess with this unless you know what you\'re doing!</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Making too many scales will slow things WAAAY down!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.makeScales_Btn.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Try to keep the total number of scales below 10,</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">otherwise peak picking could take a while.</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Example of use:</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Scale Start: 2</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Scale End: 32</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Scale Factor: 4</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">Output Scales:</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">[ 2,  6, 10, 14, 18, 22, 26, 30]</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.makeScales_Btn.setText(QtGui.QApplication.translate("MainWindow", "Create Scales", None, QtGui.QApplication.UnicodeUTF8))
        self.scalesTable.setRowCount(8)
        self.scalesTable.setColumnCount(1)
        self.scalesTable.clear()
        self.scalesTable.setColumnCount(1)
        self.scalesTable.setRowCount(8)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Misc", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCursor_A.setText(QtGui.QApplication.translate("MainWindow", "Cursor A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCursor_B.setText(QtGui.QApplication.translate("MainWindow", "Cursor B", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLabel_Peak.setText(QtGui.QApplication.translate("MainWindow", "Label Peak", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLabel_Peak.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy_to_Clipboard.setText(QtGui.QApplication.translate("MainWindow", "Copy to Clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Cursors.setText(QtGui.QApplication.translate("MainWindow", "Clear Cursors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Cursors.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRead_Me.setText(QtGui.QApplication.translate("MainWindow", "Read Me", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPeak_Picking.setText(QtGui.QApplication.translate("MainWindow", "Peak Picking", None, QtGui.QApplication.UnicodeUTF8))

from mpl_pyqt4_widget import MPL_Widget
import icons_rc
