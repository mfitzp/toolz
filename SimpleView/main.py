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
"labelpeaks":self.labelPeak_CB,
"mzhi":self.mzHi_SB,
"mzlo":self.mzLo_SB,
"excludelift":self.excludeLIFTCB,
"loadmzxml":self.loadmzXMLCB,
"autoloadfp":self.autoLoadFP_CB
"fpdir":self.fpFolder_LE
"datadir": #Not used
}

add updated pref for comboBox and label peaks

PCA after peak pick

Setup Group Class
Group Display

Double check peakfind thread

make fingerprint folder work
fix topHat, threadit?
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
import scipy.stats as stats
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
import customTable as CT

import pca_module as pca#courtesy of Henning Risvik http://folk.uio.no/henninri/pca_module/

import ui_main
import fingerPrint as FP

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

MARKERS = ['o', 'd','>', 's', '^',  'p', '<', 'h', 'v']

class Plot_Widget(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.setupVars()
        self.readThread = LoadThread(parent = self)
        self.FPT = FindPeaksThread()
        self.initConnections()
        self.setupGUI()
        self.loadPrefs()
        self.setupPlot()
        self.layoutStatusBar()


    def initConnections(self):
        '''
        Initiates all of the GUI connections
        '''
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

        self.addFileAction = QtGui.QAction("Add File", self)
        self.groupTreeWidget.addAction(self.addFileAction)

        self.topHatAction = QtGui.QAction("Apply TopHat",  self)
        self.groupTreeWidget.addAction(self.topHatAction)

        self.findPeakAction = QtGui.QAction("Find Peaks", self)
        self.groupTreeWidget.addAction(self.findPeakAction)

        self.selectAllAction = QtGui.QAction("Select All", self)
        self.groupTreeWidget.addAction(self.selectAllAction)

        self.selectGroupAction = QtGui.QAction("Select Group", self)
        self.groupTreeWidget.addAction(self.selectGroupAction)

        self.saveCSVAction = QtGui.QAction("Save to CSV", self)
        self.saveCSVAction.setShortcut("Ctrl+Alt+S")
        self.plotWidget.addAction(self.saveCSVAction)

        self.savePksAction = QtGui.QAction("Save Peak List", self)
        self.groupTreeWidget.addAction(self.savePksAction)

        self.initFPAction = QtGui.QAction("Create FP(s)", self)
        self.groupTreeWidget.addAction(self.initFPAction)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

        self.reviewFPAction = QtGui.QAction("Revise Fingerprint",  self)
        self.fpListWidget.addAction(self.reviewFPAction)
        QtCore.QObject.connect(self.reviewFPAction,QtCore.SIGNAL("triggered()"), self.reviewFP)

        self.viewFPMetaAction = QtGui.QAction("View FP Meta-data",  self)
        self.fpListWidget.addAction(self.viewFPMetaAction)
        QtCore.QObject.connect(self.viewFPMetaAction,QtCore.SIGNAL("triggered()"), self.viewFPMeta)

        QtCore.QObject.connect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)

        QtCore.QObject.connect(self.removeAction, QtCore.SIGNAL("triggered()"),self.removeFile)
        QtCore.QObject.connect(self.addFileAction, QtCore.SIGNAL("triggered()"),self.addSingleFile)
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
        QtCore.QObject.connect(self.selectGroupAction,QtCore.SIGNAL("triggered()"),self.selectAllInGroup)

        QtCore.QObject.connect(self.FPT, QtCore.SIGNAL("progress(int)"), self.threadProgress)
        QtCore.QObject.connect(self.FPT, QtCore.SIGNAL("finished(bool)"), self.PFTFinished)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished(bool)"), self.readFinished)

