
"""
This is the explicit class for Subplot.

Need to keep picked spec digger open and not reopen a new window
Add protein to each plot, set limits on frag plot.


"""
#Importing built-in python modules and functions
import sys, os
from os import walk,  path
import base64
import struct
import string
import time
import xml.etree.cElementTree as ET

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog,  QApplication

from matplotlib import rc, rcParams, use, interactive
use('Qt4Agg')

import numpy as N

from matplotlib.backends import backend_qt4, backend_qt4agg
backend_qt4.qApp = QtGui.qApp

#from io import hdfIO
#from mzXML_reader import mzXMLDoc
#from mzXMLReader import mzXMLDoc
from SpecDigger.mzXMLReader import mzXMLDoc#needed because of isinstance call
from dbscan import dbscan#used to consolidate peaks

from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector
#import GUI scripts
import ui_mzViewer
#from mpl_custom_widget import MPL_Widget
from mpl_pyqt4_widget import MPL_Widget
from SpecDigger.specDiggerModal import SpecDiggerModal as SpecDig


'''
ToDo:

Add twin axis for elution time
requires conversion of XML text to seconds and minutes

/usr/bin/pyuic4 /home/clowers/workspace/pyMZViewer/mzViewer.ui  -o /home/clowers/workspace/pyMZViewer/ui_mzViewer.py
'''

COLORS = ['#A3293D','#3B9DCE','#293DA3','#5229A3','#297AA3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']


class mzViewer(QtGui.QMainWindow, ui_mzViewer.Ui_MainWindow):
    def __init__(self, parent = None):
        super(mzViewer,  self).__init__(parent)
        self.ui = self.setupUi(self)
        #ui_mzViewer.Ui_MainWindow.setupUi(self,MainWindow)

        #self.__updatePlotScripts__()
        #self.__addWidgets__()
        self.__additionalVariables__()
        self.__additionalConnections__()
        self.__setMessages__()
        self.__initContextMenus__()
#        self.__setupChrom__()
#        self.__setupMZ__()
        self.startup()

        self.drawProfile = False


    def startup(self):

        self.curFile = None
        self.curFileName = None
        self.basePeak = True
        self.TIC = False
        self.curParentScan = None
        self.chromLine = None
        self.bpcOk = True
        self.curLine = None
        self.curScanInfo = None
        self.curScanId = None
        self.curIndex = None
        self.ignoreSignal = False
        self.tempIndex = None
        self.yMax = 1.0#will be the maximum for the Y scale after autozoom
        self.fragScanList = []
        self.fragPlotList = []
        self.precLineList = []#used to keep an index of the lines that can be picked to generate fragment spectra
        self.fragTabDict = {}
        self.xicDict = {}
        self.scanInfoList = []
        self.fragPlotted = 0#used to keep track of whether or not a fragment has been plotted
        self.fragIndex = None

        self.drawProfile = False
        self.tableWidget.clear()

        self.spectrumTabWidget.setCurrentIndex(0)
        numTabs = self.spectrumTabWidget.count()
        j=1
        for i in range(1, numTabs):#this is a weird loop because each time you kill a tab it reorders the whole bunch
            self.spectrumTabWidget.removeTab(j)

        self.__setupChrom__()
        self.__setupMZ__()

        self.chromWidget.canvas.mpl_connect('pick_event', self.OnPickChrom)
        self.mzWidget.canvas.mpl_connect('pick_event', self.OnPickMZ)

        self.childList = []

    def loadFile(self,  filename):
        if filename:
            self.fileType= str(filename).split('.')[-1]
            self.__curDir = os.path.dirname(str(filename))
        if self.fileType == 'mzXML':
#            try:

            #tempName = os.path.split(str(filename))[-1]
            tempName = os.path.basename(str(filename))
            if self.dataFileDict.has_key(tempName):
                print "File Has Already Been Loaded.  Replace?"
            else:
                self.dataFileDict[tempName] = mzXMLDoc(filename)
                self.spectra_CB.addItem(tempName)
                self.firstLoad = False
                self.spectra_CB.setCurrentIndex(len(self.dataFileDict)-1)
                #self.setupDataFile(tempName)

