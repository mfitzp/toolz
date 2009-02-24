#!/usr/bin/env python
###################################
'''To Do:
"""
Keys:            GUI Elements:
{
"showsnrest":self.plotNoiseEst_CB,
"snrnoiseest":self.snrNoiseEst_SB,
"minrowtol":self.waveletRowTol_SB,
"minrownoise":self.minRow_SB,
"defaultscales":self.useDefaultScale_CB,
"splitfactor":self.noiseFactor_SB,
"autosavepeaks":self.autoSavePkList_CB,
"scaleend":self.scaleStop_SB,
"minclust":self.minClust_SB,
"staticcutoff":self.staticCutoff_SB,
"distthresh":self.dbscanEPS_SB,
"scalestart":self.scaleStart_SB,
"scalefactor":self.scaleFactor_SB,
"plotlegend":self.plotLegendCB,
"invertcomp":self.invertCompCB,
"plotpeaklist":self.plotPkListCB,
"mzhi":self.mzHi_SB,
"mzlo":self.mzLo_SB,
"excludelift":self.excludeLIFTCB,
"loadmzxml":self.loadmzXMLCB,
"autoloadfp":self.autoLoadFP_CB
}

Add progress bar to status bar...look at Ashoka's Code

Need to add exception for when there is no data in the file (i.e. a blank spectrum)

Load a single file?

Load FP

PCA after peak pick

Setup Group Class
Group Display

if peakfit is run the commit noise if it does not already exist

'''
###################################
import os, sys, traceback
import time
import ConfigParser
import string

config = ConfigParser.ConfigParser()
from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T

from matplotlib.lines import Line2D
from matplotlib.mlab import rec2csv

from FolderParse import Load_FID_Folder as LFid
from FolderParse import Load_mzXML_Folder as LmzXML
from flexReader import brukerFlexDoc as FR
from mzXML_reader import mzXMLDoc as mzXMLR

from mpl_pyqt4_widget import MPL_Widget
from dataClass import DataClass

import supportFunc as SF
import getBaseline as GB
import cwtPeakPick as CWT

import ui_main
from fingerPrint import Finger_Widget

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

class Plot_Widget(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.setupVars()
        self.readThread = LoadThread()
        self.FPT = FindPeaksThread()
        self.initConnections()
        self.setupGUI()
        self.loadPrefs()
        self.setupPlot()
        self.layoutStatusBar()


    def initConnections(self):
        self.handleActionA = QtGui.QAction("Cursor A", self)
        self.plotWidget.addAction(self.handleActionA)

        self.handleActionB = QtGui.QAction("Cursor B", self)
        self.plotWidget.addAction(self.handleActionB)

        self.cursorClearAction = QtGui.QAction("Clear Cursors", self)
        self.plotWidget.addAction(self.cursorClearAction)

        self.labelAction = QtGui.QAction("Label Peak", self)
        self.plotWidget.addAction(self.labelAction)

        self.removeAction = QtGui.QAction("Remove File(s)", self)
        self.groupTreeWidget.addAction(self.removeAction)

        self.topHatAction = QtGui.QAction("Apply TopHat",  self)
        self.groupTreeWidget.addAction(self.topHatAction)

        self.findPeakAction = QtGui.QAction("Find Peaks", self)
        self.groupTreeWidget.addAction(self.findPeakAction)

        self.selectAllAction = QtGui.QAction("Select All", self)
        self.groupTreeWidget.addAction(self.selectAllAction)

        self.saveCSVAction = QtGui.QAction("Save to CSV", self)
        self.saveCSVAction.setShortcut("Ctrl+Alt+S")
        self.plotWidget.addAction(self.saveCSVAction)

        self.savePksAction = QtGui.QAction("Save Peak List", self)
        self.groupTreeWidget.addAction(self.savePksAction)

        self.selectGroupAction = QtGui.QAction("Process Group(s)", self)
        self.groupTreeWidget.addAction(self.selectGroupAction)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)


        self.reviewFPAction = QtGui.QAction("Review Fingerprint",  self)
        self.fpListWidget.addAction(self.reviewFPAction)
        QtCore.QObject.connect(self.reviewFPAction,QtCore.SIGNAL("triggered()"), self.reviewFP)


        QtCore.QObject.connect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)

        QtCore.QObject.connect(self.removeAction, QtCore.SIGNAL("triggered()"),self.removeFile)
        QtCore.QObject.connect(self.topHatAction, QtCore.SIGNAL("triggered()"), self.filterSpec)

        QtCore.QObject.connect(self.handleActionA, QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.handleActionB, QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.cursorClearAction, QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.labelAction, QtCore.SIGNAL("triggered()"),self.labelPeak)
#        QtCore.QObject.connect(self.mpl2ClipAction, QtCore.SIGNAL("triggered()"),self.mpl2Clip)

#        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("terminated()"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished()"), self.updateGUI)
        QtCore.QObject.connect(self.loadDirBtn, QtCore.SIGNAL("clicked()"), self.initDataList)
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.initDataList)
#        QtCore.QObject.connect(self.specListWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.specListSelect)

        #UI Action Slots
        QtCore.QObject.connect(self.actionLabel_Peak,QtCore.SIGNAL("triggered()"),self.labelPeak)
        QtCore.QObject.connect(self.actionCopy_to_Clipboard,QtCore.SIGNAL("triggered()"),self.mpl2Clip)
        QtCore.QObject.connect(self.actionCursor_A,QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.actionCursor_B,QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.actionClear_Cursors,QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.cursACB,QtCore.SIGNAL("stateChanged (int)"),self.toggleCA)
        QtCore.QObject.connect(self.cursBCB,QtCore.SIGNAL("stateChanged (int)"),self.toggleCB)

        QtCore.QObject.connect(self.useDefaultScale_CB,QtCore.SIGNAL("stateChanged (int)"),self.scaleSetup)
        QtCore.QObject.connect(self.makeScales_Btn, QtCore.SIGNAL("clicked()"), self.makeUserScale)
#        QtCore.QObject.connect(self.showNoise_Btn, QtCore.SIGNAL("clicked()"), self.getCurDataNoise)

        QtCore.QObject.connect(self.getEIC_Btn, QtCore.SIGNAL("clicked()"), self.fetchEIC)

        QtCore.QObject.connect(self.findPeakAction,QtCore.SIGNAL("triggered()"),self.findPeaks)
        QtCore.QObject.connect(self.savePksAction,QtCore.SIGNAL("triggered()"),self.savePeaks)
        QtCore.QObject.connect(self.selectAllAction,QtCore.SIGNAL("triggered()"),self.selectAllLoaded)

        QtCore.QObject.connect(self.FPT, QtCore.SIGNAL("progress(int)"), self.threadProgress)
        QtCore.QObject.connect(self.FPT, QtCore.SIGNAL("finished(bool)"), self.PFTFinished)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished(bool)"), self.readFinished)

#        QtCore.QObject.connect(self.groupTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.treeItemSelected)
        QtCore.QObject.connect(self.groupTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.treeViewSelect)
        QtCore.QObject.connect(self.selectGroupAction,QtCore.SIGNAL("triggered()"),self.selectGroups)

        #FingerPrint Related Connections:
        QtCore.QObject.connect(self.expand_Btn, QtCore.SIGNAL("clicked()"), self.expandFPSpectra)
        QtCore.QObject.connect(self.testFocus_Btn, QtCore.SIGNAL("clicked()"), self.testFocus)
        QtCore.QObject.connect(self.fpListWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.fpListSelect)

        QtCore.QObject.connect(self.loadHDF5FP_Btn, QtCore.SIGNAL("clicked()"), self.loadFPfromHDF5)

        self.useDefaultScale_CB.nextCheckState()

    def loadPrefs(self):
        if os.path.isfile(self.prefFileName):
            self._getPrefs_(self.prefFileName)
            print self.prefFileName
        else:
            print "No preference file exists...reverting to defaults"

    def _setPref_(self, val, valType, guiElement):
        '''
        guiElement = element to commit value to
        val = value to load into GUI
        valType = type used to determine which function to use to set the value to the GUI
        '''
        if valType == float or valType == int:
            guiElement.setValue(val)
        elif valType == bool:
            guiElement.setChecked(val)


    def _getPrefs_(self, configFileName):
        config = ConfigParser.ConfigParser()
        config.read(configFileName)
        i = 0
        for section in config.sections():
