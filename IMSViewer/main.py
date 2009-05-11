#!/usr/bin/env python
###################################
'''
'''
###################################
import os, sys, traceback
import time
import ConfigParser
import string
import time
import gzip

#config = ConfigParser.ConfigParser()
from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import scipy.stats as stats
#import tables as T

from matplotlib.lines import Line2D
from matplotlib.mlab import rec2csv
from pylab import load as L

from mpl_pyqt4_widget import MPL_Widget
from Plot_Options_Line2D import Plot_Options_Dialog as POD

from dataClass import DataClass
from WSU_Process import WSUDataClass as WSU

import supportFunc as SF
import getBaseline as GB
import customTable as CT
import filterIMS as FIMS

import ui_main

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

MARKERS = ['o', 'd','>', 's', '^',  'p', '<', 'h', 'v']

BOLTZ_k=1.38065E-23 ## Joules/Kelvin
eCHARGE=1.60217646E-19 ## in Coulombs

class Plot_Widget(QtGui.QMainWindow,  ui_main.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.setupVars()
        self.readThread = LoadThread(parent = self)
        self.initConnections()
        self.setupGUI()
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

        self.calcMobAction = QtGui.QAction("Mobility", self)
        self.plotWidget.addAction(self.calcMobAction)
        QtCore.QObject.connect(self.calcMobAction, QtCore.SIGNAL("triggered()"),self.calcMobility)

        self.editLinesAction = QtGui.QAction("Edit Properties", self)
        self.editLinesAction.setShortcut("Ctrl+E")
        self.plotWidget.addAction(self.editLinesAction)
        QtCore.QObject.connect(self.editLinesAction, QtCore.SIGNAL("triggered()"),self.editPlotProperties)

        self.removeAction = QtGui.QAction("Remove File(s)", self)
        self.groupTreeWidget.addAction(self.removeAction)

        self.addFileAction = QtGui.QAction("Add File", self)
        self.groupTreeWidget.addAction(self.addFileAction)

#        self.topHatAction = QtGui.QAction("Apply TopHat",  self)
#        self.groupTreeWidget.addAction(self.topHatAction)

        self.sgSmoothAction = QtGui.QAction("SG Smooth",  self)
        self.groupTreeWidget.addAction(self.sgSmoothAction)

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

        QtCore.QObject.connect(self.saveCSVAction,QtCore.SIGNAL("triggered()"), self.save2CSV)

        QtCore.QObject.connect(self.removeAction, QtCore.SIGNAL("triggered()"),self.removeFile)
        QtCore.QObject.connect(self.addFileAction, QtCore.SIGNAL("triggered()"),self.addSingleFile)
#        QtCore.QObject.connect(self.topHatAction, QtCore.SIGNAL("triggered()"), self.filterSpec)
        QtCore.QObject.connect(self.sgSmoothAction, QtCore.SIGNAL("triggered()"), self.filterSpec)

        QtCore.QObject.connect(self.handleActionA, QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.handleActionB, QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.cursorClearAction, QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.labelAction, QtCore.SIGNAL("triggered()"),self.labelPeak)
#        QtCore.QObject.connect(self.mpl2ClipAction, QtCore.SIGNAL("triggered()"),self.mpl2Clip)

#        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("terminated()"), self.updateGUI)
        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished()"), self.updateGUI)
#        QtCore.QObject.connect(self.loadDirBtn, QtCore.SIGNAL("clicked()"), self.initDataList)
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

#        QtCore.QObject.connect(self.showNoise_Btn, QtCore.SIGNAL("clicked()"), self.getCurDataNoise)


#        QtCore.QObject.connect(self.findPeakAction,QtCore.SIGNAL("triggered()"),self.findPeaks)
#        QtCore.QObject.connect(self.savePksAction,QtCore.SIGNAL("triggered()"),self.savePeaks)
        QtCore.QObject.connect(self.selectAllAction,QtCore.SIGNAL("triggered()"),self.selectAllLoaded)
        QtCore.QObject.connect(self.selectGroupAction,QtCore.SIGNAL("triggered()"),self.selectAllInGroup)

        QtCore.QObject.connect(self.readThread, QtCore.SIGNAL("finished(bool)"), self.readFinished)

        QtCore.QObject.connect(self.actionRead_Me,QtCore.SIGNAL("triggered()"),self.readMe)

#        QtCore.QObject.connect(self.groupTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.treeItemSelected)
        QtCore.QObject.connect(self.groupTreeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem *,int)"), self.treeViewSelect)
        QtCore.QObject.connect(self.freqCutoff_SB, QtCore.SIGNAL("valueChanged(double)"), self.pauseBeforeFilter)
        QtCore.QObject.connect(self.actionExit_Program, QtCore.SIGNAL("triggered()"), self.exitProgram)

        QtCore.QObject.connect(self.actionPlot_Legend, QtCore.SIGNAL("triggered()"), self.toggleLegend)
        QtCore.QObject.connect(self.actionFilter_Visible, QtCore.SIGNAL("triggered()"), self.toggleFilter)
        QtCore.QObject.connect(self.actionNormalize_Raw_Data, QtCore.SIGNAL("triggered()"), self.toggleNormalize)
        QtCore.QObject.connect(self.actionIgnore_Raw_Spectrum, QtCore.SIGNAL("triggered()"), self.toggleIgnoreRaw)
        QtCore.QObject.connect(self.actionInvert_Comparison, QtCore.SIGNAL("triggered()"), self.toggleInvert)

        QtCore.QObject.connect(self.loadWSU_CB, QtCore.SIGNAL("stateChanged (int)"), self.toggleIMSTOFLoad)


############IMS Resolving Power Widget###################
        QtCore.QObject.connect(self.tempSlider, QtCore.SIGNAL("sliderReleased()"), self.setRP_Temp)
        QtCore.QObject.connect(self.sliderTemp_SB, QtCore.SIGNAL("valueChanged (double)"), self.setSlider_Temp)

        QtCore.QObject.connect(self.voltageSlider, QtCore.SIGNAL("sliderReleased()"), self.setRP_Voltage)
        QtCore.QObject.connect(self.sliderVoltage_SB, QtCore.SIGNAL("valueChanged (double)"), self.setSlider_Voltage)

        QtCore.QObject.connect(self.gatePWSlider, QtCore.SIGNAL("sliderReleased()"), self.setRP_GPW)
        QtCore.QObject.connect(self.sliderGPW_SB, QtCore.SIGNAL("valueChanged (double)"), self.setSlider_GPW)

        QtCore.QObject.connect(self.driftTimeSlider, QtCore.SIGNAL("sliderReleased()"), self.setRP_DT)
        QtCore.QObject.connect(self.sliderDriftTime_SB, QtCore.SIGNAL("valueChanged (double)"), self.setSlider_DT)



    def setSlider_Temp(self, value):
        self.tempSlider.setValue(int(value))
        self.setRPVars()

    def setRP_Temp(self):
        self.sliderTemp_SB.setValue(self.tempSlider.value())
        self.setRPVars()

    def setSlider_Voltage(self, value):
        self.voltageSlider.setValue(int(value))
        self.setRPVars()

    def setRP_Voltage(self):
        self.sliderVoltage_SB.setValue(self.voltageSlider.value())
        self.setRPVars()

    def setSlider_GPW(self, value):
        self.gatePWSlider.setValue(int(value))
        self.setRPVars()

    def setRP_GPW(self):
        self.sliderGPW_SB.setValue(self.gatePWSlider.value())
        self.setRPVars()

    def setSlider_DT(self, value):
        self.driftTimeSlider.setValue(int(value))
        self.setRPVars()

    def setRP_DT(self):
        self.sliderDriftTime_SB.setValue(self.driftTimeSlider.value())
        self.setRPVars()


    def setRPVars(self):
        self.rpVoltage = N.arange(1,int(3*self.sliderVoltage_SB.value()))
        self.diffPW = (16*BOLTZ_k*(self.sliderTemp_SB.value()+273.15)*N.log(2))/(self.rpVoltage*eCHARGE)
        self.diffTerm = N.sqrt(1/self.diffPW)

        self.GPW = self.sliderGPW_SB.value()/1E6#convert to seconds
        self.driftTime = self.sliderDriftTime_SB.value()/1000
        self.mobility = (self.driftLength_SB.value()**2)/(self.voltage_SB.value()*self.driftTime)
        self.pulsePW = N.sqrt(1./(self.GPW**2/(self.driftLength_SB.value()**2/(self.rpVoltage*self.mobility))**2))

        self.rpArray = N.sqrt(1./(self.GPW**2/(self.driftLength_SB.value()**2/(self.rpVoltage*self.mobility))**2+self.diffPW))

        curAx = self.imRpWidget.canvas.ax
        curAx.cla()
        curAx.plot(self.rpVoltage, self.rpArray, 'r', label ='Theoretical Rp')
        curAx.plot(self.rpVoltage, self.diffTerm, '--b', label = 'Random Diffusion')
        curAx.plot(self.rpVoltage, self.pulsePW, '--g', label = 'Gate Pulse Width')
        curAx.legend()
        curAx.set_ylim(ymax = 2.5*self.rpArray.max())
        curAx.xtitle = 'Voltage'
        curAx.ytitle = 'Resolving Power'
        self.imRpWidget.canvas.format_labels()
        self.imRpWidget.canvas.draw()

#        self.plotWidget.canvas.format_labels()
#        self.plotWidget.canvas.draw()




#########################################################




    def toggleIMSTOFLoad(self, state):
        if state == 2:
            self.showTOF_CB.setEnabled(True)
        elif state == 0:
            self.showTOF_CB.setEnabled(False)


    def editPlotProperties(self):
        print "Edit Properties"
        self.setLineDict()
        if len(self.lineDict) > 0:
            curAx = self.plotWidget.canvas.ax
            if POD(self.lineDict, curAx = curAx, parent = self).exec_():
                if self.plotLegendCB.isChecked():
                    curAx.legend(borderaxespad = 0.03, borderpad=0.25)
                self.plotWidget.canvas.format_labels()
                self.plotWidget.canvas.draw()
            else:
                print "Cancel"

    def setLineDict(self):
        self.lineDict = {}
        lineList = self.plotWidget.canvas.ax.get_lines()
        if lineList > 0:
            for line in lineList:
                self.lineDict[line.get_label()]=line

    def calcMobility(self, dLabel=None, driftTime=None):
        '''
        Need to divide driftTime by 1000 to get value in seconds!
        '''
        if self.curDataName != None:
            curData = self.dataDict[self.curDataName]
            if "IMS Cell Temp." in curData.info:#case for a IMS spectrum from a PCP instrument
                if curData.temperature != None:
                    if driftTime != None:
                        #print curData.temperature, curData.voltage, curData.pressure, driftTime
                        dLength = self.driftLength_SB.value()
                        voltage = curData.voltage
                        pressure = curData.pressure
                        temperature = curData.temperature
                        reducedMob = (dLength**2/(voltage*driftTime/1000))*(pressure/760)*(273.15/(temperature+273.15))
                        return reducedMob
                    else:
                        print "No driftTime Variable Passed"
                        return 0.0
            elif "TDC Resolution" in curData.info:
                if driftTime != None:
                    dLength = self.driftLength_SB.value()
                    voltage = self.voltage_SB.value()
                    driftTime/=1000#convert to ms as WSU-TOF data is in microseconds
                    pressure = self.pressure_SB.value()
                    temperature = self.temp_SB.value()
                    reducedMob = (dLength**2/(voltage*driftTime/1000))*(pressure/760)*(273.15/(temperature+273.15))
                    return reducedMob
                else:
                    print "No driftTime Variable Passed"
                    return 0.0

            else:
                print "Mass Spectrum Displayed"
                return 0.0


    def toggleLegend(self):
        self.plotLegendCB.nextCheckState()

    def toggleFilter(self):
        self.lowPassOn_CB.nextCheckState()

    def toggleNormalize(self):
        self.normRaw_CB.nextCheckState()

    def toggleIgnoreRaw(self):
        self.ignoreRaw_CB.nextCheckState()

    def toggleInvert(self):
        self.invertCompCB.nextCheckState()

    def readMe(self):
        msg = "Remember:\n\nCtrl+Z toggles zooming\nCtrl+A zooms out\nCtrl+C copies graph to clipboard\nCtrl+Alt+S saves to csv file\n\nQuestions: bhclowers@gmail.com"
        return QtGui.QMessageBox.information(self, "IMSViewer Info",  msg)

    def exitProgram(self):
        self.close()

    def pauseBeforeFilter(self, val):
        QtCore.QTimer.singleShot(750,  self.passFreqVal)

    def passFreqVal(self):
        newVal = self.freqCutoff_SB.value()
        self.testFreqValChanged(newVal)

    def testFreqValChanged(self,newVal):
#        print newVal
        if self.freqVal == 0:#case when value is first initialized
            self.freqVal = self.freqCutoff_SB.value()
            self.freqValChanged()
        elif newVal == self.freqVal:
            self.freqValChanged()
        else:
            self.freqVal = newVal

    def freqValChanged(self, val = None):
        if val == None:
            val = self.freqCutoff_SB.value()
#        print val
        if self.lowPassOn_CB.isChecked():
            selectItems = self.groupTreeWidget.selectedItems()
            if len(selectItems) > 0:
                item = selectItems[0]
                if item.childCount() == 0:#test to see if the object is a leaf
                    curData = self.dataDict[str(item.toolTip(0))]
                    if curData.filterVal != val:
                        freqIMS = FIMS.lowPassIMS(curData.y, val)
                        curData.setFiltered(freqIMS,val)
                        self.treeViewSelect()

#        QtCore.QTimer.singleShot(500)


    def wsuMZPlot(self, data2plot):
        '''
        Misc function for plotting WSU mzdata
        '''
#        print "Test Plot Go"

#        testPlot = MPL_Widget(enableAutoScale = True, enableCSV = True)
        massPlot = CT.DataTable(N.column_stack((data2plot.mzX,data2plot.mzY)),colHeaderList = ['m/z', 'Intensity'])
        massPlot.setWindowTitle(data2plot.path)

        ax1 = massPlot.plotWidget.canvas.ax
        plotTitle = ''
        ax1.set_title(plotTitle)
        ax1.title.set_fontsize(10)
        ax1.set_xlabel('m/z', fontstyle = 'italic')
        ax1.set_ylabel('Intensity')

        ax1.plot(data2plot.mzX, data2plot.mzY, 'r')
        massPlot.show()
        self.mzPlots.append(massPlot)


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
        self.mzPlots.append(testPlot)


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
        self.mzPlots = []
        self.fingerPlots = []
        self.fingerRevTabls = []
        self.peakParams = None
        ###Preference Variables
        self.prefFileName = 'svconfig.ini'
        self.orgPrefFileName = 'original_svconfig.ini'#Don't change this.
        ##Plot Options Var
        self.lineDict = {}

        self.freqVal = 0
        self.showTOF_CB.setEnabled(False)


    def setupGUI(self):
        self.specNameEdit.clear()
        self.groupTreeWidget.setHeaderLabel('Loaded Spectra:')


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

            self.dataDict[loadedItem.path] = loadedItem

        self.numSpec = len(self.dataDict)
#        if self.numSpec == 1:
#            self.plotByIndex(0)
#            self.indexHSlider.setMaximum(self.numSpec)
#            self.indexSpinBox.setMaximum(self.numSpec)
#        else:
#            self.indexHSlider.setMaximum(self.numSpec-1)
#            self.indexSpinBox.setMaximum(self.numSpec-1)

    def getIMSDialog(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                         "Select IMS File to Load",
                                         "",
                                         "TXT (*.TXT);; IMS-TOF GZIP (*.gz)")
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

            fileName = self.getIMSDialog()
            if fileName != None:
                if self.loadWSU_CB.isChecked():
                    tempSpec = openWSUTOFFile(fileName)
                    if tempSpec[-1]:
                        data2plot = WSU(tempSpec[0],tempSpec[1],tempSpec[2],tempSpec[3], name = os.path.basename(fileName), path = fileName)
                        data2plot.setInfo(tempSpec[4])
                        self.updateGUI(data2plot)
                    else:
                        return QtGui.QMessageBox.warning(self, "Error Loading File",  tempSpec[0])
                else:
                    tempSpec = openIMSFile(fileName)
                    if tempSpec[-1]:
                        data2plot = DataClass(tempSpec[0],  tempSpec[1],  name = os.path.basename(fileName), path = fileName)
                        data2plot.setInfo(tempSpec[2])
                        self.updateGUI(data2plot)
                    else:
                        return QtGui.QMessageBox.warning(self, "Error Loading File",  tempSpec[0])
        else:
            #test to see if any item groups exists.  If not create a new one.
            self.groupTreeWidget.selectAll()
            selectItems = self.groupTreeWidget.selectedItems()
            if len(selectItems) == 0:
                fileName = self.getIMSDialog()
                if fileName != None:
                    if self.loadWSU_CB.isChecked():
                        tempSpec = openWSUTOFFile(fileName)
                        if tempSpec[-1]:
                            data2plot = WSU(tempSpec[0],tempSpec[1],tempSpec[2],tempSpec[3], name = os.path.basename(fileName), path = fileName)
                            data2plot.setInfo(tempSpec[4])
                            self.loadOk = True
                        else:
                            return QtGui.QMessageBox.warning(self, "Error Loading File",  tempSpec[0])

                    else:
                        tempSpec =  openIMSFile(fileName)
                        if tempSpec[-1]:
                            data2plot = DataClass(tempSpec[0],  tempSpec[1],  name = os.path.basename(fileName), path = fileName)
                            data2plot.setInfo(tempSpec[2])
                            self.loadOk = True
                        else:
                            return QtGui.QMessageBox.warning(self, "Error Loading File",  tempSpec[0])

                    if self.loadOk:

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

                        self.updateGUI(data2plot)
                        self.readFinished(True)

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


    def __treeContext__(self, point):
        '''Create a menu for the file list widget'''
        ct_menu = QtGui.QMenu("Tree Menu", self.groupTreeWidget)
        ct_menu.addAction(self.removeAction)
        ct_menu.addAction(self.sgSmoothAction)
#        ct_menu.addAction(self.findPeakAction)
#        ct_menu.addAction(self.savePksAction)
        ct_menu.addSeparator()
#        selectItems = self.groupTreeWidget.selectedItems()
#        groupBool = True
#        if len(selectItems) > 0:
#            for item in selectItems:
#                if item.childCount() == 0:#test to see if any of the items selected are leaves
#                    groupBool = False
#        if groupBool:
#            ct_menu.addAction(self.initFPAction)
#        ct_menu.addAction(self.selectGroupAction)
        ct_menu.addAction(self.addFileAction)
#        ct_menu.addAction(self.selectAllAction)
        ct_menu.exec_(self.groupTreeWidget.mapToGlobal(point))


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
#        ct_menu.addAction(self.handleActionA)
#        ct_menu.addAction(self.handleActionB)
        ct_menu.addAction(self.cursorClearAction)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.calcMobAction)
