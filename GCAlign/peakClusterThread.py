#!/usr/bin/env python

from PyQt4 import QtCore,  QtGui

import numpy as N

from mpl_pyqt4_widget import MPL_Widget
import hcluster_bhc as H

distTypeDist = {'Euclidean':'euclidean',
                'Normalized Euclidean':'seuclidean',
                'Chebyshev':'chebyshev',
                'Mahalanobis':'mahalanobis',
                'Squared Euclidean':'sqeuclidean',
                'Correlation':'correlation',
                'Minkowski':'minkowski',
                'Hamming':'hamming',
                'Cosine':'cosine',
                'Manhattan':'cityblock',
                'Canberra':'canberra',
                'Bray-Curtis':'braycurtis'
                }

clusterType = {'Single':'single',
               'Complete':'complete',
               'Average':'average',
               'Weighted':'weighted',
               }
#               'Centroid':'centroid',
#               'Median':'median',
#               'Ward':'ward'
#               }


def clusterPeaks(self):
    if self.showDendroCB.isChecked():
        if self.peakInfo != None:
            self.peakLoc2D = self.get2DPeakLoc(self.peakInfo['peakLoc'], self.curData.rowPoints,\
                                               self.curData.colPoints, peakIntensity = self.peakInfo['peakInt'])
            X = N.column_stack((self.peakLoc2D[0], self.peakLoc2D[1]))
            X = N.column_stack((X, N.sqrt(self.peakLoc2D[2])))
#                if self.peakLoc2D != None:
#                    X = self.peakLoc2D[0]
#                    for i in xrange(1, len(self.peakLoc2D)):
#                        X = N.column_stack((X,self.peakLoc2D[i]))
            self.linkagePlot = MPL_Widget()
            self.linkagePlot.setWindowTitle(('Clustered Peaks for %s'%self.curData.name))
            Y = H.pdist(X)
            Z = H.linkage(Y)

            self.linkagePlot.canvas.setupSub(2)
            ax1 = self.linkagePlot.canvas.axDict['ax1']
            ax2 = self.linkagePlot.canvas.axDict['ax2']
            H.dendrogram(Z, colorthreshold=10, customMPL = ax1)
            R = H.inconsistent(Z, d = 4)
            print R.shape
            ax2.plot(R[:,0])
            ax2a = ax2.twinx()
            ax2a.plot(R[:,3], 'r:')
            self.linkagePlot.show()


class PeakClusterThread(QtCore.QThread):
    def __init__(self, main = None, parent = None):
        QtCore.QThread.__init__(self, parent)

        if main != None:
            self.parent = main
        else:
            self.parent = None

        self.finished = False
        self.stopped = False
        self.mutex = QtCore.QMutex()

        self.peakInfo = None
        self.array2Cluster = None #usually will be the peakLoc2D

        self.distMethod = None
        self.clusterType = None

        self.distMatrix = None
        self.linkageResult = None

        self.peakCentroids = None
        self.flatCluster = None
        self.distThresh = None

        self.inconsistencies = None
        self.threshType = None
        self.maxDist = None
        self.maxIncon = None

        self.linkagePlot = None
        self.plotLinkage = False
        self.linkPlotOn = False

        self.linkageOK = False

        self.ready = False

    def initClusterThread(self, varMtx, distMethod = 'euclidean', threshType = 'inconsistent',\
                          distThresh = 10, clusterType = 'single', plotLinkage = True, name = None):
            '''
            Accepts a list of mzValues to get an EIC for
            '''
            self.distMethod = distMethod
            self.clusterType = clusterType
            self.plotLinkage = plotLinkage
            self.distThresh = distThresh
            self.threshType = threshType
            if name != None:
                self.name = name
            else:
                self.name = 'Data'
            if type(varMtx) is N.ndarray:
                self.array2Cluster = varMtx
                self.ready = True

    def getOptimumIncThresh(self, MI, MD):
        histMI = N.histogram(MI, bins = len(MI)/10, new = True)
        histMD = N.histogram(MD, bins = len(MD)/10, new = True)
        self.tempMIHist = histMI
        self.tempMDHist = histMD

        for i in xrange(1,len(histMI[0])):

#
#            print "No optimum length found, setting default to %s",self.distThresh
#            self.maxDist = self.distThresh
#            break
#                return self.distThresh
#                break

            histMaxMI = histMI[0][i:].argmax()+1 #the addition of one is because of the way the bins are constructed, the x,y
                                             #tuple of the histogram do not have the same lengths
            self.maxIncon = histMI[1][histMaxMI]
            distInd = N.where(MI<=self.maxIncon)
            self.maxDist = MD[distInd].max()#[histMaxMI]
            print i, self.maxIncon, self.maxDist
#            print self.maxIncon
#            self.maxDist = self.inconsistencies[:,0][histMaxMI]#this is the mean distances of the point in a given cluster
#            self.maxDist = histMD[1][histMaxMI]
            if self.maxDist >= 5:
                '''
                THIS IS KEY A MINIMUM OF 5 IS USED FOR THE DISTANCE BE AWARE!!!!!!
                is there a smarter way to do this?
                '''
#                print "Optimum Distance found at: %s", self.maxDist
#                break
                return self.maxDist
