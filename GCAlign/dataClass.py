#!/usr/bin/env python

'''
Make it so that the BPC is stored when the file is created....11/24/2008 BHC--Done
Remember to use writearray2file to append a certain array to hdf5.

'''


import os
from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T

class GC_GC_MS_CLASS(QtCore.QObject):
    def __init__(self, filePath):
        '''
        filePath is an HDF5 file that has been converted from a LECO netCDF file
        '''
        self.filePath = filePath
        self.name = os.path.basename(filePath)
        self.loadOK = False
        self.fileOpen = False
        self.handle = None

        self.peakPickOk = False
        self.peakInfo1D = None
        self.pickedPeaksCluster = None
        self.peakPickParams = None
        self.peakArrayNames = ['peakLoc', 'peakInt', 'peakWidth', 'peakArea']


        self.colPoints = None
        self.rowPoints = None
        self.ticLayer = None
        self.eicLayer = None
        self.curMZ = None
        self.EIC = None
        self.TIC = None
        self.BPC = None
        self.BPCmz = None#the mz values making up each BPC point

        self.eicOK = False
        self.ticOK = False
        self.bpcOK = False

        self.startPnt = None
        self.stopPnt = None

        #data are stored as integers but some of the functions
        #need to use floats.  This is a boolean to see if the
        #conversion to floats has occurred
        self.floated = False

        self.setAttrs()
        self.setupThreads()
        self.setTIC()
        self.ticLayer = self.make2DLayer(self.TIC, self.colPoints)
        self.setBPC()
        self.bpcLayer = self.make2DLayer(self.BPC, self.colPoints)
        self.readPeakInfo()

    def setPeakInfo(self, peakInfoDict):
        if type(peakInfoDict) is dict:
            if peakInfoDict.has_key('peakLoc'):
                self.peakPickOk = True
                self.peakInfo1D = peakInfoDict
            else:
                print "1D Peak Info Error, the dictionary does not have the appropriate keys"
        else:
            print "the supplied peak information is not in dictionary form"

    def setupThreads(self):
        self.ReadThread = ReadThread(self.filePath, self)

    def updateEIC(self, finishedBool):
        self.eicOK = finishedBool
        if finishedBool:
            self.EIC = self.ReadThread.getEIC()
            print "EIC finished processing"
        else:
            print "Please wait, EIC not finished processing"

    def updateBPC(self, finishedBool):
        self.bpcOK = finishedBool
        if finishedBool:
            self.BPC = self.ReadThread.getBPC()
#            P.plot(self.BPC)
#            P.show()
            print "BPC finished processing"
        else:
            print "Please wait, BPC not finished processing"

    def readPeakInfo(self):
        self.getHandle()
        childDict = self.handle.root._v_children #dictionary of children
        if childDict.has_key(self.peakArrayNames[0]):
            self.peakInfo1D = {}
            for arrayName in self.peakArrayNames:
                self.peakInfo1D[arrayName] = childDict[arrayName].read()
            self.peakPickOk = True
        self.closeHandle()

    def writeArray2File(self, arrayName, array):
        hdf = T.openFile(self.filePath, mode = "a")
        if hdf.root._v_children.has_key(arrayName):
            hdf.root._v_children[arrayName].remove()
        filters = T.Filters(complevel=5, complib='zlib')
        atom = T.FloatAtom()#Int32Atom()
        shape = array.shape
        try:
            ca = hdf.createCArray(hdf.root, arrayName, atom, shape,  filters = filters)
            ca[0:shape[0]] = array
            ca.flush()
            hdf.close()
            print "Write %s to HDF OK!"%arrayName
        except:
            print "error writing %s to %s"%(arrayName,self.filePath)
            hdf.close()

    def savePeakInfo(self):
        if self.peakPickOk:
            for item in self.peakInfo1D.iteritems():
                self.writeArray2File(item[0], item[1])

    def getHandle(self):
        self.handle = T.openFile(self.filePath, 'r')
        self.fileOpen = True

    def closeHandle(self):
        self.handle.close()
        self.fileOpen = False

    def _setBPC_(self):
        print "This function has been disabled"
