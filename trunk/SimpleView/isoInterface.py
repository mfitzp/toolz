import pylab as P
import numpy as N
import scipy as S
import averagine as A
import time
import gaussFunctions as GF
import supportFunc as SF
import cwtPeakPickDOG as CWT
import getBaseline as GB
import scipy.stats as stats
import scipy.signal as signal


'''
To Do:

Need to find a way to reliably get the monoisotopic peak when it is no longer the maximum peak in the distribution
Run more than once and on more than a single charge state?
how to deal with abnormally low resolutions.
Right now if the resolution of the original data is poor, this may not be right approach, then again
deisotoping is not a good idea if you don't have isotopes to look at.

'''

def courseShiftIsoPatt(isoPeaks, peakLoc):
	locDiff = isoPeaks[0]-peakLoc
	isoPeaks -= locDiff
	return isoPeaks

def fineShiftIsoPatt(expXArray, expYArray, isoArray, currMonoPeak, charge, debug = False):
	'''
	Attempts to shift the pattern to maximally correspond to the theoretical and experimantal data
	'''
	corr = N.correlate(expYArray, isoArray, mode = 'same')
	shift = N.round(corr.argmax()-len(expYArray)/2-1)
	mzShift = shift*(expXArray[1]-expXArray[0])
	#P.vlines([currMonoPeak+mzShift],0,100,'r', linestyle = 'dashed')
	#print corr
	#print "Fine Corr Shift: ", mzShift, currMonoPeak+mzShift,shift, expXArray[shift], len(expYArray), len(corr)#corrOrder[-1], expXArray[corrOrder[-1]], len(corr), len(expYArray), len(isoArray)
	if debug:
		if int(currMonoPeak) == int(1783.10285512):
			P.figure()
			P.plot(SF.normalize(corr), 'b', label = '%s %s'%(currMonoPeak, int(len(expYArray/2))/2))
			P.plot(SF.normalize(expYArray), 'r')
			#P.plot(SF.normalize(isoArray), 'g')
			P.legend()
	#account for small shifts that are not real
	#divide by 2 so you don't confuse different charge states
	#multiply by 1.5 to try and catch 1Da mis-haps common with THRASHing
	if N.abs(mzShift)<charge/2 or N.abs(mzShift)>charge*1.1:
		return 0
	else:
		print "m/z fine Shift: ", mzShift
		return mzShift

def getLocalIsoPattern(xArray, yArray, isoCentroid, charge, padWindow = 2):
	'''
	gets the local isotope profiles
	xArray -- x vector, usually m/z ratio
	yArray -- intensity vector
	isoCentroid -- potential monoisotopic mass
	charge -- ion charge
	padWindow -- the range to look below and above the isoCentroid
	Because the isotope pattern extends beyond the monoisotopic mass by its very nature we want to expand the upper
	bounds appropriately
	'''
	boundExpand = 2
	criterion = (xArray >= isoCentroid-(padWindow*boundExpand/charge)) & (xArray <= isoCentroid+(padWindow*boundExpand/charge))
	xInd = N.where(criterion)[0]
	tempX = xArray[xInd]#N.arange(iso-(pkWidth*3), iso+(pkWidth*3), mzDiff)
	tempY = yArray[xInd]
	return tempX, tempY


def plotIsoProfile(tempX, tempY, isoListX, isoListY, color = 'r', alpha = 1.0):
	#return True
	P.figure()
	P.plot(tempX, tempY, color, alpha = alpha)
	for i, tempIsoX in enumerate(isoListX):
		P.plot(tempIsoX, isoListY[i], 'r')
	P.show()

def concatenateIsos2(isoListX, isoListY):
        '''
        Takes into account overlaps in the fitting and removes redundancies
        This is not ideal as it tends to truncate the right hand parts of the Gaussian fits
        Some sort of averaging would be best but the same X values would be needed to get this right
        and or interpolation which is of course more computationally expensive
        '''
        if len(isoListX)>1:
                isoListX.reverse()
                isoListY.reverse()
                for i,iso in enumerate(isoListX[:-1]):#iterate through all but the last item in the list in this case the first isotope
                        nextIsoX = isoListX[i+1]
                        nextIsoY = isoListY[i+1]
                        curMin = iso.min()
                        delInd = N.where(nextIsoX>curMin)[0]
                        isoListX[i+1]=N.delete(nextIsoX, delInd)
                        isoListY[i+1]=N.delete(nextIsoY, delInd)
                returnX = N.array(SF.flattenX(isoListX))#theoretical profile X
                returnY = N.array(SF.flattenX(isoListY))#theoretical profile Y
                return returnX, returnY
        else:
                print "Concatenate Isos Failed"
                returnX = N.array(SF.flattenX(isoListX))#theoretical profile X
                returnY = N.array(SF.flattenX(isoListY))#theoretical profile Y
                return returnX, returnY