#        QtCore.QObject.connect(self.groupTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.treeItemSelected)
        QtCore.QObject.connect(self.groupTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.treeViewSelect)
        QtCore.QObject.connect(self.initFPAction,QtCore.SIGNAL("triggered()"),self.initFP)

        #FingerPrint Related Connections:
        QtCore.QObject.connect(self.expand_Btn, QtCore.SIGNAL("clicked()"), self.expandFPSpectra)
        QtCore.QObject.connect(self.testFocus_Btn, QtCore.SIGNAL("clicked()"), self.testFocus)
        QtCore.QObject.connect(self.fpListWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.fpListSelect)

        QtCore.QObject.connect(self.loadFP_Btn, QtCore.SIGNAL("clicked()"), self.loadFPfromHDF5)
        QtCore.QObject.connect(self.savePref_Btn, QtCore.SIGNAL("clicked()"), self.savePrefs)
        QtCore.QObject.connect(self.revert_Btn, QtCore.SIGNAL("clicked()"), self.defaultRevert)

        QtCore.QObject.connect(self.doFP_Btn, QtCore.SIGNAL("clicked()"), self.compareFP)
        QtCore.QObject.connect(self.doPCA_Btn, QtCore.SIGNAL("clicked()"), self.fpPCA)
        QtCore.QObject.connect(self.fpFolder_Btn, QtCore.SIGNAL("clicked()"), self.setDefaultFPDir)



        QtCore.QObject.connect(self.peakSetting_CB, QtCore.SIGNAL("currentIndexChanged(QString)"), self.peakComboChanged)

        self.useDefaultScale_CB.nextCheckState()




    def setDefaultFPDir(self):
        '''
        Sets the default directory for where the fingerprints are stored. An attempt is made to load the fingerprints
        into memory.  Be careful how the preferences are set.  If the load RAW FP check box is activated then
        a whole lotta memory could be used up fast!
        '''
        if self.fpDir != None:
            fpDir = self.fpDir
        else:
            fpDir = self.curDir
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', fpDir)
        directory = str(directory)
        if directory != None:
            self.fpDir = os.path.abspath(directory)
            self.fpFolder_LE.setText(self.fpDir)
            return True
        else:
            self.fpDir = None
            return False

    def peakComboChanged(self, selectedStr):
        '''
        Changes to pre-set values for peak picking
        '''
        selectedStr = str(selectedStr)
        settingsKey = {'Low SNR':0,
                       'Med SNR':1,
                       'High SNR':2
                       }
        selIndex = settingsKey[selectedStr]

        defaultParams = {'minSNR':[1,3,10],
                         'minRow':[1,1,2],
                         'minClust':[3,4,4],
                         'rowThresh':[4,3,3],
                         'staticThresh':[50,100,200],
                         }

        self.snrNoiseEst_SB.setValue(defaultParams['minSNR'][selIndex])#default 3
        self.minRow_SB.setValue(defaultParams['minRow'][selIndex])#default 1
        self.minClust_SB.setValue(defaultParams['minClust'][selIndex]) #default is 4
        self.waveletRowTol_SB.setValue(defaultParams['rowThresh'][selIndex])
        self.staticCutoff_SB.setValue(defaultParams['staticThresh'][selIndex])


    def fpPCA(self):
        '''
        Perform a PCA for the selected fingerprints.

            peakStatDict = {'aveLoc':[],
                    'stdLoc':[],
                    'aveInt':[],
                    'stdInt':[],
                    'numMembers':[],
                    'freq':[],
                    'mzTol':[],
                    'stdDevTol':[],
                    'numTot':[]
        '''
        try:
            self.fpListWidget.selectAll()
            selectItems = self.fpListWidget.selectedItems()
            fpList = []
            if len(selectItems) > 0:
                for item in selectItems:
                    if item.checkState() == 2:#Case when it is checked
                        fpList.append(str(item.text()))

                mzXVals = []
                mzStd = []
                mzYVals = []
                numVals = []
                freqCutoff = self.freqCutoff_SB.value()
                if len(fpList) < 3:
                    errMsg = "You are attempting to compare too few categories!\nTry selecting more fingerprints or plot these data\n in a different manner."
                    return QtGui.QMessageBox.warning(self, "PCA Not Advised", errMsg)
                for fpName in fpList:
                    curFPDict = self.fpDict[fpName]
                    curStats = curFPDict['peakStats']
                    fpFreq = curStats['freq']
                    validInd = N.where(fpFreq>=freqCutoff)[0]
                    fpFreq = fpFreq[validInd]
                    fpPeakLoc = curStats['aveLoc'][validInd]
                    fpPeakInt = curStats['aveInt'][validInd]
                    fpStdLoc = curStats['stdLoc'][validInd]
                    fpNum = curStats['numTot'][validInd]
                    if len(fpPeakLoc)>1:
                        mzXVals.append(fpPeakLoc)
                        mzYVals.append(SF.normalize(fpPeakInt))
                        mzStd.append(fpStdLoc)
                        numVals.append(fpNum)

                mzXVals = N.array(SF.flattenX(mzXVals))
                mzYVals = N.array(SF.flattenX(mzYVals))
                mzStd = N.array(SF.flattenX(mzStd))
                numVals = N.array(SF.flattenX(numVals))

                mzOrder = mzXVals.argsort()
                mzXVals = mzXVals[mzOrder]
                mzYVals = mzYVals[mzOrder]
                mzStd = mzStd[mzOrder]
                numVals = numVals[mzOrder]

    #            pcaXCrit, pcaStdCrit, pcaNum = self.makePCACrit(mzXVals, xStdTest, yTest, numTest)
                pcaXCrit, pcaStdCrit, pcaNum = self.makePCACrit(mzXVals, mzStd, mzYVals, numVals)
                self.makePCAMtx(pcaXCrit, pcaStdCrit, pcaNum, fpList)
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            return QtGui.QMessageBox.warning(self, "FP PCA", errorMsg)
            print errorMsg


    def makePCAMtx(self, pcaXCrit, pcaStdCrit, pcaNum, fpNameList):
        '''
        make matrix for PCA

                      x1   x2   x3   x4  --m/z Values
        FP Names

        item 1        0    1    0    0
        item 2        1    0    1    1
        item 3        0    1    0    0
        item 4        0    0    0    1

        1-present
        0-absent

        '''
        mzTolPPM = 500/1000000#500ppm cutoff
        freqCutoff = self.freqCutoff_SB.value()

        numCrit = len(pcaXCrit)
        numItems = len(fpNameList)
        pcaStdCrit*=3#3 times the stdev

        pcaMtx = N.zeros((numItems,numCrit))

        for i,fpName in enumerate(fpNameList):
            curFPDict = self.fpDict[fpName]
            curStats = curFPDict['peakStats']
            fpFreq = curStats['freq']
            validInd = N.where(fpFreq>=freqCutoff)[0]
            fpFreq = fpFreq[validInd]
            fpPeakLoc = curStats['aveLoc'][validInd]
            fpPeakInt = curStats['aveInt'][validInd]
            fpStdLoc = curStats['stdLoc'][validInd]
            fpNum = curStats['numTot'][validInd]

            print "Comp Loc", fpPeakLoc
            for j,xVal in enumerate(fpPeakLoc):
                xStd = fpStdLoc[j]
                xNum = fpNum[j]
                for m,pcaXVal in enumerate(pcaXCrit):
                    pcaXStd = pcaStdCrit[m]
                    diff = N.abs(pcaXVal-xVal)
                    tErr = N.sqrt((xStd**2/xNum)+(pcaXStd**2/pcaNum[m]))
                    maxDiff = N.max(diff, mzTolPPM*xVal)
                    tVal = N.abs(maxDiff/tErr)
                    tCrit = stats.t.ppf(0.99, (xNum+pcaNum[m]-2))
                    if tVal < tCrit:
