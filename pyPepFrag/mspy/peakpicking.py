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
from copy import deepcopy

# load configuration
import config

# register essential objects
import objects

# register essential modules
import basics
import averagine


# PEAK PICKING FUNCTIONS
# ----------------------

def findPeaks(points, pickingHeight, peakWidth, snTreshold=0, relIntTreshold=0, absIntTreshold=0, adaptiveNoise=False):
    """Find peaks.
        points: (numpy.array) spectrum points
        pickingHeight: (float) peak intensity height where the mass is picked in %/100
        peakWidth: (float) peak width approximation (peakWidth/2 for grouping, peakWidth*2 for centroides)
        snTreshold: (float) signal to noise treshold for picked peaks
        relIntTreshold: (float) relative basepeak intensity treshold for picked peaks in %/100
        absIntTreshold: (float) absolute intensity treshold for picked peaks
        adaptiveNoise: (bool) calculate noise level separately for each peak
    """
    
    # get possible peaks by local maxima
    peaklist = getLocalMax(points, peakWidth/2, adaptiveNoise)
    
    # filter peaklist
    peaklist = filterPeaks(peaklist, snTreshold, relIntTreshold, absIntTreshold)
    
    # calculate masses by centroid model
    peaklist = getCentroids(points, peaklist, pickingHeight, peakWidth*2, adaptiveNoise)
    
    # filter peaklist
    peaklist = filterPeaks(peaklist, snTreshold, relIntTreshold, absIntTreshold)
    
    # return peaklist object
    return objects.peaklist(peaklist)
# ----


def findPeak(points, mzRange, pickingHeight, adaptiveNoise=False):
    """Find one peak in given m/z range.
        points: (numpy.array) spectrum points
        mzRange: (list) m/z range where to find the peak
        pickingHeight: (float) peak intensity height where the mass is picked in %/100
        adaptiveNoise: (bool) calculate noise level separately for each peak
    """
    
    # get current selection
    i1 = _getIndex(points, mzRange[0])
    i2 = _getIndex(points, mzRange[1])
    selection = points[i1:i2]
    
    # get local max for current selection
    localMax = [0,0]
    for point in selection:
        if point[1] > localMax[1]:
            localMax = point
    
    # make peak
    peak = objects.peak(mz=localMax[0], intensity=localMax[1])
    
    # get centroid
    maxWidth = mzRange[1]-mzRange[0]
    centroids = getCentroids(points, [peak], pickingHeight, maxWidth, adaptiveNoise)
    
    if centroids:
        return centroids[0]
    else:
        return None
# ----


def findPoint(points, mz, adaptiveNoise=False):
    """Find peak for given m/z value.
        points: (numpy.array) spectrum points
        mz: (float) m/z value
        adaptiveNoise: (bool) calculate noise level separately for each peak
    """
    
    # get intensity
    i = _getIndex(points, mz)
    intensity = _interpolateLine(points[i], points[i-1], mz)
    
    # get noise
    if adaptiveNoise:
        noiseLevel, noiseWidth = getNoise(points, mz=mz)
    else:
        noiseLevel, noiseWidth = getNoise(points)
    
    # get S/N
    if noiseWidth != 0:
        sn = (intensity-noiseLevel) / noiseWidth
        sn = round(sn,3)
    else:
        sn = None
    
    # make peak
    if intensity > noiseLevel:
        peak = objects.peak(mz=mz, intensity=intensity, baseline=noiseLevel, sn=sn)
        return peak
    else:
        return False
# ---


def getLocalMax(points, groupWidth, adaptiveNoise=False):
    """Get possible peaks from the points using local maxima.
        points: (numpy.array) spectrum points
        groupWidth: (float) peaks within this range will be grouped together
        adaptiveNoise: (bool) calculate noise level separately for each peak
    """
    
    groupWidth /= 2
    buff = []
    previous = None
    localMax = points[0]
    growing = True
    
    # get local maxima
    for point in points[1:]:
        
        # remember last maximum
        if localMax[1] <= point[1]:
            localMax = point
            growing = True
        
        # store local maximum
        elif growing and localMax[1] > point[1]:
                
            # try to group with previous or add new peak
            if previous!=None and (localMax[0]-groupWidth)<previous[0]:
                if localMax[1] > previous[1]:
                    buff[-1] = (objects.peak(mz=localMax[0], intensity=localMax[1]))
                    previous = localMax
            else:
                buff.append(objects.peak(mz=localMax[0], intensity=localMax[1]))
                previous = localMax
            
            localMax = point
            growing = False
        
        else:
            localMax = point
    
    # get baseline and s/n ratio
    noiseLevel, noiseWidth = getNoise(points)
    for peak in buff:
        if adaptiveNoise:
            noiseLevel, noiseWidth = getNoise(points, mz=peak.mz)
        peak.baseline = noiseLevel
        if noiseWidth != 0:
            sn = (peak.intensity-noiseLevel) / noiseWidth
            peak.sn = round(sn,3)
    
    return objects.peaklist(buff)