#            except:
#                return QtGui.QMessageBox.information(self,'', "Problem loading data, check file")
        elif self.fileType == 'mzML':
                print "mzML Selected"

    def __initSpecDigger__(self):
        if isinstance(self.curFile, mzXMLDoc):
            for win in self.childList:
                if isinstance(win, SpecDig):
                    try:
                        win.close()
                    except:
                        pass

            w = SpecDig(mzXMLResult = self.curFile)
            w.show()
            QtCore.QObject.connect(w, QtCore.SIGNAL("specSelected(PyQt_PyObject)"), self.specDiggerSelect)
            self.childList.append(w)
        else:
            print "self.curFile is not a mzXMLDoc Instance"

    def specDiggerSelect(self, returnObj = None):
        if returnObj != None:
            if returnObj[3] == 'mzXML':
                self.curIndex = returnObj[0]
                xVal = returnObj[1]
                yVal = returnObj[2]
                self.handleA.set_data([xVal, yVal])

                self.getMZScan(self.curIndex)
                #self.chromWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
                self.chromWidget.canvas.draw()
                print "Spec Digger Connect"
                print returnObj


    def resetXIC(self):
        self.ignoreSignal = True
        self.xicList_CB.clear()
        self.xicList_CB.addItem('None')
        if len(self.curFile.data['XIC']) > 0:
            for key in self.curFile.data['XIC'].keys():
                self.xicList_CB.addItem(key)
        self.ignoreSignal = False


    def setupDataFile(self, fileKey):
        if self.dataFileDict.has_key(str(fileKey)):
            self.curFile = self.dataFileDict[str(fileKey)]#grabs loaded mzXMLDoc from dictionary
            self.__setupChrom__()#sets up span, handle for picker
            self.__setupMZ__()#clears axis, sets up span
            self.resetXIC()
            self.initiateChrom()#sets title and plots BPC, adds picker
            self.getMZScan(0)#




    def __readDataFile__(self):
        if self.firstLoad:
            dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                             self.OpenDataText,\
                                                             self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')
            if dataFileName:
                self.loadFile(dataFileName)
#

        else:
#            if self.__askConfirm__("Data Reset",self.ResetAllDataText):
            self.startup()
            dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                                 self.OpenDataText,\
                                                                 self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')
            if dataFileName:
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

        for i in xrange(self.spectrumTabWidget.count()):
            if str(self.spectrumTabWidget.tabText(i)) == showText:
                self.spectrumTabWidget.setCurrentIndex(i)
                self.mzWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
                self.mzWidget.canvas.draw()
                return True


        #handle precursor ion setup
        if self.fragScanList != None:
            if len(self.fragScanList) > 0:
                for fragScan in self.fragScanList:
#                    print "Frag Scan", fragScan
                    self.scanInfoList.append(self.curFile.getScanInfo(fragScan))
                    precurMZ = float(self.curFile.getScanInfo(fragScan).get('mz'))
                    #print precurMZ
#                    self.mzWidget.canvas.ax.axvline(precurMZ, ls=':', alpha = 0.5,  color='r',  picker = 5)
    #                        self.mzWidget.cavnas.ax2.histogram(precurMZ)
                    tabName = "m/z %.1f"%(precurMZ)
                    if tabName == showText and not self.fragTabDict.has_key(str(fragScan)):
                    #print tabName
                        self.spectrumTabWidget.addTab(self.makePrecursorTab(fragScan, tabName), tabName)

                    for i in xrange(self.spectrumTabWidget.count()):
                        if str(self.spectrumTabWidget.tabText(i)) == tabName:
                            self.spectrumTabWidget.setCurrentIndex(i)
                            continue



        self.mzWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
        self.mzWidget.canvas.draw()
        #self.updateMZTab(self.fragIndex+1)
        #print "Frag Index", self.fragIndex
        #self.spectrumTabWidget.setCurrentIndex(self.fragIndex+1)


    def setChromHandle(self):
        line = self.curLine
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
                pass