#                        print tVal, tCrit, xVal, pcaXVal
                        pcaMtx[i][m] = 1

        print pcaMtx
        self.plotPCA(pcaMtx, fpNameList)


    def plotPCA(self, dataMatrix, pcaLabels=None):
        scores, loading, explanation = pca.PCA_nipals2(dataMatrix, standardize=False)

        pc1 = scores[:, 0]
        pc2 = scores[:, 1]
#        pc3 = scores[:, 2]

        testPlot = MPL_Widget()
        testPlot.setWindowTitle('PCA Plot')

        ax1 = testPlot.canvas.ax
        plotTitle = 'PCA Comparison Plot'
        ax1.set_title(plotTitle)
        ax1.title.set_fontsize(10)
        ax1.set_xlabel('PCA 1')
        ax1.set_ylabel('PCA 2')

        for i,val in enumerate(pc1):
#            print val, pc2[i]
            self._updatePlotColor_()
            curMarker = self._getPlotMarker_()
            ax1.plot([val], [pc2[i]], alpha = 0.5, color = self.plotColor, marker = curMarker, ms = 10)
#        ax1.scatter(pc1, pc2, color = 'b', s = 25, alpha = 0.3)
        for label, x, y in map(None, pcaLabels, pc1, pc2):
            ax1.annotate(label, xy=(x, y),  size = 10)

        testPlot.show()
        self.eicPlots.append(testPlot)



    def weightedStats(self, vals, stds, numVals):
        '''
        Calculates the weighted mean and standard deviation
        of the passes arrays
        Returns:
        weighted value and weighted stdev
        '''
        stdErr = (1/stds**2).sum()
        valNumerator = vals/stds**2
        wX = valNumerator.sum()/stdErr
        wStd = N.sqrt(1/stdErr)
        wNum = numVals.sum()
        return wX, wStd, wNum


    def makePCACrit(self, xVals, xStd, yVals, numVals, yStd = None):
        '''
        Groups peaks together in order to make a standard list by which
        all of the peaks for each fingerprint will be compared.
        '''
        mzTolPPM = 500/1000000
        xStd *= 3

        xVals = N.array(xVals)
        xStd = N.array(xStd)
        yVals = N.array(yVals)
        numVals = N.array(numVals)

        xDiff = N.diff(xVals)
        groups = []
        tVals = N.zeros_like(xDiff)
        tCrits = N.zeros_like(xDiff)
        gNum = 0
        origNum = 0
        for i,diffVal in enumerate(xDiff):
            tErr = N.sqrt((xStd[i]**2/numVals[i])+(xStd[i+1]**2/numVals[i+1]))
            maxDiff = N.max(diffVal, mzTolPPM*xVals[i])
            tVal = N.abs(maxDiff/tErr)
            tCrit = stats.t.ppf(0.99, (numVals[i]+numVals[i+1]-2))
            if tVal < tCrit:
#                if ppmDiff <= mzTolPPM:
                groups.append(gNum)
            else:
                groups.append(gNum)
                gNum+=1
            tVals[i] =tVal
            tCrits[i] = tCrit

        groups.append(gNum)#handle last element of xVal array


#        print xVals
#        print groups
#        print tVals
#        print tCrits
        groups = N.array(groups)
        pcaXCrit = N.zeros(groups.max()+1)
        pcaStdCrit = N.zeros(groups.max()+1)
        pcaNum = N.zeros(groups.max()+1)
        for i in xrange(groups.max()+1):
            gIndex = N.where(groups == i)[0]
            gXVals = xVals[gIndex]
            gXStds = xStd[gIndex]
            gNumVals = numVals[gIndex]

            wX, wStd, wNum = self.weightedStats(gXVals, gXStds, gNumVals)
            pcaXCrit[i] = wX
            pcaStdCrit[i] = wStd
            pcaNum[i] = wNum

        print "PCA X Crit",pcaXCrit
#        print pcaStdCrit

        return pcaXCrit, pcaStdCrit, pcaNum


    def _testPlot_(self, data2plot):
        '''
        Misc function for plotting data
        '''
#        print "Test Plot Go"

        testPlot = MPL_Widget()
        testPlot.setWindowTitle('Test Plot')

        ax1 = testPlot.canvas.ax
        plotTitle = 'Composite Plot'
        ax1.set_title(plotTitle)
        ax1.title.set_fontsize(10)
        ax1.set_xlabel('m/z', fontstyle = 'italic')
        ax1.set_ylabel('Intensity')

        xValList = data2plot[0]
        yValList = data2plot[1]
        for i,xVal in enumerate(xValList):
            self._updatePlotColor_()
            yVal = yValList[i]