#        ct_menu.addSeparator()
        ct_menu.addAction(self.labelAction)
        ct_menu.addSeparator()
        ct_menu.addAction(self.editLinesAction)
        ct_menu.addSeparator()
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
        if self._getDir_():
            if self.loadWSU_CB.isChecked():
                return QtGui.QMessageBox.warning(self, "Don't Load Files This Way", "Load IMS-TOF Files one at a time\nRight Click under the Data Tab to Add a File")
#                dirList, startDir = ParseIMSDir(self.curDir, getWSUFiles = True)
            else:
                dirList, startDir = ParseIMSDir(self.curDir)
            dirList.sort()
            #You could pre load the widgetitems then fill them in
            if len(dirList) !=0:
                print dirList
                self.dirList = dirList
                self.loadOk = True
                self.firstLoad = False
                if self.readThread.updateThread(dirList):
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

            elif startDir != None:
                return QtGui.QMessageBox.warning(self, "No Data Found",  "Check selected folder, does it have any data?")

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
            self.plotColorIndex = 0
            if multiPlot:
                if len(self.multiPlotList)>0:
                    if self.invertCompCB.isChecked() and len(self.multiPlotList) == 2:
                        self._updatePlotColor_()
                        curDataName = self.multiPlotList[0]
                        self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, ignoreRaw = self.ignoreRaw_CB.isChecked())
                        self._updatePlotColor_()
                        curDataName = self.multiPlotList[1]
                        self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, invert = True, ignoreRaw = self.ignoreRaw_CB.isChecked())
                        curData = self.dataDict[curDataName]

                    else:
                        for curDataName in self.multiPlotList:
                            self._updatePlotColor_()
                            curData = self.dataDict[curDataName]
                            self.plotCurData(curData, curAx)
    #                        curData.plot(curAx, pColor = self.plotColor)
                        #the following makes it so the change is ignored and the plot does not update
                        self.specNameEdit.setText(curData.path)#use dataList to get the name?

                    self.plotWidget.canvas.ytitle="Intensity"
                    if "Mass Counts" in curData.info:
                        self.plotWidget.canvas.xtitle="m/z"
                    elif "TDC Resolution" in curData.info:
                        self.plotWidget.canvas.xtitle="Drift Time (us)"
                    else:
                        self.plotWidget.canvas.xtitle="Drift Time (ms)"
