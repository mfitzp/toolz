#
#% -------------------------------------------------------------------------
#% Function:
#% [RD,CD,order]=optics(x,k)
#% -------------------------------------------------------------------------
#% Aim:
#% Ordering objects of a data set to obtain the clustering structure
#% -------------------------------------------------------------------------
#% Input:
#% x - data set (m,n); m-objects, n-variables
#% k - number of objects in a neighborhood of the selected object
#% (minimal number of objects considered as a cluster)
#% -------------------------------------------------------------------------
#% Output:
#% RD - vector with reachability distances (m,1)
#% CD - vector with core distances (m,1)
#% order - vector specifying the order of objects (1,m)
#% -------------------------------------------------------------------------
#% Example of use:
#% x=[randn(30,2)*.4;randn(40,2)*.5+ones(40,1)*[4 4]];
#% [RD,CD,order]=optics(x,4)
#% -------------------------------------------------------------------------
#% References:
#% [1] M. Ankrest, M. Breunig, H. Kriegel, J. Sander,
#% OPTICS: Ordering Points To Identify the Clustering Structure,
#% available from www.dbs.informatik.uni-muenchen.de/cgi-bin/papers?query=--CO
#% [2] M. Daszykowski, B. Walczak, D.L. Massart, Looking for natural
#% patterns in analytical data. Part 2. Tracing local density
#% with OPTICS, J. Chem. Inf. Comput. Sci. 42 (2002) 500-507
#% -------------------------------------------------------------------------
#% Written by Michal Daszykowski
#% Department of Chemometrics, Institute of Chemistry,
#% The University of Silesia
#% December 2004
#% http://www.chemometria.us.edu.pl

#function [RD,CD,order]=optics(x,k)
import sys

import numpy as N
import hcluster as H
import scipy.special as special

def euclid(pnt, targetArray):
    d = N.zeros_like(targetArray)
    for i,val in enumerate(targetArray):
        d[i] = H.euclidean(pnt, val)
#        d.append(H.euclidean(pnt, val))
    return d
#    return N.array(d)

def optics(x,k, disMethod = 'euclidean'):
    if len(x.shape)>1:
        m,n = x.shape
    else:
        m = x.shape[0]
        n == 1
    CD = N.zeros(m)
    RD = N.ones(m)*10^10
#    CD=zeros(1,m);
#    RD=ones(1,m)*10^10;

#    % Calculate Core Distances
    for i in xrange(m):
        D = N.sort(euclid(x[i], x))
        CD[i] = D[k+1]

#    for i=1:m
#        D=sort(dist(x(i,:),x));
#        CD(i)=D(k+1);
#    end
#    order =
#    order=[];
#    seeds=[1:m];
#
#    ind=1;
#
#    while ~isempty(seeds)
#        ob=seeds(ind);
#        seeds(ind)=[];
#        order=[order ob];
#        mm=max([ones(1,length(seeds))*CD(ob);dist(x(ob,:),x(seeds,:))]);
#        ii=(RD(seeds))>mm;
#        RD(seeds(ii))=mm(ii);
#        [i1 ind]=min(RD(seeds));
#    end
#
#    RD(1)=max(RD(2:m))+.1*max(RD(2:m));


#function [D]=dist(i,x)
#def dist(i,x):
#
#% Aim:
#% Calculates the Euclidean distances between the i-th object and all objects in x
#% Input:
#% i - an object (1,n)
#% x - data matrix (m,n); m-objects, n-variables
#%
#% Output:
#% D - Euclidean distance (m,1)
#
#[m,n]=size(x);
#D=(sum((((ones(m,1)*i)-x).^2)'));
#
#if n==1
#   D=abs((ones(m,1)*i-x))';
#end

def orderDataByDist(data, distMethod = 'euclidean'):
    try:
        D = H.squareform(H.pdist(data, distMethod))
        distOK = True
    except:
        print "squareform failed"
        distOK = False

    if len(data.shape)>1:
        m,n = data.shape
    else:
        m = data.shape[0]

    minOrder = N.zeros(m, dtype = N.int)

    for i in xrange(m):
#        minOrder[i] = N.where(D[i].argsort() == 1)[0]
        minOrder[i] = D[i].argsort()[-2]

    #return ordered Data
#    return data[minOrder]
    return minOrder


if __name__ == "__main__":
    """ Simple test program (Makes use of the matplotlib graph library!)"""
    from scipy.cluster.vq import kmeans2
    import scipy as S
    import pylab as P
#    x1 = S.rand(30,2)*2
#    x2 = (S.rand(40,2)*0.5+1)*4
#    xy= N.concatenate((x1,x2))
    xy = P.load('peakLoc2D.csv', delimiter = ',')
    print xy.shape
    P.plot(xy[:,0],xy[:,1], 'ro', alpha = 0.7)
#
    order = orderDataByDist(xy)
    P.plot(order)
    print order, order.dtype
#    P.plot(order[:,0],order[:,1])



    P.show()

