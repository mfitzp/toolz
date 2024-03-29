'''
Questions weather to normalize or not when comparing?
'''

import sys

import pylab as P
import numpy as N

from iwavelets import pycwt as W

from interpolate import interpolate_spectrum

from scipy import ndimage#used for tophat filter
import time
import baseline2 as bs2
from dbscan import dbscan

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

def topHat(data, factor):
    '''
    data -- numpy array
    pntFactor determines how finely the filter is applied to data.
    A point factor of 0.01 is appropriate for the tophat filter of Bruker MALDI mass spectra.
    A smaller number is faster but a trade-off is imposed
    '''
    pntFactor = factor
    struct_pts = int(round(data.size*pntFactor))
    str_el = N.repeat([1], struct_pts)
    tFil = ndimage.white_tophat(data, None, str_el)

    return tFil

def derivative(y_data):
    '''calculates the 1st derivative'''
    y = (y_data[1:]-y_data[:-1])
    dy = y/2 #((x_data[1:]-x_data[:-1])/2)
    return N.append(dy,dy.mean())

def normalize(data):
    data/=data.max()
    data*=100
    return data

def roundLen(data):
    dl = len(data)
    place = 2
    newdl = N.round(dl,-place)#rounds to nearest tenth use -1, hundredth use -2
    if newdl > dl:
        newdl -= N.power(10,place)
#    print newdl,dl
    return data[0:newdl]

def cwtMS(X, scales, sampleScale = 1.0, wlet = 'DOG', maxClip = 1000.):
    '''
    X is the INTERPOLATED intensity array from a mass spectrum.
    interpolation IS necessary especially for TOF data as the m/z domain is non-linear.
    '''
    ans = W.cwt_a(X, scales, sampling_scale = sampleScale)#, wavelet = wlet)
    scaledCWT=N.clip(N.fabs(ans.real), 0., maxClip)#N.fabs get the element-wise absolute values
    return scaledCWT


def getCWTPeaks(scaledCWT, Y, noiseEst, minSNR = 3, minRow = 3, minClust = 4, EPS = None):
    '''
    returns: N.array(peakLoc), cwtPeakLoc, cClass, boolean

    scaledCWT is the continuous wavelet transform provided by cwtMS function
    minRow is the first row of the cwt to pick peaks from--if this is too small you'll get
    too many peaks and the algorithm will choke.  Keep in mind that the first few rows of
    the CWT are highly correlated with high frequency noise--you don't want them anyway.
    '''
    cwtPeakLoc = []
    print "Shape: ",scaledCWT.shape

    revRowArray = N.arange((scaledCWT.shape[0]-1),1,-1)#steps backwards
    for i in revRowArray:
        row = scaledCWT[i]
        if i> minRow:
            normRow = normalize(row)
            rowDeriv = derivative(normRow)
            t3 = time.clock()
            'criterion 1 -- above the threshold and a zero crossing in the derivative'

            criterion = (rowDeriv < 0.5) & (rowDeriv > -0.5) & (normRow >= minNoise)
            tempLocEst = N.where(criterion)[0]

            for m in tempLocEst[:-1]:#need to exclude last element so we don't get an IndexError for the rowDeriv array
                if N.sign(rowDeriv[m]) > N.sign(rowDeriv[m+1]):
                    if normRow[m] >= noiseEst[m]:
                        cwtPeakLoc.append([m,i])

            print "Zero Crossing", time.clock()-t3


    cwtPeakLoc = N.array(cwtPeakLoc)
#    ax2.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'oy', alpha = 0.4)
#    print 'Peak Finding: ', time.clock() - t2

    peakLoc = []

    t3 = time.clock()
    try:
        cClass, tType, Eps, boolAns = dbscan(cwtPeakLoc, minClust, Eps = EPS)
    except:
        errorMsg ='dbscan error...is your CWT huge?\n'
        errorMsg += "Sorry: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
        print errorMsg
        return None, None, None, False


    print 'Peak Cluster: ', time.clock() - t3
    if boolAns:
        print cClass.max(), len(tType), Eps
        i = cClass.max()
        for m in xrange(int(i)+1):
            ind = N.where(m == cClass)
            temp = cwtPeakLoc[ind]

#            ax2.plot(temp[:,0],temp[:,1],'-s', alpha = 0.7, ms = 3)
            if len(temp) > 0:
                sortInd = temp[:,0].argsort()
                temp = temp[sortInd]
                tempDiffX = N.diff(temp[:,0])
                tempDiffY = N.diff(temp[:,1])
                diffSumX = tempDiffX.sum()
                diffSumY = tempDiffY.sum()
                print tempDiffX, diffSumX
                print tempDiffY, diffSumY


        #        if diffSumX <= len(tempDiffX)*2:
                i = 0
                rowThresh = 3
                pntPad = 50
                staticCut = 0.2
                for j in tempDiffY:
                    if j <= rowThresh:
                        i+=1
                    else:
                        i+=-1
