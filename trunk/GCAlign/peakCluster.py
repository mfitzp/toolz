
#!/usr/bin/env python

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T
import SplitNStich as SNS


if __name__ == "__main__":
    import sys
    import pylab as P
    import hcluster as H
    import matplotlib.colors as C
    from mpl_pyqt4_widget import MPL_Widget
    import time
#    app = QtGui.QApplication(sys.argv)

    file = 'PeakLoc.txt'
    X = P.load(file, delimiter = ',')#this loads them as float64 so normalization is not needed
    Y = H.pdist(X)#, 'mahalanobis')
#    print len(Y)

    Z = H.linkage(Y, 'single')
#    sq = H.squareform(Y)
#    print X.shape
#    print Y.shape
#    print sq.shape
#    P.hist(Y, bins = 200)
#    N.savetxt('PeakDistEuc.csv',sq,fmt = '%.2f', delimiter = ',')
    #P.imshow(sq)
    #P.show()

    H.dendrogram(Z, colorthreshold=10, truncate_mode='level')
    P.show()

#    #print len(ticSam), ticSam.dtype
#
#    w = MPL_Widget()
#    w.canvas.setupSub(2)