#            ax1.plot(self.curEIC)
            ax1.vlines(xVal, 0, yVal, color = self.plotColor)


        testPlot.show()
        self.eicPlots.append(testPlot)


    def compareFP(self):
        '''
        Compares the checked fingerprints loaded into memory with raw data loaded selected on the right
        TreeView GUI object.  See the fingerprint.py for more info on the alogorithm
        '''
        self.fpListWidget.selectAll()
        selectItems = self.fpListWidget.selectedItems()
        fpList = []
        if len(selectItems) > 0:
            for item in selectItems:
                if item.checkState() == 2:#Case when it is checked
                    fpList.append(str(item.text()))
        dataDict = {}
        selectCompItems = self.fpSpecTreeWidget.selectedItems()
        if len(selectCompItems) > 0:
#            for item in selectCompItems:
            item = selectCompItems[0]
            if item.childCount() == 0:
                dataDict[str(item.toolTip(0))] = self.dataDict[str(item.toolTip(0))]

            usrFreqCutoff = self.freqCutoff_SB.value()
            compDict = FP.createFPDict(dataDict)
            for fpName in fpList:
                curFPDict = self.fpDict[fpName]
                curProb = FP.fpCompare(curFPDict['peakStats'],compDict, alpha = self.alphaLvl_SB.value(), freqCutoff = usrFreqCutoff)
                print "%s vs. %s : %s"%(str(item.toolTip(0)), fpName, curProb)


    def defaultRevert(self):
        '''
        Load default preferences
        '''
        try:
            if os.path.isfile(self.orgPrefFileName):
                self._getPrefs_(self.orgPrefFileName)
        except:
            return QtGui.QMessageBox.warning(self, "Preferences File is Hosed", "Try Reinstalling to fix this!")

    def autoLoadFP(self):
        '''
        Recursively parse through the user specified directory and load all FP
        '''
        print self.fpDir
        if self.fpDir != None:
            fpList = []
            i=0
            for root, dirs, files in os.walk(self.fpDir):
                for file in files:
                    if 'h5' in file:
                        fpPath = os.path.abspath(os.path.join(self.fpDir, file))
                        if os.path.isfile(fpPath):
                            fpList.append(fpPath)
                            self.loadFPfromHDF5(fpPath)
#            print "Auto FP List",fpList

    def loadPrefs(self):
#        try:
        if os.path.isfile(self.prefFileName):
            self._getPrefs_(self.prefFileName)
#                print self.prefFileName
            if self.autoLoadFP_CB.isChecked():
                self.fpDir = os.path.abspath(str(self.fpFolder_LE.text()))
                self.autoLoadFP()

        else:
            return QtGui.QMessageBox.warning(self, "Load Preferences Error", "No Preference File Exists\nReverting to Defaults")
#        except:
#            self.defaultRevert()
#            return QtGui.QMessageBox.warning(self, "Load Preferences Error", "No Preference File Exists\nReverting to Defaults")

    def _setGUIPref_(self, val, valType, guiElement):
        '''
        guiElement = element to commit value to
        val = value to load into GUI
        valType = type used to determine which function to use to set the value to the GUI
        '''
        if valType == float or valType == int:
            guiElement.setValue(val)
        elif valType == bool:
            guiElement.setChecked(val)
        elif valType == str:
            guiElement.setText(val)


    def _getPrefs_(self, configFileName):
        '''
        Need to get floats and ints before bools and strings.  Otherwise
        types can get mixed
        '''
        self.prefFileStruct = {}
        config = ConfigParser.ConfigParser()
        config.read(configFileName)
        i = 0
        for section in config.sections():
            tempOptions = []
#            print '\t',config.options(section)
            for option in config.options(section):
                val = None
                valOk = False

                try:
                    if not valOk:
                        val = config.getfloat(section, option)
                        valOk = True
                except:
                    pass

                try:
                    if not valOk:
                        val = config.getint(section, option)
                        valOk = True
                except:
                    pass

                try:
                    if not valOk:
                        val = config.getboolean(section, option)
                        valOk = True
                except:
                    pass

                try:
                    if not valOk:
                        val = config.get(section, option)
                        valOk = True
                except:
                    pass

                if val != None:
                    if self.prefDict.has_key(option):
#                        print " ", option, "=", val, type(val)
                        tempOptions.append([option, type(val)])
                        self._setGUIPref_(val, type(val), self.prefDict[option])
#                    print option, self.prefDict[option]
            self.prefFileStruct[section] = tempOptions

#        print self.prefFileStruct

    def savePrefs(self):
        try:
            if len(self.prefFileStruct) != len(self.prefDict):
                config = ConfigParser.ConfigParser()
                for key in self.prefFileStruct.iterkeys():
                    config.add_section(key)
                    prefList = self.prefFileStruct[key]
                    for varList in prefList:
                        varName = varList[0]
                        guiElement = self.prefDict[varName]
                        valType = varList[1]#each varList is a list containing the variable then the variable type
                        if valType == float or valType == int:
                            val = guiElement.value()
                        elif valType == bool:
                            val = guiElement.isChecked()
                        elif valType == str:
                            val = str(guiElement.text())
                        config.set(key, varName, val)

                # write to screen
                fp = open(self.prefFileName, 'w')
                config.write(fp)
                fp.close()
#                config.

    #            print "Go"
            else:
                return QtGui.QMessageBox.warning(self, "Save Preferences Error", "Dictionary mismatch")
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            return QtGui.QMessageBox.warning(self, "Save Preferences Error", errorMsg)
            print errorMsg


    def reviewFP(self):
