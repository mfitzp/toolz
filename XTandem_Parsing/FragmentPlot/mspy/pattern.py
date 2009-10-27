# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load libs
import numpy

# load configuration
import config

# register essential objects
import basics
import blocks
import objects


# ISOTOPIC PATTERN CALCULATIONS
# -----------------------------

def isoPattern(compound, fwhm=0.1, relIntTreshold=0.01, charge=1, agentFormula='H', agentCharge=1, rounding=7):
    """Calculate isotopic pattern for given compound (formula or sequence object).
    Set appropriate relative intensity treshold and resolution in fwhm.
    To charge isotopes set charge value. Charge agent can be changed from H
    to any formula."""
    
    finalPattern = []
    
    # set internal treshold
    internalTreshold = relIntTreshold/100.
    
    # add charging agent to formula and get composition
    composition = compound.getComposition()
    if charge:
        formula = compound.getFormula()
        formula += '%s%d' % (agentFormula, (charge/agentCharge))
        composition = objects.formula(formula).getComposition()
    
    # check composition
    for atom in composition:
        if composition[atom] < 0:
            return False
    
    # calculate pattern
    for atom in composition:
        atomCount = composition[atom]
        
        # get isotopic profile for current atom or specified isotope only
        atomPattern = []
        match = objects.elementPattern.match(atom)
        symbol, massNumber, tmp = match.groups()
        if massNumber:
            isotope = blocks.elements[atom].isotopes[massNumber]
            atomPattern.append([isotope[0], 1.])
        else:
            for massNumber, isotope in blocks.elements[atom].isotopes.items():
                if isotope[1] > 0.:
                    atomPattern.append(list(isotope))
        
        # add atoms
        for i in range(atomCount):
            currentPattern = {}
            
            # if pattern in empty (first atom) add current atom pattern
            if not finalPattern:
                finalPattern = atomPattern
                finalPattern.sort()
                continue
            
            # add atom to each peak of final pattern
            for peak in finalPattern:
                
                # skip peak under relevant abundance treshold
                if peak[1] < internalTreshold:
                    continue
                
                # add each isotope of current atom to peak
                for isotope in atomPattern:
                    mass = peak[0] + isotope[0]
                    abundance = peak[1] * isotope[1]
                    
                    # add abundance to stored peak or add new peak
                    mass = round(mass, rounding)
                    if mass in currentPattern:
                        currentPattern[mass] += abundance
                    else:
                        currentPattern[mass] = abundance
            
            # replace final pattern by current
            finalPattern = []
            for mass, abundance in currentPattern.items():
                finalPattern.append([mass, abundance])
            finalPattern.sort()
            
            # noramlize pattern
            finalPattern = _normalize(finalPattern)
    
    # check pattern
    if not finalPattern:
        return None
    
    # correct charge
    if charge:
        for i in range(len(finalPattern)):
            finalPattern[i][0] = (finalPattern[i][0]-0.000549*charge)/abs(charge)
    
    # collect isotopes according to resolution (FWHM)
    tol = fwhm/2
    if charge:
        tol /= abs(charge)
    collectedPeaks = [finalPattern[0]]
    lastPeak = finalPattern[0]
    for currentPeak in finalPattern[1:]:
        if (lastPeak[0] + tol) > currentPeak[0]:
            abundance = lastPeak[1] + currentPeak[1]
            mass = (lastPeak[0]*lastPeak[1] + currentPeak[0]*currentPeak[1]) / abundance
            collectedPeaks[-1] = [mass, abundance]
            lastPeak = [mass, abundance]
        else:
            collectedPeaks.append(currentPeak)
            lastPeak = currentPeak
    finalPattern = _normalize(collectedPeaks)
    
    # discard peaks below treshold
    filteredPeaks = []
    for peak in finalPattern:
        if peak[1] >= relIntTreshold:
            filteredPeaks.append(peak)
    finalPattern = filteredPeaks
    
    return finalPattern
# ----


def isoPatternProfile(pattern, fwhm):
    """Make profile spectrum for given isotopic pattern."""
    
    # make raster
    minX = numpy.minimum.reduce(pattern)[0] - 5*fwhm
    maxX = numpy.maximum.reduce(pattern)[0] + 5*fwhm
    raster = numpy.arange(minX,maxX, fwhm/10.)
    profile = numpy.zeros(raster.size, float)
    
    # calc gaussian peak for each isotope
    width = fwhm/1.66
    for isotope in pattern:
        lo = isotope[0]-5*fwhm
        hi = isotope[0]+5*fwhm
        for x in range(raster.size):
            if raster[x] < lo or raster[x] > hi:
                continue
            profile[x] += isotope[1]*numpy.exp(-1*(pow(raster[x]-isotope[0],2))/pow(width,2))
    
    # make final profile
    profile = numpy.array(zip(raster, profile))
    
    return profile
# ----


def gaussianPeak(mz, intensity, fwhm, steps=500):
    """Make Gaussian peak for given mz, intensity and fwhm."""
    
    data=[]
    
    minX = mz-(5*fwhm)
    maxX = mz+(5*fwhm)
    step = (maxX-minX)/steps
    width = fwhm/1.66
    x = minX
    for i in range(steps):
        y = intensity*numpy.exp(-1*(pow(x-mz,2))/pow(width,2))
        data.append([x,y])
        x += step
    
    data = numpy.array(data)
    
    return data
# ----



# HELPER FUNCTIONS
# ----------------

def _normalize(data):
    """Normalize data to 100%."""
    
    # get maximum Y
    maximum = data[0][1]
    for item in data:
        if item[1] > maximum:
            maximum = item[1]
    
    # normalize data data
    for x in range(len(data)):
        data[x][1] /= maximum
    
    return data
# ----