#                print "Remove Line Error"
        curXlim = self.chromWidget.canvas.ax.get_xlim()
        #self.handleAline  = self.chromWidget.canvas.ax.axvline(x = xdata[self.curIndex], ls='--', alpha=0.4, color='blue')


        #self.spectrumTabWidget.setCurrentIndex(0)
        self.getMZScan(self.curIndex)
        self.chromWidget.canvas.ax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
        self.chromWidget.canvas.draw()

    def __setupChrom__(self):

        self.chromWidget.canvas.ax.cla()
        self.handleA, = self.chromWidget.canvas.ax.plot([0], [0], 'o',\
                                        ms=8, alpha=.5, color='yellow', visible=False,  label = '_nolegend_')
        self.handleAline = self.chromWidget.canvas.ax.axvline(0, ls='--',\
                                        alpha=.5, color='blue', visible=False)

        self.chromSpan = SpanSelector(self.chromWidget.canvas.ax, self.onselectChrom, 'horizontal',
                                 useblit=True, rectprops=dict(alpha=0.5, facecolor='#C6DEFF') )
        self.chromSpan.visible = False
        self.is_hZoomChrom = False
        self.chromWidget.canvas.draw()

    def __setupMZ__(self):
        self.mzWidget.canvas.ax.cla()
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
        self.mzWidget.canvas.draw()

    def initiateChrom(self, ignoreDraw = False):
        if self.basePeak:
            self.BPC = N.array(self.curFile.data.get('BPC'))
            self.scanSBox.setMaximum(len(self.BPC))
            #self.scanHSlider.setMaximum(len(self.BPC))
            if len(self.BPC) >=1:
                self.xvalues = N.array(self.curFile.data.get('expTime'))
                self.curLine, = self.chromWidget.canvas.ax.plot(self.xvalues, self.BPC, 'r', picker = 5, label = '_nolegend_')
                self.bpcOk = True
                self.chromLine = self.curLine
                self.chromMax = self.BPC.max()*1.1
                #self.chromYScale = (BPC.min(), (BPC.max()*1.1))
                #self.chromWidget.canvas.ax.set_ylim(self.chromYScale[0], self.chromYScale[1])
                self.chromWidget.canvas.xtitle="Scan #"
                self.chromWidget.canvas.ytitle="Intensity"
                self.chromWidget.canvas.plotTitle = self.curFile.fileName
                if ignoreDraw:
                    return True
                else:
                    self.chromWidget.canvas.format_labels()
                    self.chromWidget.canvas.draw()

    def updateMZScan(self):
        if self.curFile.data.get('spectrum'):

            self.mzscan = self.curFile.data.get('spectrum')

            if self.drawProfile:
                self.mzWidget.canvas.ax.plot(self.mzscan[0], self.mzscan[1],  'b')
            else:
                self.mzWidget.canvas.ax.vlines(self.mzscan[0], 0, self.mzscan[1],  'b')

            t0 = time.clock()
            #self.labelPeaks(self.mzWidget.canvas.ax, self.mzscan)#slowest call oddly enough

            self.mzWidget.canvas.plotTitle = "Scan #"+self.curScanInfo.get('id')
            #self.mzWidget.canvas.format_labels()
            self.mzYScale = (self.mzscan[1].min(), (self.mzscan[1].max()*1.1))
            self.mzWidget.canvas.ax.set_ylim(self.mzYScale[0], self.mzYScale[1])#so that high intensity vlines don't dominate
            self.mzWidget.canvas.format_labels()
            #print "access time: ", time.clock()-t0
            self.mzWidget.canvas.draw()




    def getMZScan(self, index, curIndexdjust=None):#0 is subtract, 1 is add
        self.scanInfoList = []
        self.precLineList = []
        if self.curFile:

                #print self.curFile.data.get('')
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
                self.fragScanList.reverse()#we do this so that the mz values will be increasing



                self.mzWidget.canvas.ax.cla()
                self.fragPlotList = []
                self.fragTabDict = {}
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
#                    self.yMax = N.float(self.curScanInfo.get('basePeakIntensity'))
                    for fragScan in self.fragScanList:
                        self.scanInfoList.append(self.curFile.getScanInfo(fragScan))
                        precurMZ = N.float(self.curFile.getScanInfo(fragScan).get('mz'))

                        self.precLineList.append(self.mzWidget.canvas.ax.axvline(precurMZ, ls=':', alpha = 0.7,  color='r',  picker = 3))
