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
loadA = True
normOk = False
#loadA = True
if loadA:
#    ms = P.load('N3_Norm.txt')
    ms = P.load('exampleMS.txt')
    ms = normalize(ms)
    ms = topHat(ms, 0.01)
#    ms = ms[5000:11000]
#    ms = ms[7000:9000]
else:
    ms = P.load('J15.csv', delimiter = ',')
    x, ms = interpolate_spectrum(ms)
    ms = normalize(topHat(ms, 0.01))
    ms = roundLen(ms)

print len(ms)

#s = N.arange(2,32,2)#changed to 8 from 32
s1 = N.arange(2,32,2)
s2 = N.arange(32,64,4)
s = N.append(s1, s2)
a = W.cwt_a(ms, s,sampling_scale = 1.0)
plotcwt=N.clip(N.fabs(a.real), 0., 1000.)
print "wavelet complete"
print time.clock()-t1, 'seconds'
print "CWT Shape: ", plotcwt.shape

fig1 = P.figure()
ax = fig1.add_subplot(211)
ax2 = fig1.add_subplot(212,sharex=ax)

im=ax2.imshow(plotcwt,vmax = 100, cmap=P.cm.jet,aspect='auto')
#ax2.plot(plotcwt[1], alpha = 0.7, label = '1')
ax.plot(plotcwt[0], alpha = 0.7, label = '0')



if normOk:
#    ax.plot(normalize(plotcwt[0]),'b', label = '0')
#    ax.plot(normalize(plotcwt[1]),'r', label = '1')
    numSegs = int(len(plotcwt[0])*0.0015)
    if numSegs < 500:
        numSegs = 500
    noiseEst, minNoise = bs2.SplitNSmooth(normalize(ms),numSegs, 5)
    ax.plot(noiseEst, '-r', alpha = 0.5, label = 'smoothed')
    ax.plot(normalize(ms), 'g',alpha = 0.4, label = 'ms')
    print 'Normalized'
    mNoise = normalize(plotcwt[0]).mean()
    stdNoise = normalize(plotcwt[0]).std()
    mNoise = 3*stdNoise+mNoise

else:
#    ax.plot(plotcwt[0],'b', label = '0')
#    ax.plot(plotcwt[1],'r', label = '1')
    numSegs = int(len(plotcwt[0])*0.0015)
    if numSegs < 500:
        numSegs = 500
    noiseEst, minNoise = bs2.SplitNSmooth(ms,numSegs, 5)
    ax.plot(noiseEst, '-r', alpha = 0.5, label = 'smoothed')
    ax.plot(ms, 'g',alpha = 0.4, label = 'ms')
    mNoise = plotcwt[0].mean()
    stdNoise = plotcwt[0].std()
    mNoise = 3*stdNoise+mNoise

#ax.hlines(mNoise, 0,len(plotcwt[0]), linestyles = 'dashed', label = 'mNoise')
#
critSum = N.zeros(1)

cwtPeakDict = {}

t2 = time.clock()
revRowArray = N.arange((plotcwt.shape[0]-1),1,-1)#steps backwards
for i in revRowArray:
    row = plotcwt[i]
#for i,row in enumerate(plotcwt):
    if i>0:
        scaleWin = 1#s[i]
        if scaleWin < 5:
            scaleWin = 2
#        print scaleWin


#        ax2.plot(row,label = '%s'%i)
        normRow = normalize(row)
        rowDeriv = derivative(normRow)
#        if i>2 and i<8:
##            ax.plot(row, '-', alpha = 0.5, label = 'Row')
#            ax.plot(rowDeriv, 'o', alpha = 0.5, label = 'Deriv')
###        tempLine, = ax2.plot(temp,'-', alpha=0.4)
##        c = tempLine.get_color()
        'criterion 1 -- above the threshold and a zero crossing in the derivative'

        criterion = (rowDeriv < 0.75) & (rowDeriv > -0.75) & (normRow >= minNoise)
        tempLocEst = N.where(criterion)[0]
        tempLoc = []
        for m in tempLocEst[:-1]:#need to exclude last element so we don't get an IndexError for the rowDeriv array
            if N.sign(rowDeriv[m]) > N.sign(rowDeriv[m+1]):
                if normRow[m] >= noiseEst[m]:
                    tempLoc.append(m)

        tempLoc = N.array(tempLoc)
        zeroPnts = N.zeros_like(tempLoc)+i
        if i>1:
            ax2.plot(tempLoc,zeroPnts, 'o', alpha = 0.7, color = 'k')

