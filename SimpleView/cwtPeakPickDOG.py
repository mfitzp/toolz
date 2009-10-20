'''
Questions weather to normalize or not when comparing?
Need to cluster peaks
'''

import sys,traceback

import pylab as P
import numpy as N

import pycwt as W

from interpolate import interpolate_spectrum

from scipy import ndimage#used for tophat filter
import time
import getBaseline as GB
from dbscan import dbscan

import supportFunc as SF

from mpl_image_widget import MPL_Widget as MPL_CWT

def cwtMS(Y, scales, sampleScale = 1.0, wlet = 'MexHat', maxClip = 1000., staticThresh = None):
    '''
    Y is the INTERPOLATED intensity array from a mass spectrum.
    interpolation IS necessary especially for TOF data as the m/z domain is non-linear.
    Static Thresh is to screen out the noise and is optional.  This is done for two reasons
    1: for speed
    2: so the algorithm doesn't try to pick peaks that are statistically meaningless from a MS perspective

    staticThresh needs to be modified if the data is normalized or not
    '''
    try:
        if staticThresh != None:

            yIndex = N.where(Y>=staticThresh)[0]#find elements below static thresh
            yMod = 0.02*len(Y)#this is the modification to the length to be sure that any peaks at the edge are included
            yMax = yIndex[-1]
            if len(Y)<(yMax+yMod):
                yMod = 0
            print "Y Index Max", yMax+yMod
            ans = W.cwt_a(SF.roundLen(Y[0:(yMax+yMod)]), scales, sampling_scale = sampleScale, wavelet = wlet)
        else:
            ans = W.cwt_a(Y, scales, sampling_scale = sampleScale)#, wavelet = wlet)

        return ans.real
    except:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    print 'Error saving figure data'
        errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
        print errorMsg
        return None


def plotCWTPeaks(parent, massSpecX, massSpecY, cwtMTX, peakLoc, peakInt, cwtPeakLoc, peakClass):
    w = MPL_CWT()
    w.canvas.setupSub(2)
    ax1 = w.canvas.axDict['ax1']
    ax2 = w.canvas.axDict['ax2']

    ax1.plot(massSpecX, SF.normalize(massSpecY), 'g',alpha = 0.7, label = 'ms')
    intMax = cwtMTX.max(axis=0).max()*0.05
    im=ax2.imshow(cwtMTX,vmax = intMax, cmap=P.cm.jet,aspect='auto')
    ax2.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'oy', ms = 3, alpha = 0.4)
    if peakClass != None:
        i = peakClass.max()
        for m in xrange(int(i)+1):
            ind = N.where(m == peakClass)
            temp = cwtPeakLoc[ind]
            ax2.plot(temp[:,0],temp[:,1],'-s', alpha = 0.7, ms = 3)
        if len(peakLoc) != 0:
            ax1.vlines(peakLoc, 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)

    parent.appendMPLPlot(w)


