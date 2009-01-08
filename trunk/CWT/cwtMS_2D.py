import pylab as P
import numpy as N

from iwavelets import pycwt as W

from interpolate import interpolate_spectrum

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

t1 = time.clock()
ms = P.load('N3_Norm.txt')
#ms = P.load('J15.csv', delimiter = ',')
#x, ms = interpolate_spectrum(ms)
#ms = normalize(topHat(ms, 0.01))
#ms = roundLen(ms)

print len(ms)

s = N.arange(2,32,2)#changed to 8 from 32
a = W.cwt_a(ms, s**2,sampling_scale = 1.0)
plotcwt=N.clip(N.fabs(a.real), 0., 1000.)
print "wavelet complete"
print time.clock()-t1, 'seconds'

fig1 = P.figure()
ax = fig1.add_subplot(211)
im=ax.imshow(plotcwt,vmax = 100, cmap=P.cm.jet,aspect='auto')
ax2 = fig1.add_subplot(212,sharex=ax)
##ax3 = fig1.add_subplot(313,sharex=ax)
#ax.plot(plotcwt[0])
#ax2.plot(ms, 'r')
##ax2.plot(plotcwt[1], ':r')
##
##
##mNoise = plotcwt[0].mean()
##stdNoise = plotcwt[0].std()
##mNoise = 5*stdNoise+mNoise
###ax.hlines(mNoise, 0,len(plotcwt[0]), linestyles = 'dashed', label = 'no_legend')
###
mNoiseNorm = normalize(plotcwt[0]).mean()
stdNoiseNorm = normalize(plotcwt[0]).std()
mNoiseNorm = 3*stdNoiseNorm+mNoiseNorm
#ax.hlines(mNoiseNorm, 0,len(plotcwt[0]), linestyles = 'dashed', label = 'no_legend')
#
critSum = N.zeros(1)

for i,row in enumerate(plotcwt):
    if i>1:
#        ax.plot(row,label = '%s'%i)
        temp = normalize(derivative(row))
#        tempLine, = ax2.plot(temp,'-', alpha=0.4)
#        c = tempLine.get_color()
        criterion = (temp < 0.25) & (temp > -0.25) & (normalize(row) >= mNoiseNorm)
        tempZero = N.where(criterion)[0]
        critSum = N.append(critSum,tempZero)
        zeroPnts = N.zeros_like(tempZero)+i
        ax.plot(tempZero,zeroPnts, 'o', alpha = 0.4, color = 'k')
##
###ax2.grid(True)
ax2.plot(ms, 'r', alpha = 0.8)
###ax.legend()
##
##    #plotcwt[i] = derivative(row)
##
#
#P.figure()
#critSum = critSum.flatten()
#numBins = len(critSum)*2#len(ms)*0.1
##P.plot(critSum)
#print type(critSum), len(critSum)
#P.hist(critSum, bins = numBins)
#P.plot(ms, ':r', alpha = 0.5)
P.show()