def concatenateIsos(isoListX, isoListY):
	'''
	Takes into account overlaps in the fitting and removes redundancies
	This is not ideal as it tends to truncate the right hand parts of the Gaussian fits
	Some sort of averaging would be best but the same X values would be needed to get this right
	and or interpolation which is of course more computationally expensive
	'''
	if len(isoListX)>1:
		#isoListX.reverse()
		#isoListY.reverse()
		for i in xrange(len(isoListX)-1):#iterate through all but the last item in the list in this case the first isotope
			isoX = isoListX[i]
			isoY = isoListY[i]
			nextIsoX = isoListX[i+1]
			nextIsoY = isoListY[i+1]
			nextMin = nextIsoX.min()
			curMax = isoX.max()
			curMin = isoX.min()
			targetInd = N.where(isoX>nextMin)[0]
			#targetInd = N.where(nextIsoX<curMin)[0]
			#tempInd = []

			for j,ind in enumerate(targetInd):
				#assumes the differences in X values is negligible
				#and that the indicies are in sequential order
				curVal = isoY[ind]#intensity value of the current isotope

				nextVal = nextIsoY[j]#intensity value of the next isotope

				if curVal > nextVal:
					isoListX[i+1][j] = isoX[ind]
					isoListY[i+1][j] = curVal
					#tempInd.append(j)
#				else:
#					isoListX[i][ind] = isoX[ind]
#					isoListY[i][ind] = isoY[ind]




			isoListX[i]=N.delete(isoX, targetInd)
			isoListY[i]=N.delete(isoY, targetInd)
		returnX = N.array(SF.flattenX(isoListX))#theoretical profile X
		returnY = N.array(SF.flattenX(isoListY))#theoretical profile Y
		return returnX, returnY
	else:
		print "Concatenate Isos Failed"
		returnX = N.array(SF.flattenX(isoListX))#theoretical profile X
		returnY = N.array(SF.flattenX(isoListY))#theoretical profile Y
		return returnX, returnY

