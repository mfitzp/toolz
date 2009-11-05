#!/usr/bin/env python
#import wx
import os
import sys
import traceback

from scipy import optimize, signal
import numpy as N
import pylab as P
from matplotlib.widgets import SpanSelector, Button
import CARSMath as CM
import smoothingFilter as SF
import getBaseline as GB
import supportFunc as sFunc

#######################
'''Function to locate the positive peaks in a noisy x-y data
    % set.  Detects peaks by looking for downward zero-crossings
    % in the first derivative that exceed SlopeThreshold.
    % Returns list (P) containing peak number and
    % position, height, and width of each peak. SlopeThreshold,
    % AmpThreshold, and smoothwidth control sensitivity
    % Higher values will neglect smaller features. Peakgroup
    % is the number of points around the "top part" of the peak.
    % T. C. O'Haver, 1995.  Version 2  Last revised Oct 27, 2006

    Revised for Python by Brian H. Clowers, October 15, 2007'''

def SplitNSmooth(spec, numSegs, sigThresh = 5):

    histo = N.histogram(spec, bins = numSegs*3 , new = True)#
    minNoise = histo[1][histo[0].argmax()+1]

    gblNThresh = crudeNoiseEstimate(spec, sigmaThresh = sigThresh)
    spec = N.clip(spec, 0, gblNThresh)

    segLen = int(N.floor(len(spec)/numSegs))
    xSpec = N.zeros(1)
    noiseSpec = N.zeros(1)#N.zeros(len(spec))

    for i in xrange(numSegs):
        if i == 0:
            start = segLen*i
            stop = segLen*(i+1)
        elif i == (numSegs-1):
            start = segLen*i
            stop = segLen*(i+1)
        else:
            start = segLen*i
            stop = segLen*(i+1)

        tempSeg = spec[start:stop]
        localNThresh = crudeNoiseEstimate(tempSeg, sigmaThresh = sigThresh)
        noiseSeg = tempSeg.clip(min = tempSeg.min(), max = localNThresh)
#        indMax = int(len(tempSeg)/100)
        xVals = noiseSeg.argsort()[-1:]#[-indMax:]
#        print len(xVals)
        maxVals = noiseSeg[xVals]
#        smthSeg = SF.savitzky_golay(maxVals, kernel = 11, order = 4)

#        noiseSpec = N.append(noiseSpec, smthSeg)
        noiseSpec = N.append(noiseSpec, maxVals)
        xSpec = N.append(xSpec, xVals+start)
#        xSpec.append(xVals)
        #noiseSpec[start:stop] = noiseSeg

#    print len(xSpec), len(noiseSpec)
    ySpec = SF.savitzky_golay(noiseSpec, kernel = 11, order = 3)
#    sCoef = cspline1d(noiseSpec)
#    x = N.arange(len(spec))
#    ySpec = cspline1d_eval(sCoef,x)
    noise = N.zeros_like(spec)
    for i in xrange(len(xSpec[:-1])):
        noise[xSpec[i]:xSpec[i+1]] = ySpec[i]



    return noise, minNoise
    #return xSpec, ySpec


def peakHelper(specX, specY, minSNR = 3, slopeThresh = None, \
                 smthKern = 15, fitWidth = None, peakWidth = None,
                 ampThresh = None, numSegs = 10):
        '''
        Accepts a numpy spectrum containing gaussian like peaks...
        '''
        if len(specY)>0:

            peakInfo = findPeaks(specX, specY, peakWidth = peakWidth, minSNR = minSNR,\
                                slopeThresh = slopeThresh, ampThresh = ampThresh,\
                                smthKern = smthKern, fitWidth = fitWidth, numSegs = numSegs,\
                                resample = True)
            return peakInfo



def crudeNoiseEstimate(datArray, sigmaThresh=3):
    '''
    Accepts a numpy array and zeros the values below the user defined threshold
    '''
    mean = datArray.mean()
    std = datArray.std()
    thresh = mean+std*5
    #first pass selection to minimize contribution of large peaks
    #only takes values below the thresh
    #should use clip
    noiseArray = N.select([datArray<thresh],[datArray],default = mean)


    mean2 = noiseArray.mean()
    std2 = noiseArray.std()
    thresh2 = mean2+std2*sigmaThresh

    return thresh2


