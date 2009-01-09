import numpy as N
import pycwt as W
import time

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

def detectPeaksCWT(spectrum, scales = (N.arange(2,32,2))**2, snrThresh = 3,\
                   closePeak = True, pkScaleRange = 5, ampThresh = 0.01,\
                   ridgeLen = 24, tuneIn = False):

    minNoise = ampThresh/snrThresh

    t1 = time.clock()

    wCoefs = W.cwt_a(spectrum, scales ,sampling_scale = 1.0, wavelet = 'MexHat')

    print time.clock() - t1
#    if ampThresh != 0:
#        ampThresh *= wCoefs.max()
#
#    localMaxima = getLocalMaxCWT(wCoefs, scales, ampThresh = ampThresh)
#
#    ridgeList = getRidges(localMaxima, gapTh = 3, skip = 2)
#
#    majorPeakInfo = getMajorPeaks(spectrum, ridgeList, wCoefs, scales, snrThresh = snrThresh,\
#                                  pkScaleRange = pkScaleRange, closePeak = closePeak,\
#                                  minNoise = minNoise, ridgeLen = ridgeLen)
#
#    return (majorPeakInfo, ridgeList, localMaxima, wCoefs)

    return wCoefs

def getLocalMaxCWT(wCoefs, scales, minWinSize = 5, ampThresh = 0):
    maxList = []
    for i, s in scales:
        winSize = scale*2+1
        if winSize < minWinSize:
            winSize = minWinSize
        temp = getColumnMaxima(wCoefs[:,i],winSize)
        maxList.append(temp)
    maxList = N.array(maxList)
    filtered = N.select([maxList>ampThresh],[maxList],default = 0)#zeros items that are not above threshold

    return filtered

#def getColumnMaxima(col, winSize):
#    colLen = len(col)
#    rNum = N.ceil(len/winSize)
#    ## Transform the vector as a matrix with column length equals winSize
#    ##        and find the maximum position at each row.
#    y <- matrix(c(x, rep(x[len], rNum * winSize - len)), nrow=winSize)
#    y.maxInd <- apply(y, 2, which.max)
#    ## Only keep the maximum value larger than the boundary values
#    selInd <- which(apply(y, 2, function(x) max(x) > x[1] & max(x) > x[winSize]))
#
#    ## keep the result
#    localMax <- rep(0, len)
#    localMax[(selInd-1) * winSize + y.maxInd[selInd]] <- 1
#
#    ## Shift the vector with winSize/2 and do the same operation
#    shift <- floor(winSize/2)
#    rNum <- ceiling((len + shift)/winSize)
#    y <- matrix(c(rep(x[1], shift), x, rep(x[len], rNum * winSize - len - shift)), nrow=winSize)
#    y.maxInd <- apply(y, 2, which.max)
#    ## Only keep the maximum value larger than the boundary values
#    selInd <- which(apply(y, 2, function(x) max(x) > x[1] & max(x) > x[winSize]))
#    localMax[(selInd-1) * winSize + y.maxInd[selInd] - shift] <- 1
#
#    ## Check whether there is some local maxima have in between distance less than winSize
#    maxInd <- which(localMax > 0)
#    selInd <- which(diff(maxInd) < winSize)
#    if (length(selInd) > 0) {
#        selMaxInd1 <- maxInd[selInd]
#        selMaxInd2 <- maxInd[selInd + 1]
#        temp <- x[selMaxInd1] - x[selMaxInd2]
#        localMax[selMaxInd1[temp <= 0]] <- 0
#        localMax[selMaxInd2[temp > 0]] <- 0
#    }
#
#    return(localMax)
#}



def getMajorPeaks(spectrum, ridgeList, wCoefs, scales, snrThresh = 3,\
                  pkScaleRange = 5, ridgeLen = 32, closePeak = False, \
                  closeWinSize = 100, winNoise = 500, snrMethod = 'quantile',\
                  minNoise = 0.001):
    if ridgeLen > scales.max():
        ridgeLen = scales.max()

    #not sure about the following if statement
    if len(pkScaleRange) is 1:
        pkScaleRange

    if minNoise is None:
        minNoise = 0
    else:
        minNoise *= wCoefs.max()


if __name__ == "__main__":
    import sys
    import pylab as P

    ms = P.load('N3_Norm.txt')
    s = N.arange(2,32,2)
    a = detectPeaksCWT(ms, scales = s**2)
    plotcwt=N.clip(N.fabs(a.real), 0., 1000.)
    #P.pcolormesh(plotcwt)
    im=P.imshow(plotcwt,vmax = 100, cmap=P.cm.jet,aspect='auto')
    #im = P.pcolormesh(plotcwt)
    #P.imshow(plotcwt)
    P.show()











#ms = P.load('N3_Norm.txt')
#s = N.arange(2,32,2)
#a = W.cwt_a(ms, s**2,sampling_scale = 1.0)
#print a.shape
#plotcwt=N.clip(N.fabs(a.real), 0., 1000.)
##P.pcolormesh(plotcwt)
#im=P.imshow(plotcwt,vmax = 100, cmap=P.cm.jet,aspect='auto')
##im = P.pcolormesh(plotcwt)
##P.imshow(plotcwt)
#P.show()