#                        self.plotWidget.canvas.ax.twinx()

            if self.plotLegendCB.isChecked():
                curAx.legend(borderaxespad = 0.03, borderpad=0.25)
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
            self.setDataInfo()
            self.setupTable()
            self.setFilterInfo()

    def setFilterInfo(self):
        if self.lowPassOn_CB.isChecked():
            curData = self.dataDict[self.curDataName]
            self.filterInfo_LE.setText(curData.filterType)

    def setDataInfo(self):
        selectItems = self.groupTreeWidget.selectedItems()
        if len(selectItems) > 0:
            item = selectItems[0]
            if item.childCount() == 0:#test to see if the object is a leaf
                curData = self.dataDict[str(item.toolTip(0))]
                self.fileInfo_TE.clear()
                self.fileInfo_TE.setText(curData.info)

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
#                    self.dataDict[dataName].applyTopHat()
                    self.dataDict[dataName].applySGFilter(self.sgKernel_SB.value(), self.sgOrder_SB.value())
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


                        #if the number of children reaches zero--remove item
                        if parentItem.childCount() == 0:
                            self.groupDict.pop(str(parentItem.toolTip(0)))
                            topIndex = self.groupTreeWidget.indexOfTopLevelItem(parentItem)
                            self.groupTreeWidget.takeTopLevelItem(topIndex)


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


    def updatePlot(self, index):
        if self.ignoreSignal:
            return
        else:
            self.initIndex = index
            QtCore.QTimer.singleShot(500,  self.plotByIndex)

    def plotCurData(self, curData, curAx):
        #test to see if noise has been calculated, if not do it and then plot.
