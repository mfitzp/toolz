
import sys
import os
import os.path

import numpy as N

import time

#pytables
import tables as T

import pylab as P

#SELECT FILE LOCATION
fn = 'C:/TAi-R1_T.h5'

f = T.openFile(fn,  'r')#opens file to read 'w' is to write

#the pytables interface can use a natural naming convention--trying to be pythonic...
#HDF5 is organized by root.Leafs.Nodes (root.Groups.Arrays, etc.)
#YOU MUST KNOW THE NAME IN ORDER TO DO THIS
#OTHERWISE YOU NEED TO MANIPULATE LISTS THAT CAN BE RETURNED THROUGH PYTABLES API
mz = f.root.mzCube

#USE IF YOU"D LIKE
#rowStart = 0
#rowStop = 200
#
#row = mz[0]
#x = N.arange(0, len(row))
#
#for i in xrange(rowStart, rowStop):
#    row = mz[i]
#    P.plot(row)

fig = P.figure()
ax = fig.add_subplot(211,  title = 'Row (mz)')
ax2 = fig.add_subplot(212, title = 'EIC (column)')

rowNum = 5000
t1 = time.clock()
row = mz[rowNum]
t2 = time.clock()
print t2-t1,' sec for row extraction'
x = N.arange(0, len(row))
ax.vlines(x, 0, row)

#BECAUSE THE CHUNK SHAPE THAT WAS USED TO CREATE THE ARRAY
#IS SO SMALL THE FOLLOWING CODE IS VERY SLOW
#I NEED TO CHANGE THE CHUNKSHAPE IN ORDER TO MAKE THIS MORE REASONABLE

colNum = 41
t1 = time.clock()
col = mz[:, colNum]
t2 = time.clock()
print t2-t1,' sec for column extraction'
ax2.plot(col)

f.close()

P.show()
    
    
