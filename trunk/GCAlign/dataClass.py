#!/usr/bin/env python

from PyQt4 import QtCore,  QtGui

import numpy as N
import scipy as S
import tables as T

class GC_GC_MS_CLASS():
    def __init__(self, filePath):
        '''
        filePath is an HDF5 file that has been converted from a LECO netCDF file
        '''
        self.filePath = filePath
        self.loadOK = False
        self.fileOpen = False
        self.handle = None
        self.BPC = None
        self.BPCmz = None#the mz values making up each BPC point


        self.colPoints = None
        self.rowPoints = None
        self.ticLayer = None
        self.sicLayer = None
        self.curMZ = None
        self.SIC = None
        self.TIC = None

        self.sicOK = False
        self.ticOK = False
        self.bpcOK = False

        self.startPnt = None
        self.stopPnt = None

        #data are stored as integers but some of the functions
        #need to use floats.  This is a boolean to see if the
        #conversion to floats has occurred
        self.floated = False

        self.setTIC()
        self.setAttrs()

    def getHandle(self):
        self.handle = T.openFile(self.filePath, 'r')
        self.fileOpen = True

    def closeHandle(self):
        self.handle.close()
        self.fileOpen = False

    def setBPC(self):
        self.getHandle()
        if self.fileOpen:
            mzCube = self.handle.root.dataCube

            rows = len(self.TIC)
            bpc = N.zeros(rows)
            mzVals = N.zeros(rows)

            for i in xrange(rows):
                mz=mzCube[i]
                mzVals[i] = mz.argmax()
                bpc[i]= mz[mzVals[i]]

            self.BPC, self.BPCmz = bpc, mzVals
            self.closeHandle()
            self.bpcOK = True
        else:
            print "Error opening HDF5 data file"


    def getBPC(self):
        if self.bpcOK:
            return self.BPC, self.BPCmz

    def _makeBPC_(self, mzMTX):
        '''
        Gets base peak chromatogram
        '''


        return sic, mzVals

    def setTIC(self):
        self.getHandle()
        if self.fileOpen:
            tic = self.handle.root.TIC.read()
            self.closeHandle()
            if len(tic)>0:
                self.ticOK = True
                self.TIC = tic
            else:
                print "Error opening HDF5 data file, no TIC found"

    def getTIC(self):
        if self.ticOK:
            return self.TIC
        else:
            print "TIC not set or not found try setTIC"

    def setAttrs(self):
        self.getHandle()
        if self.fileOpen:
            cols = self.handle.root.dataCube.attrs.colPoints
            if cols != None:
                if cols > 0:
                    self.colPoints = cols
                else:
                    print 'Big Error!, check file type and how it was made. Number of rows set to ZERO!'
            else:
                print 'Big Error!, check file type and how it was made. No column attributes found!'
            rows = self.handle.root.dataCube.attrs.rowPoints
            if rows != None:
                if rows > 0:
                    self.rowPoints = rows
                else:
                    print 'Big Error!, check file type and how it was made. Number of rows set to ZERO!'
            else:
                print 'Big Error!, check file type and how it was made. No row attributes found!'

            self.closeHandle()


    def make2DTIC(self, TIC, colPoints):
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

