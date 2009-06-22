
"""
This is the explicit class for Subplot.
"""
#Importing built-in python modules and functions
import sys, os
from os import walk,  path
import base64
import struct
import string

import xml.etree.cElementTree as ET

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

from matplotlib import rc, rcParams, use, interactive
use('Qt4Agg')

import numpy as N

#import matplotlib as mymat
from matplotlib.backends import backend_qt4, backend_qt4agg
backend_qt4.qApp = QtGui.qApp
#backend_qt4agg.matplotlib = mymat


#from io import hdfIO
from mzXML_reader import mzXMLDoc
from dbscan import dbscan#used to consolidate peaks

from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector
#import GUI scripts
import ui_mzViewer
#from mpl_custom_widget import MPL_Widget
from mpl_pyqt4_widget import MPL_Widget
#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"


class mzViewer(ui_mzViewer.Ui_MainWindow):
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        ui_mzViewer.Ui_MainWindow.setupUi(self,MainWindow)

        #self.__updatePlotScripts__()
        #self.__addWidgets__()
        self.__additionalVariables__()
        self.__additionalConnections__()
        self.__setMessages__()
        self.__initContextMenus__()
        self.__setupChrom__()
        self.__setupMZ__()
        self.startup()

        self.drawProfile = True


    def startup(self):

        self.curFile = None
        self.curFileName = None
        self.basePeak = True
        self.TIC = False
        self.curParentScan = None
        self.curScanInfo = None
        self.curScanId = None
        self.curIndex = None
        self.ignoreSignal = False
        self.tempIndex = None
        self.fragScanList = []
        self.fragPlotList = []
        self.scanInfoList = []
        self.fragPlotted = 0#used to keep track of whether or not a fragment has been plotted
        self.fragIndex = None

        self.drawProfile = True

        self.spectrumTabWidget.setCurrentIndex(0)
        numTabs = self.spectrumTabWidget.count()
        j=1
        for i in range(1, numTabs):#this is a weird loop because each time you kill a tab it reorders the whole bunch
            self.spectrumTabWidget.removeTab(j)

        self.__setupChrom__()
        self.__setupMZ__()

        self.chromWidget.canvas.mpl_connect('pick_event', self.OnPickChrom)
        self.mzWidget.canvas.mpl_connect('pick_event', self.OnPickMZ)

    def loadFile(self,  filename):
        if filename:
            self.fileType= str(filename).split('.')[-1]
        if self.fileType == 'mzXML':
            try:

                self.curFile = mzXMLDoc(filename)
                #self.curFile.getDocument(dataFileName)
                self.initiateChrom()
                self.getMZScan(0)
                self.firstLoad = False

            except:
                return QtGui.QMessageBox.information(self.MainWindow,'', "Problem loading data, check file")
        elif self.fileType == 'mzML':
                print "mzML Selected"


    def __readDataFile__(self):
        if self.firstLoad:
            dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                                             self.OpenDataText,\
                                                             self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')
            if dataFileName:
                self.loadFile(dataFileName)
