
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


def findCommonMinima(segR, segS, pad, threshFactor = 2):
    '''
    segR - segment for the reference
    segS - segment for the sample
    pad - range in which a match can be found in common
    threshFactor - value by which the stdev will be multiplied by
        e.g. a threshFactor of 3 would be 3X the standard deviation

    returns start and stop (common values of local minima)
    '''
    threshR = segR.mean() + segR.std()*threshFactor
    threshS = segS.mean() + segS.std()*threshFactor
    rMin = N.select([segR>threshR],[segR],default = 0)#if the element is above thresh set to 0
    sMin = N.select([segS>threshS],[segS],default = 0)


    i=0
    while True:
        subPad = pad + pad*i/2
        startR = rMin[0:subPad]#increments by 0.5
        startS = sMin[0:subPad]
        comStart = N.where(startR == startS)
        if len(comStart[0])!=0:
            start = comStart[0][0]#take first match
            break

        if i == 3:
            start = 0
            print "No start match overlap found"
            break

        i+=1

    j=0
    while True:
        subPad = pad + pad*j/2
        endR = rMin[-subPad:]
        endS = sMin[-subPad:]
        comEnd = N.where(endR == endS)

        if len(comEnd[0])!=0:
            stop = comEnd[0][-1]#take last match because it is the end segment
            break

        if j == 3:
            stop = 0
            print "No stop match overlap found"
            break
        j+=1

    #we are adding one to stop because the indexing is from zero and pad is from 1
    return start, stop+1

def testFunc(masterSpec, spec2Align, numSegs):
    segLen = int(N.floor(len(spec2Align)/numSegs))
    ovrLen = int(N.ceil(segLen)*0.1)
    alignSpec = N.zeros(len(spec2Align))

    masterSpec = normArray(masterSpec)
    spec2Align = normArray(spec2Align)

    start = segLen*20-ovrLen
    stop = segLen*(20+1)+ovrLen

    print start, stop

    tempSeg = spec2Align[start:stop]
    refSeg = masterSpec[start:stop]

    start2, stop2, rMin, sMin= findCommonMinima(refSeg, tempSeg, ovrLen)

    print start2, stop2

    return refSeg, tempSeg, rMin, sMin


def SplitNStitch(masterSpec,  spec2Align,  numSegs):
    segLen = int(N.floor(len(spec2Align)/numSegs))
    ovrLen = int(N.ceil(segLen)*0.1)
    alignSpec = N.zeros(len(spec2Align))

#    masterSpec = normArray(masterSpec)
#    spec2Align = normArray(spec2Align)

    stopLoc = []
    oddPnts = []
    minima = N.zeros(len(masterSpec))
    peakLoc=[]
    peakInt=[]


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

        refSeg = masterSpec[start:stop]
        tempSeg = spec2Align[start:stop]


        optStart, optStop = findCommonMinima(refSeg, tempSeg, ovrLen)

        if optStart != 0 or (optStop-ovrLen) != 0:
            oddPnts.append((optStop-ovrLen)+stop)
#            print optStart, optStop-ovrLen

        optStart+=start
        optStop =(optStop-ovrLen)+stop

        refSeg = masterSpec[optStart:optStop]
        tempSeg = spec2Align[optStart:optStop]

        cor = N.correlate(refSeg, tempSeg, mode = 'same')
        shift = int(cor.argmax()-len(tempSeg)/2)#gets value to shift by
        seg = N.roll(tempSeg, shift)

        alignSeg = N.roll(tempSeg, shift)
        alignSpec[optStart:optStop] = alignSeg

        peakInfo = PF.findPeaks(refSeg, peakWidth = 25)
        if len(peakInfo['peak_location']) > 0:
            tempLoc = peakInfo['peak_location']
            tempInt = peakInfo['peak_intensity']
            for loc in tempLoc:
                peakLoc.append(loc+optStart)
            for yVal in tempInt:
                peakInt.append(yVal)
#            if len(peakInfo['peak_location']) == 1:
#                peakLoc.append(tempLoc[0])
#                peakInt.append(tempInt[0])
#            else:
#                for loc, yVal in tempLoc, tempInt:
#                    peakLoc.append(loc)
#                    peakInt.append(yVal)

        #store segment locations--used for debugging
        stopLoc.append(stop)


    return alignSpec, stopLoc, oddPnts, N.array(peakLoc), N.array(peakInt)#, minima

def normArray(arr2Norm):
    arr2Norm.dtype = N.float32
    arr2Norm /= arr2Norm.max()
    arr2Norm *= 100
    return arr2Norm

def xcorr(x, y):
    xlen = len(x)
    corX = x.copy()#N.zeros(xlen)
    corY = y.copy()
    m=0
    for i in xrange(xlen):
        roll = N.roll(corY, i)
        corX += roll*corX
    return corX

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
    testSpec = P.load('TICSam.txt')
    fig = P.figure()
    ax = fig.add_subplot(311,  title = 'Unaligned')
    ax2 = fig.add_subplot(312,  sharex = ax)
    ax3 = fig.add_subplot(313,  sharex = ax, sharey = ax2)

    print len(refSpec)
    ax.plot(refSpec)
    ax2.plot(testSpec)


#    aligned, stopLoc, oddPnts = SplitNStitch(refSpec,  testSpec,  500)
#    y = N.ones(len(stopLoc))*N.mean(aligned)
#    y1 = N.ones(len(oddPnts))*N.mean(aligned)
#    ax.plot(refSpec)
#    ax.plot(aligned)
#    ax2.plot(testSpec, 'r')
##    ax3.plot(minima, 'g')
#    ax3.plot(stopLoc, y, 'go')
#    ax3.plot(oddPnts, y1, 'ro')
#    ax3.plot(aligned)

#    fig = P.figure()
#    ax = fig.add_subplot(211)
#    ax2 = fig.add_subplot(212)
#    R, S, rMin, sMin = testFunc(refSpec,  testSpec,  312)
#    ax.plot(R)
#    ax.plot(rMin)
#    ax2.plot(S)
#    ax2.plot(sMin)


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


