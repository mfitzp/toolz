#!/usr/bin/env python
###################################
'''To Do:

Add progress bar to status bar...look at Ashoka's Code

Need to add exception for when there is no data in the file (i.e. a blank spectrum)

Load a single file?

make miniFingerprint
    show FP window for a given group, and table

PCA after peak pick

implement TreeView???


'''
###################################
import os, sys, traceback
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S

from matplotlib.lines import Line2D
from matplotlib.mlab import rec2csv

from FolderParse import Load_FID_Folder as LFid
from FolderParse import Load_mzXML_Folder as LmzXML
from flexReader import brukerFlexDoc as FR
from mzXML_reader import mzXMLDoc as mzXMLR

from mpl_pyqt4_widget import MPL_Widget

import supportFunc as SF
import getBaseline as GB
import cwtPeakPick as CWT

import ui_main

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
        self.setupPlot()
        self.layoutStatusBar()


    def initConnections(self):
        self.handleActionA = QtGui.QAction("Cursor A", self)
        self.plotWidget.addAction(self.handleActionA)

        self.handleActionB = QtGui.QAction("Cursor B", self)
        self.plotWidget.addAction(self.handleActionB)

        self.cursorClearAction = QtGui.QAction("Clear Cursors",  self)
        self.plotWidget.addAction(self.cursorClearAction)

        self.labelAction = QtGui.QAction("Label Peak",  self)
        self.plotWidget.addAction(self.labelAction)

        self.removeAction = QtGui.QAction("Remove File(s)",  self)
        self.specListWidget.addAction(self.removeAction)

        self.topHatAction = QtGui.QAction("Apply TopHat",  self)
        self.specListWidget.addAction(self.topHatAction)

        self.findPeakAction = QtGui.QAction("Find Peaks",  self)
        self.specListWidget.addAction(self.findPeakAction)

        self.selectAllAction = QtGui.QAction("Select All",  self)
        self.specListWidget.addAction(self.selectAllAction)

        self.saveCSVAction = QtGui.QAction("Save to CSV",  self)
        self.saveCSVAction.setShortcut("Ctrl+Alt+S")
        self.plotWidget.addAction(self.saveCSVAction)

        self.savePksAction = QtGui.QAction("Save Peak List",  self)
        self.specListWidget.addAction(self.savePksAction)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

        QtCore.QObject.connect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)

        QtCore.QObject.connect(self.removeAction, QtCore.SIGNAL("triggered()"),self.removeFile)
        QtCore.QObject.connect(self.topHatAction, QtCore.SIGNAL("triggered()"), self.filterSpec)

        QtCore.QObject.connect(self.handleActionA, QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.handleActionB, QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.cursorClearAction, QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.labelAction, QtCore.SIGNAL("triggered()"),self.labelPeak)
        #QtCore.QObject.connect(self.mpl2ClipAction, QtCore.SIGNAL("triggered()"),self.mpl2Clip)

        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("terminated()"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished()"), self.updateGUI)
        QtCore.QObject.connect(self.loadDirBtn, QtCore.SIGNAL("clicked()"), self.initDataList)
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.initDataList)
        QtCore.QObject.connect(self.specListWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.specListSelect)

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



        self.useDefaultScale_CB.nextCheckState()

    def selectAllLoaded(self):
        self.ignoreSignal = True
        self.specListWidget.selectAll()
        self.ignoreSignal = False


    def PFTFinished(self, finishedBool):
        self.setStatusLabel("Peak Fitting Completed!")
        self.specListSelect()
        self.resetProgressBar()

    def savePeaks(self):
        selectItems = self.specListWidget.selectedItems()
        #curRow
        if len(selectItems) > 0:
            itemRows = []
            for item in selectItems:
                curRow = self.specListWidget.indexFromItem(item).row()
                curDataName = self.dataList[curRow]
                curData = self.dataDict[curDataName]
                curData.savePkList()




    def autoscale_plot(self):