#            print '\t',config.options(section)
            for option in config.options(section):
                val = None
                try:
                    val = config.getboolean(section, option)
                except:
                    pass

                try:
                    val = config.getfloat(section, option)
                except:
                    pass

                try:
                    val = config.getint(section, option)
                except:
                    pass

                if val != None:
#                    print option, self.prefDict[option]
#                    print " ", option, "=", val, type(val)
                    self._setPref_(val, type(val), self.prefDict[option])



    def reviewFP(self):
#        print "ReviewFP"
        selectItems = self.fpListWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]#only select one FP at a time
            print str(item.text())
            tempDataDict = self.fpDict[str(item.text())]['dataDict']
            peakStatDict = self.fpDict[str(item.text())]['peakStats']
            curFingerPlot = Finger_Widget(parent = self)
            curFingerPlot.updateDataDict(tempDataDict)
            curFingerPlot.peakStatDict = peakStatDict
            curFingerPlot.setupTable()

            #set mzTol and the stdDev
            curFingerPlot.mzTol_SB.setValue(peakStatDict['mzTol'].mean())
            curFingerPlot.stdDev_SB.setValue(peakStatDict['stdDevTol'].mean())

            curFingerPlot.setupPlot()
            curFingerPlot.getFPPeakList(resetDict = True)
            curFingerPlot.show()
            self.fingerPlots.append(curFingerPlot)


#                self.fpDict

    def loadFPfromHDF5(self):
        fileName = self.openFileDialog()
        if os.path.isfile(fileName):
            hdf = T.openFile(fileName, mode = 'r')
            hdfRoot = hdf.root
            try:

                specList = hdfRoot.Spectra._v_children
                peakLists = hdfRoot.PeakLists._v_children
                peakStats = hdfRoot.PeakStats._v_children


                self.curGroupName = fileName.split(os.path.sep)[-1]
                self.groupIndex.append(self.numGroups)
                self.groupList.append(self.curGroupName)
                self.numGroups+=1

                self.curTreeItem = QtGui.QTreeWidgetItem(self.groupTreeWidget)
                self.curTreeItem.setText(0,self.curGroupName)
                self.curTreeItem.setToolTip(0, fileName)
                self.groupTreeWidget.resizeColumnToContents(0)

                #Should we add a FP tree item?
                self.curFPTreeItem = QtGui.QTreeWidgetItem(self.loadSpecTreeWidget)
                self.curFPTreeItem.setText(0,self.curGroupName)
                self.curFPTreeItem.setToolTip(0, fileName)
                self.loadSpecTreeWidget.resizeColumnToContents(0)

                self.getTextColor()

                dataDict = {}
                for i, key in enumerate(specList.keys()):

                    bName = os.path.basename(key.replace('*',os.path.sep))
                    newName = os.path.join(self.curGroupName, bName)
                    spec = specList[key].read()
                    dataFile = DataClass(spec[:,0], spec[:,1],  name = bName, path = newName, interp = True)#should already by interpolated
                    pkList = peakLists[key].read()
                    dataFile.setPeakList(pkList, normalized = True)#set to normalized as these values are by nature already normalized
                    dataDict[newName] = dataFile#used to add to FP interface
                    self.updateGUI(dataFile)

                peakStatDict = {}
                for j, key in enumerate(peakStats.keys()):
                    peakStatDict[key] = peakStats[key].read()


                fpDict = {}
                fpDict[self.curGroupName] = {'dataDict':dataDict, 'peakStats':peakStatDict}
                self.commitFP(fpDict)

                hdf.close()
                self.loadOk = True
                self.readFinished(True)
            except:
                hdf.close()
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
                errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
                return QtGui.QMessageBox.warning(self, "Load Fingerpint Error", errorMsg)
                print 'Error loading fingerprint from HDF5'
                print errorMsg
#                self.saveDict(hdf, self.dataDict, "Spectra")
#                self.saveDict(hdf, self.peakStatDict, "PeakStats")
#
#            pkListGroup = hdfInstance.createGroup("/", "PeakLists", "PeakLists")
#
#        for item in dataDict.iteritems():
#            if isinstance(item[1], DataClass):
#                specX = item[1].x
#                specY = item[1].y
#                data = N.column_stack((specX,specY))
#                pkList = item[1].peakList
#                if pkList != None and pkListOK:
#                    shape = pkList.shape
#                    ca = hdfInstance.createCArray(pkListGroup, item[0], atom, shape, filters = filters)
#                    ca[0:shape[0]] = pkList


    def openFileDialog(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                         "Select Fingerprint File to Load",
                                         "",
                                         "HDF5 Files (*.h5)")
        if not fileName.isEmpty():
#            print fileName
            return os.path.abspath(str(fileName))
        else:
            return None

    def fpListSelect(self, listItem=None):
        if listItem != None:
            if self.fpDict.has_key(str(listItem.text())):
                '''
                the value of fpDict has keys of 'dataDict' and  'peakStats'
                '''
                self.curFPName = str(listItem.text())
                self.curFPName_LE.setText(self.curFPName)
                peakStatDict = self.fpDict[self.curFPName]['peakStats']
                self.fingerPTable.clear()
                self.fingerPTable.setSortingEnabled(False)
                tableHeaders = ['aveLoc','stdLoc', 'aveInt', 'stdInt', 'numMembers', 'freq']
        #        for key in tableHeaders:
        #            self.peakStatDict[key] = N.array(self.peakStatDict[key])

                tableData = peakStatDict['aveLoc']
                for key in tableHeaders[1:]:
                    tableData = N.column_stack((tableData,peakStatDict[key]))
        #        print tableData.shape
                self.fingerPTable.addData(tableData)
                self.fingerPTable.setSortingEnabled(True)
                self.fingerPTable.setHorizontalHeaderLabels(tableHeaders)


    def commitFP(self, fpDict):
        '''
        '''
        for item in fpDict.iteritems():
            if self.fpDict.has_key(item[0]):
                if self.__askConfirm__("Fingerprint Already Exists", "Overwrite existing FP?"):
                    self.fpDict[item[0]]=item[1]
                    self.addFP(fpDict)
            else:
                self.fpDict[item[0]]=item[1]
                self.addFP(fpDict)

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def addFP(self, fpDict):
        curFPName = fpDict.keys()[0]
        matchNameList = self.fpListWidget.findItems(curFPName, QtCore.Qt.MatchExactly)
        if len(matchNameList)>0:
            return QtGui.QMessageBox.warning(self, "Fingerprint Name Error", "A fingerpint of that name already exists!" )
        else:
            curFP = QtGui.QListWidgetItem()
            curFP.setText(curFPName)
            curFP.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
            curFP.setCheckState(QtCore.Qt.Unchecked)
            self.fpListWidget.addItem(curFP)

    def testFocus(self):
        print "Test Focus"

    def _setFPFocus_(self, fpInstance=None):
        '''
        used to capture the top window focus
        '''
        if isinstance(fpInstance, Finger_Widget):
            self.curFPWidget = fpInstance
