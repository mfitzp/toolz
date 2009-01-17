
import sys
import os

from PyQt4.QtGui import QFileDialog,  QApplication
from PyQt4 import QtCore,  QtGui
import numpy as N
import scipy as S
import numpy.fft.fftpack as F
import scipy.optimize as optimize


import time


import pylab as P

def expGauss(x, pos, wid, tConst, expMod = 0.5, amp = 1):
    '''
    x -- numpy array
    pos -- centroid location
    wid -- width
    tConst -- time constance for exponential decay
    amp -- intensity of peak
    expMod -- modifies the intensity of the peak -- must be a float

    Forumulas used:

    y = a * exp(-0.5 * (x-b)^2 / c^2) --traditional gaussian forumla
    exp = N.exp(-1*expMod*N.arange(0,len(y))/Const) --function that is merged with the gaussian

    Note if expMod is too small (i.e. goes towards zero) the function will return a flat line.
    '''
    expMod *=1.0
    G = amp * N.exp(-0.5*((x-pos)/(wid))**2)
    expG = expBroaden(G, tConst, expMod)
    return expG, G

def expBroaden(y, t, expMod):
    fy = F.fft(y)
    a = N.exp(-1*expMod*N.arange(0,len(y))/t)
    fa = F.fft(a)
    fy1 = fy*fa
    yb = (F.ifft(fy1).real)/N.sum(a)
    return yb


class PeakFitThread:#(QtCore.QThread):
    def __init__(self, main=None, parent = None):
#        QtCore.QThread.__init__(self, parent)

        if main != None:
            self.parent = main
        else:
            self.parent = None
        self.finished = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.spectrum = None


        self.peakFitOK = False
        self.peakInfo = None

        self.chromX = None
        self.chromY = None

        self.numSegs = None

        self.ready = False


    def getPeakInfo(self):
        if self.peakFitOK:
            return self.peakInfo
        else:
            print "No PeakInfo exists--run peakFind again otherwise an error occured that did not commit the PeakInfo array to memory!"
            return None

    def initSpectrum(self, chromY, peakInfo, chromX = None):
            '''
            Accepts the chromatographic data to fit as X,Y arrays: chromX and chromY respectively
            the peakInfo from the peak finding must also be passed as this has the original peak locations
            '''
            if chromX == None:
                chromX = N.arange(len(chromY))
            if len(chromX)>0 and len(chromY)>0 and len(peakInfo)>0:
                self.chromX = chromX
                self.chromY = chromY
                self.peakInfo = peakInfo

                self.ready = True

    def getGaussian(self, X, Params):
        return Params[0]*N.exp(-0.5*(X-Params[1])**2/Params[2]**2)

    def errFuncGaussian(self, Params, X, compY):
        return self.getGaussian(X, Params) - compY

    def fitGaussian(self, X, Y, intensity, location, width):

        #p[0] -- intensity, p[1] -- location, p[2] -- width
        fitfuncG = lambda p, x: p[0]*N.exp(-0.5*(x-p[1])**2/p[2]**2) # Target function
        errfuncG = lambda p, x, y: fitfuncG(p, x) - y # Distance to the target function
        initialP = [intensity,location,width]
        xVals = N.arange(len(X))
        fitP, cov, infodict, errmsg, success = optimize.leastsq(errfuncG, initialP[:], args=(xVals, Y), full_output = 1)
#        fitP, cov, infodict, errmsg, success = optimize.leastsq(self.errFuncGaussian, initialP[:], args = (X, Y), full_output = 1)
        if success:
            evalFunc = fitfuncG(fitP,xVals)
