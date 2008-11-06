
import sys
import os
import os.path

from PyQt4.QtGui import QFileDialog,  QApplication
import numpy as N

import time

#puRE pyTHON neTCDF reADER
from pupynere import NetCDFFile as CDF
#pytables
import tables as T


def getHDFColumns(filename):#HDF5 filename
    if os.path.isfile(filename):
        loadedVars = []
        hdf = T.openFile(filename, mode = "r")
        r = hdf.root
        for node in r._f_iterNodes():
            loadedVars.append((node._v_hdf5name,  node.read()))
        
        return dict(loadedVars)

def make2DTIC(TIC,  colPoints):
    rowPoints = int(len(TIC)/colPoints)
    ticLayer = N.empty((rowPoints, colPoints), dtype = int)#  self.colPoints),  dtype=int)
    print ticLayer.shape
    x = 0
    for i in xrange(len(TIC)):
        y=i%colPoints
        ticLayer[x][y] = TIC[i]
        if i !=0 and (i%colPoints) == 0:
            x+=1
    
    return ticLayer
        
        

if __name__ == "__main__":
    import pylab as P
    from pylab import cm
    cmaps = [cm.spectral,  cm.hot,  cm.spectral]
    dataDict = getHDFColumns('/home/clowers/Desktop/netCDF_Reader/Alignment.h5')
    fig = P.figure()
    ax = fig.add_subplot(211,  title = 'Unaligned')
    ax2 = fig.add_subplot(212, sharex=ax, sharey=ax,  title = 'Aligned')

    columns = 1200
    
    
    i = 0
    for item in dataDict.iteritems():
        print item[0]
        tic1D = item[1]#(item[1]/item[1].max())*100
        TIC = make2DTIC(tic1D, columns)
        rows = int(len(tic1D)/columns)
        imAspect = rows/(columns*1.0)
        print imAspect
        if '_AL' not in item[0]:
            #ax.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower', aspect = imAspect, cmap = cmaps[i])
            ax.contour(N.transpose(TIC), alpha = 1,  origin = 'lower',  cmap = cmaps[i])
            
        else:
            #ax2.imshow(N.transpose(TIC), alpha = 0.5,  origin = 'lower',  aspect = imAspect,   cmap = cmaps[i])
            ax2.contour(N.transpose(TIC), alpha = 1,  origin = 'lower',  cmap = cmaps[i])
            
        i+=0
    #ax.set_xlim(0,rows)
    #ax.set_ylim(0,columns)
    #ax2.set_ylim([0,columns])
    P.show()
    
    