# ----


def getCentroids(points, peaklist, pickingHeight, maxWidth, adaptiveNoise=False):
    """Make centroided peaks for given peaklist.
        points: (numpy.array) spectrum points
        peaklist: (mspy.peaklist) peaklist
        pickingHeight: (float) peak intensity height where the mass is picked in %/100
        maxWidth: (float) maximum width allowed as peak
        adaptiveNoise: (bool) calculate noise level separately for each peak
    """
    
    # check peaklist
    if not isinstance(peaklist, objects.peaklist):
        peaklist = objects.peaklist(peaklist)
    
    # get noise
    noiseLevel, noiseWidth = getNoise(points)
    
    # walk through peaklist
    buff = []
    previous = None
    for peak in peaklist:
        
        # get relevant sub-portion of the data
        i1 = _getIndex(points, peak.mz-maxWidth)
        i2 = _getIndex(points, peak.mz+maxWidth)
        selection = points[i1:i2]
        
        # get data points at specified picking height
        minY = (peak.intensity-peak.baseline) * pickingHeight + peak.baseline
        i1 = None
        i2 = None
        for x, point in enumerate(selection):
            if point[0] < peak.mz and point[1] < minY:
                i1 = x
            elif point[0] > peak.mz and point[1] < minY:
                i2 = x
                break
        if not i1 or not i2:
            continue
        else:
            selection = selection[i1:i2+1]
        
        # get centroided mass
        leftX = _interpolateLine(selection[0], selection[1], y=minY)
        rightX = _interpolateLine(selection[-2], selection[-1], y=minY)
        mz = (leftX + rightX)/2
        peak.mz = mz
        
        # get intensity for centroided mass
        for x, point in enumerate(selection):
            if point[0] > mz:
                break
        intensity = _interpolateLine(selection[x-1], selection[x], x=mz)
        peak.intensity = intensity
        
        # get base and s/n
        if adaptiveNoise:
            noiseLevel, noiseWidth = getNoise(points, mz=peak.mz)
        peak.baseline = noiseLevel
        if noiseWidth != 0:
            sn = (peak.intensity-noiseLevel) / noiseWidth
            peak.sn = round(sn,3)
        
        # check peak intensity
        if peak.intensity < noiseLevel:
            continue
        
        # try to group with previous peak
        if previous!=None and leftX < previous:
            if peak.intensity > buff[-1].intensity:
                buff[-1] = peak
                previous = rightX
        else:
            buff.append(peak)
            previous = rightX
    
    return objects.peaklist(buff)
# ----


def getCharges(peaklist, maxCharge, massTolerance, intTolerance):
    """Calculate charges for peaks of given peaklist by isotopes differences and averagine distribution.
        maxCharge: (int) maximu charge searched
        massTolerance: (float) m/z tolerance for the next isotope
        intTolerance: (float) intensity tolerance for the next isotope in %/100
    """
    
    # check peaklist
    if not isinstance(peaklist, objects.peaklist):
        peaklist = objects.peaklist(peaklist)
    
    # get averagine distribution
    averagineKeys = averagine.averagineDist.keys()
    averagineKeys.sort()
    
    # clear previous results
    peaklist = deepcopy(peaklist)
    for x in range(len(peaklist)):
        peaklist[x].charge = None
        peaklist[x].isotope = None
    
    # precalc delta mass for each charge
    delta = {}
    for x in range(abs(maxCharge)):
        delta[x+1] = 1.00287/(x+1)
    charges = delta.keys()
    charges.reverse()
    
    # set polarity
    polarity = 1
    if maxCharge < 0:
        polarity = -1
    
    # walk in peaklist
    for x in range(len(peaklist)):
        
        # skip identified peaks
        if peaklist[x].isotope != None:
            continue
        else:
            cluster = [peaklist[x]]
        
        # try all charges
        for z in charges:
            y = 1
            isotope = 0
            
            # get isotopic pattern
            pattern = None
            mass = basics.mz(peaklist[x].mz, 0, z*polarity)
            for key in averagineKeys:
                if key >= mass:
                    pattern = averagine.averagineDist[key]
                    break
            if not pattern:
                pattern = averagine.makeAveragineDist(config.averagineFormula, massRange=mass)
            
            # search for next isotope within tolerance
            while x+y < len(peaklist) and ((peaklist[x+y].mz - cluster[-1].mz) - delta[z]) <= massTolerance:
                if abs((peaklist[x+y].mz - cluster[-1].mz) - delta[z]) <= massTolerance:
                    
                    # add peak to cluster
                    cluster.append(peaklist[x+y])
                    peaklist[x+y].charge = z*polarity
                    isotope += 1
                    
                    # check number if isotopes
                    if not pattern or len(pattern)<=isotope:
                        break
                    
                    # check isotope intensity to avoid skiping of overlaped peaks
                    calcIntens = ((cluster[-2].intensity-cluster[-2].baseline) / pattern[isotope-1][1]) * pattern[isotope][1]
                    if abs(peaklist[x+y].intensity - peaklist[x+y].baseline - calcIntens) < (calcIntens * intTolerance):
                        peaklist[x+y].isotope = isotope
                    
                y += 1
                
            # skip other charges if one isotope at least was found
            if len(cluster) > 1:
                peaklist[x].charge = z*polarity
                peaklist[x].isotope = 0
                break
    
    return peaklist