#        print "ReviewFP"
        selectItems = self.fpListWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]#only select one FP at a time
            print str(item.text())
            tempDataDict = self.fpDict[str(item.text())]['dataDict']
            if len(tempDataDict) > 0:
                peakStatDict = self.fpDict[str(item.text())]['peakStats']
                curFingerPlot = FP.Finger_Widget(parent = self)
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
            else:
                errorMsg = 'No raw data were loaded with this FP.\nPlease check the "Load Raw Data From FP?" box and reload.'
                return QtGui.QMessageBox.warning(self, "FP Review Error", errorMsg)

    def plotMetaPeaks(self,dTableInstance, peakData):
        curAx = dTableInstance.plotWidget.canvas.ax
        for peakList in peakData:
            curAx.plot(peakList[1], peakList[0], 'o', alpha = 0.6)
        print "MetaPeaks"

    def viewFPMeta(self):
        '''
        fpDict[self.curGroupName] = {'dataDict':dataDict, 'peakStats':peakStatDict, 'fileName':fileName, 'peakLists':peakListDict}
        peakListDict[key] = {'peakList':peakListDict[key].read(), 'params':paramDict}
        Need to add an instance where the full FP are loaded..
        '''
        selectItems = self.fpListWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]
            curFP = self.fpDict[str(item.text())]
            metaData = []
            peakData = []
            if curFP['peakLists'] != None:
                peakListInfo = curFP['peakLists']
                i = 0
                for key in peakListInfo.iterkeys():
                    curPeaks = peakListInfo[key]['peakList']
                    peakData.append([N.zeros_like(curPeaks)+i,curPeaks])
                    i+=1
                    curMeta = []
                    curMeta.append(key)
                    headers = ['File Name']

                    for paramItem in peakListInfo[key]['params'].iteritems():
                        headers.append(paramItem[0])
                        curMeta.append(str(paramItem[1]))
#                    print curMeta
                    metaData.append(curMeta)

                dTable = CT.DataTable(metaData, headers)
                self.plotMetaPeaks(dTable, peakData)
                dTable.show()
                self.fingerRevTabls.append(dTable)
#            print metaData


    def plotMetaPeaks(self,dTableInstance, peakData, dataLabels):
        curAx = dTableInstance.plotWidget.canvas.ax
        for i,peakList in enumerate(peakData):
            x = peakList[1][:,0]
            y = peakList[0][:,0]
            intensity = peakList[1][:,1]
            self._updatePlotColor_()
#            curAx.plot(x, y, 'o', alpha = 0.6)
            curAx.scatter(x,y,s = intensity, alpha = 0.6, color = self.plotColor, label = dataLabels[i])
#            label = dataLabels[i]
#            curAx.text(0,i,label)
#            curAx.legend()

        print "MetaPeaks"

    def viewFPMeta(self):
        '''
        fpDict[self.curGroupName] = {'dataDict':dataDict, 'peakStats':peakStatDict, 'fileName':fileName, 'peakLists':peakListDict}
        peakListDict[key] = {'peakList':peakListDict[key].read(), 'params':paramDict}
        Need to add an instance where the full FP are loaded..
        '''
        selectItems = self.fpListWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]
            curFP = self.fpDict[str(item.text())]
            metaData = []
            peakData = []
            dataLabels = []
            if curFP['peakLists'] != None:
                peakListInfo = curFP['peakLists']
                i = 0
                for key in peakListInfo.iterkeys():
                    curPeaks = peakListInfo[key]['peakList']
                    peakData.append([N.zeros_like(curPeaks)+i,curPeaks])
                    dataLabels.append(key.split(os.path.sep)[-1])
#                    print curPeaks
                    i+=1
                    curMeta = []
                    curMeta.append(key)
                    headers = ['File Name']

                    for paramItem in peakListInfo[key]['params'].iteritems():
                        headers.append(paramItem[0])
                        curMeta.append(str(paramItem[1]))
