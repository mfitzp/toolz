#used to interface to the libmercury C++ module
#written by:
'''
/*
 * $Id$
 *
 * libmercury++
 *
 * A C++ library for the calculation of accurate masses
 * and abundances of isotopic peaks
 *
 * Copyright (c) 2006 
 * 	Marc Kirchner <marc.kirchner@iwr.uni-heidelberg.de>
 *
 * Based on the emass implementation of Perttu Haimi 
 * (see Copyright notice below).
 *
 * This code may be distributed under the terms of the
 * Lesser GNU Public License (LGPL) version 2 or any later version.
 */
 *
 * Based on an algorithm developed by Alan L. Rockwood.
 *
 * Published in 
 * Rockwood, A.L. and Haimi, P.: "Efficent calculation of 
 * Accurate Masses of Isotopic Peaks",
 * Journal of The American Society for Mass Spectrometry
 * JASMS 03-2263, 2006
 
  See that included cpp file
'''
#wrapped to by python by Brian H. Clowers
#ideally we'd like to get a direct numpy interface to the std::vector class but 
#I was having a heck of time getting this to work on windows so this will have to suffice for now

import libmercury as LM
import numpy as N

def mercury(elemComp, charge, pruneLim = 1e-5):
	'''
	elemComp is a python list that defines the number of 
	atoms in a given molecule
	elemComp = [Hydrogens, Carbons, Nitrogens, Oxygens, Sulfurs]
	
	charge is the number of charges on the ion
	
	pruneLim is the minimum percentage to be considered in the
	isotope patter returned
	'''
	mzCPP = LM.DoubleVector()
	abundCPP = LM.DoubleVector()
	elemCompCPP = LM.UnsignedIntVector()
	for elem in elemComp:
		elemCompCPP.push_back(elem)
		
	retVal = LM.mercury(mzCPP, abundCPP, elemCompCPP, charge, pruneLim)
	#if retVal is 0, success, otherwise fail
	#print 'Start Size ', mzCPP.size(), abundCPP.size()
	if retVal == 0 and (mzCPP.size() == abundCPP.size()):
		mzNP = N.ones(mzCPP.size())
		abundNP = N.ones(abundCPP.size())
		for i in xrange(mzCPP.size()):
			mzNP[i] = mzCPP[i]
			abundNP[i] = abundCPP[i]
		mzCPP.clear()
		abundCPP.clear()
		#print 'End Size ', mzCPP.size(), abundCPP.size()
		del mzCPP
		del abundCPP
		return [retVal, [mzNP, abundNP]]
	else:
		del mzCPP
		del abundCPP
		return [retVal, [None, None]]