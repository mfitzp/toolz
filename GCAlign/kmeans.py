# Quick and dirty program for doing k-means clustering.
#
# (c) Paulo Marques (pmarques@dei.uc.pt)
# September 2005

from random import randint
from pylab import scatter, show, hold, axes
from matplotlib.colors import rgb2hex
from random import randint
from math import sqrt

#############################################################################

class Point:
    """Represents a simple point in a 2D space"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)

#############################################################################

def dist(point, centroids):
    """Returns a table containing the distances from a point to a list of
    points passed as parameter (centroids), representing the centroids of
    a cluster in the k-means method"""

    return [sqrt((point.x - c[0].x)**2 + (point.y - c[0].y)**2) for c in centroids]

#############################################################################

def regroup(p_dist_centroids, n_clusters):
    """Given a list containing a pair (point, distance_to_centroid) and the
    number of clusters these points should be grouped into, perform this
    grouping. It returns a list of clusters with the corresponding points."""

    clusters = [[] for i in range(n_clusters)]

    for (point, distances) in p_dist_centroids:
        index = 0
        value = distances[0]
        for i in range(1, len(distances)):
            if distances[i] < value:
                value = distances[i]
                index = i

        clusters[index] += [point]

    return clusters

#############################################################################

def calc_centroids(centroids, clusters):
    """Given a current list of centroids and a list containing several
    groups of clustered points, recalculate the centroids."""

    new_centroids = centroids

    for i in range(len(clusters)):
        cluster = clusters[i]
        if len(cluster)!=0:
            x = 0
            y = 0

            for point in cluster:
                x+= point.x
                y+= point.y

            x/= len(cluster)
            y/= len(cluster)

            d = 0.0
            for point in cluster:
                distance = sqrt((point.x - x)**2 + (point.y - y)**2)
                if distance>d:
                    d = distance

            new_centroids[i] = (Point(x, y), d)

    return new_centroids

#############################################################################

def k_means(n_clusters, POINTS):
    """Simplified version of the k-means algorithm. Given a number of
    clusters to group some points into, and the actual points, do it!"""

    # Calculate the initial centroids randomly
    centroids = [(POINTS[randint(0, len(POINTS)-1)], 0) for i in range(n_clusters)]

    # For 100 iterations, calculate the centroids and regroup the points
    # (of course, this is a shameful simplification of the algoritm, but
    # quite effective for small stuff)
    for i in range(100):
        p_dist_centroids = [(p, dist(p, centroids)) for p in POINTS]

        clusters = regroup(p_dist_centroids, n_clusters)
        new_centroids = calc_centroids(centroids, clusters)
        centroids = new_centroids

    # Return the centroids and its corresponding clusters
    return (centroids, clusters)

#############################################################################

if __name__ == "__main__":
    """ Simple test program (Makes use of the matplotlib graph library!)"""
    from scipy.cluster.vq import kmeans2
    import scipy as S
    import numpy as N
    import pylab as P
    x1 = S.rand(30,2)*2
    x2 = (S.rand(40,2)*0.5+1)*4
    xy= N.concatenate((x1,x2))
    xy = P.load('peakLoc2D.csv', delimiter = ',')
#    P.plot(xy[:,0],xy[:,1], 'ro')
    # Cluster them
    N_CLUSTERS = 20
#    cent, clusters = k_means(N_CLUSTERS, P)
    cent, clusters = kmeans2(xy, N_CLUSTERS)
    print len(cent), cent
    print len(clusters), type(clusters),clusters
    myColors = ['red', 'green', 'blue', 'yellow', 'brown', 'magenta',\
                'black', 'cyan', 'red', 'blue', 'green']
    m = 0
    for i in xrange(len(cent)):#enumerate(cent):
#        print i
        ind = N.where(clusters == i)[0]
        temp = xy[ind]
#        print "%s"%i,temp
        if len(temp)>0:
            if m == len(myColors)-1:
                m = 0
            else:
                m+=1
            col = myColors[m]
            P.scatter(temp[:,0],temp[:,1], color = col, alpha=0.8, label = '%s'%i)
            centroid = cent[i]
            print "cent",centroid
            P.plot([cent[i][0]],[cent[i][1]], 'sb', ms = 8, label = '_nolegend_')

#        x = [p.x for p in cluster]
#        y = [p.y for p in cluster]
#        c = ['red' for c in x]
#        scatter(x, y, c=myColors[i], alpha=0.9)
#
#        i+= 1

#    i = 0
#    for cluster in clusters:
#        x = [p.x for p in cluster]
#        y = [p.y for p in cluster]
#        c = ['red' for c in x]
#        scatter(x, y, c=myColors[i], alpha=0.9)
#
#        i+= 1
    P.legend()
    P.show()

