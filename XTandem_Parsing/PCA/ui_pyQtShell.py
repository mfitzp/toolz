# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\SVN\pyQTShell\pyQtShell.ui'
#
# Created: Thu Aug 21 10:59:50 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_pyQTShell(object):
    def setupUi(self, pyQTShell):
        pyQTShell.setObjectName("pyQTShell")
        pyQTShell.setWindowModality(QtCore.Qt.NonModal)
        pyQTShell.resize(QtCore.QSize(QtCore.QRect(0,0,800,800).size()).expandedTo(pyQTShell.minimumSizeHint()))
        pyQTShell.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.hboxlayout = QtGui.QHBoxLayout(pyQTShell)
        self.hboxlayout.setObjectName("hboxlayout")

        self.splitter = QtGui.QSplitter(pyQTShell)
        self.splitter.setLineWidth(1)
        self.splitter.setMidLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(8)
        self.splitter.setObjectName("splitter")

        self.pyDockWidget = QtGui.QDockWidget(self.splitter)
        self.pyDockWidget.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyDockWidget.sizePolicy().hasHeightForWidth())
        self.pyDockWidget.setSizePolicy(sizePolicy)
        self.pyDockWidget.setMinimumSize(QtCore.QSize(0,200))
        self.pyDockWidget.setBaseSize(QtCore.QSize(0,200))
        self.pyDockWidget.setObjectName("pyDockWidget")

        self.dockWidgetContents = QtGui.QWidget(self.pyDockWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName("dockWidgetContents")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.pyDockWidget.setWidget(self.dockWidgetContents)
        self.hboxlayout.addWidget(self.splitter)

        self.actionAutoScale = QtGui.QAction(pyQTShell)
        self.actionAutoScale.setObjectName("actionAutoScale")

        self.actionPlotOptions = QtGui.QAction(pyQTShell)
        self.actionPlotOptions.setObjectName("actionPlotOptions")

        self.actionClear = QtGui.QAction(pyQTShell)
        self.actionClear.setObjectName("actionClear")

        self.actionZoom = QtGui.QAction(pyQTShell)
        self.actionZoom.setObjectName("actionZoom")

        self.retranslateUi(pyQTShell)
        QtCore.QMetaObject.connectSlotsByName(pyQTShell)

    def retranslateUi(self, pyQTShell):
        self.pyDockWidget.setWindowTitle(QtGui.QApplication.translate("pyQTShell", "Python Shell", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoScale.setText(QtGui.QApplication.translate("pyQTShell", "AutoScale", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoScale.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotOptions.setText(QtGui.QApplication.translate("pyQTShell", "Plot Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotOptions.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+T", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("pyQTShell", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+Shift+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setText(QtGui.QApplication.translate("pyQTShell", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))

