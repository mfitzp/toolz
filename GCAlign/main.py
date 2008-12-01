#!/usr/bin/env python
###################################
'''To Do:
exclude list/include list with tolerance
save/load peak list that was found...
peak grouping
is the m/z range correct (zero indexing?)
kill child windows when spawned
peak info when clicked
export peak list
'''
###################################
import os, sys
import time

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T

from matplotlib import colors as C
from matplotlib.lines import Line2D
from matplotlib.widgets import SpanSelector, RectangleSelector
from pylab import cm
cmaps = [cm.jet, cm.BrBG, cm.gist_ncar, cm.bone_r,  cm.hot,  cm.spectral, cm.gist_ncar, cm.RdYlBu, cm.BrBG, cm.Accent]

#from LECO_IO import ChromaTOF_Reader as CR
#import SplitNStich as SNS
#import PeakFunctions as PF
import supportFunc as SF
from dataClass import GC_GC_MS_CLASS as GCDATA
from peakFindThread import PeakFindThread as PFT

import ui_iterate


COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

cdict ={
'blue': ((0.0, 0.01, 0.01), (0.01, 0.25, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
'green': ((0.0, 0, 0), (0.05, 0.75, 0.75), (0.25, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
'red': ((0.0, 0, 0), (0.15, 0.25, 0.25), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
}

my_cmap = C.LinearSegmentedColormap('mycmap', cdict, 512)


EXCLUDE = N.arange(30,80)

class Plot_Widget(QtGui.QMainWindow,  ui_iterate.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Plot_Widget,  self).__init__(parent)
        self.ui = self.setupUi(self)

        self.setupVars()
        self.setupGUI()
        self._setThreads_()
        self._setConnections_()
        self._setMessages_()
        self._setContext_()
        self.LayoutStatusBar()



    def _setThreads_(self):
        self.PFT = PFT()

    def _setContext_(self):
#        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._imageContext_)
        self.plotWidget2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget2.connect(self.plotWidget2, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._chromContext_)
#        self.specListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.specListWidget.connect(self.specListWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__listContext__)

    def _chromContext_(self, point):
        '''Create a menu for the chromatogram widget'''
        ct_menu = QtGui.QMenu("Plot Menu", self.plotWidget2)
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
        ct_menu.addSeparator()
        ct_menu.addAction(self.labelAction)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.plotWidget2.mpl2ClipAction)
        ct_menu.exec_(self.plotWidget2.mapToGlobal(point))

    def _setMessages_(self):
        '''This function is obvious'''
        self.ClearTableText = "Are you sure you want to erase\nthe entire table content?"
        self.ClearAllDataText = "Are you sure you want to erase\nthe entire data set?"
        self.NotEditableText = "Sorry, this data format is not table-editable."
        self.OpenScriptText = "Choose a python script to launch:"
        self.SaveDataText = "Choose a name for the data file to save:"
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        self.OpenDataText = "Choose a data file to open:"
        self.ResetAllDataText = "This operation will reset all your data.\nWould you like to continue?"
        self.EmptyArrayText = "There is no data in the array selected.  Perhaps the search criteria are too stringent.  Check ppm and e-Value cutoff values\n"

    def _setConnections_(self):

#        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)

        self.Zoom = QtGui.QAction("Zoom",  self)
        self.Zoom.setShortcut("Ctrl+Z")
        self.plotWidget.addAction(self.Zoom)
        QtCore.QObject.connect(self.Zoom,QtCore.SIGNAL("triggered()"), self.ZoomToggle)

        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

        self.handleActionA = QtGui.QAction("Cursor A", self)
        self.plotWidget2.addAction(self.handleActionA)

        self.handleActionB = QtGui.QAction("Cursor B", self)
        self.plotWidget2.addAction(self.handleActionB)

        self.cursorClearAction = QtGui.QAction("Clear Cursors",  self)
        self.plotWidget2.addAction(self.cursorClearAction)

        self.labelAction = QtGui.QAction("Label Peak",  self)
        self.plotWidget2.addAction(self.labelAction)


        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self._getDataFile_)
        QtCore.QObject.connect(self.addFileBtn,QtCore.SIGNAL("clicked()"),self._getDataFile_)
        QtCore.QObject.connect(self.fndPeaksBtn,QtCore.SIGNAL("clicked()"),self.findChromPeaks)
        QtCore.QObject.connect(self.action_Find_Peaks,QtCore.SIGNAL("triggered()"),self.findChromPeaks)


        QtCore.QObject.connect(self.handleActionA, QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.handleActionB, QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.cursorClearAction, QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.labelAction, QtCore.SIGNAL("triggered()"),self.labelPeak)

        QtCore.QObject.connect(self.actionLabel_Peak,QtCore.SIGNAL("triggered()"),self.labelPeak)
#        QtCore.QObject.connect(self.actionCopy_to_Clipboard,QtCore.SIGNAL("triggered()"),self.mpl2Clip)
        QtCore.QObject.connect(self.actionCursor_A,QtCore.SIGNAL("triggered()"),self.SelectPointsA)
        QtCore.QObject.connect(self.actionCursor_B,QtCore.SIGNAL("triggered()"),self.SelectPointsB)
        QtCore.QObject.connect(self.actionClear_Cursors,QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.cursACB,QtCore.SIGNAL("stateChanged (int)"),self.toggleCA)
        QtCore.QObject.connect(self.cursBCB,QtCore.SIGNAL("stateChanged (int)"),self.toggleCB)

        QtCore.QObject.connect(self.PFT, QtCore.SIGNAL("finished(bool)"), self.plotPickedPeaks)

        QtCore.QObject.connect(self.PFT, QtCore.SIGNAL("progress(int)"), self.threadProgress)

        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.specListSelect)

    def specListSelect(self, widgetItem=None):
        selectItems = self.listWidget.selectedItems()
        #curRow
        if len(selectItems) > 0:
            self.updatePlot(self.listWidget.indexFromItem(selectItems[0]).row())
#            self.multiPlotIndex = []#reset indexes to plot
#            for item in selectItems:
#                self.multiPlotIndex.append(self.specListWidget.indexFromItem(item).row())
#
#            self.plotByIndex(multiPlot = True)


    def _initDataFile_(self, dataFileName):
        print dataFileName
        if self.dataDict.has_key(dataFileName):
            pass
        else:
            #####Text Color Handler
            if self.colorIndex%len(COLORS) == 0:
                self.colorIndex = 0
                self.txtColor = COLORS[self.colorIndex]
                self.colorIndex +=1
            else:
                self.txtColor = COLORS[self.colorIndex]
                self.colorIndex +=1
            self.dataDict[dataFileName] = GCDATA(dataFileName)
            self.dataList.append(dataFileName)
            tempData = self.dataDict[dataFileName]
            tempItem = QtGui.QListWidgetItem(tempData.name)
            tempColor = QtGui.QColor(self.txtColor)
            tempItem.setTextColor(tempColor)
            tempItem.setToolTip(tempData.filePath)
                    #self.specListWidget.addItem(loadedItem.name)
            self.listWidget.addItem(tempItem)

            self.updatePlot(len(self.dataList)-1)


    def _getDataFile_(self):
        dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                             self.OpenDataText,\
                                                             self._curDir, 'HDF5 File (*.h5)')
        if dataFileName:
            self._initDataFile_(str(dataFileName))


    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.curDir)
        directory = str(directory)
        if directory != None:
            self.curDir = directory
        else:
            self.curDir = os.getcwd()

    def setupVars(self):

        self.ref = 'Acetone_Klean.h5'
        self.sam = 'Acetone_R.h5'

        self.numSpec = 25
        self.startIndex = 55000
        self.specIncrement = 400

        self.RSprops = {}
        self.RSprops['edgecolor'] = 'yellow'
        self.RSprops['facecolor'] = 'yellow'
        self.RSprops['alpha'] = 0.3

        self._curDir = os.getcwd()

        self.dataDict = {}
        self.dataList = []

    def setupGUI(self):

        self.plotWidget.canvas.setupSub(1)