#            print i, self.maxDist
            i = histMaxMI


    def run(self):
        self.finished = False
        self.maxDist = None
        self.maxIncon = None

        self.distMatrix = H.pdist(self.array2Cluster, self.distMethod)
        print "Distance Type Used = %s"%self.distMethod
        self.emit(QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"),'Distance Matrix Calculated')
        self.linkageResult = H.linkage(self.distMatrix, self.clusterType)
        self.emit(QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"),'Linkage Calculated')
        if self.threshType == 'inconsistent':
            print "Cluster Thresh Inconsistencies Used"
            self.inconsistencies = H.inconsistent(self.linkageResult, d = 10)#drill down a maximum of 10 nodes
    #        iCoef = self.inconsistencies[:,3]#the third column is the actual inconsistency coefficients
            MI = H.maxinconsts(self.linkageResult, self.inconsistencies)
            MD = H.maxdists(self.linkageResult)
#            print "length of MaxInc", len(MI)
            self.getOptimumIncThresh(MI, MD)

#            histMI = N.histogram(MI, bins = len(MI)/10, new = True)
#            self.tempHist = histMI
#            histMaxMI = histMI[0][1:].argmax()+1 #the addition of one is because of the way the bins are constructed, the x,y
#                                                 #tuple of the histogram do not have the same lengths
#            self.maxIncon = histMI[1][histMaxMI]
#            print self.maxIncon
#            self.maxDist = self.inconsistencies[:,0][histMaxMI]#this is the mean distances of the point in a given cluster
            self.emit(QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"),'Tree Inconsistencies Calculated')
#            self.flatCluster = H.fclusterdata(self.array2Cluster, criterion = 'inconsistent', t = self.maxIncon)
            self.flatCluster = H.fclusterdata(self.array2Cluster, criterion = 'distance', t = self.maxDist)
        elif self.threshType == 'distance':
            print "Cluster Tree Distances Used"
            self.maxDist = self.distThresh
            self.flatCluster = H.fclusterdata(self.array2Cluster, criterion = 'distance', t = self.distThresh)
        self.emit(QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"),'Flat Cluster Calculated')
        self.peakCentroids = []
        for i in xrange(0, self.flatCluster.max()+1):
            tempClust = self.array2Cluster[self.flatCluster==i,:]
            self.peakCentroids.append(tempClust.mean(axis = 0))
#            if temp.shape[0] != 0:
#                x += temp.shape[0]
#                print temp.shape, temp.mean(axis = 0), i, x
        self.peakCentroids = N.array(self.peakCentroids)
        self.linkageOK = True
        self.emit(QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"),'Clustering Finished')
        self.emit(QtCore.SIGNAL("finished(bool)"),self.linkageOK)

#        if self.plotLinkage:
#            self.linkagePlot = MPL_Widget()
#            self.linkagePlot.setWindowTitle(('Clustered Peaks for %s'%self.name))
#            self.linkagePlot.canvas.setupSub(2)
#            ax1 = self.linkagePlot.canvas.axDict['ax1']
#            ax2 = self.linkagePlot.canvas.axDict['ax2']
#            H.dendrogram(self.linkageResult, colorthreshold=10, customMPL = ax1)
#            self.emit(QtCore.SIGNAL("clusterThreadUpdate(PyQt_PyObject)"),'Linkage Plot Initiated')
#            R = H.inconsistent(self.linkageResult, d = 4)
#            ax2.plot(R[:,0])
#            ax2a = ax2.twinx()
#            ax2a.plot(R[:,3], 'r:')
#            self.linkagePlot.show()
#            self.linkPlotOn = True

        self.finished = True

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

#if __name__ == "__main__":
#    import sys
#    import pylab as P
#    import matplotlib.colors as C
#    from mpl_pyqt4_widget import MPL_Widget
#    import time
#    app = QtGui.QApplication(sys.argv)
#
#    file = 'TICRef.txt'
#    file2 = 'TICSam.txt'
#    ticRef = P.load(file)#this loads them as float64 so normalization is not needed
#    ticSam = P.load(file2)
#
##    ticRef+=100
##    ticRef = ticRef[30000:40000]
##    ticSam = ticSam[30000:40000]
#    aligned, stopLoc, oddPnts, peakLoc, peakInt = SNS.SplitNStitch(ticRef, ticSam,  500)
#
#    print len(ticRef), ticRef.dtype
#    #print len(ticSam), ticSam.dtype
#
#    w = MPL_Widget()
#    w.canvas.setupSub(2)
#    ax1 = w.canvas.axDict['ax1']
#    ax2 = w.canvas.axDict['ax2']
#    ax1.plot(ticRef)
#    ax1.plot(peakLoc, peakInt, 'ro', alpha = 0.5)
#
#    ticLayer = make2DLayer(ticRef, 500)
#
#    cdict ={
#    'blue': ((0.0, 0.01, 0.01), (0.01, 0.25, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
#    'green': ((0.0, 0, 0), (0.05, 0.75, 0.75), (0.25, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
#    'red': ((0.0, 0, 0), (0.15, 0.25, 0.25), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
#    }
#
#    my_cmap = C.LinearSegmentedColormap('mycmap', cdict, 512)
#    ax2.imshow(N.transpose(ticLayer), origin = 'lower', aspect = 'auto', cmap = my_cmap)
#
#    x,y = get2DPeakLoc(peakLoc, 555, 500)
#    ax2.plot(x,y,'yo', ms = 4, alpha = 0.5, picker = 5)
#    N.savetxt('PeakLoc.txt',N.column_stack((x,y)),fmt = '%.2f', delimiter = ',')
##    canvas.mpl_connect('pick_event', showCoord)
#
#    #ax1.plot(ticSam[0:50000], 'r:')
#    #ax2.plot(aligned)
#    #ax2.plot(ticSam)
#    #y = N.ones(len(stopLoc))*N.mean(aligned)
#    #y1 = N.ones(len(oddPnts))*N.mean(aligned)
#    #ax2.plot(stopLoc, y, 'go')
#    #ax2.plot(oddPnts, y1, 'ro')
#
#    w.show()
#    sys.exit(app.exec_())