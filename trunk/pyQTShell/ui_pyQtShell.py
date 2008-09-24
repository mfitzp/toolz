# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\SVN\toolz\pyQTShell\pyQtShell.ui'
#
# Created: Tue Sep 23 13:01:04 2008
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

        self.tabWidget = QtGui.QTabWidget(pyQTShell)
        self.tabWidget.setObjectName("tabWidget")

        self.shellTab = QtGui.QWidget()
        self.shellTab.setObjectName("shellTab")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.shellTab)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.splitter = QtGui.QSplitter(self.shellTab)
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
        self.pyDockWidget.setWidget(self.dockWidgetContents)
        self.hboxlayout1.addWidget(self.splitter)
        self.tabWidget.addTab(self.shellTab,"")

        self.scratchTab = QtGui.QWidget()
        self.scratchTab.setObjectName("scratchTab")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.scratchTab)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.script_name_cb = QtGui.QComboBox(self.scratchTab)
        self.script_name_cb.setEditable(True)
        self.script_name_cb.setObjectName("script_name_cb")
        self.hboxlayout3.addWidget(self.script_name_cb)

        self.btn_scratch2Mem = QtGui.QPushButton(self.scratchTab)
        self.btn_scratch2Mem.setMaximumSize(QtCore.QSize(100,16777215))
        self.btn_scratch2Mem.setObjectName("btn_scratch2Mem")
        self.hboxlayout3.addWidget(self.btn_scratch2Mem)

        self.btn_saveScript = QtGui.QPushButton(self.scratchTab)
        self.btn_saveScript.setMaximumSize(QtCore.QSize(100,16777215))
        self.btn_saveScript.setObjectName("btn_saveScript")
        self.hboxlayout3.addWidget(self.btn_saveScript)
        self.vboxlayout.addLayout(self.hboxlayout3)

        self.sp_widget = QtGui.QWidget(self.scratchTab)
        self.sp_widget.setObjectName("sp_widget")
        self.vboxlayout.addWidget(self.sp_widget)
        self.hboxlayout2.addLayout(self.vboxlayout)
        self.tabWidget.addTab(self.scratchTab,"")
        self.hboxlayout.addWidget(self.tabWidget)

        self.actionAutoScale = QtGui.QAction(pyQTShell)
        self.actionAutoScale.setObjectName("actionAutoScale")

        self.actionPlotOptions = QtGui.QAction(pyQTShell)
        self.actionPlotOptions.setObjectName("actionPlotOptions")

        self.actionClear = QtGui.QAction(pyQTShell)
        self.actionClear.setObjectName("actionClear")

        self.actionZoom = QtGui.QAction(pyQTShell)
        self.actionZoom.setObjectName("actionZoom")

        self.retranslateUi(pyQTShell)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(pyQTShell)

    def retranslateUi(self, pyQTShell):
        self.pyDockWidget.setWindowTitle(QtGui.QApplication.translate("pyQTShell", "Python Shell", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shellTab), QtGui.QApplication.translate("pyQTShell", "Shell", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_scratch2Mem.setText(QtGui.QApplication.translate("pyQTShell", "Cache Script", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_saveScript.setText(QtGui.QApplication.translate("pyQTShell", "Script to Disk", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scratchTab), QtGui.QApplication.translate("pyQTShell", "Scratch Pad", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoScale.setText(QtGui.QApplication.translate("pyQTShell", "AutoScale", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoScale.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotOptions.setText(QtGui.QApplication.translate("pyQTShell", "Plot Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlotOptions.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+T", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("pyQTShell", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+Shift+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setText(QtGui.QApplication.translate("pyQTShell", "Zoom", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoom.setShortcut(QtGui.QApplication.translate("pyQTShell", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))

