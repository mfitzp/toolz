'''
How to save peakParams to file?
'''


import os, sys, traceback
from PyQt4 import QtGui, QtCore
import numpy as N
import scipy.stats as stats

import tables as T

from matplotlib.patches import Rectangle as Rect
import supportFunc as SF
import ui_plotWindow
#from dbscan import dbscan
from dataClass import DataClass

COLORS = ['#297AA3','#A3293D','#3B9DCE','#293DA3','#5229A3','#8F29A3','#A3297A',
'#7AA329','#3DA329','#29A352','#29A38F','#A38F29','#3B9DCE','#6CB6DA','#CE6C3B','#DA916C',
'#0080FF','#0000FF','#7ABDFF','#8000FF','#FF0080','#FF0000','#FF8000','#FFFF00','#A35229','#80FF00',
'#00FF00','#00FF80','#00FFFF','#3D9EFF','#FF9E3D','#FFBD7A']

##Used to test whether the item is the top widget or alive
def isAlive(qobj):#new
    import sip
    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True

class EventFilter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.ActivationChange:
            if self.parent().isActiveWindow():
#                print "Got the focus @ %s"%(self.parent().windowTitle)
#                self.parent().parent.testFocus()
                self.parent().parent._setPlotFocus_(self.parent())
        return QtCore.QObject.eventFilter(self, obj, event)
############################

class PlotWidget(QtGui.QWidget, ui_plotWindow.Ui_plotWindow):
    NextId = 1
    Instances = set()

    def __init__(self, xyData = None, colHeaders = None, rowHeaders = None, dataDict = None, parent = None, windowTitle = None):
        super(PlotWidget, self).__init__(None)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        PlotWidget.Instances.add(self)#new
        self.ui = self.setupUi(self)
        self.installEventFilter(EventFilter(self))

        self.mainAx = self.plotWidget.canvas.ax
        self.plotWidget.enableCSV()
        self.plotWidget.enableEdit()
        self.dataDict = {}
        self.dataDictOK = False


        self.parent = None
        self.parentOk = False
        if parent != None:
            self.parent = parent
            self.parentOk = True
        if windowTitle != None:
            self.windowTitle = windowTitle
        else:
            self.windowTitle = "Plot %d" % PlotWidget.NextId
        self.setWindowTitle(self.windowTitle)
        PlotWidget.NextId +=1

        if xyData != None:
            if colHeaders != None:
                self.setupTable(xyData, colHeaders)
            else:
                self.setupTable(xyData)

            self.setupPlot(xyData, "Data")


        if dataDict != None:
            self.dataDict = dataDict
            self.dataDictOK = True
            self.setupPlot()

        self.setupVars()
        self.__initConnections__()
#        self.resize(500,700)

    def __initConnections__(self):
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale, QtCore.SIGNAL("triggered()"), self.autoscale_plot)

#        self.addDataAction = QtGui.QAction("Add Data",  self)#self.MainWindow)
#        self.actionAutoScale.setShortcut("Ctrl+D")
#        self.plotWidget.addAction(self.addDataActiond)
#        QtCore.QObject.connect(self.addDataAction, QtCore.SIGNAL("triggered()"), self.selectData2Add)

        QtCore.QObject.connect(self.xmin_lineEdit, QtCore.SIGNAL("editingFinished()"), self.setXMin)
        QtCore.QObject.connect(self.xmax_lineEdit, QtCore.SIGNAL("editingFinished()"), self.setXMax)

        QtCore.QObject.connect(self.ymin_lineEdit, QtCore.SIGNAL("editingFinished()"), self.setYMin)
        QtCore.QObject.connect(self.ymax_lineEdit, QtCore.SIGNAL("editingFinished()"), self.setYMax)
#        QtCore.QObject.connect(self, QtCore.SIGNAL("destroyed(QObject*)"), PlotWidget.updateInstances)

