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

def mercury(elemComp, numIsotopes, elemMasses, elemAbundances, charge, pruneLim = 1e-5):
    '''

    	elemComp is a python list that defines the number of
    	atoms in a given molecule
    	elemComp = [Hydrogens, Carbons, Nitrogens, Oxygens, Sulfurs]

    	charge is the number of charges on the ion

    	pruneLim is the minimum percentage to be considered in the
    	isotope patter returned

    	C++ Function: mercury(msa_mz, msa_abundance, composition, MAX_ELEMENTS, MAX_ISOTOPES, nIsotopes, elemMasses, elemAbundances, charge, limit)


    	//      std::vector<double> tempElem5;
    //      tempElem5.push_back(31.972070);
    //      tempElem5.push_back(32.971456);
    //      tempElem5.push_back(33.967866);
    //      tempElem5.push_back(34);
    //      tempElem5.push_back(35.967080);
    //
    //      std::vector< std::vector<double> > tempElemMasses;
    //      tempElemMasses.push_back(tempElem1);
    //      tempElemMasses.push_back(tempElem2);
    //      tempElemMasses.push_back(tempElem3);
    //      tempElemMasses.push_back(tempElem4);
    //      tempElemMasses.push_back(tempElem5);

    	'''
    mzCPP = LM.DoubleVector()
    abundCPP = LM.DoubleVector()
    elemCompCPP = LM.UnsignedIntVector()
    elemMassesCPP = LM.MultDimVector()
    elemAbundancesCPP = LM.MultDimVector()
    numIsotopesCPP = LM.UnsignedIntVector()

    if elemMasses.shape != elemAbundances.shape:
    	'''
    	While these items may not need be the same dimensions I have not tested it in another case
    	'''
    	return [retVal, [None, None]]

    for mass in elemMasses:
    	tempMass = LM.DoubleVector()
    	for val in mass:
    		tempMass.push_back(val)
    	elemMassesCPP.push_back(tempMass)

    for abund in elemAbundances:
    	tempAbund = LM.DoubleVector()
    	for val in abund:
    		tempAbund.push_back(val)
    	elemAbundancesCPP.push_back(tempAbund)

    maxDim1 = elemMasses.shape[0]
    maxDim2 = elemMasses.shape[1]
#    print maxDim1, maxDim2

    for iso in numIsotopes:
    	numIsotopesCPP.push_back(iso)

    for elem in elemComp:
    	elemCompCPP.push_back(elem)

#    print maxDim1, maxDim2
#    print elemComp, type(elemComp)
#    print numIsotopes, type(numIsotopes), numIsotopes.dtype
#    print elemMasses.shape, type(elemMasses), elemMasses.dtype
#    print elemAbundances.shape, type(elemAbundances), elemAbundances.dtype

    #C++ Function: mercury(msa_mz, msa_abundance, composition, MAX_ELEMENTS, MAX_ISOTOPES, nIsotopes, elemMasses, elemAbundances, charge, limit)
    retVal = LM.mercury(mzCPP, abundCPP, elemCompCPP, maxDim1, maxDim2, numIsotopesCPP, elemMassesCPP, elemAbundancesCPP, charge, pruneLim)
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