#

        else:
            if self.__askConfirm__("Data Reset",self.ResetAllDataText):
                self.mzWidget.canvas.ax.cla()
                self.chromWidget.canvas.ax.cla()
                self.startup()
                dataFileName = QtGui.QFileDialog.getOpenFileName(self.MainWindow,\
                                                                 self.OpenDataText,\
                                                                 self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')

                self.loadFile(dataFileName)

    def OnPickMZ(self, event):
        self.zoomWasTrue = False##
        if self.is_hZoom:##
            self.zoomWasTrue = True##
            self.hZoomToggle()
        if not isinstance(event.artist, Line2D):
            return True
        line = event.artist
        self.fragIndex = event.ind[0]
        xdata = line.get_xdata()
        try:
            self.fragHandle.remove()
            self.textHandle.remove()
        except:
            pass
        curXlim = self.mzWidget.canvas.ax.get_xlim()
        self.fragHandle = self.mzWidget.canvas.ax.axvline(xdata[self.fragIndex], ls = '--', color ='green')
        showText = 'm/z %.1f'%(xdata[self.fragIndex])
        self.textHandle = self.mzWidget.canvas.ax.text(0.03, 0.95, showText, fontsize=7,\
                                        bbox=dict(facecolor='yellow', alpha=0.1),\
                                        transform=self.mzWidget.canvas.ax.transAxes, va='top')
        self.mzWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
        self.mzWidget.canvas.draw()
        #self.updateMZTab(self.fragIndex+1)
        #print "Frag Index", self.fragIndex
        #self.spectrumTabWidget.setCurrentIndex(self.fragIndex+1)

    def setChromHandle(self):
        line = self.chromLine
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        self.handleA.set_data([xdata[self.curIndex]], [ydata[self.curIndex]])
        curXlim = self.chromWidget.canvas.ax.get_xlim()
        #self.handleAline  = self.chromWidget.canvas.ax.axvline(x = xdata[self.curIndex], ls='--', alpha=0.4, color='blue')
        self.chromWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
        self.chromWidget.canvas.draw()

    def OnPickChrom(self, event):
        if not isinstance(event.artist, Line2D):
            return True

        line = event.artist
        self.curIndex = event.ind[0]
        #print self.curIndex
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        self.handleA.set_visible(True)
        self.handleAline.set_visible(True)
        self.handleA.set_data([xdata[self.curIndex], ydata[self.curIndex]])

        #self.mzWidget.canvas.plotTitle = str(int(xdata[self.curIndex]))
        #print self.curIndex,  xdata[self.curIndex]
        if self.handleAline:
            try:
                self.handleAline.remove()
            except:
                print "Remove Line Error"
        curXlim = self.chromWidget.canvas.ax.get_xlim()
        #self.handleAline  = self.chromWidget.canvas.ax.axvline(x = xdata[self.curIndex], ls='--', alpha=0.4, color='blue')


        #self.spectrumTabWidget.setCurrentIndex(0)
        self.getMZScan(self.curIndex)
        self.chromWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
        self.chromWidget.canvas.draw()

    def __setupChrom__(self):
        self.handleA,  = self.chromWidget.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = 'Cursor A')
        self.handleAline  = self.chromWidget.canvas.ax.axvline(0, ls='--',\
                                        alpha=.5, color='blue', visible=False)

        self.chromSpan = SpanSelector(self.chromWidget.canvas.ax, self.onselectChrom, 'horizontal',
                                 useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )
        self.chromSpan.visible = False
        self.is_hZoomChrom = False

    def __setupMZ__(self):
        # set useblit True on gtkagg for enhanced performance
        self.span = SpanSelector(self.mzWidget.canvas.ax, self.onselect, 'horizontal',
                                 useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )
        #print self.span
        self.span.visible = False
        self.is_hZoom = False
        self.curIndex = 0
        self.zoomWasTrue = False
        self.mzWidget.canvas.xtitle="m/z"
        self.mzWidget.canvas.ytitle="Intensity"

    def initiateChrom(self):
        if self.basePeak:
            self.BPC = N.array(self.curFile.data.get('BPC'))
            self.scanSBox.setMaximum(len(self.BPC))
            #self.scanHSlider.setMaximum(len(self.BPC))
            if len(self.BPC) >=1:
                self.xvalues = N.array(self.curFile.data.get('expTime'))
                self.chromLine, = self.chromWidget.canvas.ax.plot(self.xvalues, self.BPC, 'r', picker = 5)
                #self.chromYScale = (BPC.min(), (BPC.max()*1.1))
                #self.chromWidget.canvas.ax.set_ylim(self.chromYScale[0], self.chromYScale[1])
                self.chromWidget.canvas.xtitle="Scan #"
                self.chromWidget.canvas.ytitle="Intensity"
                self.chromWidget.canvas.plotTitle = self.curFile.filename
                self.chromWidget.canvas.format_labels()
                self.chromWidget.canvas.draw()

    def updateMZScan(self):
        if self.curFile.data.get('spectrum'):
            self.mzscan = self.curFile.data.get('spectrum')
            if self.drawProfile:
                self.mzWidget.canvas.ax.plot(self.mzscan[0], self.mzscan[1],  'b')
            else:
                self.mzWidget.canvas.ax.vlines(self.mzscan[0], 0, self.mzscan[1],  'b')
            self.mzWidget.canvas.plotTitle = "Scan #"+self.curScanInfo.get('id')
            #self.mzWidget.canvas.format_labels()
            self.mzYScale = (self.mzscan[1].min(), (self.mzscan[1].max()*1.1))
            self.mzWidget.canvas.ax.set_ylim(self.mzYScale[0], self.mzYScale[1])#so that high intensity vlines don't dominate
            self.mzWidget.canvas.format_labels()
            self.mzWidget.canvas.draw()


    def getMZScan(self, index, curIndexdjust=None):#0 is subtract, 1 is add
        self.scanInfoList = []
        if self.curFile:
                if curIndexdjust:
                    if curIndexdjust == 0:
                        self.curParentScan = self.curFile.scanList[(index-1)]
                    elif curIndexdjust == 1:
                        self.curParentScan = self.curFile.scanList[(index+1)]
                else:
                    self.curParentScan = self.curFile.scanList[index]
                self.curFile.handleSpectrum(self.curParentScan)
                self.scanInfoList.append(self.curFile.getScanInfo(self.curParentScan))
                self.curScanInfo = self.scanInfoList[0]
                #self.curScanInfo = self.curFile.getScanInfo(self.curParentScan)
                self.fragScanList = self.curParentScan.findall(self.curFile.ns+'scan')

                self.mzWidget.canvas.ax.cla()
                self.fragPlotList = []
                self.fragPlotted = 0
                self.curFragIndex =0
                self.prevFragIndex = 0
                self.fragIndex = None

                numTabs = self.spectrumTabWidget.count()
                self.spectrumTabWidget.setCurrentIndex(0)
                j=1
                for i in range(1, numTabs):#this is a weird loop because each time you kill a tab it reorders the whole bunch
                    self.spectrumTabWidget.removeTab(j)

                if self.fragScanList:
                    for fragScan in self.fragScanList:
                        self.scanInfoList.append(self.curFile.getScanInfo(fragScan))
                        precurMZ = float(self.curFile.getScanInfo(fragScan).get('mz'))
                        #print precurMZ
                        self.mzWidget.canvas.ax.axvline(precurMZ, ls=':', alpha = 0.5,  color='r',  picker = 5)
