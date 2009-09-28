import pylab as P
import numpy as N
import scipy as S
import averagine as A
import time
import gaussFunctions as GF
import supportFunc as SF

def corrIsoPatt(isoMZ, isoAbund, peakLoc):
	#Correlate the isotope patterns
	locDiff = isoMZ[0]-peakLoc
	return locDiff

def plotIsoProfile(tempX, tempY, color = 'r', alpha = 1.0):
	P.plot(tempX, tempY, color, alpha = alpha)

def getIsoProfile(xArray, yArray, isoCentroids, isoAmplitudes, mzDiff, mzResGlobal, mzResCalc, charge=1):
	'''
	returns Gaussian profile of the isotope pattern that was provided as a series of centroids
	mzDiff -- the difference between each mz value in the x dimension
	mzRes -- is the (estimated) resolution of the measurement used to create the gaussian profile
			 defines as the centroid/FWHM.
	charge -- is the charge state of the isotope pattern
	'''
	mzResMain = mzResGlobal
	returnX = []
	returnY = []
	for i, iso in enumerate(isoCentroids):


		if i == 0:
			'''
			For the monoisotopic peak we want to estimate the resolution by fitting a gaussian and
			then use the fitted value to calculate the remaining heavier isotope profiles.
			From here we can use the end result to compare to the original data to find the "best fit"
			'''
			print "MonoIso: ", iso
			pkWidth = iso/mzResCalc#FWHM = 2.35*sigma
			criterion = (xArray <= iso+(pkWidth*3)) & (xArray >= iso-(pkWidth*3))
			xInd = N.where(criterion)[0]
			startInd = xInd[0]#used at the end to extract total original data "matching" the isotope pattern
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
							returnX.append(tempXProfile)
							returnY.append(monoIsoFit)
							plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
							mzResCalc = iso/fitParams[2]
							print "Success Achieved on Second Try!"
							continue
						else:
							continue
					if j == 1:
						print "Fit Failed Twice"
						pkWidth = iso/(mzResMain*1.5)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							print "Success Achieved on Third Try!"
							returnX.append(tempXProfile)
							returnY.append(monoIsoFit)
							plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
							mzResCalc = iso/fitParams[2]
							continue
						else:
							print "Total Fit Failure"
							continue
			else:
				returnX.append(tempXProfile)
				returnY.append(monoIsoFit)
				plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
				mzResCalc = iso/fitParams[2]
			print "Res: ", mzResCalc
			#print "FitParams: ", fitParams
			print "Fit:", fitSuccess

		else:
			pkWidth = iso/mzResCalc#FWHM = 2.35*sigma
			#fullWidth = (pkWidth/2.35)*4
			tempXProfile = N.arange(iso-(pkWidth*3), iso+(pkWidth*3), mzDiff)#N.arange(start, stop, step)
			tempYProfile = GF.getGauss(tempXProfile, iso, pkWidth, amp = isoAmplitudes[i])
			returnX.append(tempXProfile)
			returnY.append(tempYProfile)
			#plotIsoProfile(tempXProfile, tempYProfile, color = '-y')
	returnX = N.array(SF.flattenX(returnX))
	returnY = N.array(SF.flattenX(returnY))
	returnX, returnY = SF.interpolate_spectrum_XY(returnX, returnY)

	endMZ = returnX.max()
	endInd = N.where(xArray<=endMZ)[0][-1]
	tempX = xArray[startInd:endInd]
	tempY = yArray[startInd:endInd]
	tempX, tempY = SF.interpolate_spectrum_by_diff(tempX, tempY, tempX[0], tempX.max(), (returnX[1]-returnX[0]))
	#tempX, tempY = SF.interpolate_spectrum_XY(tempX, tempY, len(returnX))

	#tempX, tempY = SF.interpolate_spectrum_XY(X, Y, len()
	#print "Vector Lengths: ", len(returnX), len(tempY)
	#print "Vector X Diffs: ", returnX[1]-returnX[0], tempX[1]-tempX[0]
	tempZeros = N.zeros(N.abs(len(returnX)-len(tempX)))
	if len(returnX)>len(tempX):
		tempX = N.append(tempX, tempZeros+tempX.max())
		tempY = N.append(tempY, tempZeros)
	else:
		returnX = N.append(returnX, tempZeros+returnX.max())
		returnY = N.append(returnY, tempZeros)


	#for i, val in enumerate(returnX):
	#	print val, tempX[i]
	print "Corr Coef: ", N.corrcoef(tempY, returnY)[0][1]
	print " "
	tempY+=3
	returnY+=2
	plotIsoProfile(returnX, returnY, color = '-g')
	plotIsoProfile(tempX, tempY, color = '-m')
	return mzResCalc




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
	pks.sort()
	mzPks = mz[pks]

	P.plot(mz, abund, alpha = 0.5)
	P.vlines(mzPks, 0, 100, 'g', linestyle = 'dashed')

	t1 = time.clock()
	mzResGlobal = 6000#need to add a function to fit this
	mzResCalc = 6000#need to add a function to fit this
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

					mzRezCalc = getIsoProfile(mz, abund, isoPeaks[0]-localDiff, isoPeaks[1], mzDiff, mzResGlobal, mzResCalc, charge=1)


					#the following is dependent upon the resolution and we want to
					#P.vlines(isoPeaks[0]-localDiff+0.25, 0, isoPeaks[1], 'm', linestyle = 'dashed')
					#P.vlines(isoPeaks[0]-localDiff-0.25, 0, isoPeaks[1], 'm', linestyle = 'dashed')

	print time.clock()-t1
	P.show()