#            print "Got Finger Widget"

    def expandFPSpectra(self):
        if self.expandFPBool:
            self.expandFPBool = False
        else:
            self.expandFPBool = True

        if self.expandFPBool:
            self.loadSpecTreeWidget.expandAll()
        else:
            self.loadSpecTreeWidget.collapseAll()


    def setupVars(self):
        self.dirList = []
        self.curDir = os.getcwd()
        self.curDataName = None
        #these are used to keep track of what group is loaded
        self.groupIndex = []
        self.groupList = []
        self.groupDict = {}
        self.curGroup = None
        self.numGroups = 0
        #########################
        self.dataList = []
        self.dataDict = {}
        self.loadOk = False
        self.multiPlotIndex = []
        self.ignoreSignal = False
        self.firstLoad = True
        self.labelPks = False
        self.plotPks = False
        self.txtColor = None
        self.colorIndex = 0
        self.plotColor = None
        self.plotColorIndex = 0
        self.curEIC = None
        self.eicPlots = []
        self.fingerPlots = []
        self.curFPWidget = Finger_Widget(parent = self)
        self.fingerPlots.append(self.curFPWidget)
        self.peakParams = None
        self.setupPeakPick()
        ###FP Related Vars:
        self.expandFPBool = False
        self.fpDict = {}
        self.curFPName = None
        ###Preference Variables
        self.prefFileName = 'svconfig.ini'
        self.prefDict = {'showsnrest':self.plotNoiseEst_CB,
                         'snrnoiseest':self.snrNoiseEst_SB,
                         'minrowtol':self.waveletRowTol_SB,
                         'minrownoise':self.minRow_SB,
                         'defaultscales':self.useDefaultScale_CB,
                         'splitfactor':self.noiseFactor_SB,
                         'autosavepeaks':self.autoSavePkList_CB,
                         'scaleend':self.scaleStop_SB,
                         'minclust':self.minClust_SB,
                         'staticcutoff':self.staticCutoff_SB,
                         'distthresh':self.dbscanEPS_SB,
                         'scalestart':self.scaleStart_SB,
                         'scalefactor':self.scaleFactor_SB,
                         'plotlegend':self.plotLegendCB,
                         'invertcomp':self.invertCompCB,
                         'plotpeaklist':self.plotPkListCB,
                         'mzhi':self.mzHi_SB,
                         'mzlo':self.mzLo_SB,
                         'excludelift':self.excludeLIFTCB,
                         'loadmzxml':self.loadmzXMLCB,
                         'autoloadfp':self.autoLoadFP_CB
                         }


    def setupGUI(self):
        self.specNameEdit.clear()
        self.groupTreeWidget.setHeaderLabel('Loaded Spectra:')
        self.loadSpecTreeWidget.setHeaderLabel('Loaded Spectra:')

#        self.indexHSlider.setMaximum(0)
#        self.indexSpinBox.setMaximum(0)
        self.initContextMenus()

    def updateGUI(self,  loadedItem=None):
        if loadedItem != None:
            #So that duplicate files are not loaded into the dataDict
            #if self.dataDict.has_key(loadedItem.name):
            if self.dataDict.has_key(loadedItem.path):
                print "%s already exists...skipping"%loadedItem.path
                pass
            else:
                #self.dataList.append(loadedItem.name)
                self.dataList.append(loadedItem.path)
                #color handler
#                tempItem = QtGui.QListWidgetItem(loadedItem.name)

#                tempItem.setTextColor(tempColor)
#                tempItem.setToolTip(loadedItem.path)
#                #self.specListWidget.addItem(loadedItem.name)
#                self.specListWidget.addItem(tempItem)

                #TreeWidget Handling
                tempTWI = QtGui.QTreeWidgetItem()
                tempTWI.setText(0, loadedItem.name)
                tempColor = QtGui.QColor(self.txtColor)
                tempTWI.setTextColor(0, tempColor)
                tempTWI.setToolTip(0, loadedItem.path)
                self.curTreeItem.addChild(tempTWI)

                tempFPTWI = QtGui.QTreeWidgetItem()
                tempFPTWI.setText(0, loadedItem.name)
                tempFPTWI.setTextColor(0, tempColor)
                tempFPTWI.setToolTip(0, loadedItem.path)
                self.curFPTreeItem.addChild(tempFPTWI)

            self.dataDict[loadedItem.path] = loadedItem

        self.numSpec = len(self.dataDict)
#        if self.numSpec == 1:
#            self.plotByIndex(0)
#            self.indexHSlider.setMaximum(self.numSpec)
#            self.indexSpinBox.setMaximum(self.numSpec)
#        else:
#            self.indexHSlider.setMaximum(self.numSpec-1)
#            self.indexSpinBox.setMaximum(self.numSpec-1)

    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.curDir)
        directory = str(directory)
        if directory != None:
            self.curDir = os.path.abspath(directory)
        else:
            self.curDir = os.path.abspath(os.getcwd())
        #return directory

    def _updatePlotColor_(self):
        if self.plotColorIndex%len(COLORS) == 0:
            self.plotColorIndex = 0
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1
        else:
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1

    def initContextMenus(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__mplContext__)
        self.groupTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.groupTreeWidget.connect(self.groupTreeWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__treeContext__)
        self.fpListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.fpListWidget.connect(self.fpListWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__fpContext__)


    def __fpContext__(self, point):
        '''Create a menu for the FingerPrint list widget'''
        ct_menu = QtGui.QMenu("Fingerprint Menu", self.fpListWidget)
        ct_menu.addAction(self.reviewFPAction)
#        ct_menu.addAction(self.topHatAction)
#        ct_menu.addAction(self.findPeakAction)
#        ct_menu.addAction(self.savePksAction)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.selectAllAction)
        ct_menu.exec_(self.fpListWidget.mapToGlobal(point))

    def __treeContext__(self, point):
        '''Create a menu for the file list widget'''
        ct_menu = QtGui.QMenu("Tree Menu", self.groupTreeWidget)
        ct_menu.addAction(self.removeAction)
        ct_menu.addAction(self.topHatAction)
        ct_menu.addAction(self.findPeakAction)
        ct_menu.addAction(self.savePksAction)
        ct_menu.addSeparator()
        selectItems = self.groupTreeWidget.selectedItems()
        groupBool = True
        if len(selectItems) > 0:
            for item in selectItems:
                if item.childCount() == 0:#test to see if any of the items selected are leaves
                    groupBool = False
        if groupBool:
            ct_menu.addAction(self.selectGroupAction)
#        ct_menu.addAction(self.selectAllAction)
        ct_menu.exec_(self.groupTreeWidget.mapToGlobal(point))


    def __listContext__(self, point):
        '''Create a menu for the file list widget'''
        ct_menu = QtGui.QMenu("List Menu", self.specListWidget)
        ct_menu.addAction(self.removeAction)
        ct_menu.addAction(self.topHatAction)
        ct_menu.addAction(self.findPeakAction)
        ct_menu.addAction(self.savePksAction)
        ct_menu.addSeparator()
        ct_menu.addAction(self.selectAllAction)
        ct_menu.exec_(self.specListWidget.mapToGlobal(point))

    def __mplContext__(self, point):
        '''Create a menu for the mpl widget'''
        ct_menu = QtGui.QMenu("Plot Menu", self.plotWidget)
#        ct_menu.addAction(self.ui.actionZoom)
#        ct_menu.addAction(self.ui.actionAutoScale)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.ui.actionPlotOptions)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.ui.actionClear)
#        ct_menu.addSeparator()
        ct_menu.addAction(self.handleActionA)
        ct_menu.addAction(self.handleActionB)
        ct_menu.addAction(self.cursorClearAction)
#        ct_menu.addSeparator()
        ct_menu.addAction(self.labelAction)