#                        self.mzWidget.cavnas.ax2.histogram(precurMZ)
                        tabName = "m/z %.1f"%(precurMZ)
                        #print tabName
                        self.spectrumTabWidget.addTab(self.makePrecursorTab(fragScan, tabName), tabName)


                self.curScanId = int(self.curScanInfo.get('id'))
                self.scanSBox.setValue(self.curScanId)
                #print self.curScanId
                #print type(self.curScanId)

                self.updateMZScan()
                self.updateScanInfo()
        else:
            print "No file loaded..."

    def makePrecursorTab(self, fragScan, tabName):
        fragTab = QtGui.QWidget()
        fragTab.setWindowModality(QtCore.Qt.NonModal)
        fragTab.setEnabled(True)
        fragTab.setObjectName(tabName)
        #HISTOGRAM DISABLED
        fragPlot = MPL_Widget(fragTab, doublePlot = False)
        #fragPlot.enableEdit()
        self.fragPlotList.append(fragPlot)
        QtGui.QHBoxLayout(fragTab).addWidget(fragPlot)
        return fragTab

    def updateMZTab(self, int):
        self.curFragIndex = int
        if self.fragPlotted == len(self.fragPlotList):
            self.curScanInfo = self.scanInfoList[int]
            #print "equal"
            #return True
        elif self.curFragIndex == self.prevFragIndex:
            self.curScanInfo = self.scanInfoList[int]
        elif int != 0:
            self.prevFragIndex = int
            precursorSpec, scanInfo = self.curFile.getPreSpectrum(self.fragScanList[int-1])#minus 1 because we want to keep 0
            #self.scanInfoList.append(scanInfo)
            self.curScanInfo = self.scanInfoList[int]
            fragPlot = self.fragPlotList[int-1]
            if self.drawProfile:
                fragPlot.canvas.ax.plot(precursorSpec[0], precursorSpec[1])
            else:
                fragPlot.canvas.ax.vlines(precursorSpec[0], 0, precursorSpec[1])
            #HISTOGRAM ENABLED