#        self.ReadThread.setType('BPC')
#        self.ReadThread.start()

    def getBPC(self):
        if self.bpcOK:
#            print "BPC returned"
            return self.BPC#, self.BPCmz

    def getBPCmz(self):
        if self.bpcOK:
            return self.BPCmz

    def getMZvalues(self, mzList):
        self.getHandle()
#        self.mz = self.handle.root.mzCube
        mz = self.handle.root.dataCube[mzList[0]]
        if len(mzList)>1:
            for val in mzList[1:]:
                mz+=self.handle.root.dataCube[val]

        self.closeHandle()
        return mz

    def getMZlist(self, mzInd):
        self.getHandle()
#        self.mz = self.handle.root.mzCube
        mzList = []
        mzList.append(self.handle.root.dataCube[mzInd[0]])
        if len(mzInd)>1:
            for val in mzInd[1:]:
                mzList.append(self.handle.root.dataCube[val])

        self.closeHandle()
        return mzList

    def _setEIC_(self, mzVals):
        self.ReadThread.setType('EIC')
        self.ReadThread.initEICVals(mzVals)
        self.ReadThread.start()
        '''
        mzVals is a list of integers. If the list has a length greater than 1 ,
        a summed EIC of all numbers in the list will be returned.
        '''
#        self.getHandle()
#        if self.fileOpen and len(mzVals)>0:
#            mzCube = self.handle.root.dataCube
#
#            rows = len(self.TIC)
#            eic = N.zeros(rows)
#
#            for mz in mzVals:
#                eic +=mzCube[:,mz]
#
#            self.EIC = eic
#            self.closeHandle()
#            self.eicOK = True
#        else:
#            print "Error opening HDF5 data file"

    def getEIC(self):
        if self.eicOK:
            return self.EIC
        else:
            print "No EIC generated--try _setEIC_(mzValList)"

    def setTIC(self):
        self.getHandle()
        if self.fileOpen:
            tic = self.handle.root.TIC.read()
            self.closeHandle()
            if len(tic)>0:
                self.ticOK = True
                self.TIC = tic
            else:
                print "Error opening HDF5 data file, no TIC found"

    def setBPC(self):
        self.getHandle()
        if self.fileOpen:
            bpc = self.handle.root.BPC.read()
            bpcMZ = self.handle.root.BPC.read()
            self.closeHandle()
            if len(bpc)>0:
                self.bpcOK = True
                self.BPC = bpc
                self.BPCmz = bpcMZ
            else:
                print "Error opening HDF5 data file, no TIC found"

    def getTIC(self):
        if self.ticOK:
            return self.TIC
        else:
            print "TIC not set or not found try setTIC()"

    def setAttrs(self):
        self.getHandle()
        if self.fileOpen:
            cols = self.handle.root.dataCube.attrs.colPoints
            if cols != None:
                if cols > 0:
                    self.colPoints = cols
                else:
                    print 'Big Error!, check file type and how it was made. Number of rows set to ZERO!'
            else:
                print 'Big Error!, check file type and how it was made. No column attributes found!'
            rows = self.handle.root.dataCube.attrs.rowPoints
            if rows != None:
                if rows > 0:
                    self.rowPoints = rows
                else:
                    print 'Big Error!, check file type and how it was made. Number of rows set to ZERO!'
            else:
                print 'Big Error!, check file type and how it was made. No row attributes found!'

            self.closeHandle()

    def make2DLayer(self, cgram, colPoints):
        '''
        cgram = chromatogram
        cLayer = 2D representation of cgram
        '''
        rowPoints = int(len(cgram)/colPoints)
        cLayer = N.empty((rowPoints, colPoints), dtype = int)#  self.colPoints),  dtype=int)
        print cLayer.shape
        x = 0
        for i in xrange(len(cgram)):
            y=i%colPoints
            cLayer[x][y] = cgram[i]
            if i !=0 and (i%colPoints) == 0:
                x+=1

        return N.transpose(cLayer)

    def get2DPeakLoc(peakLoc, rows, cols):
        x = N.empty(len(peakLoc), dtype = int)
        y = N.empty(len(peakLoc), dtype = int)
        for i,loc in enumerate(peakLoc):
            x[i] = int(loc/cols)
            y[i] = loc%cols

        return x,y