#        if self.plotNoiseEst_CB.isChecked():
#            if curData.noiseOK:
#                curData.plot(curAx, pColor = self.plotColor, plotNoise = True, plotPks = self.plotPkListCB.isChecked(), labelPks = self.labelPeak_CB.isChecked())
#            else:
#                numSegs = len(curData.x)/self.noiseFactor_SB.value()
#                minSNR = self.snrNoiseEst_SB.value()
#                curData.getNoise(numSegs,minSNR)
#                curData.plot(curAx, pColor = self.plotColor, plotNoise = True, plotPks = self.plotPkListCB.isChecked(), labelPks = self.labelPeak_CB.isChecked())
#        else:
        curData.plot(curAx, pColor = self.plotColor, plotFilter = self.lowPassOn_CB.isChecked(),\
                     ignoreRaw = self.ignoreRaw_CB.isChecked(), ignoreNorm = self.normRaw_CB.isChecked())#, plotPks = self.plotPkListCB.isChecked(), labelPks = self.labelPeak_CB.isChecked())
        if self.loadWSU_CB.isChecked():
            if isinstance(curData, WSU):
                if self.showTOF_CB.isChecked():
                    openWindow = True
                    for i,window in enumerate(self.mzPlots):
                        try:#test to see if it existed and then was closed
                            if curData.path == str(window.windowTitle()):#will create and exception if the plot was previously open then closed
                                openWindow = False
                        except:
                            self.mzPlots.pop(i)
                    if openWindow:
                        self.wsuMZPlot(curData)

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
                    self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, ignoreRaw = self.ignoreRaw_CB.isChecked(), ignoreNorm = self.normRaw_CB.isChecked())
                    self._updatePlotColor_()
                    curDataName = self.dataList[self.multiPlotIndex[1]]
                    self.dataDict[curDataName].plot(curAx, pColor = self.plotColor, invert = True, ignoreRaw = self.ignoreRaw_CB.isChecked(), ignoreNorm = self.normRaw_CB.isChecked())
                else:
                    for i in self.multiPlotIndex:
                        self._updatePlotColor_()
                        curDataName = self.dataList[i]
                        curData = self.dataDict[curDataName]
                        self.plotCurData(curData, curAx, ignoreRaw = self.ignoreRaw_CB.isChecked(), ignoreNorm = self.normRaw_CB.isChecked())
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
                curAx.legend(borderaxespad = 0.03, borderpad=0.25)
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
            mplAx.text(x, y*1.05, '%.3f'%x,  fontsize=8, rotation = 45)

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
        if len(self.mzPlots) > 0:
            for plot in self.mzPlots:
#                if isinstance(plot, MPL_Widget):
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

        self.cursorAInfo=[0, 0, 0, 0, 0]#the last element is for the reduced mobility
        self.cursorBInfo=[0, 0, 0, 0, 0]

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

            #IMSViewer Only
            self.curAMob_LE.setText('')

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

            #IMSViewer Only
            self.curBMob_LE.setText('')

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
            self.curAMob_LE.setText('%.3f'%self.cursorAInfo[4])

        if self.cBOn:
            self.cBLabelLE.setText(self.cursorBInfo[3])
            self.cBIndexLE.setText(str(self.cursorBInfo[0]))
            self.cB_XLE.setText('%.4f'%self.cursorBInfo[1])
            self.cB_YLE.setText('%.4f'%self.cursorBInfo[2])
            self.curBMob_LE.setText('%.3f'%self.cursorBInfo[4])

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

        self.cursAText = self.plotWidget.canvas.ax.text(xdata[self.indexA], ydata[self.indexA], '%.3f'%xdata[self.indexA],  fontsize=9, rotation = 45)

        self.cursorAInfo[0]=self.indexA
        self.cursorAInfo[1]=xdata[self.indexA]
        self.cursorAInfo[2]=ydata[self.indexA]
        self.cursorAInfo[3]=line.get_label()
        #used for IMSViewer
        self.cursorAInfo[4]=self.calcMobility(line.get_label(), self.cursorAInfo[1])#label, driftTime

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

        self.cursBText = self.plotWidget.canvas.ax.text(xdata[self.indexB], ydata[self.indexB], '%.3f'%xdata[self.indexB],  fontsize=9, rotation = 45)

        self.cursorBInfo[0]=self.indexB
        self.cursorBInfo[1]=xdata[self.indexB]
        self.cursorBInfo[2]=ydata[self.indexB]
        self.cursorBInfo[3]=line.get_label()
        #used for IMSViewer
        self.cursorBInfo[4]=self.calcMobility(line.get_label(), self.cursorBInfo[1])#label, driftTime

        self.cursorStats()

        self.plotWidget.canvas.draw()

        #print self.cursorAInfo

        ###############################

    def setupTable(self):
        self.rawDataTable.clear()
        #need to disable sorting as it corrupts data addition
        self.rawDataTable.setSortingEnabled(False)
        header = ['Drift Time', 'Intensity']
        headerFilter =  ['Drift Time', 'Intensity', 'Filtered']
        if self.curDataName != None:
            curData = self.dataDict[self.curDataName]
            if self.normRaw_CB.isChecked():
                normFactor = 1
                filterFactor = 1
            else:
                normFactor = curData.normFactor/100
                filterFactor = normFactor*curData.filterFactor/100#/self.normFactor

            if curData.filterOK:
                dataList = N.column_stack((curData.x, curData.y*normFactor, curData.filter*filterFactor))
                self.rawDataTable.addData(dataList)
                self.rawDataTable.setHorizontalHeaderLabels(headerFilter)
            else:
                dataList = N.column_stack((curData.x, curData.y*normFactor))
                self.rawDataTable.addData(dataList)
                self.rawDataTable.setHorizontalHeaderLabels(header)

            self.rawDataTable.resizeColumnToContents(0)

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
            self.P = None
            if parent != None:
                self.P = parent

        def updateThread(self, loadList):
            self.loadList = loadList
            self.numItems = len(loadList)
            self.ready = True
            return True

        def run(self):
            if self.ready:
                while not self.finished and self.numItems > 0:
                    for item in self.loadList:
#                            print os.path.basename(item)
                        if self.P.loadWSU_CB.isChecked():
#                            pass
                            self.numItems = 0
#                            return QtGui.QMessageBox.Information(self.P, "Don't Load Files This Way", "Load IMS-TOF Files one at a time\nRight Click to Add a File")
#                            tempSpec = openWSUTOFFile(item)
#                            if tempSpec[-1]:
#                                data2plot = WSU(tempSpec[0],tempSpec[1],tempSpec[2],tempSpec[3], name = os.path.basename(item), path = item)
#                                data2plot.setInfo(tempSpec[4])
#                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)
#                            else:
#                                return QtGui.QMessageBox.warning(self.P, "Error Loading File",  tempSpec[0])
#                                print 'Empty spectrum: ', item

                        else:
                            tempSpec =  openIMSFile(item)
                            if tempSpec[-1]:
    #                                print 'Spec OK', os.path.basename(item)
                                data2plot = DataClass(tempSpec[0],  tempSpec[1], name = os.path.basename(item), path = item)
                                data2plot.setInfo(tempSpec[2])

                                #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                                #note PyQt_PyObject
                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)
                            else:
                                return QtGui.QMessageBox.warning(self.P, "Error Loading File",  tempSpec[0])
                                print 'Empty spectrum: ', item

                        self.numItems -=1
                    self.emit(QtCore.SIGNAL("finished(bool)"),True)

        def __del__(self):
            self.exiting = True
            self.wait()