def findPeaks(data_arrayX, data_arrayY, peakWidth, minSNR = 3, slopeThresh = None, ampThresh = None,\
              smthKern = None, fitWidth = None,  peakWin = None, numSegs = 10, minFrac = 2, factor = 5, resample = False):
    '''
    peakWidth = Average number of points in half-width of peaks (CHANGE TO FIT YOUR SIGNAL)
    minSNR = minimum SNR for a peak to be considered, noise is defined by function crudeNoiseEstimate
    slopeThresh = threshold of the first derivative from which a peak should be detected
    ampThresh = absolute value for the threshold cutoff
    smthKern = width to use for Savitzky-Golay smoothing of derivative
    Send it a normalized data set, things work better, let prone to fail
    resample
    '''

    data_arrayX = data_arrayX.astype(N.float32)
    data_arrayY = data_arrayY.astype(N.float32)
#    data_arrayY = sFunc.normalize(data_arrayY)
    smthKern = smthKern
    peakWidth = peakWidth
    minFrac = minFrac
    minSNR = minSNR
    #need to obtain a smoothed spectrum
    #if there are too many points things get really slow
    factor = factor
    if peakWidth/factor < 2:
        factor = peakWidth/2

    numSegs = int(round(len(data_arrayY)*0.01))#first approximation
    print numSegs
    peakWidth/=int(round(peakWidth/factor))#scale for the resampling
    #resample returns the Y,X resampled arrays
    if resample:
        resampleY, resampleX = signal.resample(data_arrayY, numSegs, data_arrayX)
    else:
        resampleY = data_arrayY
        resampleX = data_arrayX
    smoothed_data = SF.savitzky_golay(resampleY, kernel = smthKern, order = 4)
    ampThreshold, minNoise = SplitNSmooth(smoothed_data, numSegs, minSNR)
    d = derivative(smoothed_data)


    criterion = (d <= 5) & (d >= -5) & (resampleY[:-1] >= ampThreshold[:-1])
    tempLocEst = N.where(criterion)[0]

    peakLoc = []
    peakIndex = []
    for m in tempLocEst[:-1]:#need to exclude last element so we don't get an IndexError for the derivative array
        if N.sign(d[m]) > N.sign(d[m+1]):
            if ampThreshold[m]>0.1:#check to see if noise threshold is reasonable
#                if resampleY[m] >= ampThreshold[m]:
                if smoothed_data[m] >= ampThreshold[m]*1.25:
                    peakLoc.append(resampleX[m])
                    peakIndex.append(m)



    if slopeThresh == None:
        SlopeThreshold=(1/(peakWidth**4))
    else:
        SlopeThreshold = slopeThresh

    y_len = len(resampleY)

    if smthKern == None:
        smthKern = 15#=peakWidth/2 #SmoothWidth should be roughly equal to 1/2 the peak width (in points)
    else:
        smthKern = smthKern

    if fitWidth == None:
        FitWidth=peakWidth/2 #FitWidth should be roughly equal to 1/2 the peak widths(in points)
    else:
        FitWidth = fitWidth

    if peakWin == None:
        peakWindow = 0.025
    else:
        peakWindow = peakWin

    if FitWidth < 3:
        FitWidth=3

    PeakNumber=0

    peakgroup=round(FitWidth)

    n=round(peakgroup/2)
#    vectorlength=len(data_arrayY)#07-15-09
    vectorlength=len(resampleY)
    peak=1

    p=N.arange(0,3,1)#peak parameters
    peak_loc=[]
    peak_intensity=[]
    peak_width=[]
    peak_area = []

