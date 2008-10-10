# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\SVN\toolz\SimpleView\main.ui'
#
# Created: Fri Oct 10 11:49:56 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,830,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.indexHSlider = QtGui.QSlider(self.centralwidget)
        self.indexHSlider.setOrientation(QtCore.Qt.Horizontal)
        self.indexHSlider.setObjectName("indexHSlider")
        self.hboxlayout1.addWidget(self.indexHSlider)

        self.indexSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.indexSpinBox.setObjectName("indexSpinBox")
        self.hboxlayout1.addWidget(self.indexSpinBox)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.loadmzXMLCB = QtGui.QCheckBox(self.centralwidget)
        self.loadmzXMLCB.setObjectName("loadmzXMLCB")
        self.hboxlayout2.addWidget(self.loadmzXMLCB)

        self.plotPkListCB = QtGui.QCheckBox(self.centralwidget)
        self.plotPkListCB.setObjectName("plotPkListCB")
        self.hboxlayout2.addWidget(self.plotPkListCB)

        self.loadDirBtn = QtGui.QPushButton(self.centralwidget)
        self.loadDirBtn.setObjectName("loadDirBtn")
        self.hboxlayout2.addWidget(self.loadDirBtn)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.hboxlayout3.addWidget(self.label_2)

        self.specNameEdit = QtGui.QLineEdit(self.centralwidget)
        self.specNameEdit.setReadOnly(True)
        self.specNameEdit.setObjectName("specNameEdit")
        self.hboxlayout3.addWidget(self.specNameEdit)
        self.vboxlayout.addLayout(self.hboxlayout3)

        self.plotWidget = MPL_Widget(self.centralwidget)
        self.plotWidget.setObjectName("plotWidget")
        self.vboxlayout.addWidget(self.plotWidget)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.specListWidget = QtGui.QListWidget(self.centralwidget)
        self.specListWidget.setMaximumSize(QtCore.QSize(250,16777215))
        self.specListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.specListWidget.setObjectName("specListWidget")
        self.hboxlayout.addWidget(self.specListWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,830,21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.indexHSlider,QtCore.SIGNAL("valueChanged(int)"),self.indexSpinBox.setValue)
        QtCore.QObject.connect(self.indexSpinBox,QtCore.SIGNAL("valueChanged(int)"),self.indexHSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SpectrumViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Spectrum Index:", None, QtGui.QApplication.UnicodeUTF8))
        self.loadmzXMLCB.setText(QtGui.QApplication.translate("MainWindow", "Load mzXML?", None, QtGui.QApplication.UnicodeUTF8))
        self.plotPkListCB.setText(QtGui.QApplication.translate("MainWindow", "Plot Peak List?", None, QtGui.QApplication.UnicodeUTF8))
        self.loadDirBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Spectrum Location:", None, QtGui.QApplication.UnicodeUTF8))

from mpl_pyqt4_widget import MPL_Widget
