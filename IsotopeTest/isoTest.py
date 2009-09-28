import pylab as P
import numpy as N
import scipy as S
import averagine as A
import time
import gaussFunctions as GF

def corrIsoPatt(isoMZ, isoAbund, peakLoc):
	#Correlate the isotope patterns
	locDiff = isoMZ[0]-peakLoc
	return locDiff


def getIsoProfile(xArray, yArray, isoCentroids, isoAmplitudes, mzDiff, mzRes, charge=1):
	'''
	returns Gaussian profile of the isotope pattern that was provided as a series of centroids
	mzDiff -- the difference between each mz value in the x dimension
	mzRes -- is the (estimated) resolution of the measurement used to create the gaussian profile
			 defines as the centroid/FWHM.
	charge -- is the charge state of the isotope pattern
	'''
	mzResMain = mzRes
	for i, iso in enumerate(isoCentroids):

		if i == 0:
			pkWidth = iso/mzRes#FWHM = 2.35*sigma
			criterion = (xArray <= iso+(pkWidth*3)) & (xArray >= iso-(pkWidth*3))
			xInd = N.where(criterion)[0]
			tempXProfile = xArray[xInd]#N.arange(iso-(pkWidth*3), iso+(pkWidth*3), mzDiff)
			tempYProfile = yArray[xInd]#GF.getGauss(tempXProfile, iso, pkWidth, amp = isoAmplitudes[i])
			prevPeakWidth = pkWidth
			fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
			if fitSuccess == 5:
				for j, k in enumerate(xrange(2)):
					if j == 0:
						print "Fit Failed Once"
						pkWidth = iso/(mzResMain/1.5)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							P.plot(tempXProfile, monoIsoFit, '-r')
							mzRes = iso/fitParams[2]
							continue
						else:
							continue
					if j == 1:
						print "Fit Failed Twice"
						pkWidth = iso/(mzResMain*1.5)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							P.plot(tempXProfile, monoIsoFit, '-r')
							mzRes = iso/fitParams[2]
							continue
						else:
							continue
			else:
				P.plot(tempXProfile, monoIsoFit, '-r')
				mzRes = iso/fitParams[2]
			print "Res: ", mzRes
			print "FitParams: ", fitParams
			print "Fit:", fitSuccess

		else:
			pkWidth = iso/mzRes#FWHM = 2.35*sigma
			#fullWidth = (pkWidth/2.35)*4
			tempXProfile = N.arange(iso-(pkWidth*3), iso+(pkWidth*3), mzDiff)#N.arange(start, stop, step)
			tempYProfile = GF.getGauss(tempXProfile, iso, pkWidth, amp = isoAmplitudes[i])
			P.plot(tempXProfile, tempYProfile, 'y')



def normalize(npArray):
	#normalize from 0-1
	npArray /= npArray.max()
	#npArray *= 100
	return npArray

if __name__ == "__main__":

	data = P.load('Tryptone.csv', delimiter = ',')

	mz = data[:,0]
	mzDiff = mz[1]-mz[0]
	print "m/z Diff: ", mzDiff
	abund = data[:,1]
	abund /=abund.max()
	abund *=100

	#print len(mz)

	pks = [32125,
	40883,
	44041,
	44069,
	54233,
	54259,
	21455,
	35542,
	40849]

	mzPks = mz[pks]

	P.plot(mz, abund)
	P.vlines(mzPks, 0, 100, 'g', linestyle = 'dashed')

	t1 = time.clock()

	for i, pk in enumerate(mzPks):
		chargeStates = [1]#[1,2]
		colors = ['r','m']
		for j,charge in enumerate(chargeStates):
			isoAns = A.averagineCalc(pk, charge = charge)
			if isoAns != None:
				if isoAns[0] == 0:
					isoPeaks = isoAns[1]
					scaleVal = abund[pks[i]]
					normalize(isoPeaks[1])
					isoPeaks[1]*=scaleVal
					localDiff = corrIsoPatt(isoPeaks[0], isoPeaks[1], pk)
					P.vlines(isoPeaks[0]-localDiff, 0, isoPeaks[1], colors[j])
					mzRes = 5000#need to add a function to fit this
					getIsoProfile(mz, abund, isoPeaks[0]-localDiff, isoPeaks[1], mzDiff, mzRes, charge=1)


					#the following is dependent upon the resolution and we want to
					#P.vlines(isoPeaks[0]-localDiff+0.25, 0, isoPeaks[1], 'm', linestyle = 'dashed')
					#P.vlines(isoPeaks[0]-localDiff-0.25, 0, isoPeaks[1], 'm', linestyle = 'dashed')

	print time.clock()-t1
	P.show()