#        print "Cur Group", self.curGroup
#        print "Group list", self.groupList
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
            return fileName
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

                N.savetxt(str(path), N.transpose(data2write), delimiter = ',', fmt='%.4f')

            except:
                try:
                    #this is for the case where the data may not be in float format?
                    N.savetxt(str(path), N.transpose(data2write), delimiter = ',')
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
        selectItems = self.specListWidget.selectedItems()
        #curRow
        if len(selectItems) > 0:
            for item in selectItems:
                dataName = str(item.toolTip())
                self.dataDict[dataName].applyTopHat()
                #delRow = self.specListWidget.indexFromItem(item).row()
            self.specListSelect()

    def removeFile(self):
        selectItems = self.specListWidget.selectedItems()
        #curRow
        if len(selectItems) > 0:
            for item in selectItems:

                delRow = self.specListWidget.indexFromItem(item).row()
                delName = str(item.toolTip())#used because the toolTip is set to the full path which is stored in the dataDict
#                print delRow, delName
                self.specListWidget.takeItem(delRow)
                self.dataList.pop(delRow)
                self.dataDict.pop(delName)
#
#                print item.text()
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
                curData.plot(curAx, pColor = self.plotColor, plotNoise = True)#, labelPks = False)
            else:
                numSegs = len(curData.x)/self.noiseFactor_SB.value()
                minSNR = self.snrNoiseEst_SB.value()
                curData.getNoise(numSegs,minSNR)
                curData.plot(curAx, pColor = self.plotColor, plotNoise = True)#, labelPks = False)
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
        selectItems = self.specListWidget.selectedItems()
        if len(selectItems) > 0:
            dataItemList = []#reset indexes to peak Pick
            for item in selectItems:
                curRow = self.specListWidget.indexFromItem(item).row()
                curDataName = self.dataList[curRow]
                curData = self.dataDict[curDataName]
#                print curData.noiseOK
                dataItemList.append(curData)
                #peakPickIndex.append(self.specListWidget.indexFromItem(item).row())
            self.startPeakThread(dataItemList)
            return True
#            print "Find Peaks"


    def setupVars(self):
        self.dirList = []
        self.curDir = os.getcwd()
        self.curDataName = None
        #these are used to keep track of what group is loaded
        self.groupList = []
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
        self.txtColor = None
        self.colorIndex = 0
        self.plotColor = None
        self.plotColorIndex = 0
        self.curEIC = None
        self.eicPlots = []
        self.peakParams = None
        self.setupPeakPick()

    def setupGUI(self):
        self.specNameEdit.clear()
        self.indexHSlider.setMaximum(0)
        self.indexSpinBox.setMaximum(0)
        self.initContextMenus()

    def updateGUI(self,  loadedItem=None):
        if loadedItem != None:
            #So that duplicate files are not loaded into the dataDict
            #if self.dataDict.has_key(loadedItem.name):
            if self.dataDict.has_key(loadedItem.path):
                pass
            else:
                #self.dataList.append(loadedItem.name)
                self.dataList.append(loadedItem.path)
                #color handler
                tempItem = QtGui.QListWidgetItem(loadedItem.name)
                tempColor = QtGui.QColor(self.txtColor)
                tempItem.setTextColor(tempColor)
                tempItem.setToolTip(loadedItem.path)
                #self.specListWidget.addItem(loadedItem.name)
                self.specListWidget.addItem(tempItem)
            #self.dataDict[loadedItem.name] = loadedItem
            self.dataDict[loadedItem.path] = loadedItem

        self.numSpec = len(self.dataDict)
        if self.numSpec == 1:
            self.plotByIndex(0)
            self.indexHSlider.setMaximum(self.numSpec)
            self.indexSpinBox.setMaximum(self.numSpec)
        else:
            self.indexHSlider.setMaximum(self.numSpec-1)
            self.indexSpinBox.setMaximum(self.numSpec-1)

    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.curDir)
        directory = str(directory)
        if directory != None:
            self.curDir = directory
        else:
            self.curDir = os.getcwd()
        #return directory

    def _updatePlotColor_(self):
        if self.plotColorIndex%len(COLORS) == 0:
            self.plotColorIndex = 0
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1
        else:
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1


    def initDataList(self):
        #handles loading of new group.
        #####Text Color Handler
        if self.colorIndex%len(COLORS) == 0:
            self.colorIndex = 0
            self.txtColor = COLORS[self.colorIndex]
            self.colorIndex +=1
        else:
            self.txtColor = COLORS[self.colorIndex]
            self.colorIndex +=1

        if not self.firstLoad:
            #reinitialize GUI and spectrumList
            self.setupGUI()
        if self.loadmzXMLCB.isChecked():
            loadLIFT = self.excludeLIFTCB.isChecked()
            self._getDir_()
            dirList, startDir = LmzXML(self.curDir, excludeLIFT = loadLIFT)
            dirList.sort()
            if len(dirList) !=0:
                self.dirList = dirList
                self.loadOk = True
                self.firstLoad = False
                if self.readThread.updateThread(dirList,  loadmzXML = True):
                    self.readThread.start()

                self.curGroup = self.numGroups
                self.groupList.append(self.numGroups)
                self.numGroups+=1

