#!/usr/bin/env python

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T
import SplitNStich as SNS


def get2DPeakLoc(peakLoc, rows, cols):
    x = N.empty(len(peakLoc), dtype = int)
    y = N.empty(len(peakLoc), dtype = int)
    for i,loc in enumerate(peakLoc):
        x[i] = int(loc/cols)
        y[i] = loc%cols

    return x,y



def make2DLayer(cgram, colPoints):
    '''
    cgram = chromatogram
    cLayer = 2D representation of cgram
    '''
    rowPoints = int(len(cgram)/colPoints)
    cLayer = N.empty((rowPoints, colPoints), dtype = int)#  self.colPoints),  dtype=int)
    print cLayer.shape
    x = 0
    for i in xrange(len(cgram)):
        y=i%colPoints
        cLayer[x][y] = cgram[i]
        if i !=0 and (i%colPoints) == 0:
            x+=1

    return cLayer



if __name__ == "__main__":
    import sys
    import pylab as P
    import matplotlib.colors as C
    from mpl_pyqt4_widget import MPL_Widget
    import time
    app = QtGui.QApplication(sys.argv)

    file = 'TICRef.txt'
    file2 = 'TICSam.txt'
    ticRef = P.load(file)#this loads them as float64 so normalization is not needed
    ticSam = P.load(file2)

#    ticRef+=100
#    ticRef = ticRef[30000:40000]
#    ticSam = ticSam[30000:40000]
    aligned, stopLoc, oddPnts, peakLoc, peakInt = SNS.SplitNStitch(ticRef, ticSam,  500)

    print len(ticRef), ticRef.dtype
    #print len(ticSam), ticSam.dtype

    w = MPL_Widget()
    w.canvas.setupSub(2)
    ax1 = w.canvas.axDict['ax1']
    ax2 = w.canvas.axDict['ax2']
    ax1.plot(ticRef)
    ax1.plot(peakLoc, peakInt, 'ro')

    ticLayer = make2DLayer(ticRef, 500)

    cdict ={
    'blue': ((0.0, 0.01, 0.01), (0.01, 0.25, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
    'green': ((0.0, 0, 0), (0.05, 0.75, 0.75), (0.25, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
    'red': ((0.0, 0, 0), (0.15, 0.25, 0.25), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
    }

    my_cmap = C.LinearSegmentedColormap('mycmap', cdict, 512)
    ax2.imshow(N.transpose(ticLayer), origin = 'lower', aspect = 'auto', cmap = my_cmap)

    x,y = get2DPeakLoc(peakLoc, 555, 500)
    ax2.plot(x,y,'yo', ms = 4, alpha = 0.5)

    #ax1.plot(ticSam[0:50000], 'r:')
    #ax2.plot(aligned)
    #ax2.plot(ticSam)
    #y = N.ones(len(stopLoc))*N.mean(aligned)
    #y1 = N.ones(len(oddPnts))*N.mean(aligned)
    #ax2.plot(stopLoc, y, 'go')
    #ax2.plot(oddPnts, y1, 'ro')

    w.show()
    sys.exit(app.exec_())