#            evalFunc = self.getGaussian(N.arange(len(X)),fitP)
            self.ax.plot(X,evalFunc, '--r')
            chi2G = N.sum((evalFunc-Y)**2 / evalFunc)
            areaG = N.trapz(evalFunc, xVals)
            areaG2 = N.trapz(Y, xVals)
            print areaG, areaG2, (areaG/areaG2)*100, chi2G
            return chi2G, areaG
        else:
            return None, None


    def fitExpGaussian(self, X, Y, intensity, location, width, tConst = 100, expMod = 1):
        #p[0] -- intensity, p[1] -- location, p[2] -- width, p[3]--tConst, p[4] -- expMod
        fitfuncExpG = lambda p, x: expGauss(x, p[1], p[2], p[3], p[4], p[0])[0]
        errfuncExpG = lambda p, x, y: fitfuncExpG(p, x) - y # Distance to the target function
        initialP = [intensity, location, width, tConst, expMod]
        xVals = N.arange(len(X))
        fitP, cov, infodict, errmsg, success = optimize.leastsq(errfuncExpG, initialP[:], args=(xVals, Y), full_output = 1)
        if success:
            evalFunc = fitfuncExpG(fitP,xVals)
            self.ax.plot(X,evalFunc, ':g', ms = 2, lw = 2)
            chi2ExpG = N.sum((evalFunc-Y)**2 / evalFunc)
            areaExpG = N.trapz(evalFunc, X)
            return chi2ExpG, areaExpG
        else:
            return None, None



    def getArea(self, peakInfo):
        peakLoc = peakInfo['peakLoc']#:N.array(peakLoc),
        peakInt = peakInfo['peakInt']#'peakInt':N.array(peakInt),
        peakWidth = peakInfo['peakWidth']#'peakWidth':N.array(peakWidth),
        peakAreaOld = peakInfo['peakArea']#'peakArea':N.array(peakArea)
        peakArea = N.zeros_like(peakWidth)
        numPeaks = len(peakLoc)
        specLen = len(self.chromY)

        for i in xrange(numPeaks):

            location = peakLoc[i]
            width = peakWidth[i]
            intensity = peakInt[i]
            #create the moments for each distribution
            #width is at half-max with equals 2.35*sigma
            #full width = 4*sigma
            #width is in points
            sigma = width/2.35
            gWidth = int(N.ceil(5*sigma))
            #initially to be safe let's double the gWidth
            expWidth = N.ceil(gWidth*1.5)

            if (location-gWidth) < 0:
                start = 0
            else:
                start = int(N.round(location-gWidth))

            if (location+gWidth) > specLen:
                stopG = specLen
            else:
                stopG = int(N.round(location+gWidth))

            if (location+expWidth) > specLen:
                stopExpG = specLen
            else:
                stopExpG = int(N.round(location+expWidth))
            #select a range from the original chromatogram
            #the start is assumed to be same for a G and expG peak
            #as tailing peaks are what we're after
            gX = self.chromX[start:stopG]
            gY = self.chromY[start:stopG]
            expX = self.chromX[start:stopExpG]
            expY = self.chromY[start:stopExpG]

#            print i,' of ', numPeaks, len(self.chromX), start, stopG, stopExpG, gWidth, expWidth
            chi2ExpG, areaExpG = self.fitExpGaussian(expX, expY, intensity, location-start, width)
            chi2G, areaG = self.fitGaussian(gX, gY, intensity, location-start, width)

            if chi2ExpG == None and chi2G != None:
                peakArea[i] = areaG
            elif chi2G == None and chi2ExpG != None:
                peakArea[i] = areaExpG
            elif chi2G != None and chi2ExpG != None:
                if chi2G < chi2ExpG:
                    peakArea[i] = areaG
                else:
                    peakArea[i] = areaExpG

#            print peakArea[i], peakAreaOld[i]

        return peakArea


    def run(self):
        self.finished = False
        if self.ready:
#            try:
            t1 = time.clock()
            ###################
            self.fig = P.figure()
            self.ax = self.fig.gca()
            self.ax.plot(self.chromX, self.chromY, '-o', ms = 2)
            self.ax.plot(self.peakInfo['peakLoc'], self.peakInfo['peakInt'], 'ro', alpha = 0.4)

            ###################
            self.peakInfo['peakArea'] = self.getArea(self.peakInfo)
            self.peakFitOK = True
            print "Peak Fitting Time: ", time.clock()-t1
