from numpy import arange, cos, linspace, pi, sin, random
from scipy.interpolate import splprep, splev
from scipy.signal import cspline1d, cspline1d_eval

from interpolate import interpolate_spectrum
#from pycwt_Test import topHat, derivative, normalize, roundLen

import pylab as P
import numpy as N

from scipy import ndimage#used for tophat filter
import time

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

if __name__ == '__main__':

    ms = P.load('J15.csv', delimiter = ',')
    x, ms = interpolate_spectrum(ms)
    ms = normalize(topHat(ms, 0.01))
    ms = roundLen(ms)
    x = N.arange(len(ms))
    print ms.shape, x.shape
#    spl = cspline1d(ms)
#    print len(spl)
#    P.plot(spl)
    ## make ascending spiral in 3-space
    t=linspace(0,1.75*2*pi,200000)
    #
    x = sin(t)
    y = cos(t)
    z = t

    # add noise
    x+= random.normal(scale=0.1, size=x.shape)
    y+= random.normal(scale=0.1, size=y.shape)
    z+= random.normal(scale=0.1, size=z.shape)
#    print x.shape
    # spline parameters
    s=5000.0 # smoothness parameter
    k=2 # spline order
    nest=10 # estimate of number of knots needed (-1 = maximal)

    # find the knot points
    tckp,u = splprep([x,y,z],s=s,k=k,nest=-1)
#    tckp,u = splprep([x,ms],s=s,k=k,nest=-1)

    # evaluate spline, including interpolated points
    xnew,ynew,znew = splev(linspace(0,1,len(x)),tckp)


    P.subplot(1,1,1)
#    P.plot(ms)
    data,=P.plot(x,y,'bo',label='data')
    fit,=P.plot(xnew,ynew,'ro-',label='fit', ms = 3)

    #P.subplot(2,2,2)
    #data,=P.plot(x,z,'bo-',label='data')
    #fit,=P.plot(xnew,znew,'r-',label='fit')
    #P.legend()
    #P.xlabel('x')
    #P.ylabel('z')
    #
    #P.subplot(2,2,3)
    #data,=P.plot(y,z,'bo-',label='data')
    #fit,=P.plot(ynew,znew,'r-',label='fit')
    #P.legend()
    #P.xlabel('y')
    #P.ylabel('z')

    P.show()