#        self.plotWidget2.canvas.setupSub(1)

        self.imageAxis = self.plotWidget.canvas.axDict['ax1']
        self.chromAxis = self.plotWidget2.canvas.ax#Dict['ax1'] #use Dict when using multiplot PyQt4 Widget
        #for some reason when you add a second axis the zooming and autoscaling don't work well.
#        self.chromAxis2 = self.chromAxis.twiny()
#        self.format2ndAxis(self.chromAxis2)

        self.curData = None #reference to the GCGCData Class
        self.curIm = None #reference to the 2D image used during zoom events
        self.mainIm = None #primary 2D plot image initialized when file is loaded and when autoscale is called
        self.curImPlot = None #is the matplotlib axis reference
        self.curChrom = None #current chromatogram
        self.curImPlot = None #is the matplotlib axis reference
        self.plotType = 'TIC'
        self.prevChromLimits = 0
        self.prevImLimits = [0,0]
        ####Peak Info Variables############################
        self.peakInfo = None #when set will be a dictionary containing peak info for the chromatogram
        self.peakLoc2D = None #when set will be a 2D array of picked peak locations and intensities
        self.peakParams = {} #dictionary of peak parameters
        ##############################
        self.txtColor = None
        self.colorIndex = 0
        ###############################
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

        self.RS = RectangleSelector(self.imageAxis, self.imageZoom, minspanx = 2,
                        minspany = 2, drawtype='box',useblit=True, rectprops = self.RSprops)
        self.usrZoom = False
        self.RS.visible = False

        #self.plotWidget.canvas.mpl_connect('button_press_event', self.imageClick)