#    def initContextMenus(self):
#        self.plotWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.plotWidget.connect(self.plotWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__mplContext__)
#
#    def selectData2Add(self):
#        if self.parentOk:


    def __mplContext__(self, point):
        '''Create a menu for the mpl widget'''
        ct_menu = QtGui.QMenu("Plot Menu", self.plotWidget)
        ct_menu.addAction(self.addDataAction)
##        ct_menu.addSeparator()
##        ct_menu.addAction(self.calcMobAction)
##        ct_menu.addSeparator()
#        ct_menu.addAction(self.labelAction)
#        ct_menu.addSeparator()
#        ct_menu.addAction(self.editLinesAction)
        ct_menu.addSeparator()
        ct_menu.addAction(self.plotWidget.mpl2ClipAction)
        ct_menu.exec_(self.plotWidget.mapToGlobal(point))

    def addData(self, dataLabel, xyData, colHeaders = None):
#        self.dataDict[dataLabel] = xyData
        self.setupPlot(xyData, dataLabel)
        if colHeaders != None:
            self.setupTable(xyData, colHeaders = colHeaders )
        else:
            self.setupTable(xyData)

        self.resetAxisGUI()


    def setXMin(self, val=None):
        if val is None:
            val = self.xmin_lineEdit.text()
        try:
            val = float(str(val))
            self.mainAx.set_xlim(xmin=val)
            self.xMin = val
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
        except:
            msg = "Must Enter a Number for the Minimum Value"
            return QtGui.QMessageBox.information(self, "Property Error", msg)
            self.mainAx.set_xlim(xmin=self.xmin)
#            self.xmin_lineEdit.setText(str(self.xmin))

    def setXMax(self, val=None):
        if val is None:
            val = self.xmax_lineEdit.text()
        try:
            val = float(str(val))
            self.mainAx.set_xlim(xmax=val)
            self.xMax = val
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
        except:
            msg = "Must Enter a Number for the Maximum Value"
            return QtGui.QMessageBox.information(self, "Property Error", msg)
            self.mainAx.set_xlim(xmax=self.xmax)

    def setYMin(self, val = None):
        if val is None:
            val = self.ymin_lineEdit.text()
        try:
            val = float(str(val))
            self.mainAx.set_ylim(ymin=val)
            self.yMin = val
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
        except:
            msg = "Must Enter a Number for the Minimum Value"
            return QtGui.QMessageBox.information(self, "Property Error", msg)
            self.mainAx.set_ylim(ymin=self.ymin)

    def setYMax(self, val = None):
        if val is None:
            val = self.ymax_lineEdit.text()
        try:
            val = float(str(val))
            self.mainAx.set_ylim(ymax=val)
            self.yMax = val
            self.plotWidget.canvas.format_labels()
            self.plotWidget.canvas.draw()
        except:
            msg = "Must Enter a Number for the Maximum Value"
            return QtGui.QMessageBox.information(self, "Property Error", msg)
            self.mainAx.set_ylim(ymax=self.ymax)


    def updateDataDict(self, dataDict):
        for item in dataDict.iteritems():
            self.dataDict[item[0]]=item[1]
        self.dataDictOK = True

    def setupVars(self):
        self.plotColor = None
        self.plotColorIndex = 0
        self.peakStatDict = None
        self.resetAxisGUI()

    def resetAxisGUI(self):
        self.xMin = self.mainAx.get_xlim()[0]
        self.xMax = self.mainAx.get_xlim()[1]
        self.yMin = self.mainAx.get_ylim()[0]
        self.yMax = self.mainAx.get_ylim()[1]
        self.ymin_lineEdit.setText(str(self.yMin))
        self.ymax_lineEdit.setText(str(self.yMax))
        self.xmin_lineEdit.setText(str(self.xMin))
        self.xmax_lineEdit.setText(str(self.xMax))

    def _updatePlotColor_(self):
        if self.plotColorIndex%len(COLORS) == 0:
            self.plotColorIndex = 0
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1
        else:
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1

    def setupPlot(self, xyData = None, dataLabel = None):
        '''
        Remember you need to call draw and format axes if you want it to update!!!!!!!!!!!!
        '''
        if xyData != None:
            self.mainAx.plot(xyData[:,0], xyData[:,1], label = dataLabel)#, 'r')
