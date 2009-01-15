#!/usr/bin/env python
###################################
'''To Do:
exclude list/include list with tolerance
peak grouping
is the m/z range correct (zero indexing?)
kill child windows when spawned
peak info when clicked
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
from matplotlib.widgets_bhc import SpanSelector, RectangleSelector
from pylab import cm
cmaps = [cm.jet, cm.BrBG, cm.gist_ncar, cm.bone_r,  cm.hot,  cm.spectral, cm.gist_ncar, cm.RdYlBu, cm.BrBG, cm.Accent]

#from LECO_IO import ChromaTOF_Reader as CR
#import SplitNStich as SNS
#import PeakFunctions as PF
import supportFunc as SF
from dataClass import GC_GC_MS_CLASS as GCDATA
from peakFindThread import PeakFindThread as PFT
import peakClusterThread as PCT
import hcluster_bhc as H
from mpl_pyqt4_widget import MPL_Widget
from dbscan import dbscan
from lassoPlot import LassoManager as LM

#from tableSortTest import MyTableModel
#from pylab import load as L
#from customTable import customTable

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

        self._setupVars_()
        self._setThreads_()
        self._setConnections_()
        self._setupGUI_()
        self._setMessages_()
        self._setContext_()
        self.layoutStatusBar()


    def _setupVars_(self):

        self.numSpec = 25

        self._curDir = os.getcwd()

        self.dataDict = {}
        self.dataList = []

        self.curData = None #reference to the GCGCData Class
        self.curIm = None #reference to the 2D image used during zoom events
        self.mainIm = None #primary 2D plot image initialized when file is loaded and when autoscale is called
        self.curImPlot = None #is the matplotlib axis reference
        self.curChrom = None #current chromatogram
        self.curChromPlot = None

        self.peakPickPlot2D = None
        self.peakPickPlot1D = None
        self.clustPlot = None
        #######DBSCAN VARIABLES#######################
        self.densityCluster= None
        self.Type = None
        self.Eps = None
        self.dbScanOK = True

        ##############################

        self.plotType = 'TIC'
        self.prevChromLimits = 0
        self.prevImLimits = [0,0]
        ####Peak Info Variables############################
        self.peakInfo = None #when set will be a dictionary containing peak info for the chromatogram
        self.peakLoc2D = None #when set will be a 2D array of picked peak locations and intensities
        self.clustLoc2D = None
        self.peakParams = {} #dictionary of peak parameters
        self.peakArrayNames = ['peakLoc', 'peakInt', 'peakWidth']

        ##############################
        self.txtColor = None
        self.colorIndex = 0
        ###############################
        self.linkagePlot = None
        self.mzPlots = []
        ###############################
        self.chromStyles = ['BPC','TIC']#,'SIC']
        ###############################

        self.showImPickers = True
        self.clustPicker = None#these two variables are used for the picker radius
        self.peakPicker = 5

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

        self.RSprops = {}
        self.RSprops['edgecolor'] = 'yellow'
        self.RSprops['facecolor'] = 'yellow'
        self.RSprops['alpha'] = 0.3

        self.usrZoom = False
        self.usrLasso = False

        self.imLasso = None
        self.cur2DPeakLoc = None #used to pass to the lasso manager to allow selection while zooming.

        self.clustNum = 1
        self.clustDict = {}
        self.clustMembers = None
        self.memPlot = None

        self.resetRefLimits()

    def _setThreads_(self):
        self.PFT = PFT()
        self.PCT = PCT.PeakClusterThread()

    def _setConnections_(self):

#        QtCore.QObject.connect(self.indexSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.updatePlot)
        self.zoomAction = QtGui.QAction("Zoom", self)
        self.zoomAction.setShortcut("Ctrl+Z")
        self.plotWidget.addAction(self.zoomAction)
        QtCore.QObject.connect(self.zoomAction,QtCore.SIGNAL("triggered()"), self.zoomToggle)

        self.actionAutoScale = QtGui.QAction("AutoScale", self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale,QtCore.SIGNAL("triggered()"), self.autoscale_plot)

        self.actionLasso = QtGui.QAction("Lasso", self)#self.MainWindow)
        self.actionLasso.setShortcut("Ctrl+L")
        self.plotWidget.addAction(self.actionLasso)
        QtCore.QObject.connect(self.actionLasso,QtCore.SIGNAL("triggered()"), self.lassoToggle)

        self.handleActionA = QtGui.QAction("Cursor A", self)
        self.plotWidget2.addAction(self.handleActionA)

        self.handleActionB = QtGui.QAction("Cursor B", self)
        self.plotWidget2.addAction(self.handleActionB)

        self.cursorClearAction = QtGui.QAction("Clear Cursors", self)
        self.plotWidget2.addAction(self.cursorClearAction)

        self.labelAction = QtGui.QAction("Label Peak", self)
        self.plotWidget2.addAction(self.labelAction)

        self.chromClipAction = QtGui.QAction("Save to Clipboard", self)
        self.plotWidget2.addAction(self.chromClipAction)

        self.imageClipAction = QtGui.QAction("Save to Clipboard", self)
        self.plotWidget.addAction(self.imageClipAction)

        self.clustMZAction = QtGui.QAction("Show Cluster MS", self)
        self.plotWidget.addAction(self.clustMZAction)

        QtCore.QObject.connect(self.clustMZAction,QtCore.SIGNAL("triggered()"), self.showClusterMZ)

        QtCore.QObject.connect(self.action_Open,QtCore.SIGNAL("triggered()"),self._getDataFile_)
        QtCore.QObject.connect(self.addFileBtn,QtCore.SIGNAL("clicked()"),self._getDataFile_)
        QtCore.QObject.connect(self.fndPeaksBtn,QtCore.SIGNAL("clicked()"),self.findChromPeaks)
        QtCore.QObject.connect(self.action_Find_Peaks,QtCore.SIGNAL("triggered()"),self.findChromPeaks)
        QtCore.QObject.connect(self.actionSave_Peaks_to_CSV,QtCore.SIGNAL("triggered()"),self.savePeaks2CSV)
        QtCore.QObject.connect(self.actionSave_2D_Peaks_to_CSV,QtCore.SIGNAL("triggered()"),self.saveRaw2DPeaks2CSV)
        QtCore.QObject.connect(self.actionToggle_Peak_Cross_Hairs,QtCore.SIGNAL("triggered()"),self.toggleImPickers)

        QtCore.QObject.connect(self.actionHierarchical_Method,QtCore.SIGNAL("triggered()"),self.hClusterPeaks)
        QtCore.QObject.connect(self.actionDensity_Based_Clustering,QtCore.SIGNAL("triggered()"),self.dbClusterPeaks)

        QtCore.QObject.connect(self.handleActionA, QtCore.SIGNAL("triggered()"),self.toggleCA)#SelectPointsA)
        QtCore.QObject.connect(self.handleActionB, QtCore.SIGNAL("triggered()"),self.toggleCB)#SelectPointsB)
        QtCore.QObject.connect(self.cursorClearAction, QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.labelAction, QtCore.SIGNAL("triggered()"),self.labelPeak)

        QtCore.QObject.connect(self.chromClipAction,QtCore.SIGNAL("triggered()"),self.chrom2Clip)
        QtCore.QObject.connect(self.imageClipAction,QtCore.SIGNAL("triggered()"),self.image2Clip)

        QtCore.QObject.connect(self.actionLabel_Peak,QtCore.SIGNAL("triggered()"),self.labelPeak)
        QtCore.QObject.connect(self.actionCursor_A,QtCore.SIGNAL("triggered()"),self.toggleCA)#SelectPointsA)
        QtCore.QObject.connect(self.actionCursor_B,QtCore.SIGNAL("triggered()"),self.toggleCB)#SelectPointsB)
        QtCore.QObject.connect(self.actionClear_Cursors,QtCore.SIGNAL("triggered()"),self.cursorClear)
        QtCore.QObject.connect(self.cursACB,QtCore.SIGNAL("stateChanged (int)"),self.toggleCA)
        QtCore.QObject.connect(self.cursBCB,QtCore.SIGNAL("stateChanged (int)"),self.toggleCB)

        QtCore.QObject.connect(self.PFT, QtCore.SIGNAL("finished(bool)"), self.plotPickedPeaks)
        QtCore.QObject.connect(self.PFT, QtCore.SIGNAL("progress(int)"), self.threadProgress)

        QtCore.QObject.connect(self.PCT, QtCore.SIGNAL("finished(bool)"), self.plotLinkage)
        QtCore.QObject.connect(self.PCT, QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"), self.PCTProgress)

        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL("itemClicked (QListWidgetItem *)"), self.specListSelect)
        QtCore.QObject.connect(self.chromStyleCB, QtCore.SIGNAL("currentIndexChanged(QString)"), self.plotTypeChanged)

        QtCore.QObject.connect(self.savePickedPeakBtn,QtCore.SIGNAL("clicked()"),self.savePeaks2HDF)
        QtCore.QObject.connect(self.actionSave_Peaks_to_Data_File, QtCore.SIGNAL("triggered()"),self.savePeaks2HDF)
        QtCore.QObject.connect(self.clusterBtn,QtCore.SIGNAL("clicked()"),self.clusterPeaks)

        QtCore.QObject.connect(self.calcThreshCB,QtCore.SIGNAL("stateChanged(int)"),self.toggleDistance)
        QtCore.QObject.connect(self.dbScanCB,QtCore.SIGNAL("stateChanged(int)"),self.toggleClusterType)
        QtCore.QObject.connect(self.dbAutoCalcCB,QtCore.SIGNAL("stateChanged(int)"),self.toggleAutoDBDist)

#        print self.imLasso, type(self.imLasso)
#        QtCore.QObject.connect(self.imLasso,QtCore.SIGNAL("LassoUpdate(PyQt_PyObject)"),self.lassoHandler)

    def _setupGUI_(self):

        self.plotWidget.canvas.setupSub(1)

        self.imageAxis = self.plotWidget.canvas.axDict['ax1']
        self.chromAxis = self.plotWidget2.canvas.ax#Dict['ax1'] #use Dict when using multiplot PyQt4 Widget
        #for some reason when you add a second axis the zooming and autoscaling don't work well.
#        self.chromAxis2 = self.chromAxis.twiny()
#        self.format2ndAxis(self.chromAxis2)

        self.distMethodCB.addItems(PCT.distTypeDist.keys())
        self.clusterTypeCB.addItems(PCT.clusterType.keys())
        self.distMethodCB.setCurrentIndex(self.distMethodCB.findText('Euclidean'))
        self.clusterTypeCB.setCurrentIndex(self.clusterTypeCB.findText('Single'))

        self.chromStyleCB.addItems(self.chromStyles)
        self.chromStyleCB.setCurrentIndex(self.chromStyleCB.findText('BPC'))
        self.plotType = str(self.chromStyleCB.currentText())

        self.RS = RectangleSelector(self.imageAxis, self.imageZoom, minspanx = 2,
                        minspany = 2, drawtype='box',useblit=True, rectprops = self.RSprops,
                        primaryBtn = 1)#, spancoords='pixels')

        self.RS.set_active(False)# = False

        self.indexHSlider.setMinimum(1)
        self.indexSpinBox.setMinimum(1)
        self.indexHSlider.setMaximum(self.numSpec)
        self.indexSpinBox.setMaximum(self.numSpec)

        #changes state for DBSCAN parameters
        self.dbScanCB.nextCheckState()
        self.dbAutoCalcCB.nextCheckState()

        self.addChromPickers()
        self.addImPickers()
        self.zoomToggle()#this is called because there is some confusion on the PyQt4 backend regarding the plotting of the picked peaks
#        self.setupTable()

    def _setContext_(self):
        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._imageContext_)
        self.plotWidget2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plotWidget2.connect(self.plotWidget2, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self._chromContext_)
#        self.specListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.specListWidget.connect(self.specListWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__listContext__)

    def _imageContext_(self, point):
        ct_menu = QtGui.QMenu("Image Menu", self.plotWidget)
        ct_menu.addAction(self.zoomAction)
        ct_menu.addAction(self.actionAutoScale)
        ct_menu.addAction(self.actionLasso)
        ct_menu.addSeparator()
        ct_menu.addAction(self.clustMZAction)
        ct_menu.addAction(self.imageClipAction)
        ct_menu.exec_(self.plotWidget.mapToGlobal(point))

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
        ct_menu.addSeparator()
        ct_menu.addAction(self.chromClipAction)
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



    def _getDataFile_(self):
        dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                             self.OpenDataText,\
                                                             self._curDir, 'HDF5 File (*.h5)')
        if dataFileName:
            self._initDataFile_(str(dataFileName))

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
            #sets up a new GCDATA File instance and adds it to a dictionary
            #the key to that dictionary is the full file path, not simply the name
            self.dataDict[dataFileName] = GCDATA(dataFileName)
            self.dataList.append(dataFileName)
            tempData = self.dataDict[dataFileName]
            tempItem = QtGui.QListWidgetItem(tempData.name)
            tempColor = QtGui.QColor(self.txtColor)
            tempItem.setTextColor(tempColor)
            tempItem.setToolTip(tempData.filePath)
            self.listWidget.addItem(tempItem)

            self.updatePlot(len(self.dataList)-1)

    def _getDir_(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, '', self.curDir)
        directory = str(directory)
        if directory != None:
            self.curDir = directory
        else:
            self.curDir = os.getcwd()

    def clusterDBSCAN(self, Z):
        '''
        This function actually accepts an array with 3 columns: x,y,z
        The DBSCAN function can work in 3D, however, the intensity of
        chromatographic peaks skews the clustering, hence, only the x,y points are
        used for clustering.  The peak centers, however, are calculated using
        the intensity values.  This is why the intensity values are passed and
        not just the x,y values.


        Important arrays created:

        self.clustDict -- a complete listing of all the clustered
        self.clustKeys -- a simple list of keys that are in order
        self.clustLoc2D -- a stacked numpy array of the x,y coordinates of the cluster centroids
        self.clustType -- tells you which group each of the clustLoc2D points belong to.


        Also, how best to select the 2nd round of the EPS filter?
        '''
        filtered = None
        self.clustType = []
        XY = Z[:,0:2]
        if self.dbAutoCalcCB.isChecked():
            self.densityCluster, self.Type, self.Eps, self.dbScanOK = dbscan(XY, 1,\
                                                                             distMethod = PCT.distTypeDist[str(self.distMethodCB.currentText())])
        else:
            self.densityCluster, self.Type, self.Eps, self.dbScanOK = dbscan(Z[:,0:2], 1, Eps = self.densityDistThreshSB.value(),\
                                                                             distMethod = PCT.distTypeDist[str(self.distMethodCB.currentText())])

        print "1st Round",self.Eps#, self.clustLoc2D.shape

        singlesIndex = N.where(self.Type == -1)[0]#these are the indices that have 1 member per cluster
        self.clustNum = 1#i = 0
        self.clustDict = {}
        for point in singlesIndex:
            self.clustType.append(self.clustNum)
#                self.clustDict['%s%s'%(XY[point][0],XY[point])] = [XY[point],XY[point]]
            self.clustDict['%s'%self.clustNum] = [XY[point],N.array([XY[point]])]
#                print self.clustNum, XY[point]
            self.clustNum += 1


        i = self.densityCluster.max()
        for m in xrange(1,int(i)+1):#double check that adding one is ok?
            ind = N.where(m == self.densityCluster)[0]#zero is used because a list is returned
#                temp = XY[ind]
            temp = Z[ind]#this includes the intensity
            '''
            if the length of the cluster is bigger than
            the user defined threshold then the clustering
            will be done again in order to separate
            the clusters into finer pieces.
            '''
            if len(temp)<self.denGrpNumThresh.value():#need to add value from GUI
                if filtered == None:
                    filtered = temp
                else:
                    filtered = N.append(filtered,temp, axis = 0)
            else:
                self.iterDBSCAN(temp)#tempCluster, tempType, typeEps, tempBool = dbscan(temp)

        if filtered != None:
            fXY = filtered[:,0:2]
            self.densityCluster, self.Type, self.Eps, self.dbScanOK = dbscan(filtered, 1, Eps = N.sqrt(self.Eps)*2,\
                                                                             distMethod = PCT.distTypeDist[str(self.distMethodCB.currentText())])
            print "2nd Round",self.Eps#, self.clustLoc2D.shape

            singlesIndex = N.where(self.Type == -1)[0]#these are the indices that have 1 member per cluster

            for point in singlesIndex:
                self.clustType.append(self.clustNum)
    #                self.clustDict['%s'%self.clustNum] = [XY[point],N.array([XY[point]])]
                self.clustDict['%s'%self.clustNum] = [fXY[point],N.array([fXY[point]])]
    #                print self.clustNum, XY[point]
                self.clustNum += 1

            for m in xrange(1,int(i)+1):
    #                if self.colorIndex%len(COLORS) == 0:
    #                    self.colorIndex = 0
    #                curColor = COLORS[self.colorIndex]
    #                self.colorIndex +=1
                ind = N.where(m == self.densityCluster)[0]
    #                temp = filtered[:,0:2][ind]
                temp = filtered[ind]
                if len(temp)>0:

                    xTemp = temp[:,0]*temp[:,2]
                    yTemp = temp[:,1]*temp[:,2]
                    x = xTemp.sum()/(temp[:,2].sum())
                    y = yTemp.sum()/(temp[:,2].sum())

                    centroid = N.array([[x,y]])
    #                    print centroid, centroid.shape
    #                    centroid.shape = (1,2)
    #                print centroid, centroid.shape
    #                    self.clustLoc2D = N.append(self.clustLoc2D,centroid, axis = 0)
                    tempType = N.arange(len(temp))
                    tempType.fill(self.clustNum)
                    self.clustType.append(tempType)
                    self.clustDict['%s'%self.clustNum] = [centroid[0],temp]
    #                    print self.clustNum, temp
    #                    self.clustDict['%s%s'%(centroid[0][0],centroid[0][1])] = [centroid[0],temp]
                    self.clustNum += 1

        self.clustLoc2D = N.zeros((1,2))
        self.clustKeys = ['0']
        for item in self.clustDict.iteritems():
            key = item[0]
            loc = item[1]
            x = loc[0]
#                print x
            x.shape = (1,2)
            self.clustLoc2D = N.append(self.clustLoc2D,x, axis = 0)
            self.clustKeys.append(key)

#            print self.clustDict.values()[:,0]
        self.clustType = N.array(SF.flattenX(self.clustType))

        print len(self.clustDict.keys()), len(self.peakLoc2D[0]), len(self.clustType)
        i = 0

        if len(self.clustDict) > 0:
            self.setupTable2()
#            print len(self.clustType), len(self.peakLoc2D[0])

#            print len(self.clustKeys), self.clustNum-1

#            for loc in self.clustDict.iteritems():
#                print loc


    def iterDBSCAN(self, Z):
        XY = Z[:,0:2]
        tempCluster, tempType, typeEps, tempBool = dbscan(XY, 1,\
                                                          distMethod = PCT.distTypeDist[str(self.distMethodCB.currentText())])
        singlesIndex = N.where(tempType == -1)[0]#these are the indices that have 1 member per cluster
        for point in singlesIndex:
            self.clustType.append(self.clustNum)
#            self.clustDict['%s%s'%(XY[point],XY[point])] = [XY[point],XY[point]]
            self.clustDict['%s'%self.clustNum] = [XY[point],N.array([XY[point]])]
#            print self.clustNum, XY[point]
            self.clustNum += 1

        i = tempCluster.max()
        for m in xrange(1,int(i)+1):#double check that adding one is ok?
            ind = N.where(m == tempCluster)[0]
#            temp = XY[ind]
            temp = Z[ind]
            '''
            if the length of the cluster is bigger than
            the user defined threshold then the clustering
            will be done again in order to separate
            the clusters into finer pieces.
            '''
            if len(temp) > 0:
                xTemp = temp[:,0]*temp[:,2]
                yTemp = temp[:,1]*temp[:,2]
#                xTemp /=temp[:,2].sum()
#                yTemp /=temp[:,2].sum()
#                    centroid = temp[:,0:2].mean(axis=0)
#                    centroid *= intTemp
#                    centroid = temp.mean(axis = 0)
                x = xTemp.sum()/(temp[:,2].sum())
                y = yTemp.sum()/(temp[:,2].sum())
                centroid = N.array([[x,y]])
#                centroid.shape = (1,2)
#                print centroid.shape, self.clustLoc2D.shape
#                self.clustLoc2D = N.append(self.clustLoc2D, centroid, axis = 0)
                tempType = N.arange(len(temp))
                tempType.fill(self.clustNum)
                self.clustType.append(tempType)
#                self.clustDict['%s%s'%(centroid[0][0],centroid[0][1])] = [centroid[0],temp]
                self.clustDict['%s'%self.clustNum] = [centroid[0],temp]#j is the place keeper from the loop above
#                print self.clustNum, temp
                self.clustNum += 1

    def dbClusterPeaks(self):
        if self.dbScanCB.isChecked():
            self.clusterPeaks()
        else:
            self.dbScanCB.nextCheckState()
            self.clusterPeaks()

    def hClusterPeaks(self):
        if self.dbScanCB.isChecked():
            self.dbScanCB.nextCheckState()
            self.clusterPeaks()
        else:
            self.clusterPeaks()

    def clusterPeaks(self):
        if self.peakInfo != None:
            self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints,\
                                   self.curData.colPoints, peakIntensity = self.peakInfo['peakInt'])
            #we are passing the intensity along so we can calculate the intensity weighted centroid of each cluster
            Z = N.column_stack((self.peakLoc2D[0], self.peakLoc2D[1], self.peakLoc2D[2]))
            self.tabWidget.setCurrentIndex(0)#return to plot tab
            if self.dbScanCB.isChecked():
                self.clusterDBSCAN(Z)
                self.autoscale_plot()
            else:
                if self.calcThreshCB.isChecked():
                    self.PCT.initClusterThread(Z[:,0:2], plotLinkage = self.showDendroCB.isChecked(), name = self.curData.name,\
                                               threshType = 'inconsistent', distMethod = PCT.distTypeDist[str(self.distMethodCB.currentText())])
                else:
                    self.PCT.initClusterThread(Z[:,0:2], plotLinkage = self.showDendroCB.isChecked(), name = self.curData.name,\
                                               distThresh = self.maxDistThreshSB.value(), threshType = 'distance',\
                                               distMethod = PCT.distTypeDist[str(self.distMethodCB.currentText())])

                self.PCT.start()


    def updatePlot(self, plotIndex):#, plotType = 'TIC'):
        self.peakInfo = None
        self.peakLoc2D = None
        self.clustLoc2D = None
        self.clustMembers = None
        self.clustDict = {}
        self.densityCluster = None
        self.imageAxis.cla()
        self.chromAxis.cla()
        self.addChromPickers()
        self.curDataName = self.dataList[plotIndex]
        self.curData = self.dataDict[self.curDataName]
#        print type(self.curData.name), self.curData.name
#        test = self.listWidget.findItems(self.curData.name,QtCore.Qt.MatchExactly)[0]
#        print self.listWidget.indexFromItem(test).row()

#        print test
        self.specNameEdit.setText(self.curData.filePath)#use dataList to get the name
        if self.plotType == 'TIC':
            self.mainIm = self.curData.ticLayer
            self.curIm = self.curData.ticLayer
            self.curChrom = self.curData.getTIC()
        elif self.plotType == 'BPC':
            self.mainIm = self.curData.bpcLayer
            self.curIm = self.curData.bpcLayer
            self.curChrom = self.curData.getBPC()
#            self.curImPlot = self.imageAxis.imshow(self.curIm, alpha = 1,  aspect = 'auto',\
#                                                   origin = 'lower',  cmap = my_cmap, label = 'R')
        self.curChromPlot, = self.chromAxis.plot(self.curChrom, 'b', label = self.curData.name, picker = 5)
        if self.showPickedPeaksCB.isChecked():
            if self.curData.peakPickOk:
                self.peakInfo = self.curData.peakInfo1D
                self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints, self.curData.colPoints)
                self.setupTable()
        #update Chrom GUI elements for peak picking and other functions
        self.updateChromGUI()

        self.autoscale_plot()



###########################

    def plotDBSCAN(self, xpntMod = 0, ypntMod = 0, ms = 3):
        '''
        Plots result from DBSCAN clustering
        '''
        if self.densityCluster!= None and self.dbScanCB.isChecked():
            xy = N.column_stack((self.peakLoc2D[0],self.peakLoc2D[1]))
            i = self.densityCluster.max()
            for m in xrange(int(i)):
                if self.colorIndex%len(COLORS) == 0:
                    self.colorIndex = 0
                curColor = COLORS[self.colorIndex]
                self.colorIndex +=1
                ind = N.where(m == self.densityCluster)
                temp = xy[ind]
                self.imageAxis.plot(temp[:,0]+xpntMod,temp[:,1]+ypntMod,'s', alpha = 0.6, ms = ms, color = curColor)

    def autoscale_plot(self):
        '''
        This function actually does most of the plotting.  Especially when a new data set is loaded. Key
        things to not is that only picked peaks have a picker.
        '''
        self.imageAxis.cla()
        self.addImPickers()
        self.resetRefLimits()
        self.tabWidget.setCurrentIndex(0)
        if self.plotType == 'TIC':
            self.curIm = self.curData.ticLayer
        elif self.plotType == 'BPC':
            self.curIm = self.curData.bpcLayer

        self.cur2DPeakLoc = self.peakLoc2D
        self.curImPlot = self.imageAxis.imshow(self.mainIm, alpha = 1,  aspect = 'auto',\
                                               origin = 'lower',  cmap = my_cmap, label = 'R')
        #the idea here is to make it so only the clustered peaks get picked if present
        if self.clustLoc2D != None:
            self.clustPicker = 5
            self.peakPicker = None
        else:
            self.clustPicker = None
            self.peakPicker = 5

        if self.showPickedPeaksCB.isChecked():
            if self.peakInfo != None:
                self.peakPickPlot1D, = self.chromAxis.plot(self.peakInfo['peakLoc'],self.peakInfo['peakInt'], 'ro', ms = 3, alpha = 0.4, picker = self.peakPicker)
                self.peakPickPlot2D, = self.imageAxis.plot(self.cur2DPeakLoc[0],self.cur2DPeakLoc[1],'yo', ms = 3, alpha = 0.4, picker = self.peakPicker)
                if self.clustLoc2D != None:
                    self.clustPlot, = self.imageAxis.plot(self.clustLoc2D[:,0],self.clustLoc2D[:,1],'rs', ms = 4, alpha = 0.6, picker = self.clustPicker)

                if self.clustMembers != None:
                    self.memPlot, = self.imageAxis.plot(self.clustMembers[:,0],\
                                    self.clustMembers[:,1], 'go', ms = 8,\
                                    alpha = 0.5, label = 'clustMembers')


                if self.usrLasso:
                    X = N.column_stack((self.cur2DPeakLoc[0], self.cur2DPeakLoc[1]))
                    self.imLasso.update(X, self.imageAxis)

                #remember the image is transposed, so we need to swap the length of the axes
                self._setImScale_()
#                self.imageAxis.set_xlim(0,self.curData.rowPoints)
#                self.imageAxis.set_ylim(0,self.curData.colPoints)

        self.prevChromLimits = 0
        self.prevImLimits = [0,0]
        self.plotWidget2.autoscale_plot()
        self.chromAxis.set_xlim(0, len(self.curChrom))

        self._drawCanvases_()
################Original
#        self.imageAxis.autoscale_view(tight = False, scalex=True, scaley=True)
#        self.plotWidget.canvas.draw()

    def imageZoom(self, event1 = None, event2 = None):
        '''
        This function is perhaps overly complicated but I don't know of a more elegant way to do this.  In essence
        this function takes the limits supplied by the RectangleSelector and replots the data after taking the appropriate
        subset.  The xLim, self.yLim, and prevChrom/prevImLimits are used to keep track of the scaling and fancy indexing is used
        to make it appear to the user that they are actually zooming when in fact a new image is plotted each time.
        '''
#        print event1, event2
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
                self.xLim = dataCoord[:,0]
                self.yLim = dataCoord[:,1]
                self.xLim.sort()
                self.yLim.sort()
                self.chromLimits.sort()


                #indexing is done as below because the image is transposed.
                self.curIm = self.curIm[self.yLim[0]:self.yLim[1],self.xLim[0]:self.xLim[1]]

                self.imageAxis.cla()
                self.addImPickers()
                self.curImPlot = self.imageAxis.imshow(self.curIm, alpha = 1,  aspect = 'auto', \
                                                       origin = 'lower',  cmap = my_cmap, label = 'R')
                x1 = chromLimits[0]
                x2 = chromLimits[1]
                self.chromAxis.set_xlim(x1,x2)
                tempChrom = self.curChrom[x1:x2]
                if len(tempChrom) > 0:
                    self.chromAxis.set_ylim(0, tempChrom.max()*1.1)
                self.prevChromLimits = x1

                #####2D Peak Locations#####
                if self.clustLoc2D != None:
                    self.clustPlot, =self.imageAxis.plot(self.clustLoc2D[:,0]-self.xLim[0]-self.prevImLimits[0],\
                                                         self.clustLoc2D[:,1]-self.yLim[0]-self.prevImLimits[1],\
                                                         'rs', ms = 4, alpha = 0.6, picker = self.clustPicker)
                if self.clustMembers != None:
                    self.memPlot, = self.imageAxis.plot(self.clustMembers[:,0]-self.xLim[0]-self.prevImLimits[0],\
                                                        self.clustMembers[:,1]-self.yLim[0]-self.prevImLimits[1],\
                                                        'go', ms = 8, alpha = 0.5, label = 'clustMembers')

                #self.plotDBSCAN((-self.xLim[0]-self.prevImLimits[0]), (-self.yLim[0]-self.prevImLimits[1]), ms = 5)

                if self.peakInfo != None:
                    tempPeaks = self.peakInfo['peakLoc']
                    rangeCrit = (tempPeaks >= x1) & (tempPeaks <= x2) #criterion for selection
                    tempPeakInd = N.where(rangeCrit) #peak indicies
                    self.cur2DPeakLoc = self.get2DPeakLoc(self.peakInfo['peakLoc'][tempPeakInd], self.curData.rowPoints, self.curData.colPoints)
                    self.cur2DPeakLoc[0] -= self.xLim[0]
                    self.cur2DPeakLoc[0] -= self.prevImLimits[0]
                    self.cur2DPeakLoc[1] -= self.yLim[0]
                    self.cur2DPeakLoc[1] -= self.prevImLimits[1]

                    self.peakPickPlot2D, = self.imageAxis.plot(self.cur2DPeakLoc[0],\
                                                               self.cur2DPeakLoc[1],\
                                                               'yo', ms = 3, alpha = 0.6, picker = self.peakPicker)

                    #lasso handler:
#                    if self.usrLasso:
#                    X = N.column_stack((self.cur2DPeakLoc[0], self.cur2DPeakLoc[1]))
#                    self.imLasso.update(X, self.imageAxis)

                    self._setImScale_()


                xLen = len(self.imageAxis.get_xticklabels())
                yLen = len(self.imageAxis.get_yticklabels())
                xIncr = (self.xLim[1]-self.xLim[0])/(xLen-1)
                yIncr = (self.yLim[1]-self.yLim[0])/(yLen-2)
                x = N.arange(self.xLim[0]+self.prevImLimits[0], self.xLim[1]+self.prevImLimits[0]+xIncr, xIncr)
                y = N.arange(self.yLim[0]+self.prevImLimits[1], self.yLim[1]+self.prevImLimits[1]+yIncr, yIncr)
                self.imageAxis.set_xticklabels(x)
                self.imageAxis.set_yticklabels(y)

                #used for the next zooming event
                self.prevImLimits = [self.xLim[0]+self.prevImLimits[0],self.yLim[0]+self.prevImLimits[1]]

                self._drawCanvases_()
    #            else:
    #                print event1, event2
    #                print event1.button, event2.button
    #                return True

    def imageClick(self, event):
        '''Sets cross hairs for picked peaks after selection'''
#        print event
        #print event.button
#        if event.mouseevent.button == 1:
        if self.showImPickers:
            if event.mouseevent.xdata != None and event.mouseevent.ydata != None:
                if event.mouseevent.button == 1:
                    if isinstance(event.artist, Line2D):
                        thisline = event.artist
                        xdata = thisline.get_xdata()
                        ydata = thisline.get_ydata()
                        self.selectCursA.set_data(xdata[event.ind[0]], ydata[event.ind[0]])
                        xPnt, yPnt =  int(N.round(event.mouseevent.xdata)), event.mouseevent.ydata
        #                print xPnt, yPnt
                        if self.clustPicker != None:
                            x = xdata[event.ind[0]]
                            y = ydata[event.ind[0]]
                            tempKey = self.clustKeys[event.ind[0]]
                            if self.clustDict.has_key(tempKey):
                                item = self.clustDict[tempKey]
                                clustMembers = item[1]#self.clustDict[tempKey][1]
#                                center = item[0]
##                                print center, clustMembers[0]
#                                i = 0
#                                for elem in self.clustDict.iteritems():
#                                    key = elem[0]
#                                    val = elem[1]
#                                    print 'intKey ',xdata[int(key)], ydata[int(key)], 'ind[0] ', x,y, key, event.ind[0], val[0]
#                                    i+=1
#                                    if x == val[1][0][0]:
#                                        print "Match: ",key, event.ind[0]
#                                print len(clustMembers), type(clustMembers), type(clustMembers[0]), clustMembers.shape
                                try:
                                    self.memPlot.remove()
                                except:
#                                    print "no self.memPlot to remove"
                                    pass

                                self.clustMembers = clustMembers#[:,0:2]
                                self.memPlot, = self.imageAxis.plot(self.clustMembers[:,0]-self.prevImLimits[0],\
                                                                    self.clustMembers[:,1]-self.prevImLimits[1],\
                                                                    'go', ms = 8, alpha = 0.5, label = 'clustMembers')
#                                self.memPlot, = self.imageAxis.plot(self.clustMembers[:,0],\
#                                                                    self.clustMembers[:,1], 'go', ms = 8,\
#                                                                    alpha = 0.5, label = 'clustMembers')
                                self._setImScale_()
                            else:
                                print event.ind[0], " is not a key"
#                            print x,y
#                            print x+self.prevImLimits[0], y+self.prevImLimits[1], ' x',self.xLim, ' y',self.yLim#+self.prevImLimits[1]
#                            print x+self.prevImLimits[0], y+self.prevImLimits[1]
                        else:
                            if self.peakInfo != None:
                                print event.ind[0], xdata[event.ind[0]], ydata[event.ind[0]]
                                for info in self.peakInfo.itervalues():
                                    print info[event.ind[0]]

                        self.xLine.set_xdata([xPnt])
                        self.yLine.set_ydata([yPnt])

                        self.imageAxis.draw_artist(self.selectCursA)
                        self.imageAxis.draw_artist(self.xLine)
                        self.imageAxis.draw_artist(self.yLine)
                        self.plotWidget.canvas.blit(self.imageAxis.bbox)
#                        self.plotWidget.canvas.draw()

    #                self.plotWidget2.canvas.format_labels()
    #                self.plotWidget2.canvas.draw()
    #                self.plotWidget2.setFocus()
                else:
    #                event.ignore()
    #                print "Not button 1"
                    #return True
                    pass




    def _setImScale_(self):
        self.imageAxis.set_xlim(0, self.curIm.shape[1]-1)
        self.imageAxis.set_ylim(0, self.curIm.shape[0])

    def _drawCanvases_(self):
        self.plotWidget2.canvas.format_labels()
        self.plotWidget2.canvas.draw()

        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()

    def setupTable(self):
        self.tabPeakTable.clear()
        #need to disable sorting as it corrupts data addition
        self.tabPeakTable.setSortingEnabled(False)
        header = []#'Index', 'Locations', 'Intensity','Width', 'Area']
#        simpleIndex = N.arange(len(self.peakInfo['peakLoc']))
        i = 0
        for item in self.peakInfo.iteritems():
            if i == 0:
                header.append(item[0])
                peakVals = item[1]
            else:
                header.append(item[0])
                peakVals = N.column_stack((peakVals,item[1]))
            i+=1
##        peakVals = self.peakInfo.values()
#        peakVals = N.array(peakVals)
#        peakVals.transpose()
        self.tabPeakTable.addData(peakVals)
#        tm = MyTableModel(peakVals, header, self)
#        self.tabPeakTable.setModel(tm)
#        self.tabPeakTable.resizeColumnsToContents()
#        self.tabPeakTable.verticalHeader()
##        vh.setVisible(False)
        self.tabPeakTable.setHorizontalHeaderLabels(header)
        self.tabPeakTable.setSortingEnabled(True)


    def setupTable2(self):
        self.tabPeakTable_2.clear()
        #need to disable sorting as it corrupts data addition
        self.tabPeakTable_2.setSortingEnabled(False)
        header = ['Index', 'Centroid', '# Peaks','Members']
#        simpleIndex = N.arange(len(self.peakInfo['peakLoc']))
        i = 0
        keys=[]
        centroid = []
        numPeaks = []
        peakVals = []
        for item in self.clustDict.iteritems():
            entry = []
            entry.append(int(item[0]))
            entry.append(str(item[1][0][0]))
            nums = len(item[1][1][:,0])

            entry.append(nums)
            entry.append(str(item[1][1].tolist()))
            peakVals.append(entry)

            i+=1

        self.tabPeakTable_2.addData(peakVals)
#        tm = MyTableModel(peakVals, header, self)
#        self.tabPeakTable.setModel(tm)
#        self.tabPeakTable.resizeColumnsToContents()
#        self.tabPeakTable.verticalHeader()
##        vh.setVisible(False)
        self.tabPeakTable_2.setHorizontalHeaderLabels(header)
        self.tabPeakTable_2.setSortingEnabled(True)


    def showClusterMZ(self):
        if self.clustMembers != None:
            peakInd = []
            cols = self.curData.colPoints
            rows = self.curData.rowPoints
            for peak in self.clustMembers:
                chromLoc = peak[0]*cols+peak[1]#+self.prevChromLimits #this is wrong for very close zooms...
                peakInd.append(chromLoc)

            print "Cluster indices: ", peakInd
#            print 'peak[0], peak[1], self.xLim, self.yLim, self.prevChromLimits, self.prevImLimits, rows, cols'
#            print peak[0], peak[1], self.xLim, self.yLim, self.prevChromLimits, self.prevImLimits, rows, cols
            mzList = self.curData.getMZlist(peakInd)

#            if isinstance(self.mzPlot, MPL_Widget):
#                try:
#                    self.mzPlot.close()
#                except:
#                    pass
#
#                self.mzPlot = None

            mzPlot = MPL_Widget()
            mzPlot.setWindowTitle(('Clustered Peak Mass Spectrum from %s'%self.curData.name))

            ax1 = mzPlot.canvas.axDict['ax1']
            MZ = mzList[0]
            if len(mzList)>1:
                plotTitle = 'Clustered Peaks from %s - %s'%(peakInd[0], peakInd[-1])
                for i,mz in enumerate(mzList[1:]):
    #                if self.colorIndex%len(COLORS) == 0:
    #                    self.colorIndex = 0
    #                curColor = COLORS[self.colorIndex]
    #                self.colorIndex +=1
                    MZ+=mz
            else:
                plotTitle = 'Peaks at %s'%(peakInd[0])
            ax1.set_title(plotTitle)
            ax1.title.set_fontsize(10)
            ax1.set_xlabel('m/z', fontstyle = 'italic')
            ax1.set_ylabel('Intensity')
            ax1.vlines(N.arange(len(MZ)),0,MZ, color = 'k')#curColor)#, label = '%s'%peakInd[i])
#            self.mzPlot.canvas.format_labels()

#            ax1.legend()
            mzPlot.show()
            self.mzPlots.append(mzPlot)


#            self.mzPlot = MPL_Widget()
#            self.mzPlot.setWindowTitle(('Clustered Peak Mass Spectrum from %s'%self.curData.name))
##            self.mzPlot.canvas.setupSub(1)
#            ax1 = self.mzPlot.canvas.axDict['ax1']
#            MZ = mzList[0]
#            if len(mzList)>1:
#                plotTitle = 'Clustered Peaks from %s - %s'%(peakInd[0], peakInd[-1])
#                for i,mz in enumerate(mzList[1:]):
#    #                if self.colorIndex%len(COLORS) == 0:
#    #                    self.colorIndex = 0
#    #                curColor = COLORS[self.colorIndex]
#    #                self.colorIndex +=1
#                    MZ+=mz
#            else:
#                plotTitle = 'Peaks at %s'%(peakInd[0])
#            ax1.set_title(plotTitle)
#            ax1.title.set_fontsize(10)
#            ax1.set_xlabel('m/z', fontstyle = 'italic')
#            ax1.set_ylabel('Intensity')
#            ax1.vlines(N.arange(len(MZ)),0,MZ, color = 'k')#curColor)#, label = '%s'%peakInd[i])
##            self.mzPlot.canvas.format_labels()
#
##            ax1.legend()
#            self.mzPlot.show()
#
##            dataCoord = [[int(N.round(event1.xdata)), int(N.round(event1.ydata))],[int(N.round(event2.xdata)), int(N.round(event2.ydata))]]
##
##            chromLimits = [dataCoord[0][0]*cols+dataCoord[0][1]+self.prevChromLimits,\
##                           N.abs(self.prevChromLimits+(dataCoord[1][0]*cols+dataCoord[1][1]))]
##            dataCoord = N.array(dataCoord)
##            chromLimits = N.array(chromLimits)
##            self.xLim = dataCoord[:,0]
##            self.yLim = dataCoord[:,1]
##            self.xLim.sort()
##            self.yLim.sort()
##            self.chromLimits.sort()

    def plotTypeChanged(self, plotTypeQString):
        self.tabWidget.setCurrentIndex(0)#return to plot tab
        self.plotType = str(plotTypeQString)
        self.specListSelect()

    def resetRefLimits(self):
        self.xLim = [0,0]
        self.yLim = [0,0]
        self.chromLimits = [0,0]
        self.prevImLimits = [0,0]

    def plotLinkage(self, finishedBool):
        if finishedBool:
            if self.showDendroCB.isChecked():
                if isinstance(self.linkagePlot, MPL_Widget):
                    self.linkagePlot.close()
                    self.linkagePlot = None
                self.linkagePlot = MPL_Widget()
                self.linkagePlot.setWindowTitle(('Clustered Peaks for %s'%self.curData.name))
                self.linkagePlot.canvas.setupSub(1)
                ax1 = self.linkagePlot.canvas.axDict['ax1']
#                print len(self.PCT.tempMIHist[0]), len(self.PCT.tempMIHist[1])
#
#                ax1.plot(self.PCT.tempMIHist[1][1:], self.PCT.tempMIHist[0])
#                ax1.plot(self.PCT.tempMDHist[1][1:], self.PCT.tempMDHist[0])
                if self.PCT.maxDist != None:
                    print "Maximum Distance Allowed: ",self.PCT.maxDist
                    H.dendrogram(self.PCT.linkageResult, colorthreshold=self.PCT.maxDist, customMPL = ax1)
#                else:
#                    H.dendrogram(self.PCT.linkageResult, colorthreshold= 10, customMPL = ax1)
                self.linkagePlot.show()
            self.clustLoc2D = self.PCT.peakCentroids
            self.autoscale_plot()




    def closeEvent(self,  event = None):
        try:
            self.linkagePlot.close()
        except:
            pass

        if len(self.mzPlots) > 0:
            for plot in self.mzPlots:
                if isinstance(plot, MPL_Widget):
                    try:
                        plot.close()
                    except:
                        pass
#        if self.okToExit():
#            pass
#        else:
#            event.ignore()

    def savePeaks2HDF(self):
        if self.curData != None:
            if self.curData.peakPickOk:
                self.curData.savePeakInfo()
        else:
            return QtGui.QMessageBox.warning(self, "No Data to Save",  'Load a Data File!')

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

    def saveRaw2DPeaks2CSV(self):
        '''
        Saves 2D peak locations to a CSV file
        Note: these are just the raw locations--not the clustered peaks.
        '''
        path = self.SFDialog()
        if path != None:
            try:
                if self.peakLoc2D != None:
                    self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints,\
                                                       self.curData.colPoints, peakIntensity = self.peakInfo['peakInt'])
                    data2write = N.column_stack((self.peakLoc2D[0],self.peakLoc2D[1], self.peakLoc2D[2]))
                    N.savetxt(str(path), data2write, delimiter = ',', fmt='%.4f')

                else:
                    raise 'No Peak List Exists to Save'

                print "Raw Peaks written to: %s"%str(path)

            except:
                errorMsg ='Error saving figure data to csv\n\n'
                errorMsg += "Sorry: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg
                return QtGui.QMessageBox.warning(self, "Save Error",  errorMsg)

    def savePeaks2CSV(self):
        '''
        Saves the raw 1D peaks in the full chromatogram to a file
        '''
        path = self.SFDialog()
        if path != None:
            try:
                if self.peakInfo != None:
                    header = []#'Index', 'Locations', 'Intensity','Width', 'Area']
            #        simpleIndex = N.arange(len(self.peakInfo['peakLoc']))
                    i = 0
                    for item in self.peakInfo.iteritems():
                        if i == 0:
                            header.append(item[0])
                            data2write = item[1]
                        else:
                            header.append(item[0])
                            data2write = N.column_stack((data2write,item[1]))
                        i+=1

                    N.savetxt(str(path), data2write, delimiter = ',', fmt='%.4f')
                else:
                    raise 'No Peak List Exists to Save'

            except:
                errorMsg ='Error saving figure data to csv\n\n'
                errorMsg += "Sorry: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg
                return QtGui.QMessageBox.warning(self, "Save Error",  errorMsg)

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
        '''
        Pickers for the Chromatogram
        minX is provided so that the plot will scale correctly when a data trace is initiated
        Pickers for the 2D image
        '''
        self.selectHandleA,  = self.chromAxis.plot([minX], [0], 'o',\
                                        ms=8, alpha=.4, color='yellow', visible=False,  label = '_nolegend_')
        self.selectHandleB,  = self.chromAxis.plot([minX], [0], 's',\
                                        ms=8, alpha=.4, color='green', visible=False,  label = '_nolegend_')
    def addImPickers(self, minX = 0):
        '''Pickers for the 2D Chromatogram'''
        self.selectCursA,  = self.imageAxis.plot([minX], [0], 'o',\
                                        ms=5, alpha=.7, color='red', visible=self.showImPickers,  label = '_nolegend_')
        self.xLine = self.imageAxis.axvline(x=0, ls = ':', color = 'y', alpha = 0.6, visible = self.showImPickers)
        self.yLine = self.imageAxis.axhline(y=0, ls = ':', color = 'y', alpha = 0.6, visible = self.showImPickers)
#        self.cursText = self.imageAxis.text(0, 0, '0rigin',  fontsize=9)

        self.imPicker = self.plotWidget.canvas.mpl_connect('pick_event', self.imageClick)

    def toggleImPickers(self):
        '''we want to toggle the visibility of these items in a group
        so a test for one is sufficient for all of them'''
        if self.showImPickers:
            self.showImPickers = False
            self.selectCursA.set_visible(False)
            self.xLine.set_visible(False)
            self.yLine.set_visible(False)
        else:
            self.showImPickers = True
            self.selectCursA.set_visible(True)
            self.xLine.set_visible(True)
            self.yLine.set_visible(True)

    def colorScale(self, dataMtx):
        dataMtx = N.where(dataMtx<= 0, dataMtx,10)
        lev_exp = N.arange(0, N.log2(dataMtx.max())+1)
        levs = N.power(2, lev_exp)
        return levs

    def updateChromGUI(self):
        self.specLengthSB.setValue(len(self.curChrom))
        self.numSegsSB.setValue(self.curData.rowPoints)

    def specListSelect(self, widgetItem=None):
        selectItems = self.listWidget.selectedItems()
        if len(selectItems) > 0:
            self.updatePlot(self.listWidget.indexFromItem(selectItems[0]).row())



##########Peak Finding Routines######################

    def findChromPeaks(self):

        self.autoscale_plot()

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
                    self.toggleProgressBar(True)
                    self.progressMax = N.float(self.peakParams['numSegs'])
                    self.PFT.start()
                    self.tabWidget.setCurrentIndex(0)
                else:
                    return QtGui.QMessageBox.warning(self, "The Spectrum is empty",  "The spectrum has a length of zero--no peaks to pick.")
            else:
                return QtGui.QMessageBox.warning(self, "No Spectrum to Process",  "Is a file loaded...?")
        else:
            return QtGui.QMessageBox.warning(self, "Peak Find Parameter Error",  "Check selected values, all should be integers!")

    def plotPickedPeaks(self, finishedBool):#this function is called when the peak finding thread is finished
        if finishedBool:
            self.peakInfo = None
            self.peakInfo = self.PFT.getPeakInfo()
            self.curData.setPeakInfo(self.peakInfo)
            self.PFT.wait()#as per Ashoka's code...

            if self.peakPickPlot2D != None:
                self.peakPickPlot2D.remove()
            if self.peakPickPlot1D != None:
                self.peakPickPlot1D.remove()
            if self.clustPlot != None:
                try:
                    self.clustDict = {}
                    self.clustPlot.remove()
                    self.clustLoc2D = None
                except:
                    print "No clustPlot to remove:"

            if self.memPlot != None:
                try:
                    self.memPlot.remove()
                    self.clustMembers = None
                except:
                    print "No memPlot to remove:"

            if self.showPickedPeaksCB.isChecked():
                self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints, self.curData.colPoints)
                curItem = self.listWidget.findItems(self.curData.name,QtCore.Qt.MatchExactly)[0]
                curRow = self.listWidget.indexFromItem(curItem).row()
                self.updatePlot(curRow)
#                self.autoscale_plot()#this is the function that actually plots the peaks in 1 and 2D

            self.setStatusLabel("Peak Fitting Completed, %d Peaks Found" % len(self.peakInfo['peakLoc']))

            self.resetProgressBar()
            self.setupTable()##!!This needs a qualifier because if no peaks are found it fails.
        else:
            return QtGui.QMessageBox.warning(self, "Peak Find Thread Error",  "The thread did not finish or return a value properly--contact Clowers...")

    def lassoHandler(self, selectPoints):
        print selectPoints


        try:
            self.lassoSelected.remove()
        except:
            print "No selection to remove."
            pass
        self.lassoSelected, = self.imageAxis.plot(selectPoints[:,0], selectPoints[:,1], 'bo', alpha = 0.5)
        self._setImScale_()

        scaledPoints = selectPoints
#        scaledPoints[:,0] += self.xLim[0]
        scaledPoints[:,0] +=self.prevImLimits[0]
#        scaledPoints[:,1] +=self.yLim[0]
        scaledPoints[:,1] +=self.prevImLimits[1]

        print scaledPoints
#        self.memPlot, = self.imageAxis.plot(self.clustMembers[:,0]-self.xLim[0]-self.prevImLimits[0],\
#                                    self.clustMembers[:,1]-self.yLim[0]-self.prevImLimits[1],\
#                                    'go', ms = 8, alpha = 0.5, label = 'clustMembers')


    def lassoToggle(self):
        if self.usrLasso:
            self.usrLasso = False
            self.imLasso.setActive(False)
            QtCore.QObject.disconnect(self.imLasso,QtCore.SIGNAL("LassoUpdate(PyQt_PyObject)"),self.lassoHandler)
            self.imLasso = None
#            print "Turned lasso off"
        else:
            if self.usrZoom:
                'need to turn the zooming off'
                self.zoomToggle()
            if self.cur2DPeakLoc != None:
                X = N.column_stack((self.cur2DPeakLoc[0], self.cur2DPeakLoc[1]))
                self.imLasso = LM(X, self.imageAxis)
                QtCore.QObject.connect(self.imLasso,QtCore.SIGNAL("LassoUpdate(PyQt_PyObject)"),self.lassoHandler)
            self.usrLasso = True

#            print "Turned lasso on"

    def zoomToggle(self):
        #self.toolbar.zoom() #this implements the classic zoom

        if self.usrZoom:
            self.usrZoom = False
#            self.RS.visible = False
            self.RS.set_active(False)
        else:
            if self.usrLasso:
                self.lassoToggle()
            self.usrZoom = True
#            self.RS.visible = True
            self.RS.set_active(True)

    def toggleDistance(self, intState):
#        print intState
        if intState == 0:
            self.maxDistThreshSB.setEnabled(True)
            self.distanceLabel.setEnabled(True)

        elif intState == 2:
            self.maxDistThreshSB.setEnabled(False)
            self.distanceLabel.setEnabled(False)

    def toggleClusterType(self, intState):
#        print intState
        if intState == 0:
            self.dbAutoCalcCB.setEnabled(False)
            self.denGrpNumThresh.setEnabled(False)
            self.denGrpNum.setEnabled(False)
            self.denDistLbl.setEnabled(False)
            self.densityDistThreshSB.setEnabled(False)
            ##################################
            self.showDendroCB.setEnabled(True)
            self.clustTypeLbl.setEnabled(True)
            self.clusterTypeCB.setEnabled(True)

#            self.distCalMethLbl.setEnabled(True)
#            self.distMethodCB.setEnabled(True)
            self.calcThreshCB.setEnabled(True)
            if not self.distanceLabel.isEnabled():
                self.toggleDistance(self.calcThreshCB.checkState())

        elif intState == 2:
            self.dbAutoCalcCB.setEnabled(True)
            self.denGrpNumThresh.setEnabled(True)
            self.denGrpNum.setEnabled(True)
            self.toggleAutoDBDist(self.dbAutoCalcCB.checkState())

            ##################################
            self.showDendroCB.setEnabled(False)
            self.clustTypeLbl.setEnabled(False)
            self.clusterTypeCB.setEnabled(False)
#            self.distCalMethLbl.setEnabled(False)
#            self.distMethodCB.setEnabled(False)
            self.calcThreshCB.setEnabled(False)
            if self.distanceLabel.isEnabled():
                self.distanceLabel.setEnabled(False)
                self.maxDistThreshSB.setEnabled(False)

    def toggleAutoDBDist(self, intState):
        '''
        Controls visibility of DBSCAN related GUI items.
        '''
        if intState == 0:
            self.densityDistThreshSB.setEnabled(True)
            self.denDistLbl.setEnabled(True)
#            self.denGrpNumThresh.setEnabled(True)
#            self.denGrpNum.setEnabled(True)

        elif intState == 2:
            self.densityDistThreshSB.setEnabled(False)
            self.denDistLbl.setEnabled(False)
#            self.denGrpNumThresh.setEnabled(False)
#            self.denGrpNum.setEnabled(False)


    def get2DPeakLoc(self, peakLoc, rows, cols, peakIntensity = None):
        x = N.empty(len(peakLoc), dtype = int)
        y = N.empty(len(peakLoc), dtype = int)
        if peakIntensity != None:
            z = N.empty(len(peakLoc), dtype = int)
            for i,loc in enumerate(peakLoc):
                x[i] = int(loc/cols)
                y[i] = loc%cols
                z[i] = peakIntensity[i]
            return [x,y,z]
        else:
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

###########Cursor Controls####################
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
        if self.cAPicker == None:
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

    def toggleCA(self, stateInt = None):
        '''
        setting the stateInt to None allows other actions
        to toggle the state of the cursor because by calling
        the nextCheckState function this function is called again
        with the stateInt intact.  Nifty...
        '''
        if stateInt == None:
            self.cursACB.nextCheckState()
        else:
            if stateInt == 2:
                self.SelectPointsA()
            else:
                self.cursAClear()

    def toggleCB(self, stateInt = None):
        if stateInt == None:
            self.cursBCB.nextCheckState()
        else:
            if stateInt == 2:
                self.SelectPointsB()
            else:
                self.cursBClear()

####saves plot canvas to clipboard as a png
    def image2Clip(self):
        self.plotWidget.mpl2Clip()

    def chrom2Clip(self):
        self.plotWidget2.mpl2Clip()

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

###############################################
##########END CURSOR CONTROLS##################

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
        self.setStatusLabel("Fitting Peaks, %d segments completed." % progVal)
        newVal = int(100*(progVal/self.progressMax))
        self.setProgressValue(newVal)
#        self.AddMessage2Tab("  %d Iterations Done." % progVal)
#        print progVal, newVal, self.progressMax

    def PCTProgress(self, updateString):
        self.setStatusLabel(updateString)


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