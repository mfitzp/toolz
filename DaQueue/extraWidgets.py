# -*- coding: utf-8 -
from PyQt4 import QtCore, QtGui

from uiSupport import JOBKEYS, JOBTYPES, STATUSIDS, STATUSTYPES
#JOBKEYS = [0,1,2,3,4]
#JOBTYPES = ['X!Tandem', 'File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified']
#
#STATUSIDS = [0,1,2,3,4]
#STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']


class cellComboBox(QtGui.QComboBox):
    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        if parent:
            self.parent = parent

#        self.options = ['X!Tandem Run','Peak Picking','File Conversion']
        self.options = JOBTYPES
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
        self.stateList = STATUSTYPES
        self.state = 0
        self.switchStatus(self.state)

    def switchStatus(self, state):
        if state == 1:#Processing
            self.state = state
            self.setIcon(QtGui.QIcon('images/applications.png'))
        elif state == 2:#Finished
            self.state = state
            self.setIcon(QtGui.QIcon('images/clean.png'))
        elif state == 3:#Failed
            self.state = state
            self.setIcon(QtGui.QIcon('images/exitsmall.png'))
        elif state == 0:#Queued
            self.state == state
            self.setIcon(QtGui.QIcon('images/remove.png'))

    def getStatusText(self):
        return self.stateList[self.state]
