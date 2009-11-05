
from scipy.signal import cspline1d, cspline1d_eval
#import matplotlib.pylab as P

#from scipy.interpolate import interp1d
import time
import smoothingFilter as smoothF
#import decimate as D
import numpy as N
#from scipy import ndimage#used for tophat filter

import supportFunc as SF



def crudeNoiseEstimate(datArray, sigmaThresh=3):
    '''
    Accepts a numpy array and zeros the values below the user defined threshold
    '''
    mean = datArray.mean()
    min = datArray.min()
    std = datArray.std()
    thresh = mean+std*5
    #first pass selection to minimize contribution of large peaks
    #only takes values below the thresh
    #should use clip
    noiseArray = N.select([datArray<thresh],[datArray],default = min)


    mean2 = noiseArray.mean()
    std2 = noiseArray.std()
    thresh2 = mean2+std2*sigmaThresh

    return thresh2

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
    ySpec = smoothF.savitzky_golay(noiseSpec, kernel = 11, order = 3)
#    sCoef = cspline1d(noiseSpec)
#    x = N.arange(len(spec))
#    ySpec = cspline1d_eval(sCoef,x)
    noise = N.zeros_like(spec)
    for i in xrange(len(xSpec[:-1])):
        noise[xSpec[i]:xSpec[i+1]] = ySpec[i]



    return noise, minNoise
    #return xSpec, ySpec


if __name__ == '__main__':
    import pylab as P
#    ms = P.load('J15.csv', delimiter = ',')
#    x, ms = interpolate_spectrum(ms)
#    ms = SF.normalize(SF.topHat(ms, 0.01))
#    ms = SF.roundLen(ms)
#    ms = P.load('N3_Norm.txt')
    dat = P.load('J5.csv', delimiter = ',')
    x = dat[:,0]
    ms = dat[:,1]
    x, mz = SF.interpolate_spectrum_XY(x, ms)
    print ms.max(), len(ms)
#    x = N.arange(len(ms))
#    print ms.shape, x.shape

#    x = N.r_[0:10]
#    dx = x[1]-x[0]
#    newx = N.r_[-3:13:0.1]  # notice outside the original domain
#
#    y = N.sin(x)
#    cj = cspline1d(y)
#    newy = cspline1d_eval(cj, newx, dx=dx,x0=x[0])
#    print x.shape, newx.shape, cj.shape
    print x[-2]-x[-1], x[1]-x[0]
    numSegs = int(len(ms)*(x[1]-x[0]))
    print "Numsegs: ", numSegs
#    x, msSm = SplitNSmooth(ms, numSegs, 5)
    noise,minNoise = SplitNSmooth(ms, numSegs, 1.5)

    print minNoise

#    noise = N.zeros_like(ms)
#    for i in xrange(len(x[:-1])):
#        print x[i], x[i+1]
#        noise[x[i]:x[i+1]] = msSm[i]

#    print len(ms), numSegs

    P.plot(ms, 'r', alpha = 0.5)
#    P.plot(x, msSm, 'ob', alpha = 0.5)
    P.plot(noise, '-b', alpha = 0.5)

#    P.plot(newx, newy, x, y, 'o')
    P.show()
