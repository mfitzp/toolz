
import sys
import os

from PyQt4.QtGui import QFileDialog,  QApplication
from PyQt4 import QtCore,  QtGui
import numpy as N
import scipy as S

import time

from scipy import ndimage#used for tophat filter

import PeakFunctions as PF


class PeakFindThread(QtCore.QThread):
    def __init__(self, main=None, parent = None):
        QtCore.QThread.__init__(self, parent)

        if main != None:
            self.parent = main
        else:
            self.parent = None
        self.finished = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.spectrum = None


        self.peakFindOK = False
        self.peakInfo = None

        self.peakWidth = None
        self.minSNR = None
        self.slopeThresh = None
        self.ampThresh = None
        self.smthKern = None
        self.fitWidth = None
        self.peakWin = None

        self.numSegs = None

        self.ready = False


    def getPeakInfo(self):
        if self.peakFindOK:
            return self.peakInfo
        else:
            print "No PeakInfo exists--run peakFind again otherwise an error occured that did not commit the PeakInfo array to memory!"
            return None

    def findMinima(self, seg, pad, threshFactor = 2):
        '''
        seg - segment to search in
        pad - range in which a match can be found in common
        threshFactor - value by which the stdev will be multiplied by
            e.g. a threshFactor of 3 would be 3X the standard deviation

        returns start and stop (common values of local minima)
        '''
        thresh = seg.mean() + seg.std()*threshFactor
        Min = N.where(seg>thresh,seg,0)#if the element is above thresh set to 0
#        print "Min", Min
        startSeg = Min[0:pad]
        endSeg = Min[-pad:]
        startLows = N.where(startSeg == 0)[0]
#        print "StartLows",startLows
        if len(startLows)>0:
            start = startLows[0]
        else:
            start = 0
            print "no start minima found..."

        endLows = N.where(endSeg == 0)[0]
#        print "Endlows", endLows
        if len(endLows)>0:
            stop = endLows[-1]
        else:
            stop = 0
            print "no stop minima found..."
        #we are adding one to stop because the indexing is from zero and pad is from 1
#        print start, stop
        return start, stop+1

    def SplitNFind(self, spec2Pick, numSegs, pWidth = 25, minSNR = 3):
        segLen = int(N.floor(len(spec2Pick)/numSegs))
        ovrLen = int(N.ceil(segLen)*0.1)#10% overlap
        alignSpec = N.zeros(len(spec2Pick))

        stopLoc = []
        oddPnts = []
        minima = N.zeros(len(spec2Pick))
        peakLoc=[]
        peakInt=[]
        peakWidth = []
        peakArea = []


        for i in xrange(numSegs):
            if i == 0:
                start = segLen*i
                stop = segLen*(i+1)+ovrLen
            elif i == (numSegs-1):
                start = segLen*i-ovrLen
                stop = segLen*(i+1)
            else:
                start = segLen*i-ovrLen
                stop = segLen*(i+1)+ovrLen

            tempSeg = spec2Pick[start:stop]

            optStart, optStop = self.findMinima(tempSeg, ovrLen)

            if optStart != 0 or (optStop-ovrLen) != 0:
                oddPnts.append((optStop-ovrLen)+stop)
    #            print optStart, optStop-ovrLen

            optStart+=start
            optStop =(optStop-ovrLen)+stop

            tempSeg = spec2Pick[optStart:optStop]
            if len(tempSeg) > 0:
                peakInfo = PF.findPeaks(tempSeg, peakWidth = pWidth, minSNR = minSNR,\
                                        slopeThresh = self.slopeThresh, ampThresh = self.ampThresh,\
                                        smthKern = self.smthKern, fitWidth = self.fitWidth
                                        )
                if len(peakInfo['peak_location']) > 0:
                    tempLoc = peakInfo['peak_location']
                    tempInt = peakInfo['peak_intensity']
                    tempWidth = peakInfo['peak_width']
                    tempArea = peakInfo['peak_area']
                    for loc in tempLoc:
                        peakLoc.append(loc+optStart)
                    for yVal in tempInt:
                        peakInt.append(yVal)
                    for width in tempWidth:
                        peakWidth.append(width)
                    for area in tempArea:
                        peakArea.append(area)
        #            if len(peakInfo['peak_location']) == 1:
        #                peakLoc.append(tempLoc[0])
        #                peakInt.append(tempInt[0])
        #            else:
        #                for loc, yVal in tempLoc, tempInt:
        #                    peakLoc.append(loc)
        #                    peakInt.append(yVal)

                #store segment locations--used for debugging
                stopLoc.append(stop)
                self.emit(QtCore.SIGNAL("progress(int)"), i)
            else:
                print optStart, optStop, start, stop

        peakDict = {'peakLoc':N.array(peakLoc),
                    'peakInt':N.array(peakInt),
                    'peakWidth':N.array(peakWidth),
                    'peakArea':N.array(peakArea)
                    }
        return peakDict#, minima

    def initSpectrum(self, spec, numSegs, minSNR = 3, slopeThresh = None, \
                     smthKern = 15, fitWidth = None, peakWidth = None, ampThresh = None,):
            '''
            Accepts a numpy spectrum containing gaussian like peaks...
            '''
            if len(spec)>0:
                self.spectrum = spec
                self.minSNR = minSNR
                self.slopeThresh = slopeThresh
                self.ampThresh = ampThresh
                self.smthKern = smthKern
                self.fitWidth = fitWidth
                self.peakWidth = peakWidth
                self.numSegs = numSegs

                self.ready = True



    def run(self):
        self.finished = False
        if self.ready:
            t1 = time.clock()
            self.peakInfo = self.SplitNFind(self.spectrum, self.numSegs, self.peakWidth, self.minSNR)
            self.peakFindOK = True
            print "Peak Find Time: ", time.clock()-t1
            self.emit(QtCore.SIGNAL("finished(bool)"),self.peakFindOK)
        else:
            print "Error finding peaks..."


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