#                self.emit(QtCore.SIGNAL("finished(bool)"),self.peakFitOK)
#            except:
#                errorMsg ='Error with PeakFitThread\n'
#                errorMsg += "Sorry: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
#                print errorMsg
        else:
            print "Error fitting peaks...data not set or a more serious error has occured."


    def stop(self):
        print "stop try"
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        print "stop try"
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()


if __name__ == "__main__":
    import pylab as P

    chrom = P.load('chrom1D.csv', delimiter = ',')
    print chrom.shape
    peakInfo = P.load('chrom1DPeaks.csv', delimiter = ',')
#    P.plot(chrom, 'b')
#    P.plot(peakInfo[:,0], peakInfo[:,1], 'ro', alpha = 0.4)

    peakDict = {}
    peakDict['peakLoc'] = peakInfo[:,0]
    peakDict['peakInt'] = peakInfo[:,1]
    peakDict['peakWidth'] = peakInfo[:,2]
    peakDict['peakArea'] = peakInfo[:,3]

    peakFitThread = PeakFitThread()
    peakFitThread.initSpectrum(chrom, peakDict, chromX = None)
    peakFitThread.run()
#    peakFitThread.start()
#    testSpec = P.load('TICSam.txt')
#    refSpec = refSpec[100000:110000]
#    numSegs = 500
#    SNR = 2
#    fig = P.figure()
#    ax = fig.add_subplot(111,  title = 'Picked')
#
##    peakLoc, peakInt, peakWidth = SplitNFind(refSpec, numSegs, 25, minSNR = SNR)
#    peakThread = PeakFitThread()
#    peakThread.initSpectrum(refSpec, minSNR = 3, numSegs = 500, smthKern = 15, peakWidth = 25)
#    peakThread.start()
#    time.sleep(13)
#    peakInfo = peakThread.getPeakInfo()
#    ax.plot(refSpec)
#    ax.plot(peakInfo['peakLoc'],peakInfo['peakInt'], 'ro', alpha = 0.4)
#
##    ax2 = fig.add_subplot(212,  title = 'Histo')
##    ax2.hist(peakInt, log = True, bins = 1000)

    P.show()


###################################################

#    ax = fig.add_subplot(111,  title = 'Unaligned')
#    j = 5000
#    for i in range(20):
#        a = refSpec[65000+j*i:69000+j*i]
#        peakInfo = PF.findPeaks(a, peakWidth = 15)
#        ax.plot(a)
#
#        if len(peakInfo) > 0:
#            ax.plot(peakInfo['peak_location'],  peakInfo['peak_intensity'],  'ro')
#            #ax.plot(peakInfo['smoothed_deriv'])
#            #ax.plot(peakInfo['smoothed_data'])
#            #print peakInfo
#
#
#    P.show()



##########################################

#    columns = 1200
#
#
#    i = 0
#    for item in dataDict.iteritems():
#        print item[0]
#        tic1D = item[1]#(item[1]/item[1].max())*100
#        TIC = make2DTIC(tic1D, columns)
#        rows = int(len(tic1D)/columns)
#        imAspect = rows/(columns*1.0)
#        print imAspect
#        if '_AL' not in item[0]:
#            #ax.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower', aspect = imAspect, cmap = cmaps[i])
#            ax.contour(N.transpose(TIC), alpha = 1,  origin = 'lower',  cmap = cmaps[i])
#
#        else:
#            #ax2.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower',  aspect = imAspect,   cmap = cmaps[i])
#            ax2.contour(N.transpose(TIC), alpha = 1,  origin = 'lower',  cmap = cmaps[i])
#
#        i+=0
    #ax.set_xlim(0,rows)
    #ax.set_ylim(0,columns)
    #ax2.set_ylim([0,columns])
    #P.show()


