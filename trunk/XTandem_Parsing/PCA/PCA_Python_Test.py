
import os, sys

import pca_module as pca
import numpy as N
import pylab as P
#import matplotlib.axes3d as p3

from histogram import histData as H

labels = ['Mercury','Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

#dataMatrix = P.load('PlanetsLog.csv',  delimiter = ',')
dataMatrix = P.load('PCA_Matrix.csv',  delimiter = ',',  skiprows = 1)
dataMatrix2 = P.load('PCA_Matrix_noProE.csv',  delimiter = ',',  skiprows = 1)

#dataMatrix = N.log(N.array(dataMatrix))
dataMatrix = N.array(dataMatrix)
dataMatrix2 = N.array(dataMatrix2)

#scores,  loading,  explanation = pca.PCA_nipals2(dataMatrix, standardize=True, E_matrices=True)
scores,  loading,  explanation = pca.PCA_nipals2(dataMatrix, standardize=True)
scores2,  loading2,  explanation2 = pca.PCA_svd(dataMatrix2, standardize=True)

#print explanation,  N.sum(explanation)
print loading
#l1 = loading[:, 0]
#l2 = loading[:, 1]
#l3 = loading[:, 2]
#print scores
#print l1
#print l2
#print l3

pc1 = scores[:, 0]
pc2 = scores[:, 1]
pc3 = scores[:, 2]

pc1a = scores2[:, 0]
pc2a = scores2[:, 1]
pc3a = scores2[:, 2]

hirange=pc1a.max()
lorange=pc1a.min()
numbins = 300
 

histo = H(pc1a, N.arange(lorange, hirange, ((hirange-lorange)/numbins)))

fig=P.figure()
ax = fig.add_subplot(311)
#ax.contourf3D(X,Y,Z)
#ax.scatter(pc1, pc2, color = 'b', alpha = 0.3)
ax.scatter(pc1, pc2, color = 'b', alpha = 0.3)#s = 1/pc3,

#for label, x, y in map(None, labels, pc1, pc2):
#    ax.annotate(label, xy=(x, y),  size =9)

ax1 = fig.add_subplot(312)
ax1.scatter(pc1a, pc2a,  color = 'r',  alpha = 0.3)#s = 1/pc3a, 
#ax1.scatter(l1, l2,  color = 'r',  alpha = 0.3)

ax2 = fig.add_subplot(313)
ax2.plot(histo[0], histo[1])
P.show()