def getIsoProfile(xArray, yArray, isoCentroids, isoAmplitudes,
				  mzDiff, mzResGlobal, mzResCalc, charge=1, padWindow=1, corrCutOff = 0.5):
	'''
	returns Gaussian profile of the isotope pattern that was provided as a series of centroids
	mzDiff -- the difference between each mz value in the x dimension
	mzRes -- is the (estimated) resolution of the measurement used to create the gaussian profile
			 defines as the centroid/FWHM.
	charge -- is the charge state of the isotope pattern
	'''
	fitOk = True
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
			#print "MonoIso: ", iso
			pkWidthPrev = iso/mzResCalc#for re-use if fit fails
			pkWidth = iso/mzResCalc#FWHM = 2.35*sigma
			criterion = (xArray >= iso-(pkWidth*4)-padWindow/charge) & (xArray <= iso+(pkWidth*4))
			xInd = N.where(criterion)[0]
			startInd = xInd[0]#used at the end to extract total original data "matching" the isotope pattern
			tempXProfile = xArray[xInd]
			tempYProfile = yArray[xInd]
			prevPeakWidth = pkWidth
			fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
			#This attempt to take into account fits that success but are bogus
			mzResCalc = iso/fitParams[2]
			if mzResCalc < 1:
				fitSuccess = 5
			elif mzResCalc > mzResMain*5:
				fitSuccess = 5
			elif mzResCalc < mzResMain/5:
				fitSuccess = 5

			if fitSuccess == 5:
				for j, k in enumerate(xrange(5)):
					if j == 0:
						#print "Fit Failed Once"
						pkWidth = iso/(mzResMain/1.5)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							returnX.append(tempXProfile)
							returnY.append(monoIsoFit)
							#plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
							mzResCalc = iso/fitParams[2]
							#print "Success Achieved on Second Try!"
							continue
						else:
							continue
					if j == 1:
						#print "Fit Failed Twice"
						pkWidth = iso/(mzResMain*1.5)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							#print "Success Achieved on Third Try!"
							returnX.append(tempXProfile)
							returnY.append(monoIsoFit)
							#plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
							mzResCalc = iso/fitParams[2]
							continue
					if j == 2:
						#print "Fit Failed Three Times"
						pkWidth = iso/(mzResMain*10)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							#print "Success Achieved on Third Try!"
							returnX.append(tempXProfile)
							returnY.append(monoIsoFit)
							#plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
							mzResCalc = iso/fitParams[2]
							continue
					if j == 3:
						#print "Fit Failed Four Times"
						pkWidth = iso/(mzResMain/10)
						fitSuccess, fitParams, monoIsoFit = GF.fitGauss(tempXProfile, tempYProfile, isoAmplitudes[i], iso, pkWidth)
						if fitSuccess != 5:
							#print "Success Achieved on Third Try!"
							returnX.append(tempXProfile)
							returnY.append(monoIsoFit)
							#plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
							mzResCalc = iso/fitParams[2]
							continue
						else:
							fitOk = True
							print "Total Fit Failure"
							continue
					if j == 4:
						print "Total Failure, Attempting to Fix\n"
						pkWidth = pkWidthPrev/2
						mzResCalc = iso/pkWidth

						monoIsoFit = GF.getGauss(tempXProfile, iso, pkWidth, amp = isoAmplitudes[i])
						returnX.append(tempXProfile)
						returnY.append(monoIsoFit)
						continue


			else:
				mzResCalc = iso/fitParams[2]
				returnX.append(tempXProfile)
				returnY.append(monoIsoFit)
				#plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
			#print "Res: ", mzResCalc
			#print "FitParams: ", fitParams
			#print "Fit:", fitSuccess

		else:
			pkWidth = iso/mzResCalc#FWHM = 2.35*sigma
			#fullWidth = (pkWidth/2.35)*4
			tempXProfile = N.arange(iso-(pkWidth*4), iso+(pkWidth*4), mzDiff)#N.arange(start, stop, step)
			tempYProfile = GF.getGauss(tempXProfile, iso, pkWidth, amp = isoAmplitudes[i])
			#tempXProfile, tempYProfile = concatenateIsos(returnX[-1], tempXProfile, tempYProfile)
			returnX.append(tempXProfile)
			returnY.append(tempYProfile)
			#plotIsoProfile(tempXProfile, tempYProfile, color = '-y')
	if fitOk:
		returnX, returnY = concatenateIsos(returnX, returnY)#returnX and Y are the theoretical isotope patterns
		#we need to sort the theoretical profiles so that a correlation coef can be obtained
		indSort = returnX.argsort()
		returnX = returnX[indSort]
		returnY = returnY[indSort]

		endMZ = returnX.max()
		#print "XArray max: ", returnX.max(), xArray.max()
		endInd = N.where(xArray<=endMZ)[0][-1]
		tempX = xArray[startInd:endInd]

		tempY = yArray[startInd:endInd]
		returnDiff = N.diff(returnX).max()

		#using the index from 1 so that there are no interpolation errors
		tempX, tempY = SF.interpolate_spectrum_by_diff(tempX, tempY, tempX[1], tempX.max(), returnDiff)
		returnX, returnY = SF.interpolate_spectrum_by_diff(returnX, returnY, tempX[1], tempX.max(), returnDiff)
		#returnX+=returnDiff
		#isoCentroids+=returnDiff


		#the following loop pads the respective arrays so that a correlation coeff can be calculated
		#there well may be better metrics to measure the "goodness of fit" but this is used as a first pass.

		#THIS IS THE PROBLEM, THE PADDING IS SCREWING WITH THE SYSTEM
		#RESAMPLE?

#		tempX = signal.resample(tempX, len(returnX))
#		tempY = signal.resample(tempY, len(returnX))
		tempZeros = N.zeros(N.abs(len(returnX)-len(tempX)))

		if len(returnX)>len(tempX):
			tempX = N.append(tempX, tempZeros+tempX.max())
			tempY = N.append(tempY, tempZeros)
		else:
			returnX = N.append(returnX, tempZeros+returnX.max())
			returnY = N.append(returnY, tempZeros)

		fineMZShift = fineShiftIsoPatt(tempX, tempY, returnY, isoCentroids[0], charge)
		returnX+=fineMZShift
		isoCentroids+=fineMZShift


		corrScipy = stats.pearsonr(tempY, returnY)
