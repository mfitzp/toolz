'''
Questions weather to normalize or not when comparing?
'''

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

t1 = time.clock()
loadA = False
normOk = False
#loadA = True
if loadA:
#    ms = P.load('N3_Norm.txt')
    ms = P.load('exampleMS.txt')
    ms = normalize(ms)
    ms = topHat(ms, 0.01)
#    ms = ms[8000:8500]
##    ms = ms[7000:9000]
else:
    'Noisy_IMS_XY.csv'
    'BSA_XY_Full.csv'
    'J15.csv'
    'Tryptone.csv'
    ms = P.load('Tryptone2.csv', delimiter = ',')
    x, ms = interpolate_spectrum(ms)
    ms = normalize(topHat(ms, 0.01))
    ms = roundLen(ms)
    ms = ms[0:len(ms)*.75]
    x = x[0:len(ms)]

print len(ms)

#s = N.arange(2,32,2)#changed to 8 from 32
s1 = N.arange(2,30,2)
s2 = N.arange(32,64,4)
#Best for BSA High Res TOF
#s1 = N.arange(2,8,2)
#s2 = N.arange(12,48,4)
print len(s1), len(s2)
s = N.append(s1, s2)
a = W.cwt_a(ms, s,sampling_scale = 1.0, wavelet='DOG')#Morlet, DOG
plotcwt=N.clip(N.fabs(a.real), 0., 1000.)
print "wavelet complete"
print time.clock()-t1, 'seconds'
print "CWT Shape: ", plotcwt.shape

fig1 = P.figure()
ax = fig1.add_subplot(211)
ax2 = fig1.add_subplot(212)#,sharex=ax)

im=ax2.imshow(plotcwt,vmax = 1, cmap=P.cm.jet,aspect='auto')
#ax2.plot(plotcwt[1], alpha = 0.7, label = '1')
#ax.plot(plotcwt[0], alpha = 0.7, label = '0')
minSNR = 5
numSegs = len(ms)/100
#numSegs = len(ms)/10#int(len(plotcwt[0])*0.0015)
#if numSegs < 1000 and len(ms) > 1000:
#    numSegs = 1000
#else:
#    numSegs = len(ms)/2
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
    mNoise = normalize(plotcwt[0]).mean()
    stdNoise = normalize(plotcwt[0]).std()
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
    mNoise = plotcwt[0].mean()
    stdNoise = plotcwt[0].std()
    mNoise = 3*stdNoise+mNoise

#ax.hlines(mNoise, 0,len(plotcwt[0]), linestyles = 'dashed', label = 'mNoise')
#
critSum = N.zeros(1)

cwtPeakDict = {}
cwtPeakLoc = []
t2 = time.clock()
revRowArray = N.arange((plotcwt.shape[0]-1),1,-1)#steps backwards
for i in revRowArray:
    row = plotcwt[i]
    if i>2:
        scaleWin = 2


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
ax2.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'oy', alpha = 0.4)
print 'Peak Finding: ', time.clock() - t2

peakLoc = []

t3 = time.clock()
cClass, tType, Eps, boolAns = dbscan(cwtPeakLoc, 4)#, Eps = 5)
print 'Peak Cluster: ', time.clock() - t3
if boolAns:
    print cClass.max(), len(tType), Eps
    i = cClass.max()
    for m in xrange(int(i)+1):
        ind = N.where(m == cClass)
        temp = cwtPeakLoc[ind]

        ax2.plot(temp[:,0],temp[:,1],'-s', alpha = 0.7, ms = 3)
        if len(temp) > 0:
            sortInd = temp[:,0].argsort()
            temp = temp[sortInd]
            tempDiffX = N.diff(temp[:,0])
            tempDiffY = N.diff(temp[:,1])
    #        print tempDiffX
    #        print tempDiffY, '\n'
            diffSumX = tempDiffX.sum()

    #        if diffSumX <= len(tempDiffX)*2:
            i = 0
            rowThresh = 3
            for j in tempDiffY:
                if j <= rowThresh:
                    i+=1
                else:
                    i+=-1
            if i >= rowThresh:
                maxInd = temp[:,1].argmin()
                xVal = temp[maxInd][0]
#                if ms[xVal] >= noiseEst[xVal]:#*1.1:#minNoise:

#                print "Found Peak ", i, xVal, tempDiffY, '\n'
        #                ax.vlines(temp[:,0].min(), 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)
                ax.vlines(x[xVal], 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)
                peakLoc.append(x[xVal])
                print x[xVal]
#                else:
#                    print xVal, ms[xVal], noiseEst[xVal]
#            else:
#                print "No Peak ", i, tempDiffY, '\n'
    #        else:
    #            print "diffSumX too long ", diffSumX, len(tempDiffY), tempDiffY
    #        print temp[:,1]



#N.savetxt('peakLoc.csv', N.array(peakLoc), delimiter = ',')
print len(noiseEst)
P.show()