#                    print curMeta
                    metaData.append(curMeta)
            else:
                i=0
                if len(curFP['dataDict'])>0:
                    curDataDict = curFP['dataDict']
                    for dataItem in curDataDict.iteritems():
                        dataLabels.append(dataItem[0].split(os.path.sep)[-1])
                        curPeaks = dataItem[1].peakList
                        peakData.append([N.zeros_like(curPeaks)+i,curPeaks])
                        i+=1
                        curMeta = []
                        curMeta.append(dataItem[0])
                        headers = ['File Name']
                        paramDict = dataItem[1].peakParams
                        if paramDict != None:
                            for paramItem in paramDict.iteritems():
                                headers.append(paramItem[0])
                                curMeta.append(str(paramItem[1]))
    #                    print curMeta
                        metaData.append(curMeta)



            dummyPeaks = curPeaks*1
            dummyPeaks[:,1]*=0
            peakData.append([N.zeros_like(curPeaks),dummyPeaks])#add a dummy peakset to view last set
            dataLabels.append('')#'_nolegend_')#add another dummy to see the top level
            dTable = CT.DataTable(metaData, headers)
            self.plotMetaPeaks(dTable, peakData, dataLabels)
            dTable.plotWidget.canvas.ytitle="DataFile"
            dTable.plotWidget.canvas.fig.subplots_adjust(left=0.2)
            dTable.plotWidget.canvas.ax.set_yticks(N.arange(len(dataLabels)))
            dTable.plotWidget.canvas.ax.set_yticklabels(dataLabels)#, minor = True)
            dTable.plotWidget.canvas.format_labels()
            dTable.plotWidget.canvas.draw()
            dTable.show()
            self.fingerRevTabls.append(dTable)


    def loadFPfromHDF5(self, fileName = None):
        if fileName == None:
            fileName = self.openFileDialog()
        if fileName != None:
            if os.path.isfile(fileName):
                hdf = T.openFile(fileName, mode = 'r')
                hdfRoot = hdf.root
                try:
                    self.curGroupName = fileName.split(os.path.sep)[-1]
                    if self.loadRawFPData_CB.isChecked():

                        self.groupIndex.append(self.numGroups)
                        self.groupList.append(self.curGroupName)
                        self.numGroups+=1

                        self.curTreeItem = QtGui.QTreeWidgetItem(self.groupTreeWidget)
                        self.curTreeItem.setText(0,self.curGroupName)
                        self.curTreeItem.setToolTip(0, fileName)
                        self.groupTreeWidget.resizeColumnToContents(0)

                        #Should we add a FP tree item?
                        self.curFPTreeItem = QtGui.QTreeWidgetItem(self.fpSpecTreeWidget)
                        self.curFPTreeItem.setText(0,self.curGroupName)
                        self.curFPTreeItem.setToolTip(0, fileName)
                        self.fpSpecTreeWidget.resizeColumnToContents(0)

                        self.getTextColor()

                        specList = hdfRoot.Spectra._v_children
                        peakLists = hdfRoot.PeakLists._v_children

                        dataDict = {}
                        for i, key in enumerate(specList.keys()):

                            bName = os.path.basename(key.replace('*',os.path.sep))
                            newName = os.path.join(self.curGroupName, bName)
                            spec = specList[key].read()
                            dataFile = DataClass(spec[:,0], spec[:,1],  name = bName, path = newName, interp = True)#should already by interpolated
                            dataFile.mzPad = specList[key].attrs.mzPad
                            pkList = peakLists[key]

                            paramDict = {'scales':None,
                                         'minSNR':None,
                                         'minRow':None,
                                         'minClust':None,
                                         'dbscanEPS':None,
                                         'rowThresh':None,
                                         'noiseFactor':None,
                                         'staticThresh':None,
                                         'autoSave':None
                                         }
                            if pkList.attrs.__contains__('minSNR'):
                                paramDict['scales'] = pkList.attrs.scales
                                paramDict['minSNR'] = pkList.attrs.minSNR
                                paramDict['minRow'] = pkList.attrs.minRow
                                paramDict['noiseFactor'] = pkList.attrs.noiseFactor
                                paramDict['minClust'] = pkList.attrs.minClust
                                paramDict['rowThresh'] = pkList.attrs.rowThresh
                                paramDict['dbscanEPS'] = pkList.attrs.EPS
                                paramDict['staticThresh'] = pkList.attrs.staticThresh


                            dataFile.setPeakList(pkList.read(), normalized = True)#set to normalized as these values are by nature already normalized
                            dataFile.setPeakParams(paramDict)
                            dataDict[newName] = dataFile#used to add to FP interface
                            self.updateGUI(dataFile)


                        peakStatDict = {}
                        peakStats = hdfRoot.PeakStats._v_children
                        for j, key in enumerate(peakStats.keys()):
#                            print key
                            peakStatDict[key] = peakStats[key].read()


                        fpDict = {}
                        fpDict[self.curGroupName] = {'dataDict':dataDict, 'peakStats':peakStatDict, 'fileName':fileName, 'peakLists':None}
                        self.commitFP(fpDict)

                        hdf.close()
                        self.loadOk = True
                        self.readFinished(True)
                    else:
                        dataDict = {}
                        peakStatDict = {}
                        peakStats = hdfRoot.PeakStats._v_children
                        peakLists = hdfRoot.PeakLists._v_children
                        for j, key in enumerate(peakStats.keys()):

                            peakStatDict[key] = peakStats[key].read()

                        peakListDict = {}
                        for j, key in enumerate(peakLists.keys()):
                            bName = os.path.basename(key.replace('*',os.path.sep))
                            newName = os.path.join(self.curGroupName, bName)
#                            print key
                            pkList = peakLists[key]
                            paramDict = {}
                            if pkList.attrs.__contains__('minSNR'):
                                paramDict['scales'] = pkList.attrs.scales
                                paramDict['minSNR'] = pkList.attrs.minSNR
                                paramDict['minRow'] = pkList.attrs.minRow
                                paramDict['noiseFactor'] = pkList.attrs.noiseFactor
                                paramDict['minClust'] = pkList.attrs.minClust
                                paramDict['rowThresh'] = pkList.attrs.rowThresh
                                paramDict['dbscanEPS'] = pkList.attrs.EPS
                                paramDict['staticThresh'] = pkList.attrs.staticThresh

                            peakListDict[newName] = {'peakList':pkList.read(), 'params':paramDict}

                        fpDict = {}
                        fpDict[self.curGroupName] = {'dataDict':dataDict, 'peakStats':peakStatDict, 'fileName':fileName, 'peakLists':peakListDict}
                        self.commitFP(fpDict)
                        hdf.close()


                except:
                    hdf.close()
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
                    errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
                    return QtGui.QMessageBox.warning(self, "Load Fingerpint Error", errorMsg)
                    print 'Error loading fingerprint from HDF5'
                    print errorMsg


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
                self.fingerPTable.resizeColumnsToContents()


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
        if isinstance(fpInstance, FP.Finger_Widget):
            self.curFPWidget = fpInstance
