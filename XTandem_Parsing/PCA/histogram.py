from pylab import *
from numpy import *

# A helper function to make histograms
def histData(dataIn, binsIn=None):
    """
    Make a histogram that can be plotted with plot() so that
    the histogram just has the outline rather than bars as it
    usually does.
    """
    if (binsIn == None):
        (en, eb) = matplotlib.mlab.hist(dataIn)
        binsIn = eb
    else:
        (en, eb) = matplotlib.mlab.hist(dataIn, bins=binsIn)

    stepSize = binsIn[1] - binsIn[0]

    bins = zeros(len(eb)*2.0 + 2)
    data = zeros(len(eb)*2.0 + 2)
    for bb in range(len(binsIn)):
        bins[2*bb + 1] = binsIn[bb]
        bins[2*bb + 2] = binsIn[bb] + stepSize
        data[2*bb + 1] = en[bb]
        data[2*bb + 2] = en[bb]

    bins[0] = bins[1]
    bins[-1] = bins[-2]
    data[0] = 0
    data[-1] = 0

    return (bins, data)