#        self.mzAxis = self.plotWidget2.canvas.axDict['ax2']

        self.indexHSlider.setMinimum(1)
        self.indexSpinBox.setMinimum(1)
        self.indexHSlider.setMaximum(self.numSpec)
        self.indexSpinBox.setMaximum(self.numSpec)

        self.addChromPickers()
        self.addImPickers()

    def format2ndAxis(self, axis):
        labels_x = axis.get_xticklabels()
        labels_y = axis.get_yticklabels()
#        axis.set_yticklabels([''])

        for xlabel in labels_x:
            xlabel.set_fontsize(8)
        for ylabel in labels_y:
            ylabel.set_fontsize(8)
            ylabel.set_color('b')

    def addChromPickers(self, minX = 0):
        #minX is provided so that the plot will scale correctly when a data trace is initiated
        #Pickers for the 2D image
        self.selectHandleA,  = self.chromAxis.plot([minX], [0], 'o',\
                                        ms=8, alpha=.4, color='yellow', visible=False,  label = '_nolegend_')
        self.selectHandleB,  = self.chromAxis.plot([minX], [0], 's',\
                                        ms=8, alpha=.4, color='green', visible=False,  label = '_nolegend_')
    def addImPickers(self, minX = 0):
        #Pickers for the Chromatogram
        self.selectCursA,  = self.imageAxis.plot([minX], [0], 'o',\
                                        ms=5, alpha=.7, color='red', visible=True,  label = '_nolegend_')
        self.xLine = self.imageAxis.axvline(x=0, ls = ':', color = 'y', alpha = 0.6, visible = True)
        self.yLine = self.imageAxis.axhline(y=0, ls = ':', color = 'y', alpha = 0.6, visible = True)

#        self.cursText = self.imageAxis.text(0, 0, '0rigin',  fontsize=9)

        self.peakPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.imageClick)
#        self.plotWidget.canvas.mpl_connect('pick_event', self.imageClick)

    def imageClick(self, event):
        '''how to use just mousebutton 3 or right mouse click without messing up zoom?'''
        #print event.button

        if event.mouseevent.xdata != None and event.mouseevent.ydata != None:
            if event.mouseevent.button == 1:
                if isinstance(event.artist, Line2D):
                    thisline = event.artist
                    xdata = thisline.get_xdata()
                    ydata = thisline.get_ydata()
                    self.selectCursA.set_data(xdata[event.ind[0]], ydata[event.ind[0]])
#                    self.selectCursA.set_data([event.mouseevent.xdata], [event.mouseevent.ydata])
                    xPnt, yPnt =  int(N.round(event.mouseevent.xdata)), event.mouseevent.ydata
    #                print xPnt, yPnt

                    if self.peakInfo != None:
                        print event.ind[0]
                        for info in self.peakInfo.itervalues():
                            print info[event.ind[0]]

                    self.xLine.set_xdata([xPnt])
                    self.yLine.set_ydata([yPnt])

                    self.imageAxis.draw_artist(self.selectCursA)
                    self.imageAxis.draw_artist(self.xLine)
                    self.imageAxis.draw_artist(self.yLine)
                    self.plotWidget.canvas.blit(self.imageAxis.bbox)