class ReadThread(QtCore.QThread):
    def __init__(self, fileName, main, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.parent = main
        self.finished = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.fileName = fileName
        self.handle = None
        self.fileOpen = False

        self.bpcOK = False
        self.BPC = None

        self.ready = False

        self.eicOK = False
        self.EIC = None
        self.mzVals = None
        self.specType = None

    def setType(self, specType):
            self.specType = specType

    def getHandle(self):
        self.handle = T.openFile(self.fileName, 'r')
        self.fileOpen = True

    def closeHandle(self):
        self.handle.close()
        self.fileOpen = False

    def setBPC(self):
        self.getHandle()
        if self.fileOpen:
            mzCube = self.handle.root.dataCube

            rows = mzCube.shape[0]
            bpc = N.zeros(rows)
            mzVals = N.zeros(rows)

            for i in xrange(rows):
                mz=mzCube[i]
                mzVals[i] = mz.argmax()
                bpc[i]= mz[mzVals[i]]
                if i%10000 == 0:
                    print i

            self.BPC, self.BPCmz = bpc, mzVals
            self.closeHandle()
            return True
        else:
            print "Error opening HDF5 data file"
            return False

    def getBPC(self):
        if self.bpcOK:
            return self.BPC

    def getEIC(self):
        if self.eicOK:
            return self.EIC

    def initEICVals(self, mzList):
            '''
            Accepts a list of mzValues to get an EIC for
            '''
            if type(mzList) is list and len(mzList)>0:
                self.mzVals = mzList
                self.ready = True

    def setEIC(self):
        self.getHandle()
        if self.fileOpen and len(self.mzVals)>0:
            mzCube = self.handle.root.dataCube

            rows = mzCube.shape[0]
            eic = N.zeros(rows)

            for mz in self.mzVals:
                eic +=mzCube[:,mz]

            self.EIC = eic
            self.closeHandle()
            return True
        else:
            print "Error opening HDF5 data file"
            return False


    def run(self):
        self.finished = False
        if self.specType == 'BPC':

            self.bpcOK = self.setBPC()
    #        self.emit(QtCore.SIGNAL("finished(bool)"),self.bpcOK)
            self.finished = True
            self.parent.updateBPC(self.bpcOK)
        elif self.specType == 'EIC':
            if self.ready:
                self.finished = False
                self.eicOK = self.setEIC()
        #        self.emit(QtCore.SIGNAL("finished(bool)"),self.eicOK)
                self.finished = True
                self.ready = False
                self.parent.updateEIC(self.eicOK)
            else:
                print "No mz value list set, run initEICVals(mzList)"


    def stop(self):
        print "stop try"
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        print "stop try"
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()




if __name__ == "__main__":
    import sys
    import pylab as P
    import matplotlib.colors as C
    from mpl_pyqt4_widget import MPL_Widget
    import time
    app = QtGui.QApplication(sys.argv)

    file = 'Acetone_Klean.h5'
    data = GC_GC_MS_CLASS(file)
#    mz = data.getMZvalues([3000,3010,3020])
    mzList = data.getMZlist([3000,3010,3020,3030,3040])

#    print mz
#    tic = data.getTIC()

    w = MPL_Widget()
#    w.canvas.setupSub(1)
    ax1 = w.canvas.axDict['ax1']
#    ax1.vlines(N.arange(len(mz)),0,mz)
    i = 0
    col = ['r','b','g','k','y']
    for mz in mzList:
        ax1.vlines(N.arange(len(mz)),0,mz, color = col[i])
        print i
        i+=1


#    ax2 = w.canvas.axDict['ax2']

#    t1 = time.clock()
#    data._setEIC_([53])
#    time.sleep(6)
#    bpc = data.getBPC()
#    print 'EIC Generation: ', time.clock()-t1


#    t1 = time.clock()
#    ticLayer = data.ticLayer
#    bpcLayer = data.bpcLayer
#    print 'TIC Layer Generation: ', time.clock()-t1
#
#    t1 = time.clock()
##    data._setBPC_()
#    print 'BPC Generation: ', time.clock()-t1

#    bpc, bpcMZ = data.getBPC()

#    imAspect = data.rowPoints/(data.colPoints*1.0)
#
#    cdict ={
#    'blue': ((0.0, 0.01, 0.01), (0.01, 0.25, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
#    'green': ((0.0, 0, 0), (0.05, 0.75, 0.75), (0.25, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
#    'red': ((0.0, 0, 0), (0.15, 0.25, 0.25), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
#    }
#
#    my_cmap = C.LinearSegmentedColormap('mycmap', cdict, 512)
#    ax1.imshow(bpcLayer, origin = 'lower', aspect = 'auto', cmap = my_cmap)
    #ax2.imshow(N.transpose(ticLayer), origin = 'lower', aspect = 'auto')
#    ax1.set_xlim(0, data.rowPoints)
#    ax1.set_ylim(0, data.colPoints)
#    ax1.imshow(ticLayer, aspect = 'auto')

#    tic /= tic.max()
#    tic *=100
##    bpc /= bpc.max()
##    bpc *=100
#    eic /= eic.max()
#    eic *=100


#    gc2x = N.arange(1,len(eic), data.colPoints)
#    gc2y = eic[::data.colPoints]
#
#    ax2.plot(bpc)
#    N.savetxt("TICSam.txt", eic, delimiter = ',')
#    ax2.plot(gc2x, gc2y, 'or', alpha = 0.6)
#    ax2.plot(bpc, 'r')


#    x = N.arange(0, 20)
#    y = N.sin(x)
#    ax1.plot(x, y)
#    w.canvas.fig.colorbar(ax1)
    w.show()
    sys.exit(app.exec_())


    ###########
    ############################################################
#
#class EICThread(QtCore.QThread):
#    def __init__(self, fileName, main, parent = None):
#        QtCore.QThread.__init__(self, parent)
#
#        self.parent = main
#        self.finished = False
#        self.stopped = False
#        self.mutex = QtCore.QMutex()
#        self.fileName = fileName
#        self.handle = None
#        self.fileOpen = False
#
#        self.ready = False
#
#        self.eicOK = False
#        self.EIC = None
#        self.mzVals = None
#
#
#
#    def initEICVals(self, mzList):
#        '''
#        Accepts a list of mzValues to get an EIC for
#        '''
#        if type(mzList) is list and len(mzList)>0:
#            self.mzVals = mzList
#            self.ready = True
#
#
#    def getHandle(self):
#        self.handle = T.openFile(self.fileName, 'r')
#        self.fileOpen = True
#
#    def closeHandle(self):
#        self.handle.close()
#        self.fileOpen = False
#
#    def setEIC(self):
#        self.getHandle()
#        if self.fileOpen and len(self.mzVals)>0:
#            mzCube = self.handle.root.dataCube
#
#            rows = mzCube.shape[0]
#            eic = N.zeros(rows)
#
#            for mz in self.mzVals:
#                eic +=mzCube[:,mz]
#
#            self.EIC = eic
#            self.closeHandle()
#            return True
#        else:
#            print "Error opening HDF5 data file"
#            return False
#
#    def run(self):
#        if self.ready:
#            self.finished = False
#            self.eicOK = self.setEIC()
#            self.emit(QtCore.SIGNAL("finished(bool)"),self.eicOK)
#            self.finished = True
#            self.ready = False
#            self.parent.updateEIC(self.eicOK)
#        else:
#            print "No mz value list set, run initEICVals(mzList)"
#
#    def getEIC(self):
#        if self.eicOK:
#            return self.EIC
#
#    def stop(self):
#        print "stop try"
#        try:
#            self.mutex.lock()
#            self.stopped = True
#        finally:
#            self.mutex.unlock()
#
#    def isStopped(self):
#        print "stop try"
#        try:
#            self.mutex.lock()
#            return self.stopped
#        finally:
#            self.mutex.unlock()