#                print "Cur Group", self.curGroup
#                print "Group list", self.groupList
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

    def initContextMenus(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__mplContext__)
        self.specListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.specListWidget.connect(self.specListWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__listContext__)

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
                                data2plot = DataPlot(tempSpec[0],  tempSpec[1],  name = os.path.basename(item), path = item)
                                data2plot.setPeakList(tempmzXML.data['peaklist'], normalized = False)
                                #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                                #note PyQt_PyObject
                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)
                            else:
                                print 'Empty spectrum: ', item

                            self.numItems -=1


                else:
                    while not self.finished and self.numItems > 0:
                        for item in self.loadList:
                            tempFlex = FR(item)
                            tempSpec = tempFlex.data['spectrum']
                            data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1], name = item.split(os.path.sep)[-4], path = item)#the -4 index is to handle the Bruker File Structure
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


class DataPlot(object):
    def __init__(self, xdata,  ydata,  name = None, path = None):
        self.x = xdata
        if ydata != None:
            self.y = ydata
        else:
            self.y = None

        if name:
            self.name = name
        else:
            self.name = 'None'

        if path:
            self.path = path
        else:
            self.path = 'None'

        self.axSet = False
        self.peakList = None
        self.pkListOk = False
        self.labelPks = False
        self.peakList = None
        self.mplAx = None
        self.plotModVal = 1
        self.noiseEst = None
        self.minNoiseEst = None
        self.noiseOK = False
        self.normFactor = self.y.max()
        self.interpOk = False
        self.mzPad = None#this value is used for peak picking and is equal to the number of points in 0.5 mz units
        self.interpData()


    def savePkList(self):
        if self.pkListOk:
            t1 = time.clock()
