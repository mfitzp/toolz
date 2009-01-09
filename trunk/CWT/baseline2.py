
from scipy.signal import cspline1d, cspline1d_eval
import matplotlib.pylab as P

from interpolate import interpolate_spectrum

from scipy.interpolate import interp1d
import time
import smoothingFilter as SF
import decimate as D
import numpy as N
from scipy import ndimage#used for tophat filter

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
    dy = y/2
    #one more value is added because the length
    # of y and dy are 1 less than y_data
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
    ySpec = SF.savitzky_golay(noiseSpec, kernel = 11, order = 3)
#    sCoef = cspline1d(noiseSpec)
#    x = N.arange(len(spec))
#    ySpec = cspline1d_eval(sCoef,x)
    noise = N.zeros_like(spec)
    for i in xrange(len(xSpec[:-1])):
        noise[xSpec[i]:xSpec[i+1]] = ySpec[i]



    return noise, minNoise
    #return xSpec, ySpec


if __name__ == '__main__':

#    ms = P.load('J15.csv', delimiter = ',')
#    x, ms = interpolate_spectrum(ms)
#    ms = normalize(topHat(ms, 0.01))
#    ms = roundLen(ms)
#    ms = P.load('N3_Norm.txt')
    ms = P.load('exampleMS.txt')
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
    numSegs = int(len(ms)*0.0015)
    print "Numsegs: ", numSegs
#    x, msSm = SplitNSmooth(ms, numSegs, 5)
    noise,minNoise = SplitNSmooth(ms, 500, 5)
    print minNoise

#    noise = N.zeros_like(ms)
#    for i in xrange(len(x[:-1])):
#        print x[i], x[i+1]
#        noise[x[i]:x[i+1]] = msSm[i]

#    print len(ms), numSegs

    P.plot(ms, 'r:')
#    P.plot(x, msSm, 'ob', alpha = 0.5)
    P.plot(noise, '-b', alpha = 0.5)

#    P.plot(newx, newy, x, y, 'o')
    P.show()
