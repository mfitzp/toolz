
'''
Notes:

A point factor of 0.01 is appropriate for the tophat filter of mass spectra.
This should be done before comparison, otherwise noise in the spectrum can severely diminish the
corr coeff.  (e.g. 0.46 vs 0.96) before and after filtering.

Question?  Do we need to do a 2D correlation or is there a smart way to do an 1D Xcorrelation based upon BPC in a segment?

Sunday, Nov, 2,

So the question remains how to weight appropriately the correlations that are most meaningful.  Peak pick?
Only those that have a certain correlation coefficient?  And also, how to detect when there is no statistical correlation
and perform no shift.
'''

import numpy as N
import pylab as P
import scipy as S
import tables as T


from pylab import cm
cmaps = [cm.spectral,  cm.hot,  cm.spectral]

from LECO_IO import ChromaTOF_Reader as CR
import SplitNStich as SNS
import PeakFunctions as PF


def corrMatrix(ref, sam, focusList = None, topHat = True):

    rows = ref.shape[0]
    cols = ref.shape[1]

    if topHat:
        ref = topHatMatrix(ref)
        sam = topHatMatrix(sam)


    outMtx = N.zeros_like(ref)#make a matrix that has the same dimensions as the reference
    maxShift = []#array to hold the maximum shift observed for each mz value
    corVals = []#array to hold the cross correlation array for each EIC

    if focusList != None and len(focusList)>0:
        for i in focusList:
            i = int(N.round(i))
            rSic=ref[:, i]#extracts the local chromatogram for each mz value
            sSic=sam[:, i]

            rSic = crudeNoiseFilter(rSic, 3)
            sSic = crudeNoiseFilter(sSic, 3)

            cor, corVal, shift = getShift(rSic, sSic)
            corVals.append(corVal)
            if shift == -len(rSic)/2:
                maxShift.append(0)
            else:
                maxShift.append(shift)

            outMtx[:, i]= cor

    else:
        for i in xrange(cols):
            rSic=ref[:,i]#extracts the local chromatogram for each mz value
            sSic=sam[:,i]

            cor, corVal, shift = getShift(rSic, sSic)
            corVals.append(corVal)
            if shift == -len(rSic)/2:
                maxShift.append(0)
            else:
                maxShift.append(shift)

            outMtx[:,i]= cor

    return outMtx, N.array(maxShift), N.array(corVals)


def crudeNoiseFilter(datArray, sigmaThresh):
    '''
    Accepts a numpy array and zeros the values below the user defined threshold
    '''
    mean = datArray.mean()
    std = datArray.std()
    thresh = mean+std*5
    #first pass selection to minimize contribution of large peaks
    #only takes values below the thresh
    noiseArray = N.select([datArray<thresh],[datArray],default = thresh)

    mean2 = noiseArray.mean()
    std2 = noiseArray.std()
    thresh2 = mean2+std2*sigmaThresh
    #takes values above the final threshold and zeros the others.
    filtered = N.select([datArray>thresh2],[datArray],default = 0)

    return filtered




def getShift(ref, sam):
    '''
    Returns the optimal shift for two arrays based upon the maximum of the cross correlation.
    Also returns the correlation array, and maximum correlation value
    '''

    cor = N.correlate(ref, sam, mode = 'same')
    corVal = N.correlate(ref, sam, mode = 'valid')[0]#returns max correlation
    shift = N.round(cor.argmax()-len(ref)/2)#divide by 2 because we want to know shift relative to 0

    return cor, corVal, shift




def topHatMatrix(inputMZMtx):
    '''
    Accepts a 2D numpy array with each row corresponding to a new mz value
    '''
    numRows = inputMZMtx.shape[0]
    for i in xrange(numRows):
        #replaces existing mass spectrum with a TH filtered version
        inputMZMtx[i] = SNS.topHat(inputMZMtx[i], factor = 0.01)

#    print "Finished TopHat filtering of m/z Matrix"
    return inputMZMtx



def getBPC(mzMtx):
    '''
    Gets base peak chromatogram
    '''
    rows = mzMtx.shape[0]

    sic = N.zeros(rows)
    #zVals = N.zeros(rows)

    for i in xrange(rows):
        mz=mzMtx[i]
        sic[i]= mz.max()
        #mzVal = mz.argmax()

    return sic