#    print "AmpThresh: ", gblThreshold2
    print "SlopeThresh: ", SlopeThreshold
    print "FitWidth: ", FitWidth
    print "PeakWidth: ", peakWidth
    print "minSNR: ", minSNR
    print len(resampleX), len(ampThreshold)

    FitWidth = round(FitWidth)
    yMax = resampleY.max()
    for i, pInd in enumerate(peakIndex):

        pAmp = resampleY[pInd]
        pFrac = pAmp/yMax
#        FitWidth = FitWidth*round(1/(1-pFrac))

        startX = pInd-FitWidth
        stopX = pInd+FitWidth
        if startX < 0:
            startX = 0
        if stopX > len(resampleX):
            stopX = len(resampleX)
#        tempY = resampleY[startX:stopX]
#        localMax = tempY.argmax()
#
#        startX = pInd+localMax-FitWidth
#        stopX = pInd+localMax+FitWidth
#        if startX < 0:
#            startX = 0
#        if stopX > len(resampleX):
#            stopX = len(resampleX)

        xx = resampleX[startX:stopX]
#        yy = resampleY[startX:stopX]
        yy = smoothed_data[startX:stopX]


        try:
            '''
            The peak fitting is shifting to right for linear TOF data so we are just going
            to use the derivative as a peak location.
            '''
            if yy.max()>=minFrac:
#                    print "GO JOE"
#                    print yy.max(), xx[yy.argmax()]
                if (yy.max()/yMax)>=0.1:#10% Threshold
#                        print "BOO"
                    peak_intensity.append(yy.max())
                    peak_loc.append(xx[yy.argmax()])
                    peak_width.append(0)
                    peak_area.append(N.trapz(yy, xx))
#            p = CM.fit_gaussian(xx, yy)#This isn't working quite right.  Need to re-evaluate
#
#            if pFrac >= 0.25:#pInd == val:
#                print "Index @ %s"%pInd
#                print "Intensity: ",resampleY[pInd]
#                print "Fit Intensity, Fit Loc, Fit width: ", p
##                for i,xVal in enumerate(xx):
##                    print "%s, %s"%(xVal, yy[i])
#
#            if p[0]>=minFrac:
#                peak_intensity.append(p[0])
#                peak_loc.append(abs(p[1]))
#                peak_width.append(p[2])
#                peak_area.append(N.trapz(yy, xx))
#            else:
#                if yy.max()>=minFrac:
##                    print "GO JOE"
##                    print yy.max(), xx[yy.argmax()]
#                    if (yy.max()/ymax)>=0.1:#10% Threshold
##                        print "BOO"
#                        peak_intensity.append(yy.max())
##                        peak_loc.append(xx[yy.argmax()])
#                        peak_loc.append(xx[0])
#                        peak_width.append(0)
#                        peak_area.append(N.trapz(yy, xx))

        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
            print "Fit Exception"
            print yy.max(), xx[yy.argmax()]
            print errorMsg
            continue


    file_info={}
    file_info['peak_location'] = N.array(peak_loc)
    file_info['peak_intensity'] = N.array(peak_intensity)
    file_info['peak_width'] = N.array(peak_width)
    file_info['peak_area'] = N.array(peak_area)
    file_info['smoothed_data'] = N.array(smoothed_data)
    file_info['smoothed_deriv'] = d
    file_info['resampleX'] = resampleX
    file_info['resampleY'] = resampleY
    file_info['ampThresh'] = ampThreshold
    file_info['tempLoc'] = N.array(peakLoc)

    return file_info

###################

def get_ascii_data(filename):
    data_spectrum=P.load(filename, skiprows = 0, delimiter = ',' )##remember to change this depending on file format
    print "File Loaded: ", filename
    return data_spectrum

###################

def derivative(y_data):
    '''calculates the 1st derivative'''

    y = (y_data[1:]-y_data[:-1])

    dy = y/2 #((x_data[1:]-x_data[:-1])/2)

    return dy


####################

def groupOneDim(oneDimVec, tol):
    '''
    oneDVec is already sorted
    tol is in ppm
    it would be nice to take into account the original order of the peaks to make sure that
    peaks from the same spectrum don't contribute to the same m/z fingerprint
    one way to do this is to take the closest peak
    '''
    if type(oneDimVec) is list:
        oneDimVec = N.array(oneDimVec)
    diffArray = N.diff(oneDimVec)
    groups = N.zeros_like(diffArray)
    gNum = 0
    origNum = 0
    for i,diffVal in enumerate(diffArray):