#		print "Corr Scipy: ", corrScipy

#		fig = P.figure()
#		ax = fig.add_subplot(311)
#		ax2 = fig.add_subplot(312)
#		ax3 = fig.add_subplot(313)
#		ax.plot(returnY1, tempY, 'bo', label = '%s'%corrScipy[0])
#		ax.legend()
#		ax2.plot(tempX, tempY)
#		ax2.plot(returnX1, returnY1)
#		ax3.plot(returnY1)
#		ax3.plot(tempY)

#		print "Relative Lengths", len(tempY), len(returnY)



#		corrResult = N.corrcoef(tempY, returnY)[0]
#		corrFactor = corrResult[1]
		corrCutOff = corrCutOff
		print "m/z, Corr Coef: ", isoCentroids[0], corrScipy
		print " "
		if corrScipy[0] <= corrCutOff:
			return None, None, None, None, None, False
		else:
			#P.vlines(isoCentroids, 0, isoAmplitudes, 'k')
			#plotIsoProfile(returnX, returnY, color = '-g')

			#return mzResCalc, returnX, returnY, startInd, corrFactor, fitOk
			return mzResCalc, returnX, returnY, startInd, corrScipy[0], fitOk
	else:
		return None, None, None, None, None, fitOk

def normalize2One(datArray):
	return datArray/datArray.max()

def sortPeaks(X,Y, profileX, profileY, corrFactors, xTol):
	'''
	Sorts and deletes entries in the found peaks that differ by less than a user defined cutoff
	X -- peak centroids
	Y -- peak intensities
	profileX -- fit profile in x domain
	profileY -- fit profile in y domain
	xTol -- tolerance used to group peaks, default is 2 times the increment used in the x-dimension

	The idea here would be to group the peaks together that are essentially the same and return the one within
	the group with the best "fit" to the actual data.

	The problem with this is that the correlation coefficient is not necessarily the best measure....


	Most likely you could remove the sorting but I did this to be sure
	'''
	centX = []
	centY = []
	for i,xVals in enumerate(X):
		centX.append(xVals[0])
		centY.append(Y[i][0])
	centX = N.array(centX)
	centY = N.array(centY)

	sortOrder = centX.argsort()
	xSort = centX[sortOrder]
	ySort = centY[sortOrder]
	xDiff = N.diff(xSort)
	indArray = []
	j = 0
	for k, diff in enumerate(xDiff):
		if diff <= xTol:
			indArray.append(j)
		else:
			j+=1
			indArray.append(j)

		print centX[k], diff, corrFactors[k], j

	peakGroups = []