def openWSUTOFFile(fileName):
    '''

    '''

    if os.path.isfile(fileName):
        try:
            t1 = time.clock()
            if '.gz' in fileName:
                f = gzip.open(fileName, 'rb')
            else:
                f = open(fileName, 'r')
            header = []
            for i in xrange(15):
                header.append(f.readline())
            f.close()

            mobX = header[-1]
            mobX = mobX.split(' ')
            mobX.pop(0)
            mobX = N.array(mobX, dtype = float)

            wsu = L(fileName, skiprows = 15)
            mzX = wsu[:,0]#extracts the m/z domain
            wsu = wsu[:,1:]#gets rid of first column which is the m/z values

            mobY = wsu.sum(axis = 0)


            mzY = wsu.sum(axis = 1)
            #clean up and assign to class
            header.pop(-1)
            dummyHeader = ''
            for entry in header:
                dummyHeader+=entry

            t2 = time.clock()
            print 'Load Time',t2-t1
            return mobX, mobY, mzX, mzY, dummyHeader, True

        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            print 'Error loading "IMS File" not a WSU FORMAT!: %s'%fileName
            errorMsg = 'Error loading "IMS File" not a WSU FORMAT!: %s\n\n:%s\n%s\n'%(exceptionType, exceptionValue, exceptionTraceback)
            print errorMsg
            return [errorMsg, False]#returns and empty list
    else:
        return []