#        ct_menu.addSeparator()
        ct_menu.addAction(self.plotWidget.mpl2ClipAction)
        ct_menu.exec_(self.plotWidget.mapToGlobal(point))

    def getTextColor(self):
        if self.colorIndex%len(COLORS) == 0:
            self.colorIndex = 0
            self.txtColor = COLORS[self.colorIndex]
            self.colorIndex +=1
        else:
            self.txtColor = COLORS[self.colorIndex]
            self.colorIndex +=1

    def initDataList(self):
        #handles loading of new group.
        #####Text Color Handler
        self.getTextColor()

        if not self.firstLoad:
            #reinitialize GUI and spectrumList
            self.setupGUI()
        if self.loadmzXMLCB.isChecked():
            loadLIFT = self.excludeLIFTCB.isChecked()
            self._getDir_()
            dirList, startDir = LmzXML(self.curDir, excludeLIFT = loadLIFT)
            dirList.sort()
            if len(dirList) !=0:
                print dirList
                self.dirList = dirList
                self.loadOk = True
                self.firstLoad = False
                if self.readThread.updateThread(dirList,  loadmzXML = True):
                    self.readThread.start()

                self.curGroup = self.numGroups
                if sys.platform == 'win32':
                    self.curGroupName = self.curDir.split(os.path.sep)[-1]
                else:
                    self.curGroupName = self.curDir.split(os.path.sep)[-1]#[-2]
                self.groupIndex.append(self.numGroups)
                self.groupList.append(self.curGroupName)
                self.numGroups+=1

                self.curTreeItem = QtGui.QTreeWidgetItem(self.groupTreeWidget)
                self.curTreeItem.setText(0,self.curGroupName)
                self.curTreeItem.setToolTip(0, self.curDir)

                #items for the fingerprint comparison
                self.curFPTreeItem = QtGui.QTreeWidgetItem(self.loadSpecTreeWidget)
                self.curFPTreeItem.setText(0,self.curGroupName)
                self.curFPTreeItem.setToolTip(0, self.curDir)

#                print self.curDir

#                print "Cur Group", self.curGroup
#                print "Group Index", self.groupIndex
#                print "Group List", self.groupList
#                print "Num Groups", self.numGroups

            elif startDir != None:
                return QtGui.QMessageBox.warning(self, "No Data Found",  "Check selected folder, does it have any data?")

        else:
            self._getDir_()
            dirList, startDir = LFid(self.curDir)
            dirList.sort()
            if len(dirList) !=0:
                self.dirList = dirList
                self.loadOk = True
                self.firstLoad = False
                if self.readThread.updateThread(dirList):
                    self.readThread.start()
            elif startDir != None:
                return QtGui.QMessageBox.warning(self, "No Data Found",  "Check selected folder, does it have any data?")


#    def treeItemSelected(self, item = None, index = None):
#        if item != None:
#            print index
#            print item.text(index)
#            if item.parent() != None:
#                print item.parent().text(index)

    def selectAllLoaded(self):
        self.ignoreSignal = True
        self.groupTreeWidget.selectAll()
        self.ignoreSignal = False

    def readFinished(self, finishedBool):
        print "File Load Finished"
#        self.curTreeItem.sortChildren(0,QtCore.Qt.AscendingOrder)#sort column 0 in ascending order
        tempGroupItems = []#the temporary list to contain the names of each file in the group
        for i in xrange(self.curTreeItem.childCount()):
            tempGroupItems.append(str(self.curTreeItem.child(i).toolTip(0)))
        self.groupDict[str(self.curTreeItem.toolTip(0))] = tempGroupItems
        self.curTreeItem.sortChildren(0,QtCore.Qt.AscendingOrder)#sort column 0 in ascending order
#        print self.groupDict

    def selectGroups(self):
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            curFingerPlot = Finger_Widget(parent = self)
            for item in selectItems:
                curGroupName = str(item.toolTip(0))
                if self.groupDict.has_key(curGroupName):
                    tempItemList = self.groupDict[curGroupName]
                    if len(tempItemList)>0:
                        tempDataDict = {}#self.dataDict.fromkeys(tempItemList)
                        for childName in tempItemList:
                            tempDataDict[childName] = self.dataDict[childName]
                        curFingerPlot.updateDataDict(tempDataDict)

                print item.toolTip(0)


            curFingerPlot.setupPlot()
            curFingerPlot.getFPPeakList()
            curFingerPlot.show()
            self.fingerPlots.append(curFingerPlot)

    def PFTFinished(self, finishedBool):
        self.setStatusLabel("Peak Fitting Completed!")
        self.treeViewSelect()
        self.resetProgressBar()

    def treeViewSelect(self, widgetItem=None, index = None):
        if self.ignoreSignal:
            return
        else:
            selectItems = self.groupTreeWidget.selectedItems()
            if len(selectItems) > 0:
                self.multiPlotList = []#reset indexes to plot
                for item in selectItems:
                    if item.childCount() == 0:#test to see if the object is a leaf
                        self.multiPlotList.append(str(item.toolTip(0)))#get the toolTip which is a key to the dataDict
                if len(self.multiPlotList)>0:
                    self.plotByList(multiPlot = True)

    def plotByList(self, multiPlot = False):
        curDataName = None
        if self.loadOk:
            curAx = self.plotWidget.canvas.ax
            curAx.cla()
            self.labelPks = self.plotPkListCB.isChecked()
            self.plotColorIndex = 0
            if multiPlot:
                if len(self.multiPlotList)>0:
                    if self.invertCompCB.isChecked() and len(self.multiPlotList) == 2:
                        self._updatePlotColor_()
                        curDataName = self.multiPlotList[0]
                        self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, plotPks = self.plotPkListCB.isChecked())
                        self._updatePlotColor_()
                        curDataName = self.multiPlotList[1]
                        self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, invert = True, plotPks = self.plotPkListCB.isChecked())
                    else:
                        for curDataName in self.multiPlotList:
                            self._updatePlotColor_()
                            curData = self.dataDict[curDataName]
                            self.plotCurData(curData, curAx)
    #                        curData.plot(curAx, pColor = self.plotColor)
                        #the following makes it so the change is ignored and the plot does not update
                        self.specNameEdit.setText(curData.path)#use dataList to get the name?
    #                    self.ignoreSignal = True
    #                    self.indexHSlider.setValue(i)
    #                    self.indexSpinBox.setValue(i)
    #                    self.ignoreSignal = False
    #            else:
    #                if plotIndex == None:
    #                    plotIndex = self.initIndex
    #                if plotIndex == self.indexSpinBox.value():#this is just to see if the user is still sliding things around before updating plot
    #                    self._updatePlotColor_()
    #                    curDataName = self.dataList[plotIndex]
    #                    curData = self.dataDict[curDataName]
    #                    #test to see if noise has been calculated, if not do it and then plot.
    ##                    print self.plotNoiseEst_CB.isChecked()
    #                    self.plotCurData(curData, curAx)

    #                    if self.plotNoiseEst_CB.isChecked():
    #                        if curData.noiseOK:
    #                            curData.plot(curAx, pColor = self.plotColor, plotNoise = True)#, labelPks = False)
    #                        else:
    #                            numSegs = len(curData.x)/self.noiseFactor_SB.value()
    #                            minSNR = self.snrNoiseEst_SB.value()
    #                            curData.getNoise(numSegs,minSNR)
    #                            curData.plot(curAx, pColor = self.plotColor, plotNoise = True)#, labelPks = False)
    #                    else:
    #                        curData.plot(curAx, pColor = self.plotColor)#, labelPks = False)
    #                    self.specNameEdit.setText(curData.path)#use dataList to get the name?
    #                    #the following makes it so the change is ignored and the plot does not update
    #                    self.ignoreSignal = True
    #                    self.groupTreeWidget.setCurrentRow(plotIndex)
    #                    self.ignoreSignal = False
            if self.plotLegendCB.isChecked():
                curAx.legend(axespad = 0.03, pad=0.25)
            try:
                minX = curAx.get_lines()[0].get_xdata()[0]
                self.addPickers(minX)
            except:
                errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg
                self.addPickers()
            #used so that the scales will not be wonkey
            if multiPlot:
                if self.invertCompCB.isChecked() and len(self.multiPlotList) == 2:
                    pass
                else:
                    curAx.set_ylim(ymin = 0)
            else:
                curAx.set_ylim(ymin = 0)
            self.curDataName = curDataName
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
            self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom




    def savePeaks(self):
        selectItems = self.groupTreeWidget.selectedItems()
        #curRow
        if len(selectItems) > 0:
            itemRows = []
            for item in selectItems:
                curRow = self.groupTreeWidget.indexFromItem(item).row()
                curDataName = self.dataList[curRow]
                curData = self.dataDict[curDataName]
                curData.savePkList()

    def autoscale_plot(self):
