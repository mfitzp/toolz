import pylab as P
import numpy as N
import scipy as S
import averagine as A
import time
import gaussFunctions as GF
import supportFunc as SF
import cwtPeakPick as CWT
import getBaseline as GB


'''
To Do:

Need to find a way to get the monoisotopic peak when it is no longer the maximum peak in the distribution
Run more than once and on more than a single charge state
how to deal with abnormally low resolutions.

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
	P.vlines([currMonoPeak+mzShift],0,100,'r', linestyle = 'dashed')
	#print corr
	#corrOrder = corr.argsort()
	print "Fine Corr Shift: ", mzShift, currMonoPeak+mzShift,shift, expXArray[shift], len(expYArray), len(corr)#corrOrder[-1], expXArray[corrOrder[-1]], len(corr), len(expYArray), len(isoArray)
	if debug:
		if int(currMonoPeak) == int(1783.10285512):
			P.figure()
			P.plot(SF.normalize(corr), 'b', label = '%s %s'%(currMonoPeak, int(len(expYArray/2))/2))
			P.plot(SF.normalize(expYArray), 'r')
			#P.plot(SF.normalize(isoArray), 'g')
			P.legend()
	#account for small shifts that are not real
	if N.abs(mzShift)<charge/2:
		return 0
	else:
		return mzShift

def corrIsoPatt(xArray, yArray, isoMZ, isoAbund, peakLoc, charge, padWindow = 2):
	#Correlate the isotope patterns
	locDiff = isoMZ[0]-peakLoc#get the peaks close
	isoMZ -=locDiff
	tempX, tempY = getLocalIsoPattern(xArray, yArray, isoMZ[0], charge, padWindow)
	#P.plot(tempX, tempY, ':k')
	corr = N.correlate(isoAbund, tempY, mode = 'full')
	corrOrder = corr.argsort()
	#return the difference between the actual values and the maximum correlation
	#narrow the value down to even tighter
	#corrHist = N.histogram(corr, int(len(corr)/10))
	#P.figure()
	#P.hist(corr, int(len(corr)/10))

	print "Corr Values: ",len(corr), len(isoMZ), corr.argmax(), len(tempY), tempX[corrOrder[-1]], tempX[corrOrder[-2]]
	if (corr.argmax()+1) <= len(corr):
		fineDiff = isoMZ[0]-tempX[corrOrder[-1]]
	else:
		fineDiff = isoMZ[0]-tempX[corrOrder[-1]]

	isoMZ -=fineDiff
	return isoMZ

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



def plotIsoProfile(tempX, tempY, color = 'r', alpha = 1.0):
	#return True
	P.plot(tempX, tempY, color, alpha = alpha)

def concatenateIsos(isoListX, isoListY):
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

def getIsoProfile(xArray, yArray, isoCentroids, isoAmplitudes, mzDiff, mzResGlobal, mzResCalc, charge=1, padWindow=1):
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
			criterion = (xArray >= iso-(pkWidth*4)-padWindow/charge) & (xArray <= iso+(pkWidth*4))
			xInd = N.where(criterion)[0]
			startInd = xInd[0]#used at the end to extract total original data "matching" the isotope pattern
			tempXProfile = xArray[xInd]
			tempYProfile = yArray[xInd]
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
				#take into account fits that result in poor resolution
				mzResCalc = iso/fitParams[2]
				#if
				returnX.append(tempXProfile)
				returnY.append(monoIsoFit)
				plotIsoProfile(tempXProfile, monoIsoFit, color = '-r')
			print "Res: ", mzResCalc
			#print "FitParams: ", fitParams
			print "Fit:", fitSuccess

		else:
			pkWidth = iso/mzResCalc#FWHM = 2.35*sigma
			#fullWidth = (pkWidth/2.35)*4
			tempXProfile = N.arange(iso-(pkWidth*3), iso+(pkWidth*3), mzDiff)#N.arange(start, stop, step)
			tempYProfile = GF.getGauss(tempXProfile, iso, pkWidth, amp = isoAmplitudes[i])
			#tempXProfile, tempYProfile = concatenateIsos(returnX[-1], tempXProfile, tempYProfile)
			returnX.append(tempXProfile)
			returnY.append(tempYProfile)
			#plotIsoProfile(tempXProfile, tempYProfile, color = '-y')
	returnX, returnY = concatenateIsos(returnX, returnY)
	#returnX = N.array(SF.flattenX(returnX))#theoretical profile X
	#returnY = N.array(SF.flattenX(returnY))#theoretical profile Y
	#returnDiff = N.diff(returnY)
	#diffInd = N.where(N.abs(returnDiff)>0.1)[0]
	#print returnDiff
	#zeroInd = N.where(returnY <1e-5)[0]
	#print returnY
	#returnX = N.delete(returnX, diffInd)
	#returnY = N.delete(returnY, diffInd)
	#we need to sort the theoretical profiles so that a correlation coef can be obtained
	indSort = returnX.argsort()
	returnX = returnX[indSort]
	returnY = returnY[indSort]
	#returnX, returnY = SF.interpolate_spectrum_XY(returnX, returnY)

	endMZ = returnX.max()
	endInd = N.where(xArray<=endMZ)[0][-1]
	tempX = xArray[startInd:endInd]
	tempY = yArray[startInd:endInd]
	tempX, tempY = SF.interpolate_spectrum_by_diff(tempX, tempY, tempX[0], tempX.max(), (returnX[1]-returnX[0]))
	#tempX, tempY = SF.interpolate_spectrum_XY(tempX, tempY, len(returnX))

	#tempX, tempY = SF.interpolate_spectrum_XY(X, Y, len()
	#print "Vector Lengths: ", len(returnX), len(tempY)
	print "Vector X Diffs: ", returnX[1]-returnX[0], tempX[1]-tempX[0]

	#the following loop pads the respective arrays so that a correlation coeff can be calculated
	#there well may be better metrics to measure the "goodness of fit" but this is used as a first pass.
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
	#for i, val in enumerate(returnX):
	#	print val, tempX[i]
	print "Corr Coef: ", N.corrcoef(tempY, returnY)[0][1]
	print " "
	tempY+=4
	#returnY+=4


	#isoCentroids = corrIsoPatt(tempX, tempY, isoCentroids, isoAmplitudes, isoCentroids[0], charge)

	P.vlines(isoCentroids, 0, isoAmplitudes, 'k')

	plotIsoProfile(returnX, returnY, color = '-g')
	#newYArray = yArray
	#replaceInd = N.where(xArray == tempX)[0]
	#newYArray[replaceInd] -= returnY
#	P.figure()
#	P.plot(xArray, yArray, 'b', alpha = 0.5)
#	P.plot(xArray, newYArray, 'r')

	#plotIsoProfile(tempX, tempY, color = '-m')
	return mzResCalc, returnX, returnY, startInd




def normalize(npArray):
	#normalize from 0-1
	npArray /= npArray.max()
	#npArray *= 100
	return npArray

if __name__ == "__main__":

	data = P.load('Tryptone.csv', delimiter = ',')
	#data = P.load('BSA_Sum5.csv', delimiter = ',')
	#data = P.load('I5.csv', delimiter = ',')
	#data = P.load('J1_LIFT.csv', delimiter = ',')
	#data = P.load('J5.csv', delimiter = ',')

	mz = data[:,0]
	mzDiff = mz[1]-mz[0]
	print "m/z Diff: ", mzDiff
	abund = data[:,1]

	mz, abund = SF.interpolate_spectrum_XY(mz, abund)
	abund = SF.normalize(abund)

	#scales = N.arange(2,32,4)
#	scales = N.array([2,8,12,16,20,24,32])#,4)
#	cwt = CWT.cwtMS(abund, scales, staticThresh = (2/abund.max())*100)
#	minSNR = 2
#	numSegs = len(abund)/10
#
#	noiseEst, minNoise = GB.SplitNSmooth(abund,numSegs, minSNR)
#	mNoise = SF.normalize(cwt[0]).mean()
#	stdNoise = SF.normalize(cwt[0]).std()
#	mNoise = 3*stdNoise+mNoise
#
#
#
#	peakLoc, peakInt, rawPeakInd, cwtPeakLoc, cClass, boolAns = CWT.getCWTPeaks(cwt, mz, abund, noiseEst, minRow = 1, minClust = 3, minNoiseEst = minNoise, EPS = None, debug = True)
##	if boolAns:
##		fig1 = P.figure()
##		ax = fig1.add_subplot(211)
##		ax2 = fig1.add_subplot(212,sharex=ax)
##        ax2.plot(cwtPeakLoc[:,0], cwtPeakLoc[:,1], 'oy', ms = 3, alpha = 0.4)
##        if cClass != None:
##            i = cClass.max()
##            for m in xrange(int(i)+1):
##                ind = N.where(m == cClass)
##                temp = cwtPeakLoc[ind]
##                ax2.plot(temp[:,0],temp[:,1],'-s', alpha = 0.7, ms = 3)
##            if len(peakLoc) != 0:
##                ax.vlines(peakLoc, 0, 100, 'r', linestyle = 'dashed', alpha = 0.5)
##
##		for pk in peakLoc:
##			print pk
#
#
#	mzPks = N.array(peakLoc)
#	abundPks = N.array(peakInt)
#	peakOrder = mzPks.argsort()
#	mzPks = mzPks[peakOrder]
#	abundPks = abundPks[peakOrder]

	mzPks = N.array([  686.40688458,   756.36696924,   784.36302718,   788.45121317,  1052.64021234,
					 1377.79127898,  1488.87370501,  1556.84981706,  1668.97432972,  1690.9182692,
					 1783.10285512,  2037.09142945,  2069.09551287,  2169.17590897,  2185.24809113])
	abundPks = N.array([   1.28591711,    1.26585702,    1.43095886,    1.19203978,   12.62451346,
					    7.30007314,   85.8765913,     2.15042644,  100.,            1.01928368,
					    24.51163459,    1.38676941,    1.05888408,    4.68080701,    1.37690154])

#	P.plot(mz, abund, 'g', alpha = 0.5)
	#P.vlines(mzPks, 0, abundPks*1.5, 'r', linestyle = 'dashed', alpha = 0.5)

#	print type(mzPks)
#	print mzPks.shape
	print mzPks
	print abundPks

#	#print len(mz)
#	#Peaks for Tryptone
#	pks = N.array([32125,
#	40883,
#	44041,
#	44069,
#	54233,
#	54259,
#	21455,
#	35542,
#	40849])
#	pks.sort()
#	pks-=10
#	mzPks = mz[pks]
	P.figure()
	P.plot(mz, abund, alpha = 0.5)
	t1 = time.clock()
	isoX = []
	isoY = []
	startPnts = []
	if len(mzPks)>0:
		P.vlines(mzPks, 0, 100, 'g', linestyle = 'dashed')


		mzResGlobal = 6000#need to add a function to fit this
		mzResCalc = 6000#need to add a function to fit this
		for i, pk in enumerate(mzPks):
			chargeStates = [1]#[1,2]
			colors = ['r','m']
			for j,charge in enumerate(chargeStates):
				isoAns = A.averagineCalc(pk, charge = charge)
				if isoAns != None:
					if isoAns[0] == 0:#successful isotope pattern exit code
						isoPeaks = isoAns[1]
						#scaleVal = abund[pks[i]]
						scaleVal = abundPks[i]
						normalize(isoPeaks[1])
						isoPeaks[1]*=scaleVal
						tempX = []
						tempY = []
						#tempX, tempY = getLocalIsoPattern(mz, abound, isoCentroid, charge, padWindow)

						#isoPeaks[0] = corrIsoPatt(mz, abund, isoPeaks[0], isoPeaks[1], pk, charge)
						isoPeaks[0] = courseShiftIsoPatt(isoPeaks[0], pk)
						#P.vlines(isoPeaks[0], 0, isoPeaks[1], colors[j])

						mzRezCalc, tempIsoX, tempIsoY, startInd = getIsoProfile(mz, abund, isoPeaks[0], isoPeaks[1], mzDiff, mzResGlobal, mzResCalc, charge=1)

						isoX.append(tempIsoX)
						isoY.append(tempIsoY)
						startPnts.append(startInd)


	newYArray = abund.copy()
	print len(isoX)
	print startPnts
	P.figure()
	for k, pnt in enumerate(startPnts):
		P.plot(isoX[k], isoY[k]+3, 'g')
		for m, yVal in enumerate(isoY[k]):
			newYArray[pnt+m]=0#-=yVal
	newYArray = SF.normalize(newYArray)
#	for k,isoArray in enumerate(isoY):
#		for m, pnt in enumerate(newYArray[startPnts[k]:startInd[k]+len(isoArray)]):
#			pnt -= isoArray[m]
		#newYArray[startPnts[k]:startInd[k]+len(isoArray)]-=isoArray
		#newYArray[replaceInd] -= isoY[k]


	P.plot(mz, abund, 'b', alpha = 0.5)
	P.plot(mz, newYArray, 'r')


	print time.clock()-t1
	P.show()