def getHDFColumns(filename):#HDF5 filename
    if os.path.isfile(filename):
        loadedVars = []
        hdf = T.openFile(filename, mode = "r")
        r = hdf.root
        for node in r._f_iterNodes():
            loadedVars.append((node._v_hdf5name,  node.read()))
        hdf.close()
        return dict(loadedVars)

def make2DTIC(TIC,  colPoints):
    rowPoints = int(len(TIC)/colPoints)
    ticLayer = N.empty((rowPoints, colPoints), dtype = int)#  self.colPoints),  dtype=int)
    print ticLayer.shape
    x = 0
    for i in xrange(len(TIC)):
        y=i%colPoints
        ticLayer[x][y] = TIC[i]
        if i !=0 and (i%colPoints) == 0:
            x+=1

    return ticLayer




def testFunc(masterSpec, spec2Pick, numSegs):
    segLen = int(N.floor(len(spec2Pick)/numSegs))
    ovrLen = int(N.ceil(segLen)*0.1)
    alignSpec = N.zeros(len(spec2Pick))

    masterSpec = normArray(masterSpec)
    spec2Pick = normArray(spec2Pick)

    start = segLen*20-ovrLen
    stop = segLen*(20+1)+ovrLen

    print start, stop

    tempSeg = spec2Pick[start:stop]
    refSeg = masterSpec[start:stop]

    start2, stop2, rMin, sMin= findCommonMinima(refSeg, tempSeg, ovrLen)

    print start2, stop2

    return refSeg, tempSeg, rMin, sMin




def normArray(arr2Norm):
    arr2Norm.dtype = N.float32
    arr2Norm /= arr2Norm.max()
    arr2Norm *= 100
    return arr2Norm

def topHat(data, factor):
    '''
    data -- numpy array
    pntFactor determines how finely the filter is applied to data.
    A smaller number is faster but a trade-off is imposed
    '''
    pntFactor = factor
    struct_pts = int(round(data.size*pntFactor))
    str_el = N.repeat([1], struct_pts)
    tFil = ndimage.white_tophat(data, None, str_el)

    return tFil
#

if __name__ == "__main__":
    import pylab as P
    from pylab import cm
    cmaps = [cm.spectral,  cm.hot,  cm.spectral]
#    dataDict = getHDFColumns('Alignment.h5')
#    refSpec = dataDict.get('Acetone_Klean.h5')
#    testSpec = dataDict.get('')

    refSpec = P.load('TICRef.txt')
#    testSpec = P.load('TICSam.txt')
#    refSpec = refSpec[100000:110000]
    numSegs = 500
    SNR = 2
    fig = P.figure()
    ax = fig.add_subplot(111,  title = 'Picked')

#    peakLoc, peakInt, peakWidth = SplitNFind(refSpec, numSegs, 25, minSNR = SNR)
    peakThread = PeakFindThread()
    peakThread.initSpectrum(refSpec, minSNR = 3, numSegs = 500, smthKern = 15, peakWidth = 25)
    peakThread.start()
    time.sleep(13)
    peakInfo = peakThread.getPeakInfo()
    ax.plot(refSpec)
    ax.plot(peakInfo['peakLoc'],peakInfo['peakInt'], 'ro', alpha = 0.4)

#    ax2 = fig.add_subplot(212,  title = 'Histo')
#    ax2.hist(peakInt, log = True, bins = 1000)

    P.show()


###################################################

#    ax = fig.add_subplot(111,  title = 'Unaligned')
#    j = 5000
#    for i in range(20):
#        a = refSpec[65000+j*i:69000+j*i]
#        peakInfo = PF.findPeaks(a, peakWidth = 15)
#        ax.plot(a)
#
#        if len(peakInfo) > 0:
#            ax.plot(peakInfo['peak_location'],  peakInfo['peak_intensity'],  'ro')
#            #ax.plot(peakInfo['smoothed_deriv'])
#            #ax.plot(peakInfo['smoothed_data'])
#            #print peakInfo
#
#
#    P.show()



##########################################

#    columns = 1200
#
#
#    i = 0
#    for item in dataDict.iteritems():
#        print item[0]
#        tic1D = item[1]#(item[1]/item[1].max())*100
#        TIC = make2DTIC(tic1D, columns)
#        rows = int(len(tic1D)/columns)
#        imAspect = rows/(columns*1.0)
#        print imAspect
#        if '_AL' not in item[0]:
#            #ax.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower', aspect = imAspect, cmap = cmaps[i])
#            ax.contour(N.transpose(TIC), alpha = 1,  origin = 'lower',  cmap = cmaps[i])
#
#        else:
#            #ax2.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower',  aspect = imAspect,   cmap = cmaps[i])
#            ax2.contour(N.transpose(TIC), alpha = 1,  origin = 'lower',  cmap = cmaps[i])
#
#        i+=0
    #ax.set_xlim(0,rows)
    #ax.set_ylim(0,columns)
    #ax2.set_ylim([0,columns])
    #P.show()