#        print "Cur Group", self.curGroup
#        print "Group list", self.groupIndex
#        print "Num Groups", self.numGroups

        curAx = self.plotWidget.canvas.ax
        #self.toolbar.home() #implements the classic return to home
        curAx.autoscale_view(tight = False, scalex=True, scaley=True)
        if self.invertCompCB.isChecked() and len(self.multiPlotIndex) == 2:
            pass
        else:
            curAx.set_ylim(ymin = 0)
        self.plotWidget.canvas.draw()


    def SFDialog(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                         "Select File to Save",
                                         "",
                                         "csv Files (*.csv)")
        if not fileName.isEmpty():
            print fileName
            return str(fileName)
        else:
            return None

    def save2CSV(self):
        path = self.SFDialog()
        if path != None:
            try:
                lines = self.plotWidget.canvas.ax.get_lines()
                tempList = []
                numCols = 0
                maxLen = 0
                for line in lines:
                    if line.get_label() is not '_nolegend_':
                        x = line.get_xdata()
                        y = line.get_ydata()
                        #at times a masked array can be returned and
                        #this is incompatible with the csv writer as there is meta-data stored
                        if type(x) is N.ma.core.MaskedArray:
                            x = x.filled()
                        if type(y) is N.ma.core.MaskedArray:
                            y = y.filled()
                        tempList.append(x)
                        tempList.append(y)
                        numCols+=2 #one col for x and for y
                        curLen = len(x)
                        if curLen > maxLen:
                            maxLen = curLen

                data2write = N.zeros((numCols, maxLen))
                #need to fill in zeros with data and N.resize will not work for this
                i=0
                for data in tempList:
                    data2write[i][0:len(data)] = data
                    i+=1

                N.savetxt(path, N.transpose(data2write), delimiter = ',', fmt='%.4f')

            except:
                try:
                    #this is for the case where the data may not be in float format?
                    N.savetxt(path, N.transpose(data2write), delimiter = ',')
                except:
                    errorMsg ='Error saving figure data to csv\n\n'
                    errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                    print errorMsg
                    return QtGui.QMessageBox.warning(self, "Save Error",  errorMsg)



    def toggleCA(self, stateInt):
        if stateInt == 2:
            self.SelectPointsA()
        else:
            self.cursAClear()

    def toggleCB(self, stateInt):
        if stateInt == 2:
            self.SelectPointsB()
        else:
            self.cursBClear()

    def filterSpec(self):
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            for item in selectItems:
                if item.childCount() == 0:
                    dataName = str(item.toolTip(0))
                    self.dataDict[dataName].applyTopHat()
                #delRow = self.groupTreeWidget.indexFromItem(item).row()
                self.treeViewSelect()

    def removeFile(self):
        '''
        Need to add code to remove item from the FP treeWidget too.
        Need to remove parent when num of children == 0
        '''
#        QtGui.QTreeWidget.clear
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            for item in selectItems:
                if item.childCount() == 0:
                    parentItem = item.parent()
                    if parentItem != None:

                        delRow = parentItem.indexOfChild(item)#self.groupTreeWidget.indexFromItem(item).row()
                        delName = str(item.toolTip(0))#used because the toolTip is set to the full path which is stored in the dataDict
                        self.dataDict.pop(delName)
                        parentItem.takeChild(delRow)
                        #remove file reference from groupDict
                        if self.groupDict.has_key(str(parentItem.toolTip(0))):
                            tempItemList = self.groupDict[str(parentItem.toolTip(0))]
                            for j,name in enumerate(tempItemList):
                                if name == delName:
                                    tempItemList.pop(j)

                        #used to remove from loadSpecTreeWidget
                        foundItems = self.loadSpecTreeWidget.findItems(parentItem.text(0),QtCore.Qt.MatchExactly, 0)#take only the first item
                        fpParent = None
                        if len(foundItems) > 0:
                            fpParent = foundItems[0]
                            numChidren = fpParent.childCount()
                            for i in xrange(numChidren):
                                fpChild = fpParent.child(i)
                                if fpChild != None:
                                    if fpChild.toolTip(0) == item.toolTip(0):#check to see if it is the same file
                                        delFPRow = fpParent.indexOfChild(fpChild)
                                        fpParent.takeChild(delFPRow)
    #                                    fpParent.removeChild(fpChild)
                                        i = numChidren

                        #if the number of children reaches zero--remove item
                        if parentItem.childCount() == 0:
                            self.groupDict.pop(str(parentItem.toolTip(0)))
                            topIndex = self.groupTreeWidget.indexOfTopLevelItem(parentItem)
                            self.groupTreeWidget.takeTopLevelItem(topIndex)

                        if fpParent != None:
                            if fpParent.childCount() == 0:
                                topIndex = self.loadSpecTreeWidget.indexOfTopLevelItem(fpParent)
                                self.loadSpecTreeWidget.takeTopLevelItem(topIndex)

            self.updateGUI()

    def specListSelect(self, widgetItem=None):
        if self.ignoreSignal:
            return
        else:
            selectItems = self.specListWidget.selectedItems()
            #curRow
            if len(selectItems) > 0:
                self.multiPlotIndex = []#reset indexes to plot
                for item in selectItems:
                    self.multiPlotIndex.append(self.specListWidget.indexFromItem(item).row())

                self.plotByIndex(multiPlot = True)


    def updatePlotIndex(self):
        self.indexSpinBox.setValue(self.indexHSlider.value())
        self.plotByIndex(self.indexSpinBox.value())

    def updatePlot(self, index):
        if self.ignoreSignal:
            return
        else:
            self.initIndex = index
            QtCore.QTimer.singleShot(500,  self.plotByIndex)

    def fetchEIC(self):
        if len(self.dataList) == 0:
            return QtGui.QMessageBox.warning(self, "No Data Are Loaded",  "Try Loading a Data Set Again!")
        mzLo = self.mzLo_SB.value()
        mzHi = self.mzHi_SB.value()
        if mzHi != -1 and mzHi < mzLo:
            return QtGui.QMessageBox.warning(self, "EIC Range Error",  "m/z Hi is larger than m/z Lo\nCheck the ranges!")
        else:
            self.curEIC = []
            for curDataName in self.dataList:
                tempData = self.dataDict[curDataName]
                eicVal = tempData.getEICVal(mzLo, mzHi)
                self.curEIC.append(eicVal)

            if len(self.curEIC) != 0:
                eicPlot = MPL_Widget()
                eicPlot.setWindowTitle('Loaded Data EIC')

                ax1 = eicPlot.canvas.ax
                plotTitle = 'EIC from %.2f to %.2f'%(mzLo, mzHi)
                ax1.set_title(plotTitle)
                ax1.title.set_fontsize(10)
                ax1.set_xlabel('Data Index', fontstyle = 'italic')
                ax1.set_ylabel('Intensity')
                ax1.plot(self.curEIC)

                eicPlot.show()
                self.eicPlots.append(eicPlot)

    def plotCurData(self, curData, curAx):
        #test to see if noise has been calculated, if not do it and then plot.
        if self.plotNoiseEst_CB.isChecked():
            if curData.noiseOK:
                curData.plot(curAx, pColor = self.plotColor, plotNoise = True, plotPks = self.plotPkListCB.isChecked())#, labelPks = False)
            else:
                numSegs = len(curData.x)/self.noiseFactor_SB.value()
                minSNR = self.snrNoiseEst_SB.value()
                curData.getNoise(numSegs,minSNR)
                curData.plot(curAx, pColor = self.plotColor, plotNoise = True, plotPks = self.plotPkListCB.isChecked())#, labelPks = False)
        else:
            curData.plot(curAx, pColor = self.plotColor)#, labelPks = False)

    def plotByIndex(self, plotIndex=None,  multiPlot = False):
        curDataName = None
        if self.loadOk:
            curAx = self.plotWidget.canvas.ax
            curAx.cla()
            self.labelPks = self.plotPkListCB.isChecked()

            self.plotColorIndex = 0
            if multiPlot:
                if self.invertCompCB.isChecked() and len(self.multiPlotIndex) == 2:
                    self._updatePlotColor_()
                    curDataName = self.dataList[self.multiPlotIndex[0]]
                    self.dataDict[curDataName].plot(curAx, pColor = self.plotColor)
                    self._updatePlotColor_()
                    curDataName = self.dataList[self.multiPlotIndex[1]]
                    self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, invert = True)
                else:
                    for i in self.multiPlotIndex:
                        self._updatePlotColor_()
                        curDataName = self.dataList[i]
                        curData = self.dataDict[curDataName]
                        self.plotCurData(curData, curAx)
