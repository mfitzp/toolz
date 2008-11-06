#!/usr/bin/env python


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

        self.startPnt = None
        self.stopPnt = None

        #data are stored as integers but some of the functions
        #need to use floats.  This is a boolean to see if the
        #conversion to floats has occurred
        self.floated = False

    def getHandle(self):
        self.handle = T.openFile(self.filePath, 'r')
        self.fileOpen = True

    def closeHandle(self):
        self.handle.close()
        self.fileOpen = False

    def getBPC(self):
        if self.fileOpen:
            mzCube = self.handle.root.dataCube
            self.BPC, self.BPCmz = self._makeBPC_(mzCube)
            self.closeHandle()

        else:
            self.getHandle()
            if self.fileOpen:
                mzCube = self.handle.root.dataCube
                self.BPC, self.BPCmz = self._makeBPC_(mzCube)
                self.closeHandle()
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

    def getTIC(self):
        if self.fileOpen:
            self.TIC = self.handle.root.TIC.read()
            self.closeHandle()
            self.ticOK = True

        else:
            self.getHandle()
            if self.fileOpen:
                self.TIC = self.handle.root.TIC.read()
                self.closeHandle()
                self.ticOK = True
            else:
                print "Error opening HDF5 data file, no TIC found"



