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

# load essential modules
import smoothing


# SPECTRUM BASELINE FUNCTIONS
# ---------------------------

def getBaseline(points, segments, offset=0., smooth=True):
    """Calculate baseline for given points.
        points: (numpy.array)
        segments: (int) number of baseline segments
        offset: (float) intensity offset in %/100
        smooth: (bool) smooth final baseline
    """
    
    baseline = []
    
    # get number of points per segment
    width = int(len(points)/segments)
    
    # unpack x and y values
    xAxis, yAxis = numpy.hsplit(points,2)
    xAxis = xAxis.flatten()
    yAxis = yAxis.flatten()
    
    # get first point
    segment = yAxis[0:width/2]
    med = float(numpy.median(segment))
    mad = numpy.median(numpy.absolute(segment - med))
    baseline.append([xAxis[0], med-mad])
    
    # calculate baseline as medians of each segments
    for i in xrange(0, len(points)-width, width):
        segment = yAxis[i:i+width]
        med = float(numpy.median(segment))
        mad = numpy.median(numpy.absolute(segment - med))
        x = xAxis[i] + (xAxis[i+width]-xAxis[i])/2
        baseline.append([x, med-mad])
    
    # get last point
    segment = yAxis[-width/2:-1]
    med = float(numpy.median(segment))
    mad = numpy.median(numpy.absolute(segment - med))
    baseline.append([xAxis[-1], med-mad])
    
    # convert to array
    baseline = numpy.array(baseline)
    
    # smooth baseline
    if smooth:
        windowSize = 5*(points[-1][0]-points[0][0])/segments
        baseline = smoothing.smoothSG(baseline, windowSize, 2)
    
    # offset baseline
    baseline = baseline * numpy.array([1., 1.-offset])
    
    return baseline
# ----


def subtractBaseline(points, segments, offset=0., smooth=True):
    """Subtract baseline from given points.
        points: (numpy.array)
        segments: (int) number of baseline segments
        offset: (float) intensity offset in %/100
        smooth: (bool) smooth final baseline
    """
    
    # get baseline points
    baseline = getBaseline(points, segments, offset, smooth)
    
    # set first baseline segment
    i = 0
    m = (baseline[i][1] - baseline[i-1][1])/(baseline[i][0] - baseline[i-1][0])
    b = baseline[i-1][1] - m * baseline[i-1][0]
    
    # calculate offsets
    offsets = []
    for x in xrange(len(points)):
        while baseline[i][0] < points[x][0]:
            i += 1
            m = (baseline[i][1] - baseline[i-1][1])/(baseline[i][0] - baseline[i-1][0])
            b = baseline[i-1][1] - m * baseline[i-1][0]
        offsets.append((0., m * points[x][0] + b))
    offsets = numpy.array(offsets)
    
    # shift points to zero level
    shifted = points - offsets
    
    # remove negative intensities
    minXY = numpy.minimum.reduce(shifted)
    maxXY = numpy.maximum.reduce(shifted)
    shifted = shifted.clip([minXY[0],0.],maxXY)
    
    return shifted
# ----

