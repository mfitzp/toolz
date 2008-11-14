# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\d3p483\workspace\GCAlign\iterate.ui'
#
# Created: Mon Nov 10 10:54:38 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,1000,750).size()).expandedTo(MainWindow.minimumSizeHint()))
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

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.plotWidget = MPL_Widget(self.plotTab)
        self.plotWidget.setObjectName("plotWidget")
        self.hboxlayout3.addWidget(self.plotWidget)

        self.plotWidget2 = MPL_Widget(self.plotTab)
        self.plotWidget2.setObjectName("plotWidget2")
        self.hboxlayout3.addWidget(self.plotWidget2)
        self.vboxlayout.addLayout(self.hboxlayout3)
        self.tabWidget.addTab(self.plotTab,"")

        self.optionsTab = QtGui.QWidget()
        self.optionsTab.setObjectName("optionsTab")

        self.layoutWidget = QtGui.QWidget(self.optionsTab)
        self.layoutWidget.setGeometry(QtCore.QRect(11,13,261,141))
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridlayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout.setObjectName("gridlayout")

        self.loadmzXMLCB = QtGui.QCheckBox(self.layoutWidget)
        self.loadmzXMLCB.setChecked(True)
        self.loadmzXMLCB.setObjectName("loadmzXMLCB")
        self.gridlayout.addWidget(self.loadmzXMLCB,0,0,1,1)

        self.plotPkListCB = QtGui.QCheckBox(self.layoutWidget)
        self.plotPkListCB.setObjectName("plotPkListCB")
        self.gridlayout.addWidget(self.plotPkListCB,0,1,1,1)

        self.plotLegendCB = QtGui.QCheckBox(self.layoutWidget)
        self.plotLegendCB.setChecked(True)
        self.plotLegendCB.setObjectName("plotLegendCB")
        self.gridlayout.addWidget(self.plotLegendCB,1,0,1,1)

        self.loadDirBtn = QtGui.QPushButton(self.layoutWidget)
        self.loadDirBtn.setObjectName("loadDirBtn")
        self.gridlayout.addWidget(self.loadDirBtn,1,1,1,1)

        self.excludeLIFTCB = QtGui.QCheckBox(self.layoutWidget)
        self.excludeLIFTCB.setObjectName("excludeLIFTCB")
        self.gridlayout.addWidget(self.excludeLIFTCB,2,0,1,1)
        self.tabWidget.addTab(self.optionsTab,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,1000,21))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.menu_File.addAction(self.action_Open)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.indexHSlider,QtCore.SIGNAL("valueChanged(int)"),self.indexSpinBox.setValue)
        QtCore.QObject.connect(self.indexSpinBox,QtCore.SIGNAL("valueChanged(int)"),self.indexHSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Iterate", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Spectrum Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Spectrum Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.loadmzXMLCB.setText(QtGui.QApplication.translate("MainWindow", "Load mzXML", None, QtGui.QApplication.UnicodeUTF8))
        self.plotPkListCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Peak List", None, QtGui.QApplication.UnicodeUTF8))
        self.plotLegendCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.loadDirBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.excludeLIFTCB.setText(QtGui.QApplication.translate("MainWindow", "Exclude LIFT MS/MS Files", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))

from mpl_pyqt4_widget import MPL_Widget
import icons_rc