#                        curData.plot(curAx, pColor = self.plotColor)
                    #the following makes it so the change is ignored and the plot does not update
                    self.specNameEdit.setText(curData.path)#use dataList to get the name?
                    self.ignoreSignal = True
                    self.indexHSlider.setValue(i)
                    self.indexSpinBox.setValue(i)
                    self.ignoreSignal = False
            else:
                if plotIndex == None:
                    plotIndex = self.initIndex
                if plotIndex == self.indexSpinBox.value():#this is just to see if the user is still sliding things around before updating plot
                    self._updatePlotColor_()
                    curDataName = self.dataList[plotIndex]
                    curData = self.dataDict[curDataName]
                    #test to see if noise has been calculated, if not do it and then plot.
#                    print self.plotNoiseEst_CB.isChecked()
                    self.plotCurData(curData, curAx)

#                    if self.plotNoiseEst_CB.isChecked():
#                        if curData.noiseOK:
#                            curData.plot(curAx, pColor = self.plotColor, plotNoise = True)#, labelPks = False)
#                        else:
#                            numSegs = len(curData.x)/self.noiseFactor_SB.value()
#                            minSNR = self.snrNoiseEst_SB.value()
#                            curData.getNoise(numSegs,minSNR)
#                            curData.plot(curAx, pColor = self.plotColor, plotNoise = True)#, labelPks = False)
#                    else:
#                        curData.plot(curAx, pColor = self.plotColor)#, labelPks = False)
                    self.specNameEdit.setText(curData.path)#use dataList to get the name?
                    #the following makes it so the change is ignored and the plot does not update
                    self.ignoreSignal = True
                    self.specListWidget.setCurrentRow(plotIndex)
                    self.ignoreSignal = False
            if self.plotLegendCB.isChecked():
                curAx.legend(axespad = 0.03, pad=0.25)
            try:
                minX = curAx.get_lines()[0].get_xdata()[0]
                self.addPickers(minX)
            except:
                errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg
                self.addPickers()
            #used so that the scales will not be wonkey
            if multiPlot:
                if self.invertCompCB.isChecked() and len(self.multiPlotIndex) == 2:
                    pass
                else:
                    curAx.set_ylim(ymin = 0)
            else:
                curAx.set_ylim(ymin = 0)
            self.curDataName = curDataName
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
            self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom

    def makeUserScale(self):
        self.startScale = self.scaleStart_SB.value()
        self.endScale = self.scaleStop_SB.value()
        self.scaleFactor = self.scaleFactor_SB.value()
        try:
            self.scales = N.arange(self.startScale, self.endScale, self.scaleFactor)
        except:
            QtGui.QMessageBox.warning(self, "Error creating Scales",  "Scale Start must be less than Scale End\n and the Scale Factor fall between.\nUsing Defaults.")
            self.scales = N.arange(2,64,8)

        if len(self.scales) < 1:
            QtGui.QMessageBox.warning(self, "Error creating Scales",  "You Created and Empty Scale\nUsing Defaults.")
            self.scales = N.arange(2,64,8)
        self.setupScaleTable()

    def scaleSetup(self, value=None):
#        print value
        if value == 2:
            self.scaleStart_SB.setEnabled(False)
            self.scaleStartLbl.setEnabled(False)
            self.scaleEndLbl.setEnabled(False)
            self.scaleStop_SB.setEnabled(False)
            self.scaleFactorLbl.setEnabled(False)
            self.scaleFactor_SB.setEnabled(False)
            self.makeScales_Btn.setEnabled(False)

            self.scales = N.arange(2,64,8)
            self.setupScaleTable()

        elif value == 0:
            self.scaleStart_SB.setEnabled(True)
            self.scaleStartLbl.setEnabled(True)
            self.scaleEndLbl.setEnabled(True)
            self.scaleStop_SB.setEnabled(True)
            self.scaleFactorLbl.setEnabled(True)
            self.scaleFactor_SB.setEnabled(True)
            self.makeScales_Btn.setEnabled(True)

            self.makeUserScale()
        else:
            self.scales = N.arange(2,64,8)
            self.setupScaleTable()

    def setupScaleTable(self):
        self.scalesTable.clear()
        self.scalesTable.setColumnCount(1)
        self.scalesTable.setRowCount(len(self.scales))
        for i,scale in enumerate(self.scales):
            newitem = QtGui.QTableWidgetItem(0)
            newitem.setData(0,QtCore.QVariant(scale))
            self.scalesTable.setItem(i,0,newitem)

    def setupPeakPick(self):
        self.progressMax = 0
        self.staticThresh = self.staticCutoff_SB.value()
        self.noiseSplitFactor = self.noiseFactor_SB.value()#default 10
        self.snrNoiseEst = self.snrNoiseEst_SB.value()#default 3
        self.minRows = self.minRow_SB.value()#default 1
        self.minClust = self.minClust_SB.value() #default is 4
        self.rowThresh = self.waveletRowTol_SB.value()
        self.dbScanEPS = self.dbscanEPS_SB.value() #default -1 for auto calculate
        self.autoSavePks = self.autoSavePkList_CB.isChecked()
        if self.dbScanEPS == -1:
            self.dbScanEPS = None#this is done because if no EPS is passed autocalculate is enabled.
        self.scales = None

        self.peakParams = {'scales':None,
                          'minSNR':None,
                          'minRow':None,
                          'minClust':None,
                          'dbscanEPS':None,
                          'noiseFactor':None,
                          'rowThresh':None,
                          'staticThresh':None,
                          'autoSave':None
                          }


    def startPeakThread(self, dataItemList, dataItemDict=None):
        self.noiseSplitFactor = self.noiseFactor_SB.value()#default 10
        self.snrNoiseEst = self.snrNoiseEst_SB.value()#default 3
        self.minRow = self.minRow_SB.value()#default 1
        self.minClust = self.minClust_SB.value() #default is 4
        self.dbScanEPS = self.dbscanEPS_SB.value() #default -1 for auto calculate
        self.rowThresh = self.waveletRowTol_SB.value()
        self.noiseSplitFactor = self.noiseFactor_SB.value()
        self.staticThresh = self.staticCutoff_SB.value()
        self.autoSavePks = self.autoSavePkList_CB.isChecked()
        if self.dbScanEPS == -1:
            self.dbScanEPS = None#this is done because if no EPS is passed autocalculate is enabled.
        if self.scales != None:
            if len(self.scales) > 0:
                self.peakParams = {'scales':self.scales,
                                  'minSNR':self.snrNoiseEst,
                                  'minRow':self.minRow,
                                  'minClust':self.minClust,
                                  'rowThresh':self.rowThresh,
                                  'noiseFactor':self.noiseSplitFactor,
                                  'dbscanEPS':self.dbScanEPS,
                                  'staticThresh':self.staticThresh,
                                  'autoSave':self.autoSavePks
                                  }