class ReadThread(QtCore.QThread):
    def __init__(self, fileName, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.finished = False
        self.ready = False
        self.fileName = fileName
        self.handle = None
        self.fileOpen = False

    def updateThread(self, loadList, loadmzXML = False):
        self.loadList = loadList
        self.loadmzXML = loadmzXML
        self.numItems = len(loadList)
        self.ready = True
        return True

    def getHandle(self):
        self.handle = T.openFile(self.filePath, 'r')
        self.fileOpen = True

    def closeHandle(self):
        self.handle.close()
        self.fileOpen = False

    def getBPC(self):
        self.getHandle()
        if self.fileOpen:
            mzCube = self.handle.root.dataCube
            BPC, BPCmz = self._makeBPC_(mzCube)
            self.closeHandle()
            self.bpcOK = True
        else:
            print "Error opening HDF5 data file"

    def _makeBPC_(self, mzMTX):
        '''
        Gets base peak chromatogram
        '''
        rows = mzMtx.shape[0]

        sic = N.zeros(rows)
        mzVals = N.zeros(rows)

        for i in xrange(rows):
            mz=mzMtx[i]
            mzVals[i] = mz.argmax()
            sic[i]= mz[mzVals[i]]

        return sic, mzVal

    def run(self):
        if self.ready:
            if self.loadmzXML:
                while not self.finished and self.numItems > 0:
                    for item in self.loadList:
#                            print os.path.basename(item)
                        tempmzXML =  mzXMLR(item)
                        tempSpec = tempmzXML.data['spectrum']
                        if len(tempSpec)>0:
#                                print 'Spec OK', os.path.basename(item)
                            data2plot = DataPlot(tempSpec[0],  tempSpec[1],  name = os.path.basename(item), path = item)
                            data2plot.setPeakList(tempmzXML.data['peaklist'])
                            #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                            #note PyQt_PyObject
                            self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)
                        else:
                            print 'Empty spectrum: ', item

                        self.numItems -=1
            else:
                while not self.finished and self.numItems > 0:
                    for item in self.loadList:
                        tempFlex = FR(item)
                        tempSpec = tempFlex.data['spectrum']
                        data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1], name = item.split(os.path.sep)[-4], path = item)#the -4 index is to handle the Bruker File Structure
                        data2plot.setPeakList(tempFlex.data['peaklist'])
                        #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
                        self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)#note PyQt_PyObject
                        self.numItems -=1

        def __del__(self):
            self.exiting = True
            self.wait()


if __name__ == "__main__":
    import sys
    import pylab as P
    import matplotlib.colors as C
    from mpl_pyqt4_widget import MPL_Widget
    import time
    app = QtGui.QApplication(sys.argv)

    file = 'Acetone_Klean.h5'
    data = GC_GC_MS_CLASS(file)
    tic = data.getTIC()

    w = MPL_Widget()
    w.canvas.setupSub(2)
    ax1 = w.canvas.axDict['ax1']
    ax2 = w.canvas.axDict['ax2']



    t1 = time.clock()
    ticLayer = data.make2DTIC(tic, data.colPoints)
    print 'TIC Layer Generation: ', time.clock()-t1

    t1 = time.clock()
    #data.setBPC()
    print 'BPC Generation: ', time.clock()-t1

    #bpc, bpcMZ = data.getBPC()

    imAspect = data.rowPoints/(data.colPoints*1.0)
    #print imAspect
#    cdict ={
#    'blue': ((0.0, 0.01, 0.05), (0.05, 0.75, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
#    'green': ((0.0, 0, 0), (0.125, 0, 0), (0.375, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
#    'red': ((0.0, 0, 0), (0.34999999999999998, 0, 0), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
#    }
    cdict ={
    'blue': ((0.0, 0.01, 0.01), (0.01, 0.25, 1), (0.65000000000000002, 1, 1), (0.75000000000000002, 0, 0), (1, 0, 0)),
    'green': ((0.0, 0, 0), (0.05, 0.75, 0.75), (0.25, 1, 1), (0.64000000000000001, 1, 1), (0.91000000000000003, 0, 0), (1, 0, 0)),
    'red': ((0.0, 0, 0), (0.15, 0.25, 0.25), (0.56000000000000003, 1, 1), (0.89000000000000001, 1, 1), (1, 0.75, 0.75))
    }


    my_cmap = C.LinearSegmentedColormap('mycmap', cdict, 512)
    ax1.imshow(N.transpose(ticLayer), origin = 'lower', aspect = 'auto', cmap = my_cmap)
    ax2.imshow(N.transpose(ticLayer), origin = 'lower', aspect = 'auto')
#    ax1.set_xlim(0, data.rowPoints)
#    ax1.set_ylim(0, data.colPoints)
#    ax1.imshow(ticLayer, aspect = 'auto')

    tic /= tic.max()
    tic *=100
#    bpc /= bpc.max()
#    bpc *=100
    #ax2.plot(tic)
#    ax2.plot(bpc, 'r')


#    x = N.arange(0, 20)
#    y = N.sin(x)
#    ax1.plot(x, y)
#    w.canvas.fig.colorbar(ax1)
    w.show()
    sys.exit(app.exec_())