#                if i >= rowThresh:
                if tempDiffY.mean() <= rowThresh:
                    maxInd = temp[:,1].argmin()
                    xVal = temp[maxInd][0]

                    #this screening assumes there is a low value to the first
                    #scale value e.g. 1 or 2

                    tempVals = Y[(xVal-pntPad):xVal]
                    if len(tempVals)>0:
                        localMaxInd = tempVals.argmax()
    #                    print localMaxInd
                        yMaxInd = xVal-pntPad+localMaxInd
    #                    if Y[xVal] >= noiseEst[xVal]:
                        if Y[yMaxInd] >= noiseEst[yMaxInd]*minSNR/2 and Y[yMaxInd] >= staticCut:
    #                    if Y[xVal]>=scaledCWT[0][xVal]*minSNR/2 and Y[xVal] >= noiseEst[xVal]*minSNR/2:
                            peakLoc.append(x[yMaxInd])
                            print "Appended, %s\n"%x[yMaxInd]
                        else:
                            print "too low @ %s\n"%x[xVal]
                else:
                    print "\n"
#                    print x[xVal]

    return N.array(peakLoc), cwtPeakLoc, cClass, True


if __name__ == "__main__":

    t1 = time.clock()
    loadA = False
    normOk = False
    #loadA = True
    if loadA:
    #    ms = P.load('N3_Norm.txt')
        ms = P.load('exampleMS.txt')
        x = N.arange(len(ms))
        ms = normalize(ms)
        ms = topHat(ms, 0.01)
    #    ms = ms[8000:8500]
    ##    ms = ms[7000:9000]
    else:
        'Noisy_IMS_XY.csv'
        'BSA_XY_Full.csv'
        'J15.csv'
        'Tryptone.csv'
        ms = P.load('Tryptone.csv', delimiter = ',')
        x, ms = interpolate_spectrum(ms)
        ms = normalize(topHat(ms, 0.01))
        ms = roundLen(ms)
        start = 0#63000
        stop = int(len(ms)*.75)##79000#len(ms)*.75
        ms = ms[start:stop]
        x = x[start:stop]
        x = N.arange(len(x))

    print len(ms)

    #s = N.arange(2,32,2)#changed to 8 from 32
    s1 = N.arange(2,64,8)
    s2 = N.arange(32,64,8)
    #Best for BSA High Res TOF
    #s1 = N.arange(2,8,2)
    #s2 = N.arange(12,48,4)
    print len(s1), len(s2)
    s = N.append(s1, s2)
#    print type(s), s

    cwt = cwtMS(ms, s1)

    print "wavelet complete"
    print time.clock()-t1, 'seconds'
    print "CWT Shape: ", cwt.shape

    fig1 = P.figure()
    ax = fig1.add_subplot(211)
    ax2 = fig1.add_subplot(212,sharex=ax)
    print "CWT Max", cwt.max(axis=0).max()
    intMax = cwt.max(axis=0).max()*0.05
    im=ax2.imshow(cwt,vmax = intMax, cmap=P.cm.jet,aspect='auto')
    #ax2.plot(plotcwt[1], alpha = 0.7, label = '1')
    #ax.plot(plotcwt[0], alpha = 0.7, label = '0')
    minSNR = 15
    numSegs = len(ms)/10
    #numSegs = len(ms)/10#int(len(plotcwt[0])*0.0015)
#    if numSegs < 1000 and len(ms) > 1000:
#        numSegs = 1000
#    else:
#        numSegs = len(ms)/5
    print "Length of ms, numSegs: ", len(ms), numSegs
    if normOk:
    #    ax.plot(normalize(plotcwt[0]),'b', label = '0')
    #    ax.plot(normalize(plotcwt[1]),'r', label = '1')

        noiseEst, minNoise = bs2.SplitNSmooth(normalize(ms),numSegs, minSNR)
        ax.plot(x, noiseEst, '-r', alpha = 0.5, label = 'smoothed')
    #    minNoise*=3
    #    ax.hlines(minNoise, 0, len(ms))
        ax.plot(x, normalize(ms), 'g',alpha = 0.7, label = 'ms')
        print 'Normalized'
        mNoise = normalize(cwt[0]).mean()
        stdNoise = normalize(cwt[0]).std()
        mNoise = 3*stdNoise+mNoise

    else:
    #    ax.plot(plotcwt[0],'b', label = '0')
    #    ax.plot(plotcwt[1],'r', label = '1')

        noiseEst, minNoise = bs2.SplitNSmooth(ms,numSegs, minSNR)
        print len(x), len(noiseEst)
        ax.plot(x, noiseEst, '-r', alpha = 0.5, label = 'smoothed')
    #    minNoise*=3
    #    ax.hlines(minNoise, 0, len(ms))
    #    print minNoise
        ax.plot(x,ms, 'g',alpha = 0.7, label = 'ms')
        mNoise = cwt[0].mean()
        stdNoise = cwt[0].std()
        mNoise = 3*stdNoise+mNoise

    peakLoc, cwtPeakLoc, cClass, boolAns = getCWTPeaks(cwt, ms, noiseEst, minRow = 1, minClust = 4, EPS = 19.5)
    if boolAns:
        ax2.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'oy', ms = 3, alpha = 0.4)
        if cClass != None:
            i = cClass.max()
            for m in xrange(int(i)+1):
                ind = N.where(m == cClass)
                temp = cwtPeakLoc[ind]
                ax2.plot(temp[:,0],temp[:,1],'-s', alpha = 0.7, ms = 3)
            if len(peakLoc) != 0:
                ax.vlines(peakLoc, 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)
        #ax.plot(x, cwt[0], 'b', alpha = 0.7)

    P.show()