#                self.plotWidget2.canvas.format_labels()
#                self.plotWidget2.canvas.draw()
#                self.plotWidget2.setFocus()


    def colorScale(self, dataMtx):
        dataMtx = N.where(dataMtx<= 0, dataMtx,10)
        lev_exp = N.arange(0, N.log2(dataMtx.max())+1)
        levs = N.power(2, lev_exp)
        return levs

    def updateChromGUI(self):
        self.specLengthSB.setValue(len(self.curChrom))
        self.numSegsSB.setValue(self.curData.rowPoints)

    def updatePlot(self, plotIndex):#, plotType = 'TIC'):
        self.imageAxis.cla()
        self.chromAxis.cla()
        self.addChromPickers()
        self.addImPickers()
        curDataName = self.dataList[plotIndex]
        self.curData = self.dataDict[curDataName]
        self.specNameEdit.setText(self.curData.filePath)#use dataList to get the name
        if self.plotType == 'TIC':
            self.mainIm = self.curData.ticLayer
            self.curIm = self.curData.ticLayer
            self.curChrom = self.curData.getTIC()
            self.curImPlot = self.imageAxis.imshow(self.curIm, alpha = 1,  aspect = 'auto',\
                                                   origin = 'lower',  cmap = my_cmap, label = 'R')
            self.curChromPlot = self.chromAxis.plot(self.curChrom, 'b', label = self.curData.name,\
                                                    picker = 5)

        #update Chrom GUI elements for peak picking and other functions
        self.updateChromGUI()

        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.plotWidget.setFocus()#this is needed so that you can use CTRL+Z to zoom

        self.plotWidget2.canvas.format_labels()
        self.plotWidget2.canvas.draw()
        self.plotWidget2.setFocus()


###########################

    def autoscale_plot(self):
        self.imageAxis.cla()
        self.addImPickers()
        if self.plotType == 'TIC':
            self.curIm = self.curData.ticLayer
        self.imageAxis.imshow(self.mainIm, alpha = 1,  aspect = 'auto', origin = 'lower',  cmap = my_cmap, label = 'R')

        if self.showPickedPeaksCB.isChecked():
            if self.peakInfo != None:
                self.chromAxis.plot(self.peakInfo['peakLoc'],self.peakInfo['peakInt'], 'ro', ms = 3, alpha = 0.4, picker = 5)
                self.imageAxis.plot(self.peakLoc2D[0],self.peakLoc2D[1],'yo', ms = 3, alpha = 0.6, picker = 5)
                #remember the image is transposed, so we need to swap the length of the axes
                self.imageAxis.set_xlim(0,self.curData.rowPoints)
                self.imageAxis.set_ylim(0,self.curData.colPoints)

        self.prevChromLimits = 0
        self.prevImLimits = [0,0]
        self.plotWidget2.autoscale_plot()

        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.plotWidget2.canvas.format_labels()
        self.plotWidget2.canvas.draw()
################Original
#        self.imageAxis.autoscale_view(tight = False, scalex=True, scaley=True)
#        self.plotWidget.canvas.draw()

    def imageZoom(self, event1, event2):
        if self.usrZoom:
            if event1.button == 1 and event2.button == 1:
                'event1 and event2 are the press and release events'
                #print event1.xdata, event1.ydata, event2.xdata, event2.ydata
                dataCoord = [[int(N.round(event1.xdata)), int(N.round(event1.ydata))],[int(N.round(event2.xdata)), int(N.round(event2.ydata))]]
                cols = self.curData.colPoints
                chromLimits = [dataCoord[0][0]*cols+dataCoord[0][1]+self.prevChromLimits,\
                               N.abs(self.prevChromLimits+(dataCoord[1][0]*cols+dataCoord[1][1]))]
                dataCoord = N.array(dataCoord)
                chromLimits = N.array(chromLimits)
                xLim = dataCoord[:,0]
                yLim = dataCoord[:,1]
                xLim.sort()
                yLim.sort()
                chromLimits.sort()
#                print dataCoord
#                print 'X Limits', xLim
#                print 'Y Limits',yLim
#                self.imageAxis.set_xlim(xLim[0],xLim[1])
#                self.imageAxis.set_ylim(yLim[0],yLim[1])
                #####################