#            print self.name
            #print self.path
            try:
                peakListFN = self.path.replace('.mzXML', '_pks.csv')
                N.savetxt(peakListFN, self.peakList, delimiter = ',', fmt='%.4f')
                print "Peak List Save Time: ", time.clock()-t1
            except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
    #                    print 'Error saving figure data'
                errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
    #            return QtGui.QMessageBox.warning(self, "Interpolation Error", errorMsg)
                print errorMsg
                print self.path



    def getEICVal(self, mzLo, mzHi, type = 'sum'):#the other type is 'max'
        if mzHi == -1:
            crit = (self.x >= mzLo)
        else:
            crit = (self.x >= mzLo) & (self.x <= mzHi)
        range = N.where(crit)[0]
        if len(range) != 0:
            if type == 'sum':
                return self.y[range].sum()
            elif type == 'max':
                return self.y[range].max()

    def setAxis(self,  mplAxInstance):
        self.axSet = True
        self.mplAx = mplAxInstance

    def setPeakList(self, peakList, normalized = True):
        #peak list is two arrays peakLoc and intensity
        if normalized:
            if peakList != None:
                if len(peakList)>0:
                    self.pkListOk = True#CHANGE ME True
                    self.peakList = peakList
        else:
            if peakList != None:
                if len(peakList)>0:
                    self.pkListOk = True#CHANGE ME True
                    self.peakList = peakList
                    if type(self.peakList[0]) == N.ndarray:
                        self.peakList[:,1] = SF.normalize(self.peakList[:,1])


    def applyTopHat(self):
        self.y = SF.topHat(self.y, 0.01)

    def interpData(self):
        #this of course slows loading down but is necessary for the peak picking using CWT
        try:
            newX, newY = SF.interpolate_spectrum_XY(self.x, self.y)

            meanMZ = N.round(newX.mean())
            crit = (newX >= meanMZ) & (newX <= (meanMZ+0.5))#CHECK ME
            #MZ Pad is a windowing factor to find the maximum of the peak rather than a valley.
            #This also must be done after interpolation
            self.mzPad = len(N.where(crit)[0])
#            print "MZ Pad", self.mzPad

            self.x = newX
            self.y = SF.normalize(newY)

            self.interpOk = True
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    print 'Error saving figure data'
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
#            return QtGui.QMessageBox.warning(self, "Interpolation Error", errorMsg)
            print self.name
            print errorMsg

        if self.interpOk:
            self.x = newX
            self.y = newY

    def getNoise(self, numSegs, minSNR):
        noiseEst, minNoiseEst = GB.SplitNSmooth(self.y,numSegs, minSNR)
        if noiseEst != None:
            if len(noiseEst) == len(self.x):
                self.noiseEst = noiseEst
                self.minNoiseEst = minNoiseEst
                self.noiseOK = True
#                print "Get Noise Ok"

    def plot(self,  mplAxInstance, pColor = 'r', scatter = False, labelPks = False, invert = False, plotNoise = False):
        #if self.axSet:
        self.labelPks = labelPks
        self.mplAx = mplAxInstance
        if self.y != None:
            if invert:
                self.plotModVal = -1
            else:
                self.plotModVal = 1

            if scatter:
                self.mplAx.scatter(self.x,  self.y,  label = self.name)
            else:
                self.mplAx.plot(self.x,  self.y*self.plotModVal,  label = self.name,  picker = 5,  color = pColor)
                if plotNoise:
                    if self.noiseOK:
                        self.mplAx.plot(self.x,  self.noiseEst,  label = '_nolegend_',  color = 'r', alpha = 0.6)
                    else:
                        print "No noise to plot"
                if self.pkListOk:
                    try:
                        if type(self.peakList[0]) == N.ndarray:
                            self.mplAx.vlines(self.peakList[:, 0], 0, self.peakList[:, 1]*1.15*self.plotModVal,  color = 'r',  label = '_nolegend_')
                            if self.labelPks:
                                for peak in self.peakList:
                                    self.mplAx.text(peak[0], peak[1]*1.1*self.plotModVal, '%.4f'%peak[0],  fontsize=8, rotation = 45)
                        elif type(self.peakList[0]) == N.float64:
                            #this is the case where there is only one value in the peaklist
                            self.mplAx.vlines(self.peakList[[0]], 0, self.peakList[[1]]*1.1*self.plotModVal,  color = 'r',  label = '_nolegend_')
                            if self.labelPks:
                                self.mplAx.text(self.peakList[0], self.peakList[1]*1.1*self.plotModVal, '%.4f'%self.peakList[0],  fontsize=8, rotation = 45)

                        else:
                            print 'Type of First peakList element', type(self.peakList[0])
                            print "Error plotting peak list"

                    except:
                        print "Error plotting peak list"
                        errorMsg = "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                        print errorMsg



        else:
            self.mplAx.plot(self.x,  label = self.name)
#    else:
#        errMsg = 'axis must be set before attempting to plot'
#        raise errMsg



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())