#                for # need to get dataItemList self.dataDict[curDataName]
                print self.peakParams
                if self.FPT.updateThread(dataItemList, self.peakParams):
                    self.toggleProgressBar(True)
                    self.progressMax = N.float(len(dataItemList))
                    print self.progressMax
                    self.FPT.start()


    def findPeaks(self):
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            dataItemList = []#reset indexes to peak Pick
            for item in selectItems:
                if item.childCount() == 0:
                    curRow = self.groupTreeWidget.indexFromItem(item).row()
                    curDataName = str(item.toolTip(0))
                    curData = self.dataDict[curDataName]
    #                print curData.noiseOK
                    dataItemList.append(curData)
                #peakPickIndex.append(self.groupTreeWidget.indexFromItem(item).row())
            self.startPeakThread(dataItemList)
            return True
#            print "Find Peaks"





    ###########Peak Label#########################
    def labelPeak(self):
        mplAx = self.plotWidget.canvas.ax
        if self.cAOn:
            x = self.cursorAInfo[1]
            y = self.cursorAInfo[2]
            mplAx.text(x, y*1.05, '%.4f'%x,  fontsize=8, rotation = 45)

#        if self.cBOn:
#            x = self.cursorBInfo[1]
#            y = self.cursorBInfo[2]
#            mplAx.text(x, y*1.05, '%.4f'%x,  fontsize=8, rotation = 45)

    ##########Saving canvas to Clipboard
    def mpl2Clip(self):
        self.plotWidget.mpl2Clip()
        print "GO Clipboard"

        #########  Index Picker  ###############################

    def closeEvent(self,  event = None):
        if len(self.eicPlots) > 0:
            for plot in self.eicPlots:
                if isinstance(plot, MPL_Widget):
                    try:
                        plot.close()
                    except:
                        pass
        if len(self.fingerPlots)>0:
            for plot in self.fingerPlots:
                if isinstance(plot, Finger_Widget):
                    try:
                        plot.close()
                    except:
                        pass

    def setupPlot(self):
        self.cAPicker = None
        self.cBPicker = None

        self.cAOn = False#also used for picker
        self.cBOn = False

        self.cursorAInfo=[0, 0, 0, 0]
        self.cursorBInfo=[0, 0, 0, 0]

        self.indexA = 0
        self.indexB = 0

        self.dx = 0
        self.dy = 0

        self.addPickers()

    def addPickers(self, minX = 0):
        #minX is provided so that the plot will scale correctly when a data trace is initiated
        self.selectHandleA,  = self.plotWidget.canvas.ax.plot([minX], [0], 'o',\
                                        ms=8, alpha=.4, color='yellow', visible=False,  label = '_nolegend_')
        self.selectHandleB,  = self.plotWidget.canvas.ax.plot([minX], [0], 's',\
                                        ms=8, alpha=.4, color='green', visible=False,  label = '_nolegend_')

    def cursAClear(self):
        if self.cAOn:# and self.cAPicker:
            self.selectHandleA.set_visible(False)
            self.plotWidget.canvas.mpl_disconnect(self.cAPicker)
            self.cAOn = False
            self.cAPicker = None
            self.cALabelLE.setText('')
            self.cAIndexLE.setText('')
            self.cA_XLE.setText('')
            self.cA_YLE.setText('')

            self.dxLE.setText('')
            self.dyLE.setText('')

            try:#this is so that the cursor label gets removed
                self.cursAText.remove()
            except:
                pass

            self.plotWidget.canvas.draw()


    def cursBClear(self):
        if self.cBOn:# and self.cBPicker:
            self.selectHandleB.set_visible(False)
            self.plotWidget.canvas.mpl_disconnect(self.cBPicker)
            self.cBOn = False
            self.cBPicker = None
            self.cBLabelLE.setText('')
            self.cBIndexLE.setText('')
            self.cB_XLE.setText('')
            self.cB_YLE.setText('')

            self.dxLE.setText('')
            self.dyLE.setText('')

            try:#this is so that the cursor label gets removed
                self.cursBText.remove()
            except:
                pass

            self.plotWidget.canvas.draw()


    def cursorClear(self):
        self.cursACB.nextCheckState()
        self.cursBCB.nextCheckState()#setCheckState(0)
        self.cursAClear()
        self.cursBClear()

    def cursorStats(self):
        if self.cAOn:
            self.cALabelLE.setText(self.cursorAInfo[3])
            self.cAIndexLE.setText(str(self.cursorAInfo[0]))
            self.cA_XLE.setText('%.4f'%self.cursorAInfo[1])
            self.cA_YLE.setText('%.4f'%self.cursorAInfo[2])

        if self.cBOn:
            self.cBLabelLE.setText(self.cursorBInfo[3])
            self.cBIndexLE.setText(str(self.cursorBInfo[0]))
            self.cB_XLE.setText('%.4f'%self.cursorBInfo[1])
            self.cB_YLE.setText('%.4f'%self.cursorBInfo[2])

        if self.cAOn and self.cBOn:
            self.dx = self.cursorAInfo[1]-self.cursorBInfo[1]
            self.dy = self.cursorAInfo[2]-self.cursorBInfo[2]
            self.dxLE.setText('%.4f'%self.dx)
            self.dyLE.setText('%.4f'%self.dy)
            #return True

    def SelectPointsA(self):
        """
        This method will be called from the plot context menu for
        selecting points
        """
        self.plotWidget.canvas.mpl_disconnect(self.cBPicker)
        self.cBPicker = None
        if self.cAPicker ==None:
            self.cAPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickA)
            self.cAOn = True


    def SelectPointsB(self):

        self.plotWidget.canvas.mpl_disconnect(self.cAPicker)
        self.cAPicker = None
        if self.cBPicker == None:
            self.cBPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickB)
            self.cBOn = True

    def OnPickA(self, event):
        """
        This is the pick_event handler for matplotlib
        This is the pick_event handler for matplotlib
        This method will get the coordinates of the mouse pointer and
        finds the closest point and retrieves the corresponding peptide sequence.
        Also draws a yellow circle around the point.--from Ashoka 5/29/08
        """

        #print "Pick A"
        if not isinstance(event.artist, Line2D):
            return True

        try:#this is so that the cursor label gets removed
            self.cursAText.remove()
        except:
            pass

        line = event.artist
        self.indexA = event.ind[0]
        xdata = line.get_xdata()
        ydata = line.get_ydata()

        self.selectHandleA.set_data([xdata[self.indexA]], [ydata[self.indexA]])
        self.selectHandleA.set_visible(True)

        self.cursAText = self.plotWidget.canvas.ax.text(xdata[self.indexA], ydata[self.indexA], '%.4f'%xdata[self.indexA],  fontsize=9, rotation = 45)

        self.cursorAInfo[0]=self.indexA
        self.cursorAInfo[1]=xdata[self.indexA]
        self.cursorAInfo[2]=ydata[self.indexA]
        self.cursorAInfo[3]=line.get_label()
        self.cursorStats()

        self.plotWidget.canvas.draw()

        #print self.cursorAInfo

    def OnPickB(self, event):
        #print "Pick B"
        if not isinstance(event.artist, Line2D):
            return True

        try:#this is so that the cursor label gets removed
            self.cursBText.remove()
        except:
            pass

        line = event.artist
        self.indexB = event.ind[0]
        xdata = line.get_xdata()
        ydata = line.get_ydata()

        self.selectHandleB.set_data([xdata[self.indexB]], [ydata[self.indexB]])
        self.selectHandleB.set_visible(True)

        self.cursBText = self.plotWidget.canvas.ax.text(xdata[self.indexB], ydata[self.indexB], '%.4f'%xdata[self.indexB],  fontsize=9, rotation = 45)

        self.cursorBInfo[0]=self.indexB
        self.cursorBInfo[1]=xdata[self.indexB]
        self.cursorBInfo[2]=ydata[self.indexB]
        self.cursorBInfo[3]=line.get_label()
        self.cursorStats()

        self.plotWidget.canvas.draw()

        #print self.cursorAInfo

        ###############################