#                chromMin = chromLimits.min()
#                chromMax = chromLimits.max()
#                print chromLimits
#                xRange = []
#                yRange = []
#                xRange.append(int(chromMin/self.curData.colPoints))
#                xRange.append(int(chromMax/self.curData.colPoints))
#                yRange.append(int(chromMin%self.curData.colPoints))
#                yRange.append(int(chromMax%self.curData.colPoints))
#                xRange = N.array(xRange)
#                yRange = N.array(yRange)
#                xRange.sort()
#                yRange.sort()
#
#                x = N.arange(xRange[0], xRange[1])
#                y = N.arange(yRange[0], yRange[1])

                #indexing is done as below because the image is transposed.
                self.curIm = self.curIm[yLim[0]:yLim[1],xLim[0]:xLim[1]]
#                print 'Shape', self.curIm.shape, len(x), len(y)

                self.imageAxis.cla()
                self.addImPickers()
                self.imageAxis.imshow(self.curIm, alpha = 1,  aspect = 'auto', \
                                      origin = 'lower',  cmap = my_cmap, label = 'R')
                xLen = len(self.imageAxis.get_xticklabels())
                yLen = len(self.imageAxis.get_yticklabels())
                x = N.arange(xLim[0], xLim[1], int(((xLim[1]-xLim[0])/xLen)))
                y = N.arange(yLim[0], yLim[1], int(((yLim[1]-yLim[0])/yLen)))
                self.imageAxis.set_xticklabels(x)
                self.imageAxis.set_yticklabels(y)
#                print self.imageAxis.get_xticklabels()
#                print self.imageAxis.get_yticklabels()

                x1 = chromLimits[0]
                x2 = chromLimits[1]
                self.chromAxis.set_xlim(x1,x2)
                tempChrom = self.curChrom[x1:x2]
                if len(tempChrom) > 0:
                    self.chromAxis.set_ylim(0, tempChrom.max()*1.1)
                self.prevChromLimits = x1

                #####2D Peak Locations#####

                if self.peakInfo != None:
                    tempPeaks = self.peakInfo['peakLoc']
                    rangeCrit = (tempPeaks >= x1) & (tempPeaks <= x2) #criterion for selection
                    tempPeakInd = N.where(rangeCrit) #peak indicies
                    tempPeakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'][tempPeakInd], self.curData.rowPoints, self.curData.colPoints)
                    self.imageAxis.plot(tempPeakLoc2D[0]-xLim[0]-self.prevImLimits[0],\
                                        tempPeakLoc2D[1]-yLim[0]-self.prevImLimits[1],\
                                        'yo', ms = 3, alpha = 0.6, picker = 5)
                    #self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints, self.curData.colPoints)
                    self.imageAxis.set_xlim(0, self.curIm.shape[1]-1)
                    self.imageAxis.set_ylim(0, self.curIm.shape[0])
                    #print tempPeakInd

                self.prevImLimits = [xLim[0]+self.prevImLimits[0],yLim[0]+self.prevImLimits[1]]

                self.plotWidget2.canvas.format_labels()
                self.plotWidget2.canvas.draw()

                self.plotWidget.canvas.format_labels()
                self.plotWidget.canvas.draw()
                ##############################Original without color scaling
                #self.imageAxis
                #self.curIm = self.imageAxis.imshow(curData.ticLayer, alpha = 1,  aspect = 'auto', origin = 'lower',  cmap = my_cmap, label = 'R', picker = 5)
    #
    #            self.refIm.norm.autoscale(localRef)
    #            self.plotWidget.canvas.draw()