def getCWTPeaks(scaledCWT, X, Y, noiseEst, minSNR = 3,\
                minRow = 3, rowThresh = 4,\
                pntPad = 50, staticThresh = 0.1, minNoiseEst = 0.025,
                EPS = None, debug = False, tempAxis = None):
    '''
    returns: N.array(peakLoc), cwtPeakLoc, cClass, boolean

    pntPad is the number of points (interpolated) that spans 0.5 m/z units
    staticCut is the lower threshold limit--NOT USED

    scaledCWT is the continuous wavelet transform provided by cwtMS function
    minRow is the first row of the cwt to pick peaks from--if this is too small you'll get
    too many peaks and the algorithm will choke.  Keep in mind that the first few rows of
    the CWT are highly correlated with high frequency noise--you don't want them anyway.

    This version uses the "derivative of gaussian" wavelet or DOG.
    By searching through each wavelet scale you can get the zero crossings which translate
    into peak maxima in you real data.  By looking across difference frequencies you can
    get an idea which peaks are real and which ones only correlate with noise.

    Provides prospective peaks for future fitting
    '''
    if debug:
        print "Length X,Y ", len(X), len(Y)
        print "Noise Est: ", noiseEst
        print "minSNR: ", minSNR
        print "rowThresh: ", rowThresh
        print "pntPad: ", pntPad
        print "staticThresh: ", staticThresh
        print "minNoiseEst", minNoiseEst
        print "EPS: ", EPS
    cwtPeakLoc = []
    peakLoc = []
    peakInt = []
    rawPeakInd = []
    print "Shape: ",scaledCWT.shape
    revRowArray = N.arange((scaledCWT.shape[0]-1),1,-1)#steps backwards


    for i in revRowArray:
        row = scaledCWT[i]

        if i> minRow:
            row = SF.normalize(row)
            row *=-1
            if debug:
                if tempAxis != None:
                    tempAxis.plot(row, '-', alpha = 0.5)

            criterion = (row <= 5) & (row >= -5) & (Y[0:len(row)] >= noiseEst[0:len(row)])
            tempLocEst = N.where(criterion)[0]

            for m in tempLocEst[:-1]:#need to exclude last element so we don't get an IndexError for the derivative array
                if N.sign(row[m]) > N.sign(row[m+1]):
                #this screening assumes there is a low value to the first
                #scale value e.g. 1 or 2
                    if (m-pntPad) > 0:
                        xStart = m-pntPad
                    else:
                        xStart = 0

                    if (m+pntPad) < len(Y):
                        xStop = m+pntPad
                    else:
                        xStop = len(Y)


                    tempVals = Y[xStart:xStop]#BHC added 3/25/09
                    if len(tempVals)>0:
                        localMaxInd = tempVals.argmax()


                        yMaxInd = m-pntPad+localMaxInd

                        rawPeakInd.append(yMaxInd)

                        if Y[yMaxInd] >= noiseEst[xStart:xStop].mean()*minSNR:#minSNR/2:# and Y[yMaxInd] >= staticCut:

                            peakLoc.append(X[yMaxInd])
                            peakInt.append(Y[yMaxInd])
                            cwtPeakLoc.append([X[yMaxInd],i])



            t3 = time.clock()



    cwtPeakLoc = N.array(cwtPeakLoc)

    peakLoc = N.array(peakLoc)
    peakInt = N.array(peakInt)
    rawPeakInd = N.array(rawPeakInd)
    peakOrder = peakLoc.argsort()
    peakLoc = peakLoc[peakOrder]
    peakInt = peakInt[peakOrder]
    rawPeakInd = rawPeakInd[peakOrder]
    #peakLoc, peakInt, rawPeakInd = consolidatePeaks(peakLoc, peakInt, rawPeakInd)
    peakLoc, peakInt = removeDuplicatePeaks(peakLoc, peakInt)
    cClass = None



    return peakLoc, peakInt, rawPeakInd, cwtPeakLoc, cClass, True
    #return None, None, None, None, None, False

def removeDuplicatePeaks(peakLoc, peakInt):
    peakOrder = peakLoc.argsort()
    peakLoc = peakLoc[peakOrder]
    peakInt = peakInt[peakOrder]
    peakLocDiff = N.diff(peakLoc)
    duplicateInd = N.where(peakLocDiff == 0)[0]
    peakLoc = N.delete(peakLoc, duplicateInd)
    peakInt = N.delete(peakInt, duplicateInd)
    return peakLoc, peakInt

def consolidatePeaks(peakLoc, peakInt, rawPeakInd, diffCutoff = 1.25):
    '''
    Designed to find the monoisotopic peak
    This is a hack, not a good solution but it works for now

    '''
    #need to make the input vector 2D
    #remember for cClass, -1 is an outlier (i.e. a stand alone peak), and other numbers are the groups
    cClass, tType, Eps, boolAns = dbscan(N.column_stack((N.zeros_like(peakLoc),peakLoc)), 1, Eps = diffCutoff)
#    print peakLoc
#    print cClass
    print "Consolidate Bool", boolAns
    newPeakLoc = []
    newIntLoc = []
    newPointLoc = []
    if boolAns:
        singlePnts = N.where(cClass == -1)[0]
        for pnt in singlePnts:
            newPeakLoc.append(peakLoc[pnt])
            newIntLoc.append(peakInt[pnt])
            newPointLoc.append(rawPeakInd[pnt])

        if len(cClass)>0:
            if cClass.max() > 0:#otherwise there is just one outlier
                for i in xrange(1,int(cClass.max())+1):
                    tempInd = N.where(i == cClass)[0]
                    if len(tempInd)>0:
                        maxLoc = peakInt[tempInd].argmax()

                        newPeakLoc.append(peakLoc[maxLoc+tempInd[0]])
                        newIntLoc.append(peakInt[maxLoc+tempInd[0]])
                        newPointLoc.append(rawPeakInd[maxLoc+tempInd[0]])


        return newPeakLoc, newIntLoc, newPointLoc

    else:
        print "Error with Consolidation--using raw peaks"
        return peakLoc, peakInt, rawPeakInd