#        if self.dataDictOK:
#            for curData in self.dataDict.itervalues():
#        #            curData = self.dataDict[childName]
#                self._updatePlotColor_()


    def loctest(self, meanVal, absDiff, sgma, numObs, sigLvl = 0.05, n0 = 0):
        '''
        CURRENTLY NOT USED!!!!!!!!!!!!!2/25/09 BHC
        %  Usage:   [dec] = loctest(absdiff,sgmasq,N);
        %   This funciton tests whether or not difference absdiff is significantly
        %   different from zero.  NOTE n0 is a parameter which is used in
        %   aligning MALDI peaks - it is based on how good our initial guess
        %   for the variance is.....omit this parameter unless used by pkalign.m
        %              Inputs:   absdiff = the absolute difference between obs.
        %                        sgmasq = the variance of the observations.
        %                             N = the number of observations in the average
        %                                  (the number for the other is always =1).
        %                             n0 = number of obs on which initial guess
        %                                   of variance is based.
        %
        %
        Modified by BHC to take into account ppm differences
        '''
        ppmDiff = (absDiff/meanVal)*1000000#convert to ppm domain
        sgmaSqPPM = ((sgma/meanVal)*1000000)**2#convert to ppm domain

        dec = 0 #decision whether the peak fits in the window or not
        diffMax = 0
        if (numObs+n0) > 5:
            tCrit = N.abs(stats.t.ppf(1-sigLvl/2,numObs+n0-1))
            tStat = ppmDiff/(N.sqrt((1/N+1)*sgmaSqPPM))
            if tStat>=tCrit:
                diffMax = -1
                dec = 1
        else:
            if ppmDiff>=1.96*sgmaSqPPM:
                diffMax = -1
                dec = 1
        return dec, diffMax


    def setupTable(self, tableData, colHeaders = None):
        self.peakTable.clear()
        self.peakTable.setSortingEnabled(False)
        if colHeaders != None:
            self.peakTable.setHorizontalHeaderLabels(colHeaders)
        self.peakTable.addData(tableData)
        self.peakTable.setSortingEnabled(True)


    def autoscale_plot(self):
#        print "Auto Finger"
        self.mainAx.autoscale_view(tight = False, scalex=True, scaley=True)
        self.mainAx.set_ylim(ymin = 0)
        self.plotWidget.canvas.draw()

    def saveFileDialog(self):
        if self.parentOk:
            curDir = self.parent.curDir
        else:
            curDir = ""
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                         "Select File to Save",
                                         curDir,
                                         "hdf5 Files (*.h5)")
        if not fileName.isEmpty():
            fileName = os.path.abspath(str(fileName))
            self.parent.curDir = os.path.dirname(fileName)
            print fileName
            return str(fileName)
        else:
            return None
#    def changePathStr(self, pathStr):
#        ret

    def saveDict(self, hdfInstance, dataDict, groupName, attrDict = None):
        '''
        Saves the original netCDF arrays in a compressed HDF5 format
        '''

        filters = T.Filters(complevel=5, complib='zlib')
        atom = T.FloatAtom()
#        hdf = T.openFile(filename, mode = "w", title = 'Data_Array')
        varGroup = hdfInstance.createGroup("/", groupName, groupName)
        tempKey = dataDict.keys()[0]
        pkListOK = False
        if isinstance(dataDict[tempKey], DataClass):
            pkListGroup = hdfInstance.createGroup("/", "PeakLists", "PeakLists")
            pkListOK = True

        for item in dataDict.iteritems():
            natName = item[0].replace(os.path.sep, '*')#natural Name
            if isinstance(item[1], DataClass):
                specX = item[1].x
                specY = item[1].y*item[1].normFactor
                data = N.column_stack((specX,specY))
                pkList = item[1].peakList
                pkParams = item[1].peakParams
                if pkList != None and pkListOK:
                    shape = pkList.shape
