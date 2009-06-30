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
        self.cleaveNTermChange_SB.setValue(1.007825)

        #Set file path defaults:
        tempInput = os.path.join(self.defaultDir,"input.xml")
        self.inputFile_LE.setText(tempInput)

        tempOutput = os.path.join(self.defaultDir,"output.xml")
        self.outputFile_LE.setText(tempOutput)


    def _setConnections_(self):
        QtCore.QObject.connect(self.cleaveSite_CB, QtCore.SIGNAL("currentIndexChanged(QString)"), self.setCleaveRule)

        QtCore.QObject.connect(self.xtInputFile_Btn, QtCore.SIGNAL("clicked()"), self.setXTInputFile)
        QtCore.QObject.connect(self.xtOutputFile_Btn, QtCore.SIGNAL("clicked()"), self.setXTOutputFile)
        QtCore.QObject.connect(self.defaultTaxFile_Btn, QtCore.SIGNAL("clicked()"), self.setTaxonomyFile)
        QtCore.QObject.connect(self.defaultXTEXE_Btn, QtCore.SIGNAL("clicked()"), self.setXTEXE)
        QtCore.QObject.connect(self.defaultFolder_Btn, QtCore.SIGNAL("clicked()"), self.getDefaultFolder)

        QtCore.QObject.connect(self.makeXT_Output_Btn, QtCore.SIGNAL("clicked()"), self.makeXTOutput)


    def _setVars_(self):
        self.defaultIndex = None
        self.cleaveRule = None
        self.defaultDir = os.getcwd()
        self.xtInputFile = None
        self.xtOutputFile = None
        self.taxonomyFile = None
        self.taxa = None
        self.taxaOk = False
        self.inputDict = None
        self.fragDict = {}
        self.fragDictOk = False

    def resetFragDict(self):
        self.fragDict['a'] = 'no'
        self.fragDict['b'] = 'no'
        self.fragDict['c'] = 'no'
        self.fragDict['x'] = 'no'
        self.fragDict['y'] = 'no'
        self.fragDict['z'] = 'no'
        self.fragDictOk = False

    def setTaxa(self):
        self.taxonListWidget.selectAll()
        selectItems = self.taxonListWidget.selectedItems()
        taxaList = []
        if len(selectItems) > 0:
            for item in selectItems:
                if item.checkState() == 2:#Case when it is checked
                    taxaList.append([str(item.text())])
            self.taxa = taxaList
            self.taxaOk = True
        else:
            errMsg = "You must select at least one taxa to search against."
            self.taxaOk = False
            return QtGui.QMessageBox.warning(self, "Search Aborted", errMsg)


    def setFragDict(self):
        self.fragTypeListWidget.selectAll()
        selectItems = self.fragTypeListWidget.selectedItems()
        fragList = []
        if len(selectItems) > 0:
            for item in selectItems:
                if item.checkState() == 2:#Case when it is checked
                    self.fragDict[str(item.text())] = 'yes'
                    #fpList.append(str(item.text()))
            self.fragDictOk = True
        else:
            errMsg = "You must select at least one type of fragment."
            self.fragDictOk = False
            return QtGui.QMessageBox.warning(self, "Search Aborted", errMsg)

    def setInputDict(self):
        self.inputDict = {}
        self.inputDict['maxCharge']=self.maxCharge_SB.value()
        #####################
        self.inputDict['defaultPath'] = "C:Default_Input.xml"#"list path, default parameters"
        #####################
        self.inputDict['taxonomyPath'] = "C:Taxonomy.xml"#self.taxonomyFile#"list path, taxonomy information"
        #####################
        self.inputDict['fragSpecError'] = self.fragErr_SB.value()
        self.inputDict['parentErrPos'] = self.parentErrPos_SB.value()
        self.inputDict['parentErrNeg'] = self.parentErrNeg_SB.value()
        self.inputDict['isotopeErr'] = self.isotopeErr_CB.isChecked()#use isotope error?
        self.inputDict['fragUnits'] = str(self.fragErr_Type_CB.currentText())#Daltons or ppm
        self.inputDict['parentErrUnits'] = str(self.parentErrType_CB.currentText())#"spectrum, parent monoisotopic mass error units"#Daltons or ppm
        self.inputDict['fragMassType'] = str(self.fragType_CB.currentText())#"spectrum, fragment mass type"#monoisotopic or average
        self.inputDict['totalPeaks'] = self.totalPeaks_SB.value()
        self.inputDict['maxCharge'] = self.maxCharge_SB.value()
        self.inputDict['noiseSupress'] = self.noiseSuppress_CB.isChecked()#True#"spectrum, use noise suppression"
        self.inputDict['minParentMZ'] = self.minParent_SB.value()
        self.inputDict['minFragMZ'] = self.minFrag_SB.value()
        self.inputDict['minPeaks'] = self.minPeaks_SB.value()
        self.inputDict['threads'] = self.numThreads_SB.value()
        self.inputDict['aaModStr'] = str(self.aaMod_LE.text())#"residue, modification mass"
        #self.inputDict['potentialModMass'] = "residue, potential modification mass"
        self.inputDict['potentialModMotif'] = str(self.userDefinedMods_LE.text())#"residue, potential modification motif"
        ###############
        self.inputDict['taxon'] = self.taxa#"protein, taxon"
        ###############
        self.inputDict['cleavageSite'] = str(self.customCleaveRule_LE.text())#"protein, cleavage site"
        self.inputDict['protCTermChange'] = self.cleaveCTermChange_SB.value()#"protein, cleavage C-terminal mass change"#>+17.002735</note>
        self.inputDict['protNTermChange'] = self.cleaveNTermChange_SB.value()#"protein, cleavage N-terminal mass change"#>+1.007825</note>
        #self.inputDict['protNModMass'] = self.protNTerm_LE.value()#"protein, N-terminal residue modification mass"#>0.0</note>
        #self.inputDict['protCModMass'] = self.protCTerm_LE.value()#"protein, C-terminal residue modification mass"#>0.0</note>
        self.inputDict['refine'] = self.refineModel_CB.isChecked()#"refine"#>yes</note>
        #self.inputDict['refineModMass'] = "refine, modification mass"#></note>
        #self.inputDict[''] = "refine, sequence path"#></note>
        #self.inputDict['ticPercent'] = "refine, tic percent"#>20</note>
        self.inputDict['synthesizeSpec'] = self.specSyn_CB.isChecked()#"refine, spectrum synthesis"#>yes</note>
        self.inputDict['maxEValue'] = self.refineEVal_SB.value()#"refine, maximum valid expectation value"#>0.1</note>
        self.inputDict['refinePotNTermMod'] = str(self.potenNTermMods_LE.text())#"refine, potential N-terminus modifications"#>+42.010565@[</note>
        self.inputDict['refinePotCTermMod'] = str(self.potenCTermMods_LE.text())#"refine, potential C-terminus modifications"#></note>
        self.inputDict['refineUnanticipated'] = self.unanticipatedCleave_CB.isChecked()#"refine, unanticipated cleavage"#>yes</note>
        #self.inputDict[''] = "refine, potential modification mass"#></note>
        self.inputDict['pointMutations1'] = self.pointMut_CB.isChecked()#"refine, point mutations"#>no</note>
        self.inputDict['useModsforFull'] = self.useModsThroughout_CB.isChecked()#"refine, use potential modifications for full refinement"#>no</note>
        #self.inputDict['pointMutations2'] = "refine, point mutations"#>no</note>
        #self.inputDict['refinePotModMotif'] = "refine, potential modification motif"#></note>
        #self.inputDict['minIonCount'] = "scoring, minimum ion count"
        self.inputDict['maxMissedCleavages'] = self.maxMissedCleaves_SB.value()
        self.inputDict['xIons'] = self.fragDict['x']#
        self.inputDict['yIons'] = self.fragDict['y']#"scoring, y ions"
        self.inputDict['zIons'] = self.fragDict['z']#"scoring, z ions"
        self.inputDict['aIons'] = self.fragDict['a']#"scoring, a ions"
        self.inputDict['bIons'] = self.fragDict['b']#"scoring, b ions"
        self.inputDict['cIons'] = self.fragDict['c']#"scoring, c ions"

        self.inputDict['outputPath'] = str(self.outputFile_LE.text())#"output, path"
        self.inputDict['outputAll'] = self.outputAll_CB.isChecked()#

        #Set all bool values to a string either: 'yes' or 'no'
        for item in self.inputDict.iteritems():
            if type(item[1]) == bool:
                if item[1]:
                    self.inputDict[item[0]]='yes'
                else:
                    self.inputDict[item[0]]='no'


    def setCleaveRule(self, value=None):
        if value == None:
            index = self.cleaveSite_CB.currentIndex()
            value = self.cleaveSite_CB.itemText(index)

        curEnzyme = str(value)#convert from QString
        self.cleaveRule = SE.enzymeTypes[curEnzyme]
        self.cleaveRule_LE.setText(self.cleaveRule)

    def getFragTypes(self):
        print "Get Frag Types"


    def getTaxa(self):
        print "Get Taxa to search"


    def makeXTOutput(self):
        self.setTaxa()
        self.resetFragDict()
        self.setFragDict()
        self.setInputDict()
        self.writeXMLTree(self.inputDict['outputPath'])


    def writeXMLTree(self, fileName):
        root = ET.Element('xml', version = '1.0')
        head = ET.SubElement(root, "bioml")
        note = ET.SubElement(head, "note")
        for key in SE.xtInputDict.iterkeys():
            if self.inputDict.has_key(key):
                subNote = ET.SubElement(head, "note", type = "input", label = SE.xtInputDict[key])
                subNote.text = str(self.inputDict[key])

        note4 = ET.SubElement(head, "note", type = "input", label = "spectrum, path")
        note4.text='test_spectra.mgf'
        note5 = ET.SubElement(head, "note", type = "input", label = "output, path")
        note5.text='test_spectra.mgf'
        note5.text = 'clowers.xml'

        SE.indent(root)#makes it print pretty
        tree = ET.ElementTree(root)
        tree.write(fileName, encoding = 'utf-8')

    def saveXTInputFile(self):
        tempInput = str(self.inputFile_LE.text())
        tempDirInput = os.path.dirname(tempInput)

        tempOutput = str(self.outputFile_LE.text())
        tempDirOutput = os.path.dirname(tempOutput)

        if os.path.isdir(tempDirInput):
            self.xtInputFile = tempInput
            if os.path.isdir(tempDirOutput):
                self.xtOutputFile = tempOutput
                self.writeXMLTree(self.xtInputFile, self.xtOutputFile)
        else:
            print "Invalid X!Tandem input file path"


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