##########Begin Ashoka Progress Bar Code....
    def layoutStatusBar(self):
        self.progressBar = QtGui.QProgressBar()
        self.statusLabel = QtGui.QLabel("Ready")
#        self.statusLabel.setMinimumSize(self.statusLabel.sizeHint())
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.statusLabel.setText("Ready")
        self.statusbar.addPermanentWidget(self.statusLabel)
        self.progressBar.setTextVisible(False)
        self.progressBar.setRange(0,100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedHeight(15)
        self.progressBar.setFixedWidth(100)
        self.toggleProgressBar(False)
        self.statusbar.addWidget(self.progressBar)

    def resetProgressBar(self):
        self.setProgressValue(0)
        self.toggleProgressBar(False)

    def setStatusLabel(self, text):
        self.statusLabel.setText(text)

    def showStatusMessage(self, text, stime):
        self.statusBar().showMessage(text, stime)

    def setProgressValue(self, val):
        self.progressBar.setValue(val)

    def toggleProgressBar(self, toggle):
        self.progressBar.setVisible(toggle)

    def threadProgress(self, progVal):
        print progVal
        self.setStatusLabel("Fitting Peaks, %d spectra completed." % progVal)
        newVal = int(100*(progVal/self.progressMax))
        self.setProgressValue(newVal)
#        self.AddMessage2Tab("  %d Iterations Done." % progVal)
#        print progVal, newVal, self.progressMax

    def PCTProgress(self, updateString):
        self.setStatusLabel(updateString)


class LoadThread(QtCore.QThread):
        def __init__(self, parent = None):
            QtCore.QThread.__init__(self, parent)

            self.finished = False
            self.ready = False
            self.loadmzXML = False

        def updateThread(self, loadList, loadmzXML = False):
            self.loadList = loadList
            self.loadmzXML = loadmzXML
            self.numItems = len(loadList)
            self.ready = True
            return True

        def run(self):
            if self.ready:
                if self.loadmzXML:
                    while not self.finished and self.numItems > 0:
                        for item in self.loadList:
#                            print os.path.basename(item)
                            tempmzXML =  mzXMLR(item)
                            tempSpec = tempmzXML.data['spectrum']
                            if len(tempSpec)>0:
#                                print 'Spec OK', os.path.basename(item)
                                data2plot = DataClass(tempSpec[0],  tempSpec[1],  name = os.path.basename(item), path = item)
                                data2plot.setPeakList(tempmzXML.data['peaklist'], normalized = False)
                                #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                                #note PyQt_PyObject
                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)
                            else:
                                print 'Empty spectrum: ', item

                            self.numItems -=1
                        self.emit(QtCore.SIGNAL("finished(bool)"),True)


                else:
                    while not self.finished and self.numItems > 0:
                        for item in self.loadList:
                            tempFlex = FR(item)
                            tempSpec = tempFlex.data['spectrum']
                            data2plot = DataClass(tempSpec[:, 0],  tempSpec[:, 1], name = item.split(os.path.sep)[-4], path = item)#the -4 index is to handle the Bruker File Structure
                            data2plot.setPeakList(tempFlex.data['peaklist'],  nomralized = False)
                            #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                            self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)#note PyQt_PyObject
                            self.numItems -=1

        def __del__(self):
            self.exiting = True
            self.wait()


class FindPeaksThread(QtCore.QThread):
        def __init__(self, parent = None):
            QtCore.QThread.__init__(self, parent)

            self.finished = False
            self.ready = False
            self.cwt = None
            self.numItems = None
            self.iteration = 0
            self.dataItemList = None
#            self.dataItemDict = None
            self.dataList = None
            self.xData = None
            self.yData = None
            self.paramDict = {'scales':None,
                              'minSNR':None,
                              'minRow':None,
                              'minClust':None,
                              'dbscanEPS':None,
                              'rowThresh':None,
                              'noiseFactor':None,
                              'staticThresh':None,
                              'autoSave':None
                              }

        def updateThread(self, dataItemList, paramDict):
            self.iteration = 0
            self.dataItemList = dataItemList
#            self.dataItemDict = dataItemDict
            self.numItems = len(self.dataItemList)
            self.paramDict = paramDict
            self.scales = self.paramDict['scales']
            self.minSNR = self.paramDict['minSNR']
            self.minRow = self.paramDict['minRow']
            self.noiseFactor = self.paramDict['noiseFactor']
            self.minClust = self.paramDict['minClust']
            self.rowThresh = self.paramDict['rowThresh']
            self.EPS = self.paramDict['dbscanEPS']
            self.staticThresh = self.paramDict['staticThresh']
            self.autoSave = self.paramDict['autoSave']
            self.ready = True
            return True

        def run(self):
            if self.ready:
                t0 = time.clock()
                for dataItem in self.dataItemList:
#                    dataItem = self.dataItemDict[name]

#                    print "Length of Y: ", len(dataItem.y)
#                    print "Thresh: ", self.staticThresh/dataItem.normFactor, dataItem.normFactor, self.staticThresh
                    self.cwt = CWT.cwtMS(dataItem.y, self.scales, staticThresh = (self.staticThresh/dataItem.normFactor)*100)
                    if self.cwt != None:
                        if not dataItem.noiseOK:
                            numSegs = len(dataItem.x)/self.noiseFactor
                            dataItem.getNoise(numSegs,self.minSNR)
                        #static Thresh is scaled for each individual spectrum and uses the normFactor or maximum of the
                        # Y values to compute where a spectrum should be cut
                        cwtResult = CWT.getCWTPeaks(self.cwt, dataItem.x, dataItem.y,\
                                                    dataItem.noiseEst, minSNR = self.minSNR,\
                                                    minRow = self.minRow, minClust =self.minClust,\
                                                    rowThresh = self.rowThresh, pntPad = dataItem.mzPad,\
                                                    minNoiseEst = dataItem.minNoiseEst,\
                                                    staticThresh = self.staticThresh/dataItem.normFactor,\
                                                    EPS = self.EPS)

#                        def getCWTPeaks(scaledCWT, X, Y, noiseEst, minSNR = 3,\
#                                        minRow = 3, minClust = 4, rowThresh = 3,\
#                                        pntPad = 50, staticThresh = 0.2, minNoiseEst = 0.025,
#                                        EPS = None):

                        peakLoc, peakInt, cwtPeakLoc, cClass, boolAns = cwtResult

                        if boolAns:
                            if cClass != None:
                                if len(peakLoc) != 0:
                                    print peakLoc
                                    dataItem.setPeakList(N.column_stack((peakLoc,peakInt)))
                                    dataItem.pkListOk = boolAns
                                    if self.autoSave:
                                        dataItem.savePkList()
                                    self.numItems += -1
                                    self.iteration +=1
                                    self.emit(QtCore.SIGNAL("progress(int)"),self.iteration)
                                    self.ready = False
                            else:
                                print "Error with Peak Picking"
                                self.emit(QtCore.SIGNAL("returnPeakList(PyQt_PyObject)"),None)
                    ##############
                    #need to emit a signal that the process is finished here
                    #which tells the program which item to replot
                    ##############

                    else:
                        print "Error with CWT"
                        self.emit(QtCore.SIGNAL("returnPeakList(PyQt_PyObject)"),None)
                #emit finished signal
                print "Peak Find Time: ", time.clock()-t0
                self.emit(QtCore.SIGNAL("finished(bool)"),True)

#                    while not self.finished and self.numItems > 0:
#                        for item in self.loadList:
#                            tempFlex = FR(item)


        def __del__(self):
            self.exiting = True
            self.wait()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())