#                        print self.precLineList


                self.curScanId = int(self.curScanInfo.get('id'))
                self.scanSBox.setValue(self.curScanId)
                #print self.curScanId
                #print type(self.curScanId)

                self.updateMZScan()#this is the slow method call
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
        fragPlot.canvas.ax.set_ylim(ymin = 0)
        #fragPlot.enableEdit()
        self.fragPlotList.append(fragPlot)
        self.fragTabDict[str(fragScan)] = '0'#this is a dummy value, we just want to be able to search quickly through the keys
        QtGui.QHBoxLayout(fragTab).addWidget(fragPlot)
        return fragTab

    def updateMZTab(self, intVal):
        self.curFragIndex = intVal
        if self.fragPlotted == len(self.fragPlotList):
            self.curScanInfo = self.scanInfoList[intVal]
        elif self.curFragIndex == self.prevFragIndex:
            self.curScanInfo = self.scanInfoList[intVal]
        elif self.curFragIndex != 0:#was int
            self.prevFragIndex = intVal
            precursorSpec, scanInfo = self.curFile.getPreSpectrum(self.fragScanList[intVal-1])#minus 1 because we want to keep 0
            #self.scanInfoList.append(scanInfo)
            self.curScanInfo = self.scanInfoList[intVal]
            fragPlot = self.fragPlotList[intVal-1]
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
            fragPlot.canvas.ax.set_ylim(ymin = 0)
            fragPlot.canvas.draw()

            self.fragPlotted +=1
            #return True

        self.updateScanInfo()

    def labelPeaks(self, mplAxis, xyVals):
        dbscanOK = False
        '''
        As of python 2.6 this is not working...need to investigate.
        '''
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

    def scaleMZYAxis(self, boolAns):
        if boolAns:
            self.autoscaleMZ()

    def scaleChromYAxis(self, boolAns):
        if boolAns:
            self.chromWidget.canvas.ax.autoscale_view(tight = False, scalex=True, scaley=True)
            self.chromWidget.canvas.ax.set_ylim(0, self.chromMax)
            self.chromWidget.canvas.draw()


    def autoscaleMZ(self):
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

    def removeFile(self):
        #get current index value and text for popping and removing of data
        curIndex = self.spectra_CB.currentIndex()
        curText = str(self.spectra_CB.itemText(curIndex))
        #set next value to move to so we can avoid conflicts regarding deletion of data that is currently plotted
        if (self.spectra_CB.count()-1) == 0:#if the current index is 0 then after deletion there will be no data
            self.startup()
            self.chromWidget.autoscale_plot()
            self.mzWidget.autoscale_plot()

        else:
            nextIndex = curIndex - 1
            self.spectra_CB.setCurrentIndex(nextIndex)

        if self.dataFileDict.has_key(curText):
            self.dataFileDict.pop(curText)
            self.spectra_CB.removeItem(curIndex)


    def __initContextMenus__(self):
        #self.mzWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.spectrumTabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.chromWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.spectra_CB.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.mzWidget.connect(self.mzWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.mzWidgetContext)
        self.chromWidget.connect(self.chromWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.chromWidgetContext)
        self.spectrumTabWidget.connect(self.spectrumTabWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.spectrumTabContext)
        self.spectra_CB.connect(self.spectra_CB, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.fileListContext)

    def fileListContext(self, point):
        flct_menu = QtGui.QMenu("Menu", self.spectra_CB)
        flct_menu.addAction(self.removeFileAction)
        flct_menu.exec_(self.spectra_CB.mapToGlobal(point))

    def mzWidgetContext(self, point):
        '''Create a menu for mzWidget'''
        mzct_menu = QtGui.QMenu("Menu", self.mzWidget)
        mzct_menu.addAction(self.mzWidget.Zoom)
        mzct_menu.addAction(self.mzWidget.actionAutoScale)
        mzct_menu.exec_(self.mzWidget.mapToGlobal(point))

    def chromWidgetContext(self, point):
        '''Create a menu for mzWidget'''
        chromct_menu = QtGui.QMenu("Menu", self.chromWidget)
        chromct_menu.addAction(self.chromWidget.Zoom)
        chromct_menu.addAction(self.chromWidget.actionAutoScale)
        #chromct_menu.addAction(self.removeFileAction)
        chromct_menu.exec_(self.chromWidget.mapToGlobal(point))

    def spectrumTabContext(self, point):
        '''Create a menu for spectrumTabWidget'''
        STct_menu = QtGui.QMenu("Menu", self.spectrumTabWidget)