#            print "Got Finger Widget"

    def expandFPSpectra(self):
        if self.expandFPBool:
            self.expandFPBool = False
        else:
            self.expandFPBool = True

        if self.expandFPBool:
            self.fpSpecTreeWidget.expandAll()
        else:
            self.fpSpecTreeWidget.collapseAll()


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
        self.markerIndex = 0
        self.plotColor = None
        self.plotColorIndex = 0
        self.curEIC = None
        self.eicPlots = []
        self.fingerPlots = []
        self.fingerRevTabls = []
        self.curFPWidget = FP.Finger_Widget(parent = self)
        self.fingerPlots.append(self.curFPWidget)
        self.peakParams = None
        self.setupPeakPick()
        ###FP Related Vars:
        self.expandFPBool = False
        self.fpDict = {}
        self.curFPName = None
        self.fpDir = None
        ###Preference Variables
        self.prefFileName = 'svconfig.ini'
        self.orgPrefFileName = 'original_svconfig.ini'#Don't change this.
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
                         'labelpeaks':self.labelPeak_CB,
                         'mzhi':self.mzHi_SB,
                         'mzlo':self.mzLo_SB,
                         'excludelift':self.excludeLIFTCB,
                         'loadmzxml':self.loadmzXMLCB,
                         'autoloadfp':self.autoLoadFP_CB,
                         'fpdir':self.fpFolder_LE
                         }
        self.prefFileStruct = {}
        self.peakSettingTypes = ['High SNR','Med SNR','Low SNR']
        self.peakSetting_CB.addItems(self.peakSettingTypes)
        peakFindInt = self.peakSetting_CB.findText('Med SNR')
        self.peakSetting_CB.setCurrentIndex(peakFindInt)


    def setupGUI(self):
        self.specNameEdit.clear()
        self.groupTreeWidget.setHeaderLabel('Loaded Spectra:')
        self.fpSpecTreeWidget.setHeaderLabel('Loaded Spectra:')

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

    def getMZXMLDialog(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                         "Select mzXML File to Load",
                                         "",
                                         "mzXML (*.mzXML)")
        if not fileName.isEmpty():
