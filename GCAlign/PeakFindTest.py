#!/usr/bin/env python

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T
import SplitNStich as SNS

distTypeDist = {'Euclidiean':'euclidean',
                'Normalized Euclidiean':'seuclidean',
                'Chebyshev':'chebyshev',
                'Mahalanobis':'mahalanobis',
                'Squared Euclidiean':'sqeuclidean',
                'Correlation':'correlation',
                'Minkowski':'minkowski',
                'Hamming':'hamming',
                'Cosine':'cosine',
                'Manhattan':'cityblock',
                'Canberra':'canberra',
                'Bray-Curtis':'braycurtis'
                }

clusterType = {'Linkage':'linkage',
               'Single':'single',
               'Complete':'complete',
               'Average':'average',
               'Weighted':'weighted',
               'Centroid':'centroid',
               'Median':'median',
               'Ward':'ward'
               }


class PeakClusterThread(QtCore.QThread):
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

def get2DPeakLoc(peakLoc, rows, cols):
    x = N.empty(len(peakLoc), dtype = int)
    y = N.empty(len(peakLoc), dtype = int)
    for i,loc in enumerate(peakLoc):
        x[i] = int(loc/cols)
        y[i] = loc%cols

    return x,y



def make2DLayer(cgram, colPoints):
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

    return cLayer

#def showCoord(event):


if __name__ == "__main__":
    import sys
    import pylab as P
    import matplotlib.colors as C
    from mpl_pyqt4_widget import MPL_Widget
    from dbscan import dbscan
    import time
    app = QtGui.QApplication(sys.argv)

    file = 'TICRef.txt'
    file2 = 'TICSam.txt'
    ticRef = P.load(file)#this loads them as float64 so normalization is not needed
    ticSam = P.load(file2)

#    ticRef+=100
#    ticRef = ticRef[30000:40000]
#    ticSam = ticSam[30000:40000]
    aligned, stopLoc, oddPnts, peakLoc, peakInt = SNS.SplitNStitch(ticRef, ticSam,  500)

    print len(ticRef), ticRef.dtype
    #print len(ticSam), ticSam.dtype

    w = MPL_Widget()
    w.canvas.setupSub(2)
    ax1 = w.canvas.axDict['ax1']
    ax2 = w.canvas.axDict['ax2']
    ax1.plot(ticRef)
    ax1.plot(peakLoc, peakInt, 'ro', alpha = 0.5)

    ticLayer = make2DLayer(ticRef, 500)

    cdict ={
    'blue': ((0.0, 0.01, 0.01), (0.01, 0.25, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
    'green': ((0.0, 0, 0), (0.05, 0.75, 0.75), (0.25, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
    'red': ((0.0, 0, 0), (0.15, 0.25, 0.25), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
    }

    my_cmap = C.LinearSegmentedColormap('mycmap', cdict, 512)
    ax2.imshow(N.transpose(ticLayer), origin = 'lower', aspect = 'auto', cmap = my_cmap)

    x,y = get2DPeakLoc(peakLoc, 555, 500)
    ax2.plot(x,y,'yo', ms = 4, alpha = 0.5, picker = 5)
    xy = N.column_stack((x,y))
#    N.savetxt('PeakLoc.txt',xy,fmt = '%.2f', delimiter = ',')

    cClass, tType, Eps, boolAns = dbscan(xy, 1)
    print cClass.max(), len(tType)
    i = cClass.max()
    for m in xrange(int(i)):
        ind = N.where(m == cClass)
        temp = xy[ind]
        ax2.plot(temp[:,0],temp[:,1],'s', alpha = 0.7, ms = 3)

#    canvas.mpl_connect('pick_event', showCoord)

    #ax1.plot(ticSam[0:50000], 'r:')
    #ax2.plot(aligned)
    #ax2.plot(ticSam)
    #y = N.ones(len(stopLoc))*N.mean(aligned)
    #y1 = N.ones(len(oddPnts))*N.mean(aligned)
    #ax2.plot(stopLoc, y, 'go')
    #ax2.plot(oddPnts, y1, 'ro')

    w.show()
    sys.exit(app.exec_())