#        STct_menu.addAction(self.hZoom)
#        STct_menu.addAction(self.actionAutoScale)
#        STct_menu.addAction(self.actionToggleDraw)
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
        self.dataFileDict = {}
        self.firstLoad = True


    def __additionalConnections__(self):
#        self.hZoom = QtGui.QAction("Horizontal Zoom",  self)
#        self.hZoom.setShortcut("Ctrl+Z")
#        self.spectrumTabWidget.addAction(self.hZoom)
#        QtCore.QObject.connect(self.hZoom,QtCore.SIGNAL("triggered()"), self.hZoomToggle)
#
#        self.actionAutoScale = QtGui.QAction("AutoScale",  self)
#        self.actionAutoScale.setShortcut("Ctrl+A")
#        self.spectrumTabWidget.addAction(self.actionAutoScale)
#        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)
#
#        self.actionAutoScaleChrom = QtGui.QAction("Autoscale",  self.chromWidget)
#        self.chromWidget.addAction(self.actionAutoScaleChrom)
#        self.actionAutoScaleChrom.setShortcut("Ctrl+Shift+A")
#        QtCore.QObject.connect(self.actionAutoScaleChrom,QtCore.SIGNAL("triggered()"), self.autoscaleChrom)
#
#        self.hZoomChrom = QtGui.QAction("Horizontal Zoom",  self.chromWidget)
#        self.chromWidget.addAction(self.hZoomChrom)
#        self.hZoomChrom.setShortcut("Ctrl+Shift+Z")
#        QtCore.QObject.connect(self.hZoomChrom,QtCore.SIGNAL("triggered()"), self.hZoomToggleChrom)

        self.removeFileAction = QtGui.QAction("Remove File",  self.spectra_CB)
        self.spectra_CB.addAction(self.removeFileAction)
        QtCore.QObject.connect(self.removeFileAction, QtCore.SIGNAL("triggered()"), self.removeFile)

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

        self.actionTabLeft = QtGui.QAction("",  self.mzWidget)
        self.chromWidget.addAction(self.actionTabLeft)
        self.actionTabLeft.setShortcut("Left")
        QtCore.QObject.connect(self.actionTabLeft,QtCore.SIGNAL("triggered()"), self.tabLeft)

        self.actionTabRight = QtGui.QAction("",  self.mzWidget)
        self.chromWidget.addAction(self.actionTabRight)
        self.actionTabRight.setShortcut("Right")
        QtCore.QObject.connect(self.actionTabRight,QtCore.SIGNAL("triggered()"), self.tabRight)

        '''File menu actions slots'''
        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionFileOpen,QtCore.SIGNAL("triggered()"),self.__readDataFile__)
        QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("triggered()"),self.__showAbout__)
        QtCore.QObject.connect(self.actionHints,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.actionRunScript,QtCore.SIGNAL("triggered()"),self.__showHints__)
        QtCore.QObject.connect(self.action_Exit,QtCore.SIGNAL("triggered()"),self.__exitProgram__)
        QtCore.QObject.connect(self.spectrumTabWidget,QtCore.SIGNAL("currentChanged(int)"),self.updateMZTab)
        #this method is called when spectrum index is changed
        QtCore.QObject.connect(self.spectra_CB,QtCore.SIGNAL("currentIndexChanged (QString)"),self.setupDataFile)

        QtCore.QObject.connect(self.xicList_CB,QtCore.SIGNAL("currentIndexChanged (QString)"),self.setupXIC)
        QtCore.QObject.connect(self.getXIC_Btn,QtCore.SIGNAL("clicked()"),self.getXIC)


        #I know this scaling mechanism is a hack but in order to allow for the axvlines to work appropriately this will have to do.
        QtCore.QObject.connect(self.mzWidget,QtCore.SIGNAL("autoScaleAxis(bool)"),self.scaleMZYAxis)

        QtCore.QObject.connect(self.chromWidget,QtCore.SIGNAL("autoScaleAxis(bool)"),self.scaleChromYAxis)

        QtCore.QMetaObject.connectSlotsByName(self)
        QtCore.QObject.connect(self.actionSpectrum_Digger,QtCore.SIGNAL("triggered()"),self.__initSpecDigger__)

        #self.xicList_CB.setDuplicatesEnabled(False)

    def getXIC(self):
        if self.curFile != None:
            hiVal = self.mzHi_SB.value()
            loVal = self.mzLo_SB.value()
            if hiVal <= loVal:
                return QtGui.QMessageBox.warning(self, "XIC Error", "The High m/z value entered is lower than the Lo m/z value\nTry Again!")
            else:
                #executes getXIC for a given file
                xicKey = '%.2f - %.2f'%(loVal,hiVal)
                findVal = self.xicList_CB.findText(xicKey, QtCore.Qt.MatchExactly)
                if findVal == -1:#case where no value is found
                    self.curFile.getXIC(self.curFile.scanList, loVal, hiVal)
                    self.xicList_CB.addItem(xicKey)
                    self.xicList_CB.setCurrentIndex(self.xicList_CB.count()-1)
                else:
                    self.xicList_CB.setCurrentIndex(findVal)


    def setupXIC(self, curString):
        if self.ignoreSignal:
            return True
        if self.curFile != None:
            curString = str(curString)#in case the curString is a QString
            if curString == 'None':
                #need to clear chromWidget
                if len(self.xicDict)>0:
                    for key in self.xicDict.keys():
                        curLine = self.xicDict[key]
                        if curLine:
                            try:
                                curLine.remove()
                            except:
                                pass

                self.chromWidget.canvas.ax.legend_ = None
                self.initiateChrom()
                self.chromTabWidget.setCurrentIndex(0)

                return True
            else:
                if self.overlayBPC_CB.isChecked():
                    if self.bpcOk:
                        pass
                    else:
                        self.initiateChrom(ignoreDraw = True)
                else:
                    if self.bpcOk:
                        self.chromLine.remove()
                        self.bpcOk = False


                plotKey = 'm/z %s'%curString
                xicDict = self.curFile.data.get('XIC')
                print xicDict.keys()
                if xicDict.has_key(curString):
                    xicVals = N.array(self.curFile.data.get('XIC')[curString])
                    if xicVals != None:
                        if len(self.xvalues) == len(xicVals):
                            #need to add instance where it is already plotted
                            curIndex = self.xicList_CB.currentIndex()
                            self.xicDict[plotKey], = self.chromWidget.canvas.ax.plot(self.xvalues, xicVals, color = COLORS[curIndex], label = curString, alpha = 0.6, picker = 5)
                            self.chromMax = xicVals.max()*1.1
                            self.curLine = self.xicDict[plotKey]
                            self.chromWidget.canvas.ax.legend(borderaxespad = 0.03, axespad=0.25)
                            self.chromWidget.canvas.format_labels()
                            self.chromWidget.autoscale_plot()
                            self.chromTabWidget.setCurrentIndex(0)


    def valChange(self):
        self.ignoreSignal = False#reset the value for future
        if self.tempIndex == self.curIndex:
            self.updateScan(self.curIndex)
        else:
            self.customEventHandler(self.curIndex)

    def customEventHandler(self, val):
        '''
        After a key stroke navigating through the spectra
        self.valChange is called which then calls self.updateScan
        '''
        if self.ignoreSignal:
            return True
        else:
            self.tempIndex = val
            QtCore.QTimer.singleShot(3, self.valChange)
            self.ignoreSignal = True

    def handleSpectrumLines(self):
        '''
        Used to help make the transition from full scans to
        ms/ms scans smoother and faster
        '''
        curIndex = self.spectrumTabWidget.currentIndex()
        if curIndex == 0:
            self.drawProfile = True
        else:
            self.drawProfile = False

    def tabRight(self):
