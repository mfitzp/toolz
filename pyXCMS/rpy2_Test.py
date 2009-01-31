import os
import sys
import numpy as N

import rpy2.robjects as ro
import rpy2.rinterface as ri
import rpy2.robjects.numpy2ri

from interpolate import interpolate_spectrum

from scipy import ndimage#used for tophat filter
import time
#import baseline2 as bs2

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


def initRlibs(libList):
    libDict = {}

    for lib in libList:
        try:
            libDict[lib] = ro.r('library(%s)'%lib)
        except:
            errorMsg ='Error loading R library %s'%lib
            errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg

    return libDict

def list2rpyFuntions(strList):
    funcDict = {}
    for entry in strList:
        try:
            funcDict[entry] = ro.r['%s'%entry]
        except:
            errorMsg ='Error creating function %s'%entry
            errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg

    return funcDict

if __name__ == "__main__":
    import pylab as P
#    libList = ['MassSpecWavelet']
#    funcList = ['peakDetectionCWT','plotPeak']
#    initRlibs(libList)
#    funcDict = list2rpyFuntions(funcList)

    libList = ['xcms']
    initRlibs(libList)
    a = ro.r.help("findPeaks.centWave", htmlhelp = True)
    #    print type(a)
    print a
#    print funcDict

#    ro.r('data(exampleMS)')
#
#    ms = P.load('J15.csv', delimiter = ',')
#    x, ms = interpolate_spectrum(ms)
#    ms = normalize(topHat(ms, 0.01))
#    ms = roundLen(ms)
#
#
##    peakInfo = ro.r.peakDetectionCWT(ro.r.exampleMS)
#    peakInfo = ro.r.peakDetectionCWT(ms)
#    ro.globalEnv["peakInfo"] = peakInfo
##    ro.globalEnv["group"] = group
#    ro.r('majorPeakInfo = peakInfo$majorPeakInfo')
#    pInd = ro.r('peakIndex = majorPeakInfo$peakIndex')
#    pInd = N.array(pInd, dtype = N.int32)
##    print type(ro.r.exampleMS)
##    ms = N.transpose(N.array(ro.r.exampleMS))
###    print type(ms), ms.shape
##    rows = ms.shape[0]
##    ms.shape = (rows,)
#    P.plot(ms)
#    peaks = ms[pInd]
#    P.plot(pInd, peaks, 'ro')
#
#    P.show()

#    peakDetectionCWT(ms, scales = c(1, seq(2, 30, 2), seq(32, 64, 4)),
#                     SNR.Th = 3, nearbyPeak = TRUE, peakScaleRange = 5, amp.Th = 0.01,
#                     minNoiseLevel = amp.Th/SNR.Th, ridgeLength = 24, tuneIn = FALSE, ...)

#    data(exampleMS)
#    SNR.Th <- 3
#    peakInfo <- peakDetectionCWT(exampleMS, SNR.Th=SNR.Th)
#    majorPeakInfo = peakInfo$majorPeakInfo
#    peakIndex <- majorPeakInfo$peakIndex
#    plotPeak(exampleMS, peakIndex, main=paste('Identified peaks with SNR >', SNR.Th))


#class rpy2.robjects.BoolVector(obj)
#
#    Bases: rpy2.robjects.RVector
#
#    Vector of boolean (logical) elements
#
#class rpy2.robjects.IntVector(obj)
#
#    Bases: rpy2.robjects.RVector
#
#    Vector of integer elements
#
#class rpy2.robjects.FloatVector(obj)
#
#    Bases: rpy2.robjects.RVector
#
#    Vector of float (double) elements
#
#class rpy2.robjects.StrVector(obj)
#
#    Bases: rpy2.robjects.RVector
#
#    Vector of string elements

#in R:
#sum(0, na.rm = TRUE)
#
#in Python:
#from rpy2 import robjects
#
#myparams = {'na.rm': True}
#robjects.r.sum(0, **myparams)

#NUMPY EXAMPLE:
#
#import numpy
#
#ltr = robjects.r.letters
#ltr_np = numpy.array(ltr)

#import rpy2.robjects.numpy2ri for conversion of numpy 2 R


#import rpy2.robjects as robjects
#
#def my_ri2py(obj):
#    res = robjects.default_ri2py(obj)
#    if isinstance(res, robjects.RVector) and (len(res) == 1):
#        res = res[0]
#    return res
#
#robjects.conversion.ri2py = my_ri2py


#>>> pi = robjects.r.pi
#>>>  type(pi)
#<type 'float'>
#>>>



