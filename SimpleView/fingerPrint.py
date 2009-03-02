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
import ui_fingerPrint
from dbscan import dbscan
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
                self.parent().parent._setFPFocus_(self.parent())
        return QtCore.QObject.eventFilter(self, obj, event)
############################

class Finger_Widget(QtGui.QWidget, ui_fingerPrint.Ui_fingerPlotWidget):
    NextId = 1
    Instances = set()

    def __init__(self, dataDict = None, parent = None):
        super(Finger_Widget, self).__init__(None)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        Finger_Widget.Instances.add(self)#new

        self.ui = self.setupUi(self)
        self.installEventFilter(EventFilter(self))

        self.mainAx = self.plotWidget.canvas.ax
        self.dataDict = {}
        self.dataDictOK = False
        self.setupVars()

        self.parent = None
        self.parentOk = False
        if parent != None:
            self.parent = parent
            self.parentOk = True
        self.windowTitle = "FingerPrint %d" % Finger_Widget.NextId
        self.setWindowTitle(self.windowTitle)
        Finger_Widget.NextId +=1

        if dataDict != None:
            self.dataDict = dataDict
            self.dataDictOK = True
            self.setupPlot()

        self.__initConnections__()

    def __initConnections__(self):
        self.actionAutoScale = QtGui.QAction("AutoScale",  self)#self.MainWindow)
        self.actionAutoScale.setShortcut("Ctrl+A")
        self.plotWidget.addAction(self.actionAutoScale)
        QtCore.QObject.connect(self.actionAutoScale, QtCore.SIGNAL("triggered()"), self.autoscale_plot)
        QtCore.QObject.connect(self.fingerPrint_Btn, QtCore.SIGNAL("clicked()"), self.fetchFP)
        QtCore.QObject.connect(self.saveFP_Btn, QtCore.SIGNAL("clicked()"), self.saveFinger2HDF5)
        QtCore.QObject.connect(self.commitFP_Btn, QtCore.SIGNAL("clicked()"), self.commitFinger2Parent)
        QtCore.QObject.connect(self, QtCore.SIGNAL("destroyed(QObject*)"), Finger_Widget.updateInstances)

    def commitFinger2Parent(self):
        if self.parentOk:
            fpName = str(self.fpName_LE.text())
            if fpName == 'Change me if you want to commit fingerprint!':
                return QtGui.QMessageBox.warning(self, "Fingerprint Name Error", "Please give a name to the current FP" )
            else:
                self.fpDict = {}
                self.fpDict[fpName] = {'dataDict':self.dataDict, 'peakStats':self.peakStatDict}
                self.parent.commitFP(self.fpDict)
#                self.emit(QtCore.SIGNAL("commitFP(dict)"),self.fpDict)
        else:
            return QtGui.QMessageBox.warning(self, "CRAP!", "No Parent Window Exists:\nBIG ERROR: Contact Clowers" )


    def updateDataDict(self, dataDict):
        for item in dataDict.iteritems():
            self.dataDict[item[0]]=item[1]
        self.dataDictOK = True

    def setupVars(self):
        self.plotColor = None
        self.plotColorIndex = 0
        self.compositePeakList = []
        self.resetPeakStatDict()
        self.xLoc = None
        self.yLoc = None
        self.mzTol = self.mzTol_SB.value()
        self.stdDevTol = self.stdDev_SB.value()
        self.fpDict = None
        self.numSpectra = 0

    def _updatePlotColor_(self):
        if self.plotColorIndex%len(COLORS) == 0:
            self.plotColorIndex = 0
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1
        else:
            self.plotColor = COLORS[self.plotColorIndex]
            self.plotColorIndex +=1

    def fetchFP(self):
#        print "FETCH FP"
        self.mainAx.cla()
        self.setupVars()
        if self.showRaw_CB.isChecked():
            self.setupPlot()
        self.getFPPeakList()
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()
        self.plotWidget.setFocus()

    def setupPlot(self):
        if self.dataDictOK:
            for curData in self.dataDict.itervalues():
        #            curData = self.dataDict[childName]
                self._updatePlotColor_()
                curData.plot(self.mainAx, pColor = self.plotColor)
