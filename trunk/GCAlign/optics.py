'''
 -------------------------------------------------------------------------
 Function:
 [RD,CD,order]=optics(x,k)
 -------------------------------------------------------------------------
 Aim:
 Ordering objects of a data set to obtain the clustering structure
 -------------------------------------------------------------------------
 Input:
 x - data set (m,n); m-objects, n-variables
 k - number of objects in a neighborhood of the selected object
 (minimal number of objects considered as a cluster)
 -------------------------------------------------------------------------
 Output:
 RD - vector with reachability distances (m,1)
 CD - vector with core distances (m,1)
 order - vector specifying the order of objects (1,m)
 -------------------------------------------------------------------------
 Example of use:
 x=[randn(30,2)*.4;randn(40,2)*.5+ones(40,1)*[4 4]];
 [RD,CD,order]=optics(x,4)
 -------------------------------------------------------------------------
 References:
 [1] M. Ankrest, M. Breunig, H. Kriegel, J. Sander,
 OPTICS: Ordering Points To Identify the Clustering Structure,
 available from www.dbs.informatik.uni-muenchen.de/cgi-bin/papers?query=--CO
 [2] M. Daszykowski, B. Walczak, D.L. Massart, Looking for natural
 patterns in analytical data. Part 2. Tracing local density
 with OPTICS, J. Chem. Inf. Comput. Sci. 42 (2002) 500-507
 -------------------------------------------------------------------------
 Written by Michal Daszykowski
 Department of Chemometrics, Institute of Chemistry,
 The University of Silesia
 December 2004
 http://www.chemometria.us.edu.pl


ported to python Jan, 2009 by Brian H. Clowers, Pacific Northwest National Laboratory.
Dependencies include scipy, numpy, and hcluster.
bhclowers at gmail.com
'''


import numpy as N
import pylab as P
import hcluster as H


def optics(x, k, distMethod = 'euclidean'):
    if len(x.shape)>1:
        m,n = x.shape
    else:
        m = x.shape[0]
        n == 1

    try:
        D = H.squareform(H.pdist(x, distMethod))
        distOK = True
    except:
        print "squareform or pdist error"
        distOK = False


    CD = N.zeros(m)
    RD = N.ones(m)*1E10

    for i in xrange(m):
        #again you can use the euclid function if you don't want hcluster
#        d = euclid(x[i],x)
#        d.sort()
#        CD[i] = d[k]

        tempInd = D[i].argsort()
        tempD = D[i][tempInd]
#        tempD.sort() #we don't use this function as it changes the reference
        CD[i] = tempD[k]#**2


    order = []
    seeds = N.arange(m, dtype = N.int)

    ind = 0
    while len(seeds) != 1:
#    for seed in seeds:
        ob = seeds[ind]
        seedInd = N.where(seeds != ob)
        seeds = seeds[seedInd]

        order.append(ob)
        tempX = N.ones(len(seeds))*CD[ob]
        tempD = D[ob][seeds]#[seeds]
        #you can use this function if you don't want to use hcluster
        #tempD = euclid(x[ob],x[seeds])

        temp = N.column_stack((tempX, tempD))
        mm = N.max(temp, axis = 1)
        ii = N.where(RD[seeds]>mm)[0]
        RD[seeds[ii]] = mm[ii]
        ind = N.argmin(RD[seeds])


    order.append(seeds[0])
    RD[0] = 0 #we set this point to 0 as it does not get overwritten
    return RD, CD, order

def euclid(i, x):
    """euclidean(i, x) -> euclidean distance between x and y"""
    y = N.zeros_like(x)
    y += 1
    y *= i
    if len(x) != len(y):
        raise ValueError, "vectors must be same length"

    d = (x-y)**2
    return N.sqrt(N.sum(d, axis = 1))



if __name__ == "__main__":
    import sys
    from PyQt4 import QtCore, QtGui
    from mpl_pyqt4_widget import MPL_Widget
    import supportFunc as sf

    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w.canvas.setupSub(2)
    ax1 = w.canvas.axDict['ax1']
    ax2 = w.canvas.axDict['ax2']

    xy = P.load('RawPeaks.csv', delimiter = ',')
#    xy = xy[800:850]

#    testX = N.array([[ 15.,  70.],
#                     [ 31.,  87.],
#                     [ 45.,  32.],
#                     [  5.,   8.],
#                     [ 73.,   9.],
#                     [ 32.,  83.],
#                     [ 26.,  50.],
#                     [  7.,  31.],
#                     [ 43.,  97.],
#                     [ 97.,   9.]])

#    mlabOrder = N.array(1,2,6,7,3,8,9,4,5,10)


#    P.plot(testX[:,0], testX[:,1])
    RD, CD, order = optics(xy[:,0:2], 2)
    ax1.plot(xy[:,0], xy[:,1], 'ro', ms = 3, alpha = 0.6)
    xyO = xy[order]
#    ax1.plot(xyO[:,0], xyO[:,1], 'b-')


#    ax2.plot(CD, 'bo-', alpha = 0.7)
    derivCD = sf.first_derivative(CD)
    print len(CD), len(derivCD)
    ax2.plot(derivCD, 'bo-', alpha = 0.7)
    thresh = 5
    temp = []
    for i,pnt in enumerate(derivCD):
        temp.append(i)
        if pnt > thresh:
            temp = N.array(temp, dtype = N.int)
            tempC = xy[temp]
            ax1.plot(tempC[:,0], tempC[:,1], 's', ms = 4, alpha = 0.5)
            temp = []


    w.show()
    sys.exit(app.exec_())
