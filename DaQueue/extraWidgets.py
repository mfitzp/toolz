# -*- coding: utf-8 -
from PyQt4 import QtCore, QtGui


class cellComboBox(QtGui.QComboBox):
    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        if parent:
            self.parent = parent

        self.options = ['File Conversion', 'X!Tandem Run', 'Peak Picking']
        self.addItems(self.options)

#class cellOFD(QtGui.QToolButton):
#    def __init__(self, parent = None):
#        QtGui.QToolButton.__init__(self, parent)
#        self.setIcon(QtGui.QIcon('images/fileopen.png'))

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
        self.setIcon(QtGui.QIcon('images/toolsSmall.png'))

    def switchStatus(self, state):
        if state == 0:#Processing
            self.setIcon(QtGui.QIcon('images/toolsSmall.png'))
        elif state == 1:#Finished
            self.setIcon(QtGui.QIcon('images/clean.png'))
        elif state == 2:#Failed
            self.setIcon(QtGui.QIcon('images/exitsmall.png'))