#                pkList = curData.peakList
#                self.mainAx.scatter(pkList[:,0], pkList[:,1]*0, color = self.plotColor)
    def resetPeakStatDict(self):
        self.peakStatDict = {'aveLoc':[],
                             'stdLoc':[],
                             'aveInt':[],
                             'stdInt':[],
                             'numMembers':[],
                             'freq':[],
                             'prob':[],
                             'mzTol':[],
                             'stdDevTol':[]
                             }

    def getFPPeakList(self, resetDict = False):
        '''
        Need to make this more modular so that one can plot the peak locations with circles and the window...
        '''
        if resetDict:
            self.resetPeakStatDict()

        if self.dataDictOK:
#            self.mainAx.cla()
            self.xLoc = N.zeros(1)
            self.yLoc = N.zeros(1)
            self.specNum = N.zeros(1)#this is a bookeeping array
            curSpecNum = 0
            self.numSpectra = len(self.dataDict)/1.0#used to turn into float
            print "Number of Spectra: ", self.numSpectra
            for curData in self.dataDict.itervalues():
                pkList = curData.peakList
                self.xLoc = N.append(self.xLoc, pkList[:,0])
                self.yLoc = N.append(self.yLoc, pkList[:,1])
                self.specNum = N.append(self.specNum, N.zeros_like(pkList[:,0])+curSpecNum)
                curSpecNum +=1
#                self.mainAx.scatter(pkList[:,0],pkList[:,1]*0, color = self.plotColor)
            sortInd = self.xLoc.argsort()
            self.xLoc = self.xLoc[sortInd]
            self.yLoc = self.yLoc[sortInd]
            self.specNum = self.specNum[sortInd]
#            self.mainAx.plot(self.xLoc, self.yLoc, '--r')
            self.mzTol = self.mzTol_SB.value()
            self.stdDevTol = self.stdDev_SB.value()
            groups, gNum = groupOneD(self.xLoc, self.mzTol, origOrder = self.specNum)
            for g in xrange(gNum):
                self._updatePlotColor_()
                subInd = N.where(groups == g)[0]
                curXMean = self.xLoc[subInd].mean()
                curXStd = self.xLoc[subInd].std()
                curYMean = self.yLoc[subInd].mean()
                curYStd = self.yLoc[subInd].std()

                self.peakStatDict['aveLoc'].append(curXMean)
                self.peakStatDict['stdLoc'].append(curXStd)
                self.peakStatDict['aveInt'].append(curYMean)
                self.peakStatDict['stdInt'].append(curYStd)
                self.peakStatDict['numMembers'].append(len(subInd))
                self.peakStatDict['freq'].append(len(subInd)/self.numSpectra)
                self.peakStatDict['prob'].append(len(subInd)/self.numSpectra)
                self.peakStatDict['mzTol'].append(self.mzTol)
                self.peakStatDict['stdDevTol'].append(self.stdDevTol)
                if len(subInd)>=2:
                    self.mainAx.plot(self.xLoc[subInd], self.yLoc[subInd], ms = 4, marker = 'o', alpha = 0.5, color = self.plotColor)
                    #Rect((x,y),width, height)
                    tempRect = Rect((curXMean-curXStd*self.stdDev_SB.value(),0),curXStd*2*self.stdDev_SB.value(),curYMean+curYStd, alpha = 0.5, facecolor = self.plotColor)
                    self.mainAx.add_patch(tempRect)
            #convert peakStats to Numpy
            for key in self.peakStatDict.iterkeys():
                #CHECK THIS
                self.peakStatDict[key] = N.array(self.peakStatDict[key][1:])#we want to remove the first element as it is zero and just a place holder
            self.setupTable()

    def fpCompare(self, fpStatDict, peakCompDict, alpha):
        sgmadivmu = 0.0001
        foundList, compList = self.fpextract(fpStatDict, peakCompDict, alpha, sgmadivmu)
        numPeaks = fpStatDict['numMembers'][0]
        cmpVec = N.zeros_like(foundList)
        cmpVec +=1
        indx = N.where(foundList>0)[0]
        cmpVec[indx] = 0
        probFp = fpStatDict['prob']*(1-alpha)
        fpCmpProb = self.fpCompSig(cmpVec, probFp)
        return fpCmpProb

    def fpCompSig(self, cmpVec, probFp):
        probAll = N.prod(1-probFp)
        numOnes = cmpVec.sum()
        pctDrop = numOnes/len(cmpVec)
        probs = 0
        if pctDrop > 0.8:#is this a static value?
           probs = 0
        elif pctDrop == 0:
           probs = 1
        else:
           missing = N.where(cmpVec == 1)[0]#find(zero1vec == 1);
    #           lenM = len(missing)
           observed = N.where(cmpVec == 0)[0]#find(zero1vec==0);
           prob1 = N.prod(1-probFp[missing])
           prob2 = N.prod(probFp[observed])
           probs = 1-prob2*(1-prob1)

        return probs


    def fpextract(self, fpStatDict, peakCompDict, alpha, sgmadivmu, minTolppm = 50):
        '''
        Variables needed:
        number of spectra for each dictionary
        df1 = numMembers - 1
        df2 = numMembers - 1
        dfe = df1+df2

        '''
        alpha = alpha/2#OK
        fpPeakLoc = fpStatDict['aveLoc']#OK
        fpStdLoc = fpStatDict['stdLoc']#OK
        cmpPeakLoc = peakCompDict['aveLoc']
        cmpPeakInt = peakCompDict['aveInt']
        tol = 3*(1+(fpPeakLoc*sgmadivmu)**2)#not sure why this is the case need to find out
        #need to make an instance of peakCompDict that is for one spectrum
        degF1 = fpStatDict['numMembers'][0]-1 #indexing first value as this is a list with the same values
        degF2 = (N.round(peakCompDict['numMembers']*peakCompDict['prob']))-1 #indexing first value as this is a list with the same values
        degF = degF1+degF2
        foundList = N.zeros_like(fpPeakLoc)
        foundIntList = N.zeros_like(fpPeakLoc)
        compList = N.zeros_like(cmpPeakLoc)
        for i,mz in enumerate(fpPeakLoc):
            absDiff = N.abs(mz-cmpPeakLoc)#need to make arrays the same length#OK
            pool = N.max([(minTolppm/1000000.)*mz, fpStdLoc[i]])
            tstat = absDiff/pool
            closest = N.argmin(absDiff)
            sigLvl = 1 - stats.t.cdf(tstat[closest], degF[closest])#this is 1-alpha

            if sigLvl > alpha:
                rempt = 0
            elif absDiff[closest]<tol[i]:
                rempt = 0
            else:
                rempt = 1

            if rempt == 0:
                foundList[i]= cmpPeakLoc[closest]
                foundIntList[i] = cmpPeakInt[closest]
                compList[closest] = 1

        return foundList, compList




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


    def setupTable(self):
        self.peakTable.clear()
        self.peakTable.setSortingEnabled(False)
        tableHeaders = ['aveLoc','stdLoc', 'aveInt', 'stdInt', 'numMembers', 'freq']
