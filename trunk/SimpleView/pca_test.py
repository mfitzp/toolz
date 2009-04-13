'''
PCA example using python.  Very simplified
'''

import pca_module as pca
import numpy as N
import pylab as P
import cluster_bhc as H
'''
Adapted from:

http://www.cs.mcgill.ca/~sqrt/dimr/dimreduction.html

[title]  Planets of the Solar System
[source] http://pds.jpl.nasa.gov/planets/

[columns]  distance  diameter  density
"Mercury"    0.387     4878     5.42   (black)
"Venus"      0.723    12104     5.25   (black)
"Earth"      1.000    12756     5.52   (black)
"Mars"       1.524     6787     3.94   (black)
"Jupiter"    5.203   142800     1.314  (blue)
"Saturn"     9.539   120660     0.69   (blue)
"Uranus"    19.18     51118     1.29   (blue)
"Neptune"   30.06     49528     1.64   (blue)
"Pluto"     39.53      2300     2.03   (blue)

'''

#def crossMultiply(a,b):


RawPlanets = N.array([
              [0.39,4878,5.42],
              [0.72,12104,5.25],
              [1,12756,5.52],
              [1.52,6787,3.94],
              [5.2,142800,1.31],
              [9.54,120660,0.69],
              [19.18,51118,1.29],
              [30.06,49528,1.64],
              [39.53,2300,2.03]])

#Normalize the raw values
dataMatrix = N.log10(RawPlanets)
#dataMatrix = RawPlanets

#dataMatrix = P.load('Phytones_Raw.csv', delimiter = ',').transpose()

#perform PCA--thanks Henning Risvik
scores,  loading,  explanation = pca.PCA_nipals2(dataMatrix, standardize=False)

print loading
print "\n"
print explanation#can be used for the scree plot to see how much of the variation is contained throughout the different PCs

for i in xrange(dataMatrix.shape[1]):
    dataMatrix[:,i]-=N.mean(dataMatrix[:,i])

pc1Val = N.dot(dataMatrix[0],loading[0])
pc2Val = N.dot(dataMatrix[0],loading[1])

print pc1Val, pc2Val

pc1 = scores[:, 0]
pc2 = scores[:, 1]
pc3 = scores[:, 2]


print pc1[0], pc2[0]

fig=P.figure()#create pylab figure
ax = fig.add_subplot(211)#create an ax

#add scatter plot and size based upon distance from sun
ax.scatter(pc1, pc2, color = 'b', s = 50, alpha = 0.3)

#add axis labels
ax.set_xlabel('PC1', fontsize = 12)
ax.set_ylabel('PC2', fontsize = 12)

#data labels
labels = ['Mercury','Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
#labels = ['C07','C08',    'C09',   'C10',    'C11',    'C12',    'C13',    'C14',    'C15',    'C16',    'C17']
#labels = ['P08',    'P09',    'P10',    'P11',    'P12 ',   'P13',    'P14',    'P15',    'P16',    'P17',    'P19',    'P20',    'P21',    'P22',    'P23']
#labels = ['V02',    'V03 ',   'V04',    'V05  ',  'V06  ',  'V07 ',   'V08  ',  'V09  ',  'V10  ',  'V11  ',  'V12  ',  'V13',    'V14',    'V15',    'V16',    'V17']


#add labels to each marker
for label, x, y in map(None, labels, pc1, pc2):
    ax.annotate(label, xy=(x, y),  size = 12)

ax2 = fig.add_subplot(212)

print 'pdist'
Y = H.pdist(dataMatrix)#, 'seuclidean')
print 'linkage'
Z = H.linkage(Y,'single')
print 'dendro'
H.dendrogram(Z, truncate_mode='level', show_contracted=True, customMPL = ax2, labels = labels)#, orientation='left')
print 'dendro end'

P.show()
