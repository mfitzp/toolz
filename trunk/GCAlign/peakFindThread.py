
import sys
import os
import os.path

from PyQt4.QtGui import QFileDialog,  QApplication
import numpy as N
import scipy as S

import time

#puRE pyTHON neTCDF reADER
from pupynere import NetCDFFile as CDF
#pytables
import tables as T

from scipy import ndimage#used for tophat filter

import PeakFunctions as PF

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


def findMinima(seg, pad, threshFactor = 2):
    '''
    seg - segment to search in
    pad - range in which a match can be found in common
    threshFactor - value by which the stdev will be multiplied by
        e.g. a threshFactor of 3 would be 3X the standard deviation

    returns start and stop (common values of local minima)
    '''
    thresh = seg.mean() + seg.std()*threshFactor
    Min = N.select([seg>thresh],[seg],default = 0)#if the element is above thresh set to 0

    start = Min[0:pad][0]#increments by 0.5
    stop = Min[-pad:][-1]
    #we are adding one to stop because the indexing is from zero and pad is from 1
    return start, stop+1

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


def SplitNFind(spec2Pick, numSegs, pWidth = 25, minSNR = 3):
    segLen = int(N.floor(len(spec2Pick)/numSegs))
    ovrLen = int(N.ceil(segLen)*0.1)#10% overlap
    alignSpec = N.zeros(len(spec2Pick))

    stopLoc = []
    oddPnts = []
    minima = N.zeros(len(spec2Pick))
    peakLoc=[]
    peakInt=[]
    peakWidth = []


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

        optStart, optStop = findMinima(tempSeg, ovrLen)

        if optStart != 0 or (optStop-ovrLen) != 0:
            oddPnts.append((optStop-ovrLen)+stop)
#            print optStart, optStop-ovrLen

        optStart+=start
        optStop =(optStop-ovrLen)+stop

        tempSeg = spec2Pick[optStart:optStop]

        peakInfo = PF.findPeaks(tempSeg, peakWidth = pWidth, minSNR = minSNR)
        if len(peakInfo['peak_location']) > 0:
            tempLoc = peakInfo['peak_location']
            tempInt = peakInfo['peak_intensity']
            tempWidth = peakInfo['peak_width']
            for loc in tempLoc:
                peakLoc.append(loc+optStart)
            for yVal in tempInt:
                peakInt.append(yVal)
            for width in tempWidth:
                peakWidth.append(width)
#            if len(peakInfo['peak_location']) == 1:
#                peakLoc.append(tempLoc[0])
#                peakInt.append(tempInt[0])
#            else:
#                for loc, yVal in tempLoc, tempInt:
#                    peakLoc.append(loc)
#                    peakInt.append(yVal)

        #store segment locations--used for debugging
        stopLoc.append(stop)


    return N.array(peakLoc), N.array(peakInt), N.array(peakWidth)#, minima

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
    ax = fig.add_subplot(111,  title = 'Unaligned')

    peakLoc, peakInt, peakWidth = SplitNFind(refSpec, numSegs, 25, minSNR = SNR)
    ax.plot(refSpec)
    ax.plot(peakLoc, peakInt, 'ro', alpha = 0.4)

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