###########Cursor Controls
    def cursAClear(self):
        if self.cAOn:# and self.cAPicker:
            self.selectHandleA.set_visible(False)
            self.plotWidget2.canvas.mpl_disconnect(self.cAPicker)
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

            self.plotWidget2.canvas.draw()

    def cursBClear(self):
        if self.cBOn:# and self.cBPicker:
            self.selectHandleB.set_visible(False)
            self.plotWidget2.canvas.mpl_disconnect(self.cBPicker)
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

            self.plotWidget2.canvas.draw()

    def cursorClear(self):
        self.cursACB.nextCheckState()
        self.cursBCB.nextCheckState()#setCheckState(0)
        self.cursAClear()
        self.cursBClear()

    def cursorStats(self):
        if self.cAOn:
            self.cALabelLE.setText(self.cursorAInfo[3])
            self.cAIndexLE.setText(str(self.cursorAInfo[0]))
            self.cA_XLE.setText('%.2f'%self.cursorAInfo[1])
            self.cA_YLE.setText('%.2f'%self.cursorAInfo[2])

        if self.cBOn:
            self.cBLabelLE.setText(self.cursorBInfo[3])
            self.cBIndexLE.setText(str(self.cursorBInfo[0]))
            self.cB_XLE.setText('%.2f'%self.cursorBInfo[1])
            self.cB_YLE.setText('%.2f'%self.cursorBInfo[2])

        if self.cAOn and self.cBOn:
            self.dx = self.cursorAInfo[1]-self.cursorBInfo[1]
            self.dy = self.cursorAInfo[2]-self.cursorBInfo[2]
            self.dxLE.setText('%.2f'%self.dx)
            self.dyLE.setText('%.2f'%self.dy)
            #return True

    def SelectPointsA(self):
        """
        This method will be called from the plot context menu for
        selecting points
        """
        self.plotWidget2.canvas.mpl_disconnect(self.cBPicker)
        self.cBPicker = None
        if self.cAPicker ==None:
            self.cAPicker = self.plotWidget2.canvas.mpl_connect('pick_event', self.OnPickA)
            self.cAOn = True

    def SelectPointsB(self):

        self.plotWidget2.canvas.mpl_disconnect(self.cAPicker)
        self.cAPicker = None
        if self.cBPicker == None:
            self.cBPicker = self.plotWidget2.canvas.mpl_connect('pick_event', self.OnPickB)
            self.cBOn = True

    def OnPickA(self, event):
        """
        This is the pick_event handler for matplotlib
        This is the pick_event handler for matplotlib
        This method will get the coordinates of the mouse pointer and
        finds the closest point and retrieves the corresponding peptide sequence.
        Also draws a yellow circle around the point.--from Ashoka 5/29/08
        """

        if event.mouseevent.button == 1:
            #print "Pick A"
            if not isinstance(event.artist, Line2D):
                return False

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

            self.cursAText = self.chromAxis.text(xdata[self.indexA], ydata[self.indexA], '%.1f'%xdata[self.indexA],  fontsize=9, rotation = 45)

            self.cursorAInfo[0]=self.indexA
            self.cursorAInfo[1]=xdata[self.indexA]
            self.cursorAInfo[2]=ydata[self.indexA]
            self.cursorAInfo[3]=line.get_label()
            self.cursorStats()

            self.plotWidget2.canvas.draw()

    def OnPickB(self, event):
        #print "Pick B"
        if event.mouseevent.button == 1:
            if not isinstance(event.artist, Line2D):
                return False

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

            self.cursBText = self.chromAxis.text(xdata[self.indexB], ydata[self.indexB], '%.1f'%xdata[self.indexB],  fontsize=9, rotation = 45)

            self.cursorBInfo[0]=self.indexB
            self.cursorBInfo[1]=xdata[self.indexB]
            self.cursorBInfo[2]=ydata[self.indexB]
            self.cursorBInfo[3]=line.get_label()
            self.cursorStats()

            self.plotWidget2.canvas.draw()

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

 ###########Peak Label#########################
    def labelPeak(self):
        print "Label"
        if self.cAOn:
            x = self.cursorAInfo[1]
            y = self.cursorAInfo[2]
            self.chromAxis.text(x, y*1.05, '%.1f'%x,  fontsize=8, rotation = 45)

#        if self.cBOn:
#            x = self.cursorBInfo[1]
#            y = self.cursorBInfo[2]
#            mplAx.text(x, y*1.05, '%.1f'%x,  fontsize=8, rotation = 45)


    def ZoomToggle(self):
        #self.toolbar.zoom() #this implements the classic zoom
        if self.usrZoom:
            self.usrZoom = False
            self.RS.visible = False
        else:
            self.usrZoom = True
            self.RS.visible = True

    def get2DPeakLoc(self, peakLoc, rows, cols):
        x = N.empty(len(peakLoc), dtype = int)
        y = N.empty(len(peakLoc), dtype = int)
        for i,loc in enumerate(peakLoc):
            x[i] = int(loc/cols)
            y[i] = loc%cols

        return [x,y]

    def getMZSlice(self, fileName, index):
        f = T.openFile(fileName, 'r')
        mz = f.root.dataCube
        self.maxRows = mz.shape[0]
        if self.startIndex+self.specIncrement*index >= self.maxRows:
            mzSlice = N.zeros(1)
            getState = False
        else:
            mzSlice = SF.normArray(mz[self.startIndex+self.specIncrement*(index-1):self.startIndex+self.specIncrement*index])
            getState = True

        f.close()

        return mzSlice, getState