#            fragPlot.canvas.ax2.hist(precursorSpec[1], bins = 100)
            #fragPlot.canvas.ax2.hist(precursorSpec[1], bins = 100, log = True)
            #print len(precursorSpec[1])


            fragPlot.canvas.plotTitle = "Scan #%s, m/z: %s"%(self.curScanInfo.get('id'), self.curScanInfo.get('mz'))
            fragPlot.canvas.xtitle="m/z"
            fragPlot.canvas.ytitle="Intensity"
            self.labelPeaks(fragPlot.canvas.ax, precursorSpec)
            fragPlot.canvas.format_labels()
            fragPlot.canvas.draw()

            self.fragPlotted +=1
            #return True

        self.updateScanInfo()

    def labelPeaks(self, mplAxis, xyVals):
        dbscanOK = False
        try:
            newPeaks = consolidatePeaks(xyVals[0], xyVals[1], xyVals[1].argsort(), diffCutoff = 2.00)
            dbscanOK = newPeaks[3]
        except:
            print "DBSCAN of peaks failed"
        if dbscanOK:
            xyVals = [N.array(newPeaks[0]), N.array(newPeaks[1])]

            #return newPeakLoc, newIntLoc, newPointLoc, boolAns
            #print newPeaks[3]
        order = xyVals[1].argsort()#get order intensities
        #order.sort()
        numPeaks = 5
        if len(xyVals[1])<=5:
            numPeaks = len(xyVals)

        newx = xyVals[0][order[-numPeaks:]]
        newy = xyVals[1][order[-numPeaks:]]
        for i, mz in enumerate(newx):
            showText = '%.2f'%(mz)
            mplAxis.text(mz,newy[i], showText, fontsize=7)#,\
                         #bbox=dict(facecolor='yellow', alpha=0.1),\
                         #transform=self.mzWidget.canvas.ax.transAxes, va='top')


    def updateScanInfo(self):
        n = 0
        for item in self.curScanInfo.iteritems():
            m = 0
            for entry in item:
                if entry is None:
                    entry = ""
                newitem = QtGui.QTableWidgetItem(entry)
                self.tableWidget.setItem(n,  m,  newitem)
                m+=1
            n+=1


    def hZoomToggle(self):
        if self.is_hZoom:
            self.is_hZoom = False
            self.span.visible = False
        else:
            self.is_hZoom = True
            self.span.visible = True

    def onselect(self, xmin, xmax):
        #print xmin,  xmax
        if self.is_hZoom:
            #x values provided, need to get indices for y values
            yminindex = self.mzscan[0].searchsorted(xmin)
            ymaxindex = self.mzscan[0].searchsorted(xmax)
            #get sub section of y array
            localy = self.mzscan[1][yminindex:ymaxindex]
            #get local min and local max
            if len(localy) > 0:
                localmin = localy.min()
                localmax = localy.max()
                self.mzWidget.canvas.ax.set_ylim(ymin = (localmin-0.1*(localmax)),  ymax = 1.1*localmax)
                self.mzWidget.canvas.ax.set_xlim(xmin,  xmax)
            self.mzWidget.canvas.draw()

        if self.zoomWasTrue:
            #self.hZoomToggle()
            self.is_hZoom = True
            self.span.visible = True


    def hZoomToggleChrom(self):
        if self.is_hZoomChrom:
            self.is_hZoomChrom = False
            self.chromSpan.visible = False
        else:
            self.is_hZoomChrom = True
            self.chromSpan.visible = True

    def onselectChrom(self, xmin, xmax):
            #print xmin,  xmax
            if self.is_hZoomChrom:
                #x values provided, need to get indices for y values
                yminindex = self.xvalues.searchsorted(xmin)
                ymaxindex = self.xvalues.searchsorted(xmax)
                #get sub section of y array
                localy = self.BPC[yminindex:ymaxindex]
                #get local min and local max
                if len(localy)>0:
                    localmin = localy.min()
                    localmax = localy.max()
                    self.chromWidget.canvas.ax.set_ylim(ymin = (localmin-0.1*(localmax)),  ymax = 1.1*localmax)
                    self.chromWidget.canvas.ax.set_xlim(xmin,  xmax)
                self.chromWidget.canvas.draw()

    def autoscale_plot(self):
        #self.rescale_plot()
        self.mzWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        self.mzWidget.canvas.ax.set_ylim(self.mzYScale[0], self.mzYScale[1])
        self.mzWidget.canvas.draw()

    def autoscaleChrom(self):
        self.chromWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
        #self.chromWidget.canvas.ax.set_ylim(self.chromYScale[0], self.chromYScale[1])
        self.chromWidget.canvas.draw()

    def toggleDraw(self):
        if self.drawProfile:
            self.drawProfile = False
            self.getMZScan(self.curIndex)
            print "Profile Draw Disabled"
        else:
            self.drawProfile = True
            self.getMZScan(self.curIndex)
            print "Profile Draw Enabled"

    def __initContextMenus__(self):
        #self.mzWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.spectrumTabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.chromWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.mzWidget.connect(self.mzWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.mzWidgetContext)
        self.chromWidget.connect(self.chromWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.chromWidgetContext)
        self.spectrumTabWidget.connect(self.spectrumTabWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.spectrumTabContext)

    def mzWidgetContext(self, point):
        '''Create a menu for mzWidget'''
        mzct_menu = QtGui.QMenu("Menu", self.mzWidget)
        mzct_menu.addAction(self.hZoom)
        mzct_menu.addAction(self.actionAutoScale)
        mzct_menu.exec_(self.mzWidget.mapToGlobal(point))

    def chromWidgetContext(self, point):
        '''Create a menu for mzWidget'''
        chromct_menu = QtGui.QMenu("Menu", self.chromWidget)
        chromct_menu.addAction(self.hZoomChrom)
        chromct_menu.addAction(self.actionAutoScaleChrom)
        chromct_menu.exec_(self.chromWidget.mapToGlobal(point))

    def spectrumTabContext(self, point):
        '''Create a menu for spectrumTabWidget'''
        STct_menu = QtGui.QMenu("Menu", self.spectrumTabWidget)
        STct_menu.addAction(self.hZoom)
        STct_menu.addAction(self.actionAutoScale)
        STct_menu.addAction(self.actionToggleDraw)
        STct_menu.exec_(self.spectrumTabWidget.mapToGlobal(point))

    def __setMessages__(self):
        '''This function is obvious'''
        self.SaveDataText = "Choose a name for the data file to save:"
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        self.OpenDataText = "Choose a data file to open:"
        self.ResetAllDataText = "This operation will reset all your data.\nWould you like to continue?"

    def __additionalVariables__(self):
        '''Extra variables that are utilized by other functions'''
        self.__curDir = os.getcwd()
        self.firstLoad = True


    def __additionalConnections__(self):
        self.hZoom = QtGui.QAction("Horizontal Zoom",  self.MainWindow)
        self.hZoom.setShortcut("Ctrl+Z")
        self.spectrumTabWidget.addAction(self.hZoom)
        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.hZoomToggle)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.spectrumTabWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

        self.actionAutoScaleChrom = QtGui.QAction("Autoscale",  self.chromWidget)
        self.chromWidget.addAction(self.actionAutoScaleChrom)
        self.actionAutoScaleChrom.setShortcut("Ctrl+Shift+A")
        QtCore.QObject.connect(self.actionAutoScaleChrom,QtCore.SIGNAL("triggered()"), self.autoscaleChrom)

        self.hZoomChrom = QtGui.QAction("Horizontal Zoom",  self.chromWidget)
        self.chromWidget.addAction(self.hZoomChrom)
        self.hZoomChrom.setShortcut("Ctrl+Shift+Z")
        QtCore.QObject.connect(self.hZoomChrom,QtCore.SIGNAL("triggered()"), self.hZoomToggleChrom)

        self.actionToggleDraw = QtGui.QAction("Toggle Draw Style",  self.spectrumTabWidget)
        self.spectrumTabWidget.addAction(self.actionToggleDraw)
        self.actionToggleDraw.setShortcut("Ctrl+D")
        QtCore.QObject.connect(self.actionToggleDraw,QtCore.SIGNAL("triggered()"), self.toggleDraw)

        self.actionScanUp = QtGui.QAction("",  self.chromWidget)
        self.chromWidget.addAction(self.actionScanUp)
        self.actionScanUp.setShortcut("Up")
        QtCore.QObject.connect(self.actionScanUp,QtCore.SIGNAL("triggered()"), self.scanUp)

        self.actionScanDown = QtGui.QAction("",  self.chromWidget)
        self.chromWidget.addAction(self.actionScanDown)
        self.actionScanDown.setShortcut("Down")
        QtCore.QObject.connect(self.actionScanDown,QtCore.SIGNAL("triggered()"), self.scanDown)


        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.actionRunScript,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)
        QtCore.QObject.connect(self.spectrumTabWidget,QtCore.SIGNAL("currentChanged(int)"),self.updateMZTab)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def testChange(self):
        self.ignoreSignal = False#reset the value for future
        if self.tempIndex == self.curIndex:
            self.updateScan(self.curIndex)
            print "Update Scan Go"
        else:
            self.customEventHandler(self.curIndex)

    def customEventHandler(self, val):
        if self.ignoreSignal:
            return True
        else:
            self.tempIndex = val
            QtCore.QTimer.singleShot(300, self.testChange)
            self.ignoreSignal = True

    def scanUp(self):
        if self.curScanId:
            self.curIndex+=1
            '''
            The first time self.ignoresignal is set to False
            '''
            self.customEventHandler(self.curIndex)
            print "Up"

    def scanDown(self):
        if self.curScanId:
            self.curIndex-=1
            self.customEventHandler(self.curIndex)
            #self.curScanId+=1
