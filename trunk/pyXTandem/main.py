#!/usr/bin/env python
import os, sys, traceback
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import xml.etree.ElementTree as ET#need to use correctly with py2exe
import xml.etree.cElementTree as ET#I know seems redundant but is needed by py2exe

import supportElements as SE
import ui_mainGUI


class XTandem_Widget(QtGui.QMainWindow,  ui_mainGUI.Ui_MainWindow):
    def __init__(self, parent = None):
        super(XTandem_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self._setVars_()
        self._setupGUI_()
        self._setConnections_()

    def _setupGUI_(self):

        #populate types of fragments
        defaultFrags = ['b', 'y']#default fragments, add to list if needed
        for frag in SE.fragTypes:
            curFrag = QtGui.QListWidgetItem()
            curFrag.setText(frag)
            curFrag.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
            if frag in defaultFrags:
                curFrag.setCheckState(QtCore.Qt.Checked)
            else:
                curFrag.setCheckState(QtCore.Qt.Unchecked)

            self.fragTypeListWidget.addItem(curFrag)


        #CHANGE THIS to get the actual file specified in the parameter file
        taxa = SE.getTaxonomyList()
        if len(taxa)>0:
            for taxon in taxa:
                if taxon != None:
                    curTaxon = QtGui.QListWidgetItem()
                    curTaxon.setText(taxon)
                    curTaxon.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
                    curTaxon.setCheckState(QtCore.Qt.Unchecked)
                    self.taxonListWidget.addItem(curTaxon)

        #populate digestion parameters
        enzymeKeys = SE.enzymeTypes.keys()
        enzymeKeys.sort()
        self.cleaveSite_CB.addItems(enzymeKeys)
        defaultEnzyme = "Trypsin"
        self.defaultIndex = self.cleaveSite_CB.findText(defaultEnzyme)
        self.cleaveSite_CB.setCurrentIndex(self.defaultIndex)
        self.setCleaveRule()

        self.cleaveCTermChange_SB.setValue(17.002735)
        self.doubleSpinBox_8.setValue(1.007825)

    def _setConnections_(self):
        QtCore.QObject.connect(self.cleaveSite_CB, QtCore.SIGNAL("currentIndexChanged(QString)"), self.setCleaveRule)

        QtCore.QObject.connect(self.xtInputFile_Btn, QtCore.SIGNAL("clicked()"), self.setXTInputFile)
        QtCore.QObject.connect(self.xtOutputFile_Btn, QtCore.SIGNAL("clicked()"), self.setXTOutputFile)
        QtCore.QObject.connect(self.defaultTaxFile_Btn, QtCore.SIGNAL("clicked()"), self.setTaxonomyFile)
        QtCore.QObject.connect(self.defaultXTEXE_Btn, QtCore.SIGNAL("clicked()"), self.setXTEXE)
        QtCore.QObject.connect(self.defaultFolder_Btn, QtCore.SIGNAL("clicked()"), self.getDefaultFolder)

    def _setVars_(self):
        self.defaultIndex = None
        self.cleaveRule = None
        self.defaultDir = os.getcwd()

    def setCleaveRule(self, value=None):
        if value == None:
            index = self.cleaveSite_CB.currentIndex()
            value = self.cleaveSite_CB.itemText(index)

        curEnzyme = str(value)#convert from QString
        self.cleaveRule = SE.enzymeTypes[curEnzyme]
        self.cleaveRule_LE.setText(self.cleaveRule)
    ####################################################
    '''
    FOLDER FUNCTIONS AND HANDLERS
    '''
    ####################################################
    def setTaxonomyFile(self):
        fileName = self.openFileDialog("Get X!Tandem Taxonomy File", "Taxonomy File (taxonomy.xml)")
        if fileName != None:
            self.defaultTaxFile_LE.clear()
            self.defaultTaxFile_LE.setText(fileName)

    def setXTEXE(self):
        fileName = self.openFileDialog("Set X!Tandem Executable", "X!Tandem (tandem.exe)")
        if fileName != None:
            self.defaultXTEXE_LE.clear()
            self.defaultXTEXE_LE.setText(fileName)

    def setDefaultFolder(self, dir):
        if os.path.isdir(dir):
            self.defaultDir = dir

    def getDefaultFolder(self):
        dirBool, dir = self._getDir_()
        if dirBool:
            self.setDefaultFolder(dir)
            self.defaultFolder_LE.clear()
            self.defaultFolder_LE.setText(self.defaultDir)

    def setXTInputFile(self):
        fileName = self.saveFileDialog("X!Tandem XML Input to Save:", "XML (*.xml)")
        if fileName != None:
            self.inputFile_LE.clear()
            self.inputFile_LE.setText(fileName)

    def setXTOutputFile(self):
        fileName = self.saveFileDialog("X!Tandem XML Output to Save:", "XML (*.xml)")
        if fileName != None:
            self.outputFile_LE.clear()
            self.outputFile_LE.setText(fileName)

    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.defaultDir)
        directory = str(directory)
        if directory != None:
            return True, os.path.abspath(directory)
        else:
            return False, None

    def saveFileDialog(self, dialogText = None, fileTypes = None):
        if dialogText is None:
            dialogText = "Select File to Save"
        if fileTypes is None:
            fileTypes = "All Files (*.*)"
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                         dialogText,
                                         self.defaultDir,
                                         fileTypes)
        if not fileName.isEmpty():
            return os.path.abspath(str(fileName))
        else:
            return None

    def openFileDialog(self, dialogText = None, fileTypes = None):
        if dialogText is None:
            dialogText = "Select File to Open"
        if fileTypes is None:
            fileTypes = "All Files (*.*)"
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                         dialogText,
                                         self.defaultDir,
                                         fileTypes)
        if not fileName.isEmpty():
            return os.path.abspath(str(fileName))
        else:
            return None


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    xtGUI = XTandem_Widget()
    xtGUI.show()
    sys.exit(app.exec_())