##########Peak Finding Routines######################

    def findChromPeaks(self):
        self.peakParams['numSegs'] = self.numSegsSB.value() #should be an integer
        self.peakParams['minSNR'] = self.minSNRSB.value() #should be an integer
        self.peakParams['smthKern'] = self.smthKernSB.value() #should be an integer
        self.peakParams['peakWidth'] = self.peakWidthSB.value() #should be an integer

        if type(self.peakParams['numSegs']) is int and type(self.peakParams['minSNR'])\
        is int and type(self.peakParams['smthKern']) is int and type(self.peakParams['peakWidth']) is int:
            if self.curChrom != None:
                if len(self.curChrom) > 0:
                    self.PFT.initSpectrum(self.curChrom, minSNR = self.peakParams['minSNR'], numSegs = self.peakParams['numSegs'],\
                                          smthKern = self.peakParams['smthKern'], peakWidth = self.peakParams['peakWidth'])
                    self.ToggleProgressBar(True)
                    self.progressMax = N.float(self.peakParams['numSegs'])
                    self.PFT.start()
                    self.tabWidget.setCurrentIndex(0)
                else:
                    return QtGui.QMessageBox.warning(self, "The Spectrum is empty",  "The spectrum has a length of zero--no peaks to pick.")
            else:
                return QtGui.QMessageBox.warning(self, "No Spectrum to Process",  "Is a file loaded...?")
        else:#                self.chromAxis.plot(self.peakInfo['peakLoc'],self.peakInfo['peakInt'], 'ro', ms = 3, alpha = 0.4, picker = 5)

#                self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints, self.curData.colPoints)
#                self.imageAxis.plot(self.peakLoc2D[0],self.peakLoc2D[1],'yo', ms = 3, alpha = 0.6, picker = 5)
                #remember the image is transposed, so we need to swap the length of the axes
#                self.imageAxis.set_xlim(0,self.curData.rowPoints)
#                self.imageAxis.set_ylim(0,self.curData.colPoints)

#                self.plotWidget.canvas.format_labels()
#                self.plotWidget.canvas.draw()
#
#                self.plotWidget2.canvas.format_labels()
#                self.plotWidget2.canvas.draw()
            return QtGui.QMessageBox.warning(self, "Peak Find Parameter Error",  "Check selected values, all should be integers!")

    def plotPickedPeaks(self, finishedBool):#this function is called when the peak finding thread is finished
        if finishedBool:
            self.peakInfo = self.PFT.getPeakInfo()
            self.PFT.wait()#as per Ashoka's code...

            if self.showPickedPeaksCB.isChecked():
                self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints, self.curData.colPoints)
                self.autoscale_plot()#this is the function that actually plots the peaks in 1 and 2D

            self.SetStatusLabel("Peak Fitting Completed, %d Peaks Found" % len(self.peakInfo['peakLoc']))

            self.resetProgressBar()

        else:
            return QtGui.QMessageBox.warning(self, "Peak Find Thread Error",  "The thread did not finish or return a value properly--contact Clowers...")


##########Begin Ashoka Progress Bar Code....
    def LayoutStatusBar(self):
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
        self.ToggleProgressBar(False)
        self.statusbar.addWidget(self.progressBar)

    def resetProgressBar(self):
        self.SetProgressValue(0)
        self.ToggleProgressBar(False)

    def SetStatusLabel(self, text):
        self.statusLabel.setText(text)

    def ShowStatusMessage(self, text, stime):
        self.statusBar().showMessage(text, stime)

    def SetProgressValue(self, val):
        self.progressBar.setValue(val)

    def ToggleProgressBar(self, toggle):
        self.progressBar.setVisible(toggle)

    def threadProgress(self, progVal):
        self.SetStatusLabel("Fitting Peaks, %d segments completed." % progVal)
        newVal = int(100*(progVal/self.progressMax))
        self.SetProgressValue(newVal)