#            self.getMZScan(self.curIndex, 1)
            #self.scanSBox.setValue(self.curScanId)
            #self.curScanId-=1
            #self.getMZScan(self.curScanId,  0)
            #self.scanSBox.setValue(self.curScanId)
            print "Down"

    def updateScan(self, newInd = None):
        self.getMZScan(self.curIndex, 1)
        self.setChromHandle()
        self.ignoreSignal = False#reset the value for future

    def __exitProgram__(self):
        if self.okToExit():
            self.MainWindow.close()

    def okToExit(self):
        reply = QtGui.QMessageBox.question(self.MainWindow, "Confirm Quit", "Exit now?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self.MainWindow,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def __showHints__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                             ("Hints and Known Issues"),
                                             ("<p> 1.	For files that contain spectra with a high degree of detail (i.e. not stick mass spectra) use the profile mode for drawing (Ctrl+D).  Otherwise, the plotting will be slow.</p>"
                                             "<p> 2. I haven't incorporated MS^n (where n >= 3) spectrum views at this point--I didn't have an example file to test.</p>"
                                             "<p>3.  If the program is too slow, remember python is not or ever intended to be C.</p>"
                                             "<p>4.  I have not incorporated a reader for mzData files as this format does not explictly store base peak and TIC values for chromatogram generation.  In order to do this each scan must be read simply to construct the TIC/BPC.  This is very slow.  The new mzML format will be supported in the very near future.</p>"
                                             "<p>5.  Yes, the slider is not working just yet, but give it some time...</p>"))

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self.MainWindow,
                                            ("mzViewer V.0.2, August, 2008"),
                                            ("<p><b>mzViewer</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of mzViewer was to provide a user-friendly, open-source tool"
        " for examining common mass spectrometry data formats (e.g. mzXML and mzML* (*in the future)"
        " using numpy and matplotlib.  Feel free to update"
        " (preferably with documentation) mzViewer and please share your contributions"
        " with the rest of the community.</p>"))