#            print fileName
            return os.path.abspath(str(fileName))
        else:
            return None

    def addSingleFile(self):
        '''
        Need to handle which group the file will be loaded into....
        '''
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]
            if item.childCount() == 0:
                self.curTreeItem = item.parent()
            else:
                self.curTreeItem = item

            self.curFPTreeItem = self.fpSpecTreeWidget.findItems(self.curTreeItem.text(0), QtCore.Qt.MatchExactly, 0)[0]

            fileName = self.getMZXMLDialog()
            if fileName != None:
                tempmzXML =  mzXMLR(fileName)
                numScans = tempmzXML.data['totalScans']
                if numScans == 1:
                    tempSpec = tempmzXML.data['spectrum']
                    if len(tempSpec)>0:
            #                                print 'Spec OK', os.path.basename(item)
                        data2plot = DataClass(tempSpec[0],  tempSpec[1],  name = os.path.basename(fileName), path = fileName)
                        data2plot.setPeakList(tempmzXML.data['peaklist'], normalized = True)
                        self.updateGUI(data2plot)
                    else:
                        print 'Empty spectrum: ', item
                else:
                    errMsg = "%s has more than one spectrum in the file.\nRemember this is a program for viewing MALDI data!"%item
                    if self.P != None:
                        QtGui.QMessageBox.warning(self, "Too many spectra in File", errMsg)
        else:
            #test to see if any item groups exists.  If not create a new one.
            self.groupTreeWidget.selectAll()
            selectItems = self.groupTreeWidget.selectedItems()
            if len(selectItems) == 0:
                fileName = self.getMZXMLDialog()
                if fileName != None:
                    self.getTextColor()
                    self.curGroup = self.numGroups

                    if sys.platform == 'win32':
                        self.curGroupName = fileName.split(os.path.sep)[-2]
                    else:
                        self.curGroupName = fileName.split(os.path.sep)[-2]#[-2]

                    self.curDir = os.path.dirname(fileName)
                    self.groupIndex.append(self.numGroups)
                    self.groupList.append(self.curGroupName)
                    self.numGroups+=1

                    self.curTreeItem = QtGui.QTreeWidgetItem(self.groupTreeWidget)
                    self.curTreeItem.setText(0,self.curGroupName)
                    self.curTreeItem.setToolTip(0, self.curDir)

                    #items for the fingerprint comparison
                    self.curFPTreeItem = QtGui.QTreeWidgetItem(self.fpSpecTreeWidget)
                    self.curFPTreeItem.setText(0,self.curGroupName)
                    self.curFPTreeItem.setToolTip(0, self.curDir)

                    tempmzXML =  mzXMLR(fileName)
                    numScans = tempmzXML.data['totalScans']
                    if numScans == 1:
                        tempSpec = tempmzXML.data['spectrum']
                        if len(tempSpec)>0:
                            data2plot = DataClass(tempSpec[0],  tempSpec[1],  name = os.path.basename(fileName), path = fileName)
                            data2plot.setPeakList(tempmzXML.data['peaklist'], normalized = False)
                            self.updateGUI(data2plot)
                            self.loadOk = True
                            self.readFinished(True)
                        else:
                            print 'Empty spectrum: ', item
                    else:
                        errMsg = "%s has more than one spectrum in the file.\nRemember this is a program for viewing MALDI data!"%item
                        if self.P != None:
                            QtGui.QMessageBox.warning(self, "Too many spectra in File", errMsg)




    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.curDir)
        directory = str(directory)
        if directory != None:
            self.curDir = os.path.abspath(directory)
            return True
        else:
            self.curDir = os.path.abspath(os.getcwd())
            return False
        #return directory

    def _updatePlotColor_(self):
        if self.plotColorIndex%len(COLORS) == 0:
            self.plotColorIndex = 0
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1
        else:
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1

    def _getPlotMarker_(self):
        marker = MARKERS[self.markerIndex]
        if self.markerIndex is len(MARKERS)-1:
            self.markerIndex = 0
        else:
            self.markerIndex+=1
        return marker

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
        ct_menu.addAction(self.viewFPMetaAction)
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
            ct_menu.addAction(self.initFPAction)
        ct_menu.addAction(self.selectGroupAction)
        ct_menu.addAction(self.addFileAction)
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
            if self._getDir_():
                dirList, startDir = LmzXML(self.curDir, excludeLIFT = loadLIFT)
                dirList.sort()
                #You could pre load the widgetitems then fill them in
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
                    self.curFPTreeItem = QtGui.QTreeWidgetItem(self.fpSpecTreeWidget)
                    self.curFPTreeItem.setText(0,self.curGroupName)
                    self.curFPTreeItem.setToolTip(0, self.curDir)

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

    def selectAllInGroup(self):
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]
            if item.childCount() == 0:
                self.curTreeItem = item.parent()
            else:
                self.curTreeItem = item
            numChildren = self.curTreeItem.childCount()
            self.ignoreSignal = True
            for childIndex in xrange(numChildren):
                self.groupTreeWidget.setItemSelected(self.curTreeItem.child(childIndex), True)
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

    def initFP(self):
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            curFingerPlot = FP.Finger_Widget(parent = self)
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
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 1:#this is so multiple files don't get plotted and overload the GUI
            pass
        else:
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

                self.PCTProgress("")#reset status label

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
            self.setupTable()

    def savePeaks(self):
        selectItems = self.groupTreeWidget.selectedItems()
        #curRow
        if len(selectItems) > 0:
            for item in selectItems:
                curData = self.dataDict[str(item.toolTip(0))]
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

                        #used to remove from fpSpecTreeWidget
                        foundItems = self.fpSpecTreeWidget.findItems(parentItem.text(0),QtCore.Qt.MatchExactly, 0)#take only the first item
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
                                topIndex = self.fpSpecTreeWidget.indexOfTopLevelItem(fpParent)
                                self.fpSpecTreeWidget.takeTopLevelItem(topIndex)

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
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]
            if item.childCount() == 0:
                self.curTreeItem = item.parent()
            else:
                self.curTreeItem = item
            numChildren = self.curTreeItem.childCount()
            mzLo = self.mzLo_SB.value()
            mzHi = self.mzHi_SB.value()
            if len(self.dataList) == 0:
                return QtGui.QMessageBox.warning(self, "No Data Are Loaded",  "Try Loading a Data Set Again!")

            if mzHi != -1 and mzHi < mzLo:
                return QtGui.QMessageBox.warning(self, "EIC Range Error",  "m/z Hi is larger than m/z Lo\nCheck the ranges!")
            else:
                dataNameList = []
                self.curEIC = []
                for childIndex in xrange(numChildren):
                    curDataName = str(self.curTreeItem.child(childIndex).toolTip(0))
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
                curData.plot(curAx, pColor = self.plotColor, plotNoise = True, plotPks = self.plotPkListCB.isChecked(), labelPks = self.labelPeak_CB.isChecked())
            else:
                numSegs = len(curData.x)/self.noiseFactor_SB.value()
                minSNR = self.snrNoiseEst_SB.value()
                curData.getNoise(numSegs,minSNR)
                curData.plot(curAx, pColor = self.plotColor, plotNoise = True, plotPks = self.plotPkListCB.isChecked(), labelPks = self.labelPeak_CB.isChecked())
        else:
            curData.plot(curAx, pColor = self.plotColor, plotPks = self.plotPkListCB.isChecked(), labelPks = self.labelPeak_CB.isChecked())

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
#        print "GO Clipboard"

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
                if isinstance(plot, FP.Finger_Widget):
                    try:
                        plot.close()
                    except:
                        pass
        if len(self.fingerRevTabls)>0:
            for tbl in self.fingerRevTabls:
                if isinstance(tbl, CT.DataTable):
                    try:
                        tbl.close()
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

    def setupTable(self):
        self.tabPeakTable.clear()
        #need to disable sorting as it corrupts data addition
        self.tabPeakTable.setSortingEnabled(False)
        header = ['m/z', 'Intensity']
        if self.curDataName != None:
            curData = self.dataDict[self.curDataName]
            if curData.pkListOk:
                self.tabPeakTable.addData(curData.peakList)
            self.tabPeakTable.setHorizontalHeaderLabels(header)
            self.tabPeakTable.setSortingEnabled(True)
            self.tabPeakTable.resizeColumnToContents(0)

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False


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
            self.P = None
            if parent != None:
                self.P = parent

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
                            numScans = tempmzXML.data['totalScans']
                            if numScans == 1:
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
                            else:
                                errMsg = "%s has more than one spectrum in the file.\nRemember this is a program for viewing MALDI data!"%item
                                if self.P != None:
                                    QtGui.QMessageBox.warning(self, "Too many spectra in File", errMsg)

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
                                    dataItem.setPeakParams(self.paramDict)
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