def openIMSFile(fileName):
    if os.path.isfile(fileName):
        try:
            wsuFile = False
            imsFile = open(fileName, 'r')
            lines2Skip = 4#the case for an WSU-Labview File 12 is for a PCP

            t1 = time.clock()
            header = imsFile.readline()
            if 'TDC Resolution:' in header:#this is the case for a WSU-TOF txt file
                errorMsg = 'Error loading "IMS File" not a PCP or WSU FORMAT!: %s'%fileName
                print errorMsg
                return [errorMsg, False]#

            if "Mass Counts" not in header:
                for i in xrange(lines2Skip):
                    header+=imsFile.readline()

                if 'delta t' in header:
#                    lines = imsFile.readlines()
                    wsuFile = True
                else:
                    header = ''
                    lines2Skip = 12
                    for i in xrange(lines2Skip):
                        header+=imsFile.readline()
            lines = imsFile.readlines()


    #            print header

            x = []
            y = []
            if wsuFile:
                for line in lines:
                    temp = line.split(':')
                    xy = temp[-1].split('\t')
                    x.append(float(xy[0]))
                    y.append(-1*float(xy[1]))

            else:
                for line in lines:
                    splitLine = line.split(' ')
                    x.append(N.float(splitLine[1]))
                    y.append(N.float(splitLine[2]))


            imsFile.close()
            t2 = time.clock()
            print 'Load Time',t2-t1
            return N.array(x), N.array(y), header, True
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            print 'Error loading "IMS File" not a PCP or WSU FORMAT!: %s'%fileName
            errorMsg = 'Error loading "IMS File" not a PCP or WSU FORMAT!: %s\n\n:%s\n%s\n'%(exceptionType, exceptionValue, exceptionTraceback)
            print errorMsg
            return [errorMsg, False]#returns and empty list
    else:
        return ["That is not a file", False]


def ParseIMSDir(startDir, getWSUFiles = False, debug = False):
#        if self.dbStatus:
#    directory= str(QFileDialog.getExistingDirectory())
    #print directory

    if startDir:
        directory = startDir

        t1 = time.clock()
        dirList = []
        i=0

        for root, dirs, files in os.walk(directory):
            #for dir in dirs:
            for file in files:
                if getWSUFiles:
                    if '.txt' in file:# or '.txt' in file:
                        #temptime = time.clock()
                        datadir = os.path.abspath(os.path.join(root, file))
                        dirList.append(datadir)

                        if debug:
                            i+=1
                            if i == 30:
                                t2 = time.clock()
                                for item in dirList:
                                    print item
                                    print ''
                                print t2-t1,  " sec Total"
                                return dirList

                else:
                    if '.TXT' in file or '.txt' in file:
                        #temptime = time.clock()
                        datadir = os.path.abspath(os.path.join(root, file))
                        dirList.append(datadir)

                        if debug:
                            i+=1
                            if i == 30:
                                t2 = time.clock()
                                for item in dirList:
                                    print item
                                    print ''
                                print t2-t1,  " sec Total"
                                return dirList

    #        for item in dirList:
    #            print item
            return dirList, startDir
    else:
        dirList=[]
        return dirList, None

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())