#        print "Tab Right"
        curIndex = self.spectrumTabWidget.currentIndex()
        curCount = self.spectrumTabWidget.count()
        numFrags = len(self.fragScanList)
#        print "len fragScanList: ", numFrags
        #case 1: when the next frag spectrum does not exist:
        if curIndex < numFrags:
#            print "case 1"
            if self.fragScanList != None:
                if len(self.fragScanList) > 0:
                    fragScan = self.fragScanList[curIndex]
                    self.scanInfoList.append(self.curFile.getScanInfo(fragScan))
                    precurMZ = float(self.curFile.getScanInfo(fragScan).get('mz'))
                    #print precurMZ
                    tabName = "m/z %.1f"%(precurMZ)
                    if not self.fragTabDict.has_key(str(fragScan)):
                        self.drawProfile = False#used to speed up transitions
                        self.spectrumTabWidget.addTab(self.makePrecursorTab(fragScan, tabName), tabName)

                    for i in xrange(self.spectrumTabWidget.count()):
                        if str(self.spectrumTabWidget.tabText(i)) == tabName:
                            self.spectrumTabWidget.setCurrentIndex(i)
                            return True
#                            continue


        #case 2: when at the maximum frag spectrum that is already plotted
        if curIndex == curCount-1:
#            print "case 2"
            return True
        #case 3: when below the maximum frag spectrum that is already plotted
        if curIndex < curCount-1:
#            print "case 3"
            self.spectrumTabWidget.setCurrentIndex(curIndex+1)
            return True

    def tabLeft(self):
#        print "Tab Left"
        curIndex = self.spectrumTabWidget.currentIndex()
        #case 1: when at the minimum frag spectrum that is already plotted
        if curIndex == 0:
            return True
        else:
            self.spectrumTabWidget.setCurrentIndex(curIndex-1)

    def scanUp(self):
        if self.curScanId:
            self.curIndex+=1
            '''
            The first time self.ignoresignal is set to False
            '''
            self.customEventHandler(self.curIndex)

    def scanDown(self):
        if self.curScanId:
            self.curIndex-=1
            self.customEventHandler(self.curIndex)

    def updateScan(self, newInd = None):

        self.handleSpectrumLines()#used to speed up full scan transitions

        self.getMZScan(self.curIndex, 1)
        self.setChromHandle()
        self.ignoreSignal = False#reset the value for future

    def closeEvent(self,  event = None):
        self.__exitProgram__()

    def __exitProgram__(self):
        #if self.okToExit():
        for win in self.childList:#close any child windows
            try:
                win.close()
            except:
                pass
        self.close()

    def okToExit(self):
        reply = QtGui.QMessageBox.question(self, "Confirm Quit", "Exit now?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            print "Ok to exit"
            return True
        else:
            print "Declined to exit"
            return False

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    def __showHints__(self):
        return QtGui.QMessageBox.information(self,
                                             ("Hints and Known Issues"),
                                             ("<p> 1.	For files that contain spectra with a high degree of detail (i.e. not centroided (stick) mass spectra) use the profile mode for drawing (Ctrl+D).  Otherwise, the plotting will be slow.</p>"
                                             "<p> 2. I haven't incorporated MS^n (where n >= 3) spectrum views at this point--I didn't have an example file to test.</p>"
                                             "<p>3.  If the program is too slow, remember python is not or ever intended to be C.</p>"
                                             "<p>4.  I have not incorporated a reader for mzData files as this format does not explictly store base peak and TIC values for chromatogram generation.  In order to do this each scan must be read simply to construct the TIC/BPC.  This is very slow.  The new mzML format will be supported in the very near future.</p>"
                                             "<p>4.  Ctrl+Z enables/disables zooming, Ctrl+A zooms out entirely (i.e. autoscale).  These shortcuts are by far the easiest way to navigate</p>"
                                             ""))

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self,
                                            ("mzViewer V.0.5, October, 2009"),
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
#    print "Consolidate Bool", boolAns
    newPeakLoc = []
    newIntLoc = []
    newPointLoc = []
    if boolAns:
        singlePnts = N.where(cClass == -1)[0]
        if len(singlePnts)>0:
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

            return newPeakLoc, newIntLoc, newPointLoc, boolAns
        else:
#            print "Error with Consolidation--using raw peaks"
            return newPeakLoc, newIntLoc, newPointLoc, False

    else:
        #print "Error with Consolidation--using raw peaks"
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
    #MainWindow = QtGui.QMainWindow()
    ui = mzViewer()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":

    run_main()