#                    print pkList
                    ca = hdfInstance.createCArray(pkListGroup, natName, atom, shape, filters = filters)
                    ca[0:shape[0]] = pkList
                    if pkParams != None:
                        ca._v_attrs.scales = pkParams['scales']
                        ca._v_attrs.minSNR = pkParams['minSNR']
                        ca._v_attrs.minRow = pkParams['minRow']
                        ca._v_attrs.minClust = pkParams['minClust']
                        ca._v_attrs.EPS = pkParams['dbscanEPS']
                        ca._v_attrs.rowThresh = pkParams['rowThresh']
                        ca._v_attrs.noiseFactor = pkParams['noiseFactor']
                        ca._v_attrs.staticThresh = pkParams['staticThresh']
#                        self.paramDict = {'scales':None,
#                                      'minSNR':None,
#                                      'minRow':None,
#                                      'minClust':None,
#                                      'dbscanEPS':None,
#                                      'rowThresh':None,
#                                      'noiseFactor':None,
#                                      'staticThresh':None,
#                                      'autoSave':None
#                                      }
            else:#this would be the case for PeakStatsDict
#                varGroup._v_attrs.mzTol = self.mzTol_SB.value()
#                varGroup._v_attrs.stDev = self.stdDev_SB.value()

                data = item[1]
            shape = data.shape
            ca = hdfInstance.createCArray(varGroup, natName, atom, shape, filters = filters)
            ca[0:shape[0]] = data
            if isinstance(item[1], DataClass):
                mzPad = item[1].mzPad
                if mzPad == None:
                    ca._v_attrs.mzPad = 50
                else:
                    ca._v_attrs.mzPad = item[1].mzPad

    def saveDict2CSV(self):
        "Go Joe"

    def saveFinger2HDF5(self):
        fileName = self.saveFileDialog()
        if fileName != None and self.dataDictOK:
            hdf = T.openFile(fileName, mode = 'w', title = 'FingerPrint')
            try:
                self.saveDict(hdf, self.dataDict, "Spectra")
                self.saveDict(hdf, self.peakStatDict, "PeakStats")
                csvFileName = fileName.split('.')[0]+'_Table.csv'
                writeDict2CSV(self.peakStatDict, csvFileName)
                '''
                Need to iteratively save XY spectra and each peak List
                Save Peak Table
                Need a way to handle saving dictionaries
                '''
                hdf.close()
                print "Successfully saved %s to disk!"%fileName
            except:
                hdf.close()
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
                errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
                return QtGui.QMessageBox.warning(self, "Save File Error", errorMsg)
                print 'Error saving fingerprint to HDF5'
                print errorMsg

    @staticmethod
    def updateInstances(qobj):
        PlotWidget.Instances = set([window for window \
                in PlotWidget.Instances if isAlive(window)])


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

def writeDict2CSV(dict2write, fileName):
    '''
    Assumes that the length of each
    item in the dictionary is the same
    '''
    dKeys = dict2write.keys()
    header = ','.join(dKeys)
    f = open(fileName, 'w')
    header+='\n'
    f.write(header)
    try:
        allRows = []
        for i in xrange(len(dict2write[dKeys[0]])):
            row = []
            for key in dKeys:
                row.append(str(dict2write[key][i]))
            formattedRow = ','.join(row)
            formattedRow+='\n'
            allRows.append(formattedRow)
        f.writelines(allRows)
        f.close()
    except:
        print "File Write Error"
        f.close()
        raise



if __name__ == "__main__":
    #from scipy import rand
    app = QtGui.QApplication(sys.argv)
    x = N.arange(50)
    y = N.sin(x)
    plot = PlotWidget(xyData = N.column_stack((x,y)))
    plot.mainAx.draw()
    plot.show()
#    tempRect = Rect((1,1),3,5, alpha = 0.4)
#    plot.mainAx.add_patch(tempRect)
    sys.exit(app.exec_())