#        tempLoc = N.array(tempLocEst)
        'criterion 2 -- within the window size'
        if i == plotcwt.shape[0]-1:#this is the first iteration...sets up dictionary
            for j in tempLoc:
                rowRef = [i]
                cwtPeakDict[j]=[j,1, rowRef]#peaklocation, times found

        else:
#            print i
            'criterion where the current peak locations are within the window of the previously found peaks'
            rowThresh = 3
#            for peakLoc in tempLoc:
            keys2pop = []
            keyList = cwtPeakDict.keys()#you can use iterkeys in the following because the dictionary is changing.
            for key in keyList:
                item = cwtPeakDict[key]
                for peakLoc in tempLoc:
                    'checks to see if subsequent peak maxima are within the scale window'
                    if item[0] <= (peakLoc+scaleWin) and item[0] >= (peakLoc-scaleWin):
                        #is the last peak found within rowThresh rows otherwise create a new entry
                        if item[2][-1]-i <= rowThresh:
                            if not cwtPeakDict.has_key(peakLoc):
                                keys2pop.append(key)
                            rowRef = item[2]
                            rowRef.append(i)
                            cwtPeakDict[peakLoc] = [peakLoc, item[1]+1, rowRef]

    #                            cwtPeakDict.pop(key)
                        else:
                            rowRef = [i]
                            cwtPeakDict[peakLoc] = (peakLoc, 1, rowRef)
            for key in keys2pop:
                if cwtPeakDict.has_key(key):
                    cwtPeakDict.pop(key)

            for peakLoc in tempLoc:#create a new entry if the peak doesn't have a correspondent peak
                if not cwtPeakDict.has_key(peakLoc):
                    rowRef = [i]
                    cwtPeakDict[peakLoc] = (peakLoc, 1, rowRef)

#                    else:
#                        if item[1]-1 <= 0:
#                            cwtPeakDict.pop(key)
#                        else:
#                            cwtPeakDict[key] = [item[0],item[1]-1]



#            peakLocCrit = (tempLoc < tempLocPrev+scaleWin) & (tempLoc > tempLocPrev-scaleWin)
            'this criterion makes it so the current index is kept in the peakLoc index and the old one disgarded'
#            tempLoc = N.where(peakLocCrit)[0]

            #for peakLoc in tempLocPrev:


print 'Peak Finding: ', time.clock() - t2
cwtLoc = []

for val in cwtPeakDict.itervalues():
    if val[1]>=7:
        cwtLoc.append(val[0])
        print "\tValues", val
#    else:
#        print "Values", val

cwtLoc = N.array(cwtLoc)
cwtLocInt = N.zeros_like(cwtLoc)+1
ax2.plot(cwtLoc,cwtLocInt, 'ro', alpha = 0.9)

#ax.legend()


P.show()



##P.figure()
##critSum = critSum.flatten()
##numBins = len(critSum)*2#len(ms)*0.1
###P.plot(critSum)
##print type(critSum), len(critSum)
##P.hist(critSum, bins = numBins)
##P.plot(ms, ':r', alpha = 0.5)




#        critSum = N.append(critSum,tempLoc1)
#        zeroPnts = N.zeros_like(tempLoc)+i
#        if i>1:
#            ax2.plot(tempLoc,zeroPnts, 'o', alpha = 0.7, color = 'k')
#        print len(tempLoc)
#        tempLocPrev = tempLoc


#for i,row in enumerate(plotcwt):
#    if i<plotcwt.shape[0]-1:
#
#
##        ax2.plot(row,label = '%s'%i)
#        temp1 = normalize(derivative(row))
#        temp2 = normalize(derivative(plotcwt[i+1]))
#        tempDiff1 = N.zeros_like(row)
#        tempDiff2 = N.zeros_like(row)
###        tempLine, = ax2.plot(temp,'-', alpha=0.4)
##        c = tempLine.get_color()
#        criterion1 = (temp1 < 0.25) & (temp1 > -0.25) & (normalize(row) >= mNoise)
#        criterion2 = (temp2 < 0.25) & (temp2 > -0.25) & (normalize(plotcwt[i+1]) >= mNoise)
#        tempZero1 = N.where(criterion1)[0]
#        tempZero2 = N.where(criterion2)[0]
#        tempDiff1[tempZero1] = i
#        tempDiff2[tempZero2] = i
##        critSum = N.append(critSum,tempZero)
##        zeroPnts = N.zeros_like(tempZero)+i
##        ax2.plot(tempZero,zeroPnts, 'o', alpha = 0.4, color = 'k')
#        ax2.plot(N.abs((tempDiff2-tempDiff1)), '-o',ms = 3,alpha = 0.5)