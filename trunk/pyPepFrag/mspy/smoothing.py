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


# SPECTRUM SMOOTHING FUNCTIONS
# ----------------------------

def smoothMA(points, windowSize, cycles=1):
    """Smooth points by moving average.
        points: (numpy.array) points to be smoothed
        windowSize: (float) m/z window size for smoothing
        cycles: (int) number of repeating cycles
    """
    
    # approximate number of points within windowSize
    windowSize = int(windowSize*len(points)/(points[-1][0]-points[0][0]))
    if windowSize < 2:
        return points
    if not windowSize % 2:
        windowSize += 1
    
    # unpack mz and intensity
    xAxis,yAxis = numpy.hsplit(points,2)
    xAxis = xAxis.flatten()
    yAxis = yAxis.flatten()
    
    # smooth the points
    while cycles:
        s=numpy.r_[2*yAxis[0]-yAxis[windowSize:1:-1],yAxis,2*yAxis[-1]-yAxis[-1:-windowSize:-1]]
        w=numpy.ones(windowSize,'f')
        y=numpy.convolve(w/w.sum(),s,mode='same')
        smoothData = y[windowSize-1:-windowSize+1]
        yAxis = smoothData
        cycles -=1
    
    # return smoothed scan
    return numpy.array(zip(xAxis, yAxis))
# ----


def smoothSG(points, windowSize, cycles=1, order=3):
    """Smoothe points by Savitzky-Golay filter.
        points: (numpy.array) points to be smoothed
        windowSize: (float) m/z window size for smoothing
        cycles: (int) number of repeating cycles
        order: (int) order of polynom used
    """
    
    # approximate number of points within windowSize
    windowSize = int(windowSize*len(points)/(points[-1][0]-points[0][0]))
    if windowSize <= order:
        return points
    
    # unpack axes
    xAxis,yAxis = numpy.hsplit(points,2)
    xAxis = xAxis.flatten()
    yAxis = yAxis.flatten()
    
    # coeficients
    orderRange = range(order+1)
    halfWindow = (windowSize-1) // 2
    b = numpy.mat([[k**i for i in orderRange] for k in range(-halfWindow, halfWindow+1)])
    m = numpy.linalg.pinv(b).A[0]
    windowSize = len(m)
    halfWindow = (windowSize-1) // 2
    
    # precompute the offset values for better performance
    offsets = range(-halfWindow, halfWindow+1)
    offsetData = zip(offsets, m)
    
    # smooth the data
    while cycles:
        smoothData = list()
        yAxis = numpy.concatenate((numpy.zeros(halfWindow)+yAxis[0], yAxis, numpy.zeros(halfWindow)+yAxis[-1]))
        for i in range(halfWindow, len(yAxis) - halfWindow):
            value = 0.0
            for offset, weight in offsetData:
                value += weight * yAxis[i + offset]
            smoothData.append(value)
        yAxis = smoothData
        cycles -=1
    
    # return smoothed data
    return numpy.array(zip(xAxis, yAxis))
# ----