#class precursorTabWidget(QtGui.QWidget):
#    def __init__(self, precursorScan,  parent, name=None):
#        QtGui.QWidget.__init__(self,  parent.mzTab)
#        #def makePrecursorTab(self, fragScan, tabName):
#        #fragTab = QtGui.QWidget()
#        self.parent = parent
#        self.scan = precursorScan
#        self.setWindowModality(QtCore.Qt.NonModal)
#        self.setEnabled(True)
#        if name:
#            self.setObjectName(name)
#        self.fragPlot = MPL_Widget(self)
#        self.horizontalLayout = QtGui.QHBoxLayout()
#        self.horizontalLayout.addWidget(self.fragPlot)
#        self.precursorSpec = None
#        self.scanInfo = None
#
#
#    def updatePlot(self):
#        self.precursorSpec, self.scanInfo = self.parent.curFile.getPreSpectrum(self.scan)
#        self.fragPlot.canvas.ax.vlines(self.precursorSpec[0], 0, self.precursorSpec[1])
#        self.fragPlot.canvas.plotTitle = "Scan #%s"%(self.scanInfo.get('id'))
#        self.fragPlot.canvas.draw()


def consolidatePeaks(peakLoc, peakInt, rawPeakInd, diffCutoff = 2.00):
    '''
    Designed to find the monoisotopic peak
    This is a hack, not a good solution but it works for now

    '''
    #need to make the input vector 2D
    #remember for cClass, -1 is an outlier (i.e. a stand alone peak), and other numbers are the groups
    cClass, tType, Eps, boolAns = dbscan(N.column_stack((N.zeros_like(peakLoc),peakLoc)), 1, Eps = diffCutoff)