#        if origOrder[i+1]!=origNum:#test to make sure that the next value does not come from the same spectrum
        ppmDiff = (diffVal/oneDimVec[i+1])*1000000
        if ppmDiff <= tol:
            groups[i] = gNum
        else:
            groups[i] = gNum
            gNum+=1
#        else:
#            groups[i] = gNum
#            gNum+=1
#        origNum = origOrder[i+1]

    return groups, gNum

############################
def plot_results(raw_data_x, raw_data_y, peak_result_dict):

    fig = P.figure(figsize=(8,6))
    ax = fig.add_subplot(111, axisbg='#FFFFFF')
    x=raw_data_x
    y=raw_data_y
    ax.plot(x,y, 'b')
#    sdata = peak_result_dict['smoothed_data']

#    ax.plot(x, peak_result_dict.get('smoothed_data'), 'r')
    ax.plot(peak_result_dict.get('peak_location'), peak_result_dict.get('peak_intensity'), 'go')
    noise,minNoise = SplitNSmooth(y, len(y)/10, 10)
    print len(y)
    smthNoise = SF.savitzky_golay(N.clip(noise,0,noise.max()), kernel = 15, order = 4)
    smthNoiseZero = N.clip(smthNoise, 0, smthNoise.max())
    gblThreshold2=crudeNoiseEstimate(smthNoiseZero, 10/5)
#    smthAmpThresh = SF.savitzky_golay(N.clip(AmpThreshold, 0, AmpThreshold.max()), kernel = smthKern, order = 4)
    ax.plot(smthNoise, '-g', alpha = 0.5)
#    ax.plot(smthNoiseZero, '-k', alpha = 0.5)
    ax.plot(noise, '-r', alpha = 0.5)
    ax.hlines(crudeNoiseEstimate(y, 10), 0, len(y))
    ax.hlines(gblThreshold2, 0, len(y), 'b')

#    ax.set_title('Widget')
#
#    ax2 = fig.add_subplot(212, axisbg='#FFFFFF', sharex=ax)
#    line2, = ax2.plot(peak_result_dict.get('smoothed_deriv'))

    P.show()




if __name__ == '__main__':
    import time
    import scipy.signal as signal
#    data_array = get_ascii_data(File_Dialog())
    getChrom = False
    if getChrom:
        data_array = get_ascii_data('chrom1D.csv')
        y = data_array[20000:25000]
        y = data_array
        y = sFunc.normalize(y)
        x = N.arange(len(y))
    else:
        data_array = get_ascii_data('linTOF_tHat.csv')
        x = data_array[:,0]
        y = data_array[:,1]
#        y = y[3000:10000]
#        x = x[3000:10000]
        y = sFunc.roundLen(y)
        y = sFunc.normalize(y)
        x = x[0:len(y)]


    P.plot(x,y, 'r', alpha=0.8)
    peak_info=findPeaks(x, y, peakWidth = 100, minSNR = 10, smthKern = 17, minFrac = 2, factor = 5, resample = True)
#    print len(peak_info['peak_location'])

    resampleX = peak_info['resampleX']
    resampleY = peak_info['resampleY']
    ampThresh = peak_info['ampThresh']
    smoothed_data = peak_info['smoothed_data']
    deriv = peak_info['smoothed_deriv']
    tempLoc = peak_info['tempLoc']
    tempLocY = N.zeros_like(tempLoc)

    P.plot(peak_info['peak_location'], peak_info['peak_intensity'], 'go')
    P.plot(peak_info['resampleX'], peak_info['smoothed_data'], 'b')
    P.plot(peak_info['resampleX'][:-1], peak_info['smoothed_deriv'], 'm')
    P.plot(peak_info['resampleX'], peak_info['ampThresh'], 'y')
    P.plot(tempLoc, tempLocY, 'ko')


    P.show()



