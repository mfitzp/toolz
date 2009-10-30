#Adapted by BHC from:
# $Id: ams.averagine.R 124 2006-10-20 10:02:25Z mkirchner $

import numpy as N


try:
	import libmercuryInterface as LMI
	libmercuryOk = True
except:
	libmercuryOk = False


def averagineCalc(avgMass, charge = 1):

	elemList = ['H','C','N','O','S']

	avgDict = {}
	avgDict['H']=7.7583
	avgDict['C']=4.9384
	avgDict['N']=1.3577
	avgDict['O']=1.4773
	avgDict['S']=0.0417

	avgMassDict = {}#this is the averagine mass dictionary not the average mass!
	avgMassDict['H']=1.00794
	avgMassDict['C']=12.011
	avgMassDict['N']=14.00670
	avgMassDict['O']=15.99940
	avgMassDict['S']=32.06600

	avgMonomerMass = 111.1254

	#n = int(N.round(avgMass/avgMonomerMass))
	n = avgMass/avgMonomerMass

	modelComp = []
	modelComp.append(int(N.round(avgDict['H']*n)))
	modelComp.append(int(N.round(avgDict['C']*n)))
	modelComp.append(int(N.round(avgDict['N']*n)))
	modelComp.append(int(N.round(avgDict['O']*n)))
	modelComp.append(int(N.round(avgDict['S']*n)))

	modelMass = 0.0
	for i,elem in enumerate(elemList):
		modelMass+=avgMassDict[elem]*modelComp[i]

	actualMass = avgMonomerMass*n
	modelDev = actualMass - modelMass

	print "Actual Mass, Deviation: ", actualMass, modelDev

	if libmercuryOk:
		mercAns = LMI.mercury(modelComp, charge, 1e-3)
		if mercAns[0] == 0:
			return mercAns
	else:
		print "libmercury failed"


if __name__ == "__main__":
	ans = averagineCalc(1672, 1)
	print ans

'''
"ams.averagine" <-
function(avgmass)
{
	# Senko et al., 1995
	model.freq <- list(H=7.7583, C=4.9384, N=1.3577, O=1.4773, S=0.0417);
	# avg. atom masses from GPMAW (http://welcome.to/gpmaw)
	elem.avgmass <- list(H=1.00794, C=12.011, N=14.00670, O=15.99940, S=32.06600);
	model.mass.avg <- 111.1254;

	# number of averagine AAs
	n <- avgmass / model.mass.avg;
	# number of atoms
	freq <- round(sapply(model.freq, '*', n));
	# pad with hydrogen
	modelmass <- sum(freq * as.numeric(elem.avgmass));
	deviance.mass <- avgmass - modelmass; # may be negative for round towards larger ints
	deviance.H <- deviance.mass %/% elem.avgmass$H;
	freq["H"] <- freq["H"] + deviance.H;
	# calculate error
	err.mass <- deviance.mass - deviance.H*elem.avgmass$H;

	return(list(model=as.list(freq), masserror=err.mass, hydrogencorrection=deviance.H));
}
'''