def processSpectrum(X, Y, scales, minSNR, pkResEst, corrCutOff):
	'''
	This is the main function call
	assumes data have been interpolated (for CWT)
	X -- array of x values (usually m/z)
	Y -- array of intensity values
	scales -- the scales used in the CWT
	minSNR -- the minimum SNR used for noise estimate and peak picking
	pkResEst -- the estimate peak resolution measured in peak location/FWHM

	To Do:

	need to adjust so that isotopes that are found but no valid fit is achieved are
	also returned.
	'''


	#this estimation of the numSegs may work for other data sets but has
	#only been tested with m/z data
	numSegs = int(len(X)*(X[1]-X[0]))
	noiseEst, minNoise = GB.SplitNSmooth(Y, numSegs, minSNR)


	yMax = Y.max()
	xDiff = X[1]-X[0]
	cwt = CWT.cwtMS(Y, scales, staticThresh = (2/Y.max())*100, wlet='DOG')

	ANS = CWT.getCWTPeaks(cwt, X, Y, noiseEst, minRow = 0,
						  minNoiseEst = minNoise, EPS = None, debug = True)

	peakLoc, peakInt, rawPeakInd, cwtPeakLoc, cClass, boolAns = ANS

	pkLoc = N.array(peakLoc)
	pkInt = N.array(peakInt)
	peakOrder = pkLoc.argsort()
	pkLoc = pkLoc[peakOrder]
	pkInt = pkInt[peakOrder]

	centX = []#will store the peak centroids after correction
	centY = []#will store the peak intensities after correction
	isoX = []#will hold the profiles for the fitted isotope patterns in the m/z dimension
	isoY = []#will hold the intensity profiles for the fitted isotope patterns
	corrFactors=[]#cross correlation factors between the theoretical and actual data
	startPnts = []

	if boolAns:
		if len(pkLoc)>0:

				resGlobal = pkResEst#this is the initial value provided by user
				resCalc = pkResEst
				for i, pk in enumerate(pkLoc):
					#adjust to account for different charge states
					#not tested as of 10/05/09 BHC
					chargeStates = [1]#[1,2]
					for j,charge in enumerate(chargeStates):
						isoAns = A.averagineCalc(pk, charge = charge)#C++ wrapper to averagine calculation
						if isoAns != None:
							if isoAns[0] == 0:#successful isotope pattern exit code
								isoPeaks = isoAns[1]
								scaleVal = pkInt[i]
								isoPeaks[1] = normalize2One(isoPeaks[1])
								isoPeaks[1] *= scaleVal

								isoPeaks[0] = courseShiftIsoPatt(isoPeaks[0], pk)#sometimes there are big shifts needed

								isoAns = getIsoProfile(X, Y, isoPeaks[0], isoPeaks[1], xDiff, resGlobal, resCalc, charge=charge, corrCutOff = corrCutOff)
								rezCalc, tempIsoX, tempIsoY, startInd, corrFactor, fitOk = isoAns

								if fitOk:
									isoX.append(tempIsoX)
									isoY.append(tempIsoY)
									centX.append(isoPeaks[0])
									centY.append(isoPeaks[1])
									corrFactors.append(corrFactor)
									startPnts.append(startInd)

				returnANS = [centX, centY, isoX, isoY, corrFactors]


				#sortPeaks(returnANS[0],returnANS[1], returnANS[2], returnANS[3], returnANS[4], xTol = xDiff*2)
#				plotIsoProfile(X, Y, isoX, isoY)
				return returnANS, True
		return None, False
	return None, False


if __name__ == "__main__":

#	data = P.load('Tryptone.csv', delimiter = ',')
	data = P.load('A2.csv', delimiter = ',')

	mz = data[:,0]


	abund = data[:,1]
	abund = SF.topHat(abund, 0.01)

	abund = SF.roundLen(abund)
	mz = mz[0:len(abund)]

	mz, abund = SF.interpolate_spectrum_XY(mz, abund)

	mzDiff = mz[1]-mz[0]
	print "m/z Diff: ", mzDiff, mz[-1]-mz[-2]
	print len(mz)
	start = 0
	stop = len(mz)
#	start = 10000
#	stop = 20000
	mz = mz[start:stop]
	abund = abund[start:stop]
	abund = SF.normalize(abund)
	#mz = N.arange(len(mz))

	#scales = N.arange(2,32,4)
	#scales = N.array([2,10,18,26,34,42,50,58])#,4)
	scales = N.array([1,2,4,6,8,12,16])
	minSNR = 1.5
	resEst = 10000
	corrCutOff = 0.3
	t1 = time.clock()
	ANS, boolAns = processSpectrum(mz, abund, scales, minSNR, resEst, corrCutOff = corrCutOff)
	print "Peak Picking and Isotopic Fitting Time: ", time.clock()-t1

	fig = P.figure()
	ax = fig.add_subplot(111)
	ax.plot(mz, abund, 'b', alpha = 0.6)


	print " "
	if ANS != None:
		centX, centY, isoX, isoY, corrFits = ANS
		if len(centX)>0:
			for i, centroid in enumerate(centX):
				ax.vlines(centroid, 0, centY[i]*1.1, 'g', linestyle = 'dashed')
				ax.plot(isoX[i], isoY[i], 'r', alpha = 0.5)
				#plots the correlation value above the "monoisotopic" peak
				ax.text(centroid[0], centY[i][0]*1.1, '%.3f'%corrFits[i])

#	startInd = N.where(mz>=isoX[2].min())[0][0]
#	endInd = N.where(mz<=isoX[2].max())[0][-1]
#	print startInd, endInd
#	P.figure()
#	subX = mz[startInd:endInd]
#	subY = abund[startInd:endInd]
#	P.plot(subY, 'og', alpha = 0.7)
#	P.plot(isoY[2], 'or', alpha = 0.6)
#	print len(isoX[2]), len(subX)
	P.show()