# ----


def getNoise(points, minX=None, maxX=None, mz=None, deviation=0.1):
    """Calculate noise for given points.
        points: (numpy.array) spectrum points
        minX, maxX: (float or None) points selection
        mz: (float or None) m/z value for which to calculate the noise +- deviation
        deviation: (float) m/z range for noise calculation in %/100
    """
    
    # use sub-portion of the data
    if mz != None:
        i1 = _getIndex(points, mz-mz*deviation)
        i2 = _getIndex(points, mz+mz*deviation)
        points = points[i1:i2]
    elif minX != None and maxX != None:
        i1 = _getIndex(points, minX)
        i2 = _getIndex(points, maxX)
        points = points[i1:i2]
    
    # check points
    if len(points) == 0:
        return None, None
    
    # unpack data
    x,y = numpy.hsplit(points,2)
    y = y.flatten()
    
    # get noise offset
    noiseLevel = numpy.median(y)
    
    # get noise width
    noiseWidth = numpy.median(numpy.absolute(y - noiseLevel))
    noiseWidth = float(noiseWidth)*2
    
    return noiseLevel, noiseWidth
# ----


def filterPeaks(peaklist, snTreshold=0, relIntTreshold=0, absIntTreshold=0):
    """Remove peaks below treshold.
        peaklist: (mspy.peaklist) peaklist to be filtered
        snTreshold: (float) signal to noise treshold for picked peaks
        relIntTreshold: (float) relative basepeak intensity treshold for picked peaks in %/100
        absIntTreshold: (float) absolute intensity treshold for picked peaks
    """
    
    # check peaklist
    if len(peaklist) == 0:
        return peaklist
    
    # get absolute treshold
    if relIntTreshold:
        maxInt = max([(peak.intensity - peak.baseline) for peak in peaklist])
        relIntTreshold = maxInt * relIntTreshold
    treshold = max(relIntTreshold, absIntTreshold)
    
    # check peaks
    buff = []
    for peak in peaklist:
        if (peak.intensity - peak.baseline) >= treshold \
            and (peak.sn==None or peak.sn >= snTreshold):
            buff.append(peak)
    
    return objects.peaklist(buff)
# ----



# HELPER FUNCTIONS
# ----------------

def _getIndex(points, x):
    """Get nearest index for selected point."""
    
    lo = 0
    hi = len(points)
    while lo < hi:
        mid = (lo + hi) / 2
        if x < points[mid][0]:
            hi = mid
        else:
            lo = mid + 1
        
    return lo
# ----


def _interpolateLine(point1, point2, x=None, y=None):
    """Get interpolated X or Y value from line defined by two points (y = mx + b)."""
    
    # check points
    if point1[0] == point2[0] and x!=None:
        return point1[0]
    elif point1[0] == point2[0] and y!=None:
        return max(point1[1], point2[1])
    
    # get equation
    m = (point2[1] - point1[1])/(point2[0] - point1[0])
    b = point1[1] - m * point1[0]
    
    # get point
    if x != None:
        return m * x + b
    elif y != None:
        return (y - b) / m
# ----


