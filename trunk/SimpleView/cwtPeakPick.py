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

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

def cwtMS(Y, scales, sampleScale = 1.0, wlet = 'DOG', maxClip = 1000., staticThresh = None):
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
            #Y[yIndex] *= 0.#set them to 0
#            yTemp = Y[0:yIndex[-1]]#clip length of Y to make it faster
#            yTemp = SF.roundLen(yTemp)
#            print "Clipped", len(yTemp)


        scaledCWT=N.clip(N.fabs(ans.real), 0., maxClip)#N.fabs get the element-wise absolute values
        return scaledCWT
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
#    peakLoc, peakInt, cwtPeakLoc, cClass = 0
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
#    w.show()


def getCWTPeaks(scaledCWT, X, Y, noiseEst, minSNR = 3,\
                minRow = 3, minClust = 4, rowThresh = 3,\
                pntPad = 50, staticThresh = 0.1, minNoiseEst = 0.025,
                EPS = None, debug = False):
    '''
    returns: N.array(peakLoc), cwtPeakLoc, cClass, boolean

    pntPad is the number of points (interpolated) that spans 0.5 m/z units
    staticCut is the lower threshold limit--NOT USED

    scaledCWT is the continuous wavelet transform provided by cwtMS function
    minRow is the first row of the cwt to pick peaks from--if this is too small you'll get
    too many peaks and the algorithm will choke.  Keep in mind that the first few rows of
    the CWT are highly correlated with high frequency noise--you don't want them anyway.
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
    print "Shape: ",scaledCWT.shape

    revRowArray = N.arange((scaledCWT.shape[0]-1),1,-1)#steps backwards
    for i in revRowArray:
        row = scaledCWT[i]
        if i> minRow:
            normRow = SF.normalize(row)
            rowDeriv = SF.derivative(normRow)
            t3 = time.clock()
            'criterion 1 -- above the threshold and a zero crossing in the derivative'
            criterion = (rowDeriv < 0.5) & (rowDeriv > -0.5) & (normRow >= minNoiseEst)
            tempLocEst = N.where(criterion)[0]

            for m in tempLocEst[:-1]:#need to exclude last element so we don't get an IndexError for the rowDeriv array
                if N.sign(rowDeriv[m]) > N.sign(rowDeriv[m+1]):
                    if normRow[m] >= noiseEst[m]:
                        cwtPeakLoc.append([m,i])

#            print "Zero Crossing", time.clock()-t3


    cwtPeakLoc = N.array(cwtPeakLoc)
#    ax2.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'oy', alpha = 0.4)
#    print 'Peak Finding: ', time.clock() - t2

    peakLoc = []
    peakInt = []
    rawPeakInd = []
    snr = []

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
#        print cClass.max(), len(tType), Eps
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
#                print tempDiffX, diffSumX
#                print tempDiffY, diffSumY


        #        if diffSumX <= len(tempDiffX)*2:
                i = 0
                for j in tempDiffY:
                    if j <= rowThresh:
                        i+=1
                    else:
                        i+=-1
#                if i >= rowThresh:
#                if tempDiffY.mean() <= rowThresh:

#                    tempInd = temp[:,1].argsort()
#                    if len(tempInd) > 1:
#                        maxInd = tempInd[1]
#                    else:
                maxInd = temp[:,1].argmin()#temp[:,1].argmin()
                xVal = temp[maxInd][0]

                #this screening assumes there is a low value to the first
                #scale value e.g. 1 or 2
                if (xVal-pntPad) > 0:
                    xStart = xVal-pntPad
                else:
                    xStart = 0

                if (xVal+pntPad) < len(Y):
                    xStop = xVal+pntPad
                else:
                    xStop = len(Y)


                tempVals = Y[xStart:xStop]#BHC added 3/25/09
                if len(tempVals)>0:
                    localMaxInd = tempVals.argmax()

#                    print localMaxInd
                    yMaxInd = xVal-pntPad+localMaxInd
#                    print X[yMaxInd], Y[yMaxInd], noiseEst[yMaxInd]
                    rawPeakInd.append(yMaxInd)
#                    if Y[xVal] >= noiseEst[xVal]:
                    if int(yMaxInd-pntPad/2) >= 0:#case where peak is close to the beginning of the spectrum
                        noiseStart = int(yMaxInd-pntPad/2)
                    else:
                        noiseStart = 0

                    if int(yMaxInd+pntPad/2) < len(Y):#case where peak is close to the end of the spectrum
                        noiseEnd = int(yMaxInd+pntPad/2)
                    else:
                        noiseEnd = len(Y)
#                        noiseStart = noiseEnd
                    if noiseStart < noiseEnd:

                        if Y[yMaxInd] >= noiseEst[noiseStart:noiseEnd].mean()*minSNR:# and Y[yMaxInd] >= staticCut:
    #                    if Y[xVal]>=scaledCWT[0][xVal]*minSNR/2 and Y[xVal] >= noiseEst[xVal]*minSNR/2:
                            peakLoc.append(X[yMaxInd])
                            peakInt.append(Y[yMaxInd])
                            snr.append(Y[yMaxInd]/noiseEst[noiseStart:noiseEnd].mean())

                    else:
                        if Y[yMaxInd] >= noiseEst[yMaxInd]*minSNR:# and Y[yMaxInd] >= staticCut:
    #                    if Y[xVal]>=scaledCWT[0][xVal]*minSNR/2 and Y[xVal] >= noiseEst[xVal]*minSNR/2:
                            peakLoc.append(X[yMaxInd])
                            peakInt.append(Y[yMaxInd])
                            snr.append(Y[yMaxInd]/noiseEst[yMaxInd])

    peakLoc = N.array(peakLoc)
    peakInt = N.array(peakInt)
    snr = N.array(snr)
    rawPeakInd = N.array(rawPeakInd)
    peakOrder = peakLoc.argsort()
    peakLoc = peakLoc[peakOrder]
    peakInt = peakInt[peakOrder]
    snr = snr[peakOrder]
#    rawPeakInd = rawPeakInd[peakOrder]
    peakLoc, peakInt, rawPeakInd, snr = consolidatePeaks(peakLoc, peakInt, rawPeakInd, snr)

    return peakLoc, peakInt, rawPeakInd, snr, cwtPeakLoc, cClass, True


def consolidatePeaks(peakLoc, peakInt, rawPeakInd, snr, diffCutoff = 2.50):
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
    newSNR = []
    if boolAns:
        singlePnts = N.where(cClass == -1)[0]
        for pnt in singlePnts:
            newPeakLoc.append(peakLoc[pnt])
            newIntLoc.append(peakInt[pnt])
            newPointLoc.append(rawPeakInd[pnt])
            newSNR.append(snr[pnt])

        if len(cClass)>0:
            if cClass.max() > 0:#otherwise there is just one outlier
                for i in xrange(1,int(cClass.max())+1):
                    tempInd = N.where(i == cClass)[0]
                    if len(tempInd)>0:
    #                    print tempInd
                        maxLoc = peakInt[tempInd].argmax()
        #                intSort = peakInt[tempInd].argsort()

        #                maxLoc = intSort[0]

        #                print peakLoc[maxLoc+tempInd[0]], peakInt[maxLoc+tempInd[0]], rawPeakInd[maxLoc+tempInd[0]]
                        newPeakLoc.append(peakLoc[maxLoc+tempInd[0]])
                        newIntLoc.append(peakInt[maxLoc+tempInd[0]])
                        newPointLoc.append(rawPeakInd[maxLoc+tempInd[0]])
                        newSNR.append(snr[maxLoc+tempInd[0]])

#            print newPeakLoc
#            print newIntLoc
#            print newPointLoc
        return newPeakLoc, newIntLoc, newPointLoc, newSNR
#        else:
#            print "Error with Consolidation--using raw peaks"
#            return peakLoc, peakInt, rawPeakInd
    else:
        print "Error with Consolidation--using raw peaks"
        return peakLoc, peakInt, rawPeakInd, snr



#    xDiff = N.diff(peakLoc)
#    extraPeakInd = N.where(xDiff<diffCutoff)[0]
#    extraPeakInd+=1
#    validPeakInd = peakLoc.argsort().tolist()
#    j=0
#    for extra in extraPeakInd:
##        if peakInt[extra] < peakInt[extra-j]:
#        validPeakInd.pop(extra-j)
##        else:
##            validPeakInd.pop(j)
#        j+=1#need this because each time you pop the length gets shorter
#
#    validPeaks = peakLoc[validPeakInd]
#    validInt = peakInt[validPeakInd]
#    validRawPeaks = rawPeakInd[validPeakInd]
#    return validPeaks, validInt, validRawPeaks

if __name__ == "__main__":
    import mzXML_reader as mzXML
    t1 = time.clock()
    loadA = False
    normOk = False
    #loadA = True
    if loadA:
    #    ms = P.load('N3_Norm.txt')
        ms = P.load('exampleMS.txt')
        x = N.arange(len(ms))
        ms = SF.normalize(ms)
        ms = SF.topHat(ms, 0.01)
    #    ms = ms[8000:8500]
    ##    ms = ms[7000:9000]
    else:
        'Noisy_IMS_XY.csv'
        'BSA_XY_Full.csv'
        'J15.csv'
        'Tryptone.csv'
        ms = P.load('LIFT2.csv', delimiter = ',')

        x = ms[:,0]
        ms = ms[:,1]


        fn = 'HG_pt01_mg_mL_B12_1.mzXML'

        mzx = mzXML.mzXMLDoc(fn)
        spectrum = mzx.data.get('spectrum')

        x = spectrum[0]
        ms = spectrum[1]
#        x, ms = interpolate_spectrum(ms)
        msMax = ms.max()
        print len(ms)
        print "MS Max", msMax
        ms = SF.normalize(SF.topHat(ms, 0.01))
        ms = SF.roundLen(ms)
        start = 0#63000
        stop = int(len(ms)*1)##79000#len(ms)*.75
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
    #CWT.cwtMS(dataItem.y, self.scales, staticThresh = (self.staticThresh/dataItem.normFactor)*100)
    cwt = cwtMS(ms, s1, staticThresh = (2/msMax)*100)

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
    minSNR = 1.5
    numSegs = len(ms)/10
    #numSegs = len(ms)/10#int(len(plotcwt[0])*0.0015)
#    if numSegs < 1000 and len(ms) > 1000:
#        numSegs = 1000
#    else:
#        numSegs = len(ms)/5
    print "Length of ms, numSegs: ", len(ms), numSegs
    if normOk:
    #    ax.plot(SF.normalize(plotcwt[0]),'b', label = '0')
    #    ax.plot(SF.normalize(plotcwt[1]),'r', label = '1')

        noiseEst, minNoise = GB.SplitNSmooth(SF.normalize(ms),numSegs, minSNR)
        ax.plot(x, noiseEst, '-r', alpha = 0.5, label = 'smoothed')
    #    minNoise*=3
    #    ax.hlines(minNoise, 0, len(ms))
        ax.plot(x, SF.normalize(ms), 'g',alpha = 0.7, label = 'ms')
        print 'Normalized'
        mNoise = SF.normalize(cwt[0]).mean()
        stdNoise = SF.normalize(cwt[0]).std()
        mNoise = 3*stdNoise+mNoise

    else:
    #    ax.plot(plotcwt[0],'b', label = '0')
    #    ax.plot(plotcwt[1],'r', label = '1')

        noiseEst, minNoise = GB.SplitNSmooth(ms,numSegs, minSNR)
        print len(x), len(noiseEst)
        ax.plot(x, noiseEst, '-r', alpha = 0.5, label = 'smoothed')
    #    minNoise*=3
    #    ax.hlines(minNoise, 0, len(ms))
    #    print minNoise
        ax.plot(x,ms, 'g',alpha = 0.7, label = 'ms')
        mNoise = cwt[0].mean()
        stdNoise = cwt[0].std()
        mNoise = 3*stdNoise+mNoise
    print "minNoiseEst: ", minNoise
    peakLoc, peakInt, rawPeakInd, snr, cwtPeakLoc, cClass, boolAns = getCWTPeaks(cwt, x, ms, noiseEst, minRow = 1, minClust = 4, minNoiseEst = minNoise, EPS = None, debug = True)
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
		for pk in peakLoc:
			print pk
        #ax.plot(x, cwt[0], 'b', alpha = 0.7)

    P.show()