if __name__ == "__main__":

    import smoothingFilter as SmoothF
    import scipy.signal as signal
    import mzXML_reader as mzXML


    fn = 'Z:/data/Clowers/061008/HG_pt01_mg_mL_B12_1.mzXML'

    mzx = mzXML.mzXMLDoc(fn)
    spectrum = mzx.data.get('spectrum')


    t1 = time.clock()
    loadA = False
    normOk = True

    'Noisy_IMS_XY.csv'
    'BSA_XY_Full.csv'
    'J5.csv'
    'Tryptone.csv'
    dat = P.load('E4.csv', delimiter = ',')

    xArray = dat[:,0]
    yArray = dat[:,1]
    xArray, yArray = SF.interpolate_spectrum_XY(xArray, yArray)
    #xArray = N.arange(len(yArray))
    #xArray, yArray = signal.resample(yArray, len(xArray)/4, xArray)
    #xArray, yArray = SF.interpolate_spectrum_by_diff(xArray, yArray, xArray.min(), xArray.max(), 0.025)
    xDiffNew = xArray[1]-xArray[0]
    print "X Diff New: ", xDiffNew

    xArray = spectrum[0]
    yArray = spectrum[1]

    #xArray, yArray = SF.interpolate_spectrum_by_diff(xArray, yArray, xArray.min(), xArray.max(), 0.01)

    if normOk:
        yArray = SF.normalize(yArray)
    abundMax = yArray.max()
    #print len(yArray)
    #print "Y Max", abundMax
    #yArray = SF.normalize(SF.topHat(yArray, 0.01))
    yArray = SF.roundLen(yArray)
    start = 0#100000#0
    stop = int(len(yArray)*1)##79000#len(ms)*.75
    #start = 48000
    #stop = 58000
    #yArray = yArray[start:stop]
    #xArray = xArray[start:stop]
    numSegs = int(len(xArray)*(xArray[1]-xArray[0]))
    print "Length of ms, numSegs: ", len(yArray), numSegs
    xArray = N.arange(len(yArray))

    print len(yArray)

    #s = N.arange(2,32,2)#changed to 8 from 32
    #s1 = N.arange(2,64,8)
    #s2 = N.arange(32,64,8)
    s3 = N.array([1,2,4,6,8,12,16])
    #Best for BSA High Res TOF
    #print len(s1), len(s2)
    #s = N.append(s1, s2)
    cwt = cwtMS(yArray, s3, staticThresh = (2/abundMax)*100, wlet='DOG')

    print "wavelet complete"
    print time.clock()-t1, 'seconds'
    print "CWT Shape: ", cwt.shape

    fig1 = P.figure()
    ax = fig1.add_subplot(311)
    ax2 = fig1.add_subplot(312,sharex=ax)
    ax3 = fig1.add_subplot(313,sharex=ax)
    print "CWT Max", cwt.max(axis=0).max()
    intMax = cwt.max(axis=0).max()*0.05
    im=ax3.imshow(cwt, vmax = intMax, cmap=P.cm.jet,aspect='auto')

    minSNR = 5
    #numSegs = len(yArray)/20


    #smoothed_data = SmoothF.savitzky_golay(yArray, kernel = 31, order = 7)
    t1 = time.clock()
    noiseEst, minNoise = GB.SplitNSmooth(yArray ,numSegs, minSNR)

    print "SplitNSmooth: ", time.clock()-t1
    if len(xArray) == len(noiseEst):
        ax.plot(xArray, noiseEst, '-r', alpha = 0.5, label = 'smoothed')
#    minNoise*=3
#    ax.hlines(minNoise, 0, len(ms))
    ax.plot(xArray, yArray, 'g',alpha = 0.7, label = 'ms')
    #ax.plot(xArray, smoothed_data, 'k',alpha = 0.7, label = 'ms')
    ax.plot(xArray, noiseEst, 'r',alpha = 0.4, label = 'ms')
#    mNoise = GB.crudeNoiseEstimate(yArray, sigmaThresh=3)
#    mNoise = SF.normalize(cwt[0]).mean()
#    stdNoise = SF.normalize(cwt[0]).std()
#    mNoise = 3*stdNoise+mNoise
    t1 = time.clock()
    peakLoc, peakInt, rawPeakInd, cwtPeakLoc, cClass, boolAns = getCWTPeaks(cwt, xArray, yArray, noiseEst, minRow = 0, minNoiseEst = minNoise, EPS = None, debug = True, tempAxis = ax2)
    print "getCWTPeaks: ", time.clock()-t1
    print "# peaks found: ", len(peakLoc)
#    print peakLoc
#    print cwtPeakLoc
    print "peaksFound"
    if boolAns:
        ax3.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'ob', ms = 3, alpha = 0.7)
        ax.vlines(peakLoc, 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)
        if cClass != None:
            i = cClass.max()
            for m in xrange(int(i)+1):
                ind = N.where(m == cClass)
                temp = cwtPeakLoc[ind]
                ax3.plot(temp[:,0],temp[:,1],'-s', alpha = 0.7, ms = 3)
            if len(peakLoc) != 0:
                ax.vlines(peakLoc, 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)

#        for pk in peakLoc:
#            print pk

    P.show()