#        self.AddMessage2Tab("  %d Iterations Done." % progVal)
#        print progVal, newVal, self.progressMax

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    plot = Plot_Widget()
    plot.show()
    sys.exit(app.exec_())
###################MISC
#
#        for ax in self.imageAxisplotWidget.canvas.axDict.itervalues():
#            ax.cla()
#
#        for ax in self.plotWidget2.canvas.axDict.itervalues():
#            ax.cla()
#
#        #self.addPickers()
#        self.refZ, refOK = self.getMZSlice(self.ref, index)
#        self.samZ, samOK = self.getMZSlice(self.sam, index)
#
#        if refOK and samOK:
#            rows = self.refZ.shape[0]
#            cols = self.samZ.shape[1]
#
#            sicR = SF.getBPC(self.refZ)
#            sicS = SF.getBPC(self.samZ)
#
#
#
##            cor2D, maxShift, corVals = SF.corrMatrix(self.refZ, self.samZ)
#            cor2D, maxShift, corVals = SF.corrMatrix(self.refZ, self.samZ, excludeList = EXCLUDE)
#
#            cor = N.correlate(sicR, sicS, mode = 'same')
#            shift = N.round(cor.argmax()-len(sicR)/2)#gets value to shift by
#            self.specNameEdit.setText(str(shift))
#            print shift
#
#            corVals = SF.crudeNoiseFilter(corVals, 2)
#            corIndices = N.where(corVals>0)[0]
#            corMax = corVals[corIndices]
#
#            self.refZ = N.where(self.refZ>0, self.refZ, 2)
##            self.samZ = N.where(self.samZ>0, self.samZ, 1)
#
#
#            ax1 = self.plotWidget.canvas.axDict['ax1']

#            self.refIm = ax1.contour(self.refZ, alpha = 1,  aspect = 'auto', origin = 'lower',  cmap = cmaps[0], label = 'R')
#            self.samIm = ax1.contour(self.samZ, alpha = 1,  origin = 'lower',  cmap = cmaps[1], label = 'S')
            #ax1.imshow(self.refZ, alpha = 1,  origin = 'lower',  cmap = cmaps[3], label = 'R')

            ############colorMap Section
#            cLvlsZ = self.colorScale(self.refZ)
#            ax1.contour(self.refZ, cLvlsZ, norm = colors.LogNorm(), alpha = 1,  origin = 'lower',  label = 'R')

#            ax1a = self.plotWidget2.canvas.axDict['ax1']
#            ax2a = self.plotWidget2.canvas.axDict['ax2']
#            ax1a.plot(sicR)
#            ax1a.plot(sicS)

            #was ax3
#            ax3 = self.plotWidget.canvas.axDict['ax3']
#            ax1a.plot(corVals)
#            ax1a.plot(corIndices, corMax, 'ro')

#            ax4 = self.plotWidget.canvas.axDict['ax4']

#            nHist = N.histogram(maxShift[corIndices], bins = int(cols*0.5), new=True, weights = N.sqrt(corMax[corMax.argsort()[-len(corIndices):]]))
#            nHisty = nHist[0]
#            nHistx = nHist[1][:-1]
#            ax2a.vlines(nHistx,0, nHisty, lw = 2.0)


########################################################################################
#            ax1a = self.plotWidget2.canvas.axDict['ax1']
#            ax1a.hist(maxShift[corVals.argsort()[-20:]], bins = int(cols*0.5))
#
#            ax2a = self.plotWidget2.canvas.axDict['ax2']
##            ax2a.hist(maxShift[corVals.argsort()[-25:]], bins = int(cols*0.5))
#            indicies = corVals.argsort()[-25:]
#            nHist2 = N.histogram(maxShift[indicies], bins = int(cols*0.5), new=True, weights = N.sqrt(corVals[indicies]))
#            nHisty2 = nHist2[0]
#            nHistx2 = nHist2[1][:-1]
#            ax2a.vlines(nHistx2,0, nHisty2, lw = 2.0)


#        else:
#            print "Requested rows exceed data size!"
#            print "Requested end row: %s", self.startIndex+self.specIncrement*index
#            print "Available: %s", self.maxRows