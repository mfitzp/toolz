# -*- coding: utf-8 -
from PyQt4 import QtCore, QtGui


class cellComboBox(QtGui.QComboBox):
    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        if parent:
            self.parent = parent

        self.options = ['X!Tandem Run', 'Peak Picking','File Conversion']
        self.addItems(self.options)
        self.setCurrentIndex(0)
        self.setEditable(False)
        self.setEnabled(False)#Setting this option because only X!Tandem runs are enabled at this point

class cellOFD(QtGui.QTableWidgetItem):
    def __init__(self, parent = None):
        QtGui.QTableWidgetItem.__init__(self, '')
        self.setFlags(QtCore.Qt.ItemIsSelectable)
        self.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setIcon(QtGui.QIcon('images/fileopen.png'))

class cellStatus(QtGui.QTableWidgetItem):
    def __init__(self, parent = None):
        QtGui.QTableWidgetItem.__init__(self, '')
        self.setFlags(QtCore.Qt.ItemIsSelectable)
        self.setFlags(QtCore.Qt.ItemIsEnabled)
        self.stateList = ['Processing', 'Finished', 'Failed', 'Queued']
        self.state = 3
        self.switchStatus(self.state)

    def switchStatus(self, state):
        if state == 0:#Processing
            self.state = state
            self.setIcon(QtGui.QIcon('images/applications.png'))
        elif state == 1:#Finished
            self.state = state
            self.setIcon(QtGui.QIcon('images/clean.png'))
        elif state == 2:#Failed
            self.state = state
            self.setIcon(QtGui.QIcon('images/exitsmall.png'))
        elif state == 3:#Queued
            self.state == state
            self.setIcon(QtGui.QIcon('images/remove.png'))

    def getStatusText(self):
        return self.stateList[self.state]