#    print peakLoc
#    print cClass
    print "Consolidate Bool", boolAns
    newPeakLoc = []
    newIntLoc = []
    newPointLoc = []
    if boolAns:
        singlePnts = N.where(cClass == -1)[0]
        for pnt in singlePnts:
            newPeakLoc.append(peakLoc[pnt])
            newIntLoc.append(peakInt[pnt])
            newPointLoc.append(rawPeakInd[pnt])

        if len(cClass)>0:
            if cClass.max() > 0:#otherwise there is just one outlier
                for i in xrange(1,int(cClass.max())+1):
                    tempInd = N.where(i == cClass)[0]
                    if len(tempInd)>0:
    #                    print tempInd
                        maxLoc = peakInt[tempInd].argmax()
        #                intSort = peakInt[tempInd].argsort()

        #                maxLoc = intSort[0]

        #                print peakLoc[maxLoc+tempInd[0]], peakInt[maxLoc+tempInd[0]], rawPeakInd[maxLoc+tempInd[0]]
                        newPeakLoc.append(peakLoc[maxLoc+tempInd[0]])
                        newIntLoc.append(peakInt[maxLoc+tempInd[0]])
                        newPointLoc.append(rawPeakInd[maxLoc+tempInd[0]])

#            print newPeakLoc
#            print newIntLoc
#            print newPointLoc
        return newPeakLoc, newIntLoc, newPointLoc, boolAns
#        else:
#            print "Error with Consolidation--using raw peaks"
#            return peakLoc, peakInt, rawPeakInd
    else:
        print "Error with Consolidation--using raw peaks"
        return peakLoc, peakInt, rawPeakInd, boolAns

def groupOneD(oneDVec, tol, origOrder):
    '''
    oneDVec is already sorted
    tol is in ppm
    it would be nice to take into account the original order of the peaks to make sure that
    peaks from the same spectrum don't contribute to the same m/z fingerprint
    one way to do this is to take the closest peak
    '''
    diffArray = N.diff(oneDVec)
    groups = N.zeros_like(diffArray)
    gNum = 0
    origNum = 0
    for i,diffVal in enumerate(diffArray):
        if origOrder[i+1]!=origNum:#test to make sure that the next value does not come from the same spectrum
            ppmDiff = (diffVal/oneDVec[i+1])*1000000
            if ppmDiff <= tol:
                groups[i] = gNum
            else:
                groups[i] = gNum
                gNum+=1
        else:
            groups[i] = gNum
            gNum+=1
        origNum = origOrder[i+1]

    return groups, gNum

def run_main():
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = mzViewer(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":

    run_main()