if __name__ == "__main__":

    fn = 'TAi-R1_T.h5'#'TAi-R1.h5'#open_file()
    fn2 = 'TCiv-R1_T.h5'
    f = T.openFile(fn,  'r')
    f2 = T.openFile(fn2,  'r')

    mzR = f.root.dataCube
    mzS = f2.root.dataCube

    specStart = 312900
    specLen = 400

    rows = mzR.shape[0]
    cols = mzR.shape[1]

    randTest = S.rand(specLen*cols)
    randTest.shape = (specLen,cols)

    imR = SNS.normArray(mzR[specStart:specStart+specLen])
    #imS = SNS.normArray(mzS[specStart:specStart+specLen])
    imS = randTest
    #rowS = SNS.normArray(mzS[65000])

    f.close()
    f2.close()

    sicR = getBPC(imR)
    sicS= getBPC(imS)
    cor2D, maxShift, corVals = corrMatrix(imR, imS)#, focusList = [41,42,43,45,84,83,82,81])

    cor = N.correlate(sicR, sicS, mode = 'same')
    shift = N.round(cor.argmax()-len(sicR)/2)#gets value to shift by
    print shift

    corVals = crudeNoiseFilter(corVals, 2)
    corIndices = N.where(corVals>0)[0]
    #corMax = corVals.argsort()
    corMax = corVals[corIndices]

    fig = P.figure()
    ax = fig.add_subplot(411)

    #ax.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower', aspect = imAspect, cmap = cmaps[i])
    ax.contour(imR, alpha = 1,  origin = 'lower',  cmap = cmaps[0], label = 'R')
    ax.contour(imS, alpha = 0.5,  origin = 'lower',  cmap = cmaps[1], label = 'S')

    ax2 = fig.add_subplot(412)

    ax2.plot(sicR)
    ax2.plot(sicS)

    ax3 = fig.add_subplot(413)
    ax3.plot(corVals)
    #print corIndices
    #print corMax
    ax3.plot(corIndices, corMax, 'ro')
    #ax3.plot(corMax[-50:], corVals[corMax[-50:]], 'ro')

    ax4 = fig.add_subplot(414)

    #corNorm = N.select([corVals>0],[corVals],default = 1)
    #ax4.plot(corNorm, '-o')
    #ax4.plot(corVals)
    #ax4.set_yscale('log')


    #print corMax[-10:]
    #print corVals[corMax[-10:]]
#    ax4.hist(maxShift[corVals.argsort()[-50:]], bins = 50)
    #print corMax
    #print len(corMax)

    ax4.hist(maxShift[corIndices], bins = int(cols*0.5))

    fig2 = P.figure()
#    axCor = fig2.add_subplot(111)
#    axCor.contour(cor2D, alpha = 0.5,  origin = 'lower',  cmap = cmaps[0])

    axA = fig2.add_subplot(211)
    axA.hist(maxShift[corVals.argsort()[-50:]], bins = int(cols*0.5))


    axB = fig2.add_subplot(212)
    axB.hist(maxShift[corIndices], bins = int(cols*0.5))

    P.show()


    '''
    The code below will extract a specific row and demonstrate the utility of TH filtering and
    its relation to correlation coeff.
    '''
#    rowR = SNS.normArray(mzR[65000])
#    rowS = SNS.normArray(mzS[65000])
#
#    rowRtH=SNS.topHat(rowR, factor = 0.01)
#    rowStH=SNS.topHat(rowS, factor = 0.01)
#
#    f.close()
#    f2.close()
#
#    fig = P.figure()
#    ax = fig.add_subplot(211)
#    ax.plot(rowRtH)
#    ax.plot(rowStH)
#
#    #ax.plot(rowR)
#    #ax.plot(rowS)
#
#    cor = N.correlate(rowR, rowS, mode = 'valid')
#    print N.corrcoef(rowR, rowS)
#    print cor
#
#    cor2 = N.correlate(rowRtH, rowStH, mode = 'valid')
#    print N.corrcoef(rowRtH, rowStH)
#    print cor2
#
#
#    ax2 = fig.add_subplot(212)
#
#    cor = N.correlate(rowR, rowS, mode = 'same')
#
#    cor2 = N.correlate(rowRtH, rowStH, mode = 'same')
#
#    #ax2.plot(cor)
#    ax2.plot(cor2)
#
#
#
##    pf = 0.001
##    for i in range(5):
##        ax.plot(SNS.topHat(rowR, factor = pf),label = '%s'%pf)
##        pf+=0.005
##    ax.legend()
#
#
#    P.show()