#        for key in tableHeaders:
#            self.peakStatDict[key] = N.array(self.peakStatDict[key])

        tableData = self.peakStatDict['aveLoc']
        for key in tableHeaders[1:]:
            tableData = N.column_stack((tableData,self.peakStatDict[key]))
#        print tableData.shape
        self.peakTable.addData(tableData)
        self.peakTable.setSortingEnabled(True)
        self.peakTable.setHorizontalHeaderLabels(tableHeaders)

    def autoscale_plot(self):
#        print "Auto Finger"
        self.mainAx.autoscale_view(tight = False, scalex=True, scaley=True)
        self.mainAx.set_ylim(ymin = 0)
        self.plotWidget.canvas.draw()

    def saveFileDialog(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                         "Select File to Save",
                                         "",
                                         "hdf5 Files (*.h5)")
        if not fileName.isEmpty():
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
                specY = item[1].y
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
#            ca.flush()
#            print "%s written"%natName


    def saveFinger2HDF5(self):
        fileName = self.saveFileDialog()
        if fileName != None and self.dataDictOK:
            hdf = T.openFile(fileName, mode = 'w', title = 'FingerPrint')
            try:
                self.saveDict(hdf, self.dataDict, "Spectra")
                self.saveDict(hdf, self.peakStatDict, "PeakStats")
                '''
                Need to iteratively save XY spectra and each peak List
                Save Peak Table
                Need a way to handle saving dictionaries
                '''
                hdf.close()
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
        Finger_Widget.Instances = set([window for window \
                in Finger_Widget.Instances if isAlive(window)])


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



#    for


if __name__ == "__main__":
    #from scipy import rand
    app = QtGui.QApplication(sys.argv)
    finger = Finger_Widget()
    finger.show()
    tempRect = Rect((1,1),3,5, alpha = 0.4)
    finger.mainAx.add_patch(tempRect)
    sys.exit(app.exec_())
