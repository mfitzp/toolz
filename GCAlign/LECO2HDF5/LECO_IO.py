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
#HDF5 File saver
from hdfIO import saveDict, loadHDF5#accepts a dictionary of pupynere objects and a file name


#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"


def open_file():
    filename = str(QFileDialog.getOpenFileName())
    if filename:
        #print "Opened: ", filename
        return filename

class ChromaTOF_Reader:
    def __init__(self,  path,  fileType = None, GC2Time = None):

        self.fileType = fileType
        if self.fileType != 'NetCDF' and self.fileType != 'HDF5':
            print "NO FILE TYPE SPECIFIED, TRY AGAIN!!"
            return

        # the keys used to retrieve certain data from the NetCDF file
        self.fileName = path

        self.path = None
        self.vars = None
        self.loadOK = False
        self.ticOK =False
        self.sicOK = False
        #this is stored in the file, it is known based upon the experiment setup
        #blame LECO not me. 500 points == 5 seconds
        if GC2Time != None:
            self.colPoints = int(GC2Time)
        else:
            self.colPoints = 500#default of 5 seconds
        self.rowPoints = None
        self.mz = None
        self.intensity =None
        self.pntCount = None
        self.scanIndex = None
        self.ticLayer = None
        self.TIC = None
        self.SIC = None
        self.mzMin = None
        self.mzMax = None
        self.rTime = None

        self.initFile()

    def initFile(self):
        try:
            if self.fileType == 'HDF5':
                self.file,  self.vars = loadHDF5(self.fileName)
                #self.TIC = self.vars['total_intensity'].read()
                #print self.TIC
                #print type(self.TIC)
                #self.file.close()

            elif self.fileType == 'NetCDF':
                self.file = CDF(self.fileName)
                self.vars = self.file.variables
            self.populateValues()
        except:
            errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg
            print "Cannot open file '%s'"%self.fileName

    def populateValues(self):
        try:
            if self.fileType =='NetCDF':

                #self.mz = N.array(self.vars['mass_values'].data)
                #self.intensity = N.array(self.vars['intensity_values'].data)
                self.scanIndex = N.array(self.vars['scan_index'].data)
                self.pntCount = N.array(self.vars['point_count'].data)
                self.TIC = N.array(self.vars['total_intensity'].data)
                self.rowPoints = len(self.scanIndex)/self.colPoints
                self.loadOK = True
                #print self.fileName, ' NetCDF Loaded'
            elif self.fileType == 'HDF5':
                self.scanIndex = self.vars['scan_index'].read()
                self.pntCount = self.vars['point_count'].read()
                self.TIC = self.vars['total_intensity'].read()
                self.rowPoints = int(len(self.scanIndex)/self.colPoints)
                self.loadOK = True
        except:
            errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
            print errorMsg
            print 'Data parse for %s failed'%self.fileName

    def makeSIC(self, mzValue):
        #mzValue is an integer
        if self.loadOK:
            t1 = time.clock()
            self.SIC = []
            m = 0#needed to iterate through pntCount
            if self.fileType =='NetCDF':
                for i in self.scanIndex:
                    localMaxIndex = i+self.pntCount[m]
                    localMZ = N.array(self.vars['mass_values'].data[i:localMaxIndex])
                    if mzValue > localMZ.max:#the following tests to see if the mz is found within the limits of the mz list
                        mzIntesnity = 0
                        self.SIC.append(mzIntesnity)
                    elif mzValue < localMZ.min():
                        mzIntesnity = 0
                        self.SIC.append(mzIntesnity)
                    else:
                        mzIndex = N.searchsorted(localMZ, mzValue)
                        localIntesnity = N.array(self.vars['intensity_values'].data[i:localMaxIndex])
                        mzIntesnity = localIntesnity[mzIndex]
                        self.SIC.append(mzIntesnity)
                    m+=1
            elif self.fileType == 'HDF5':
                for i in self.scanIndex:
                    localMaxIndex = i+self.pntCount[m]
                    localMZ = self.vars['mass_values'].read()[i:localMaxIndex]
                    if mzValue > localMZ.max:#the following tests to see if the mz is found within the limits of the mz list
                        mzIntesnity = 0
                        self.SIC.append(mzIntesnity)
                    elif mzValue < localMZ.min():
                        mzIntesnity = 0
                        self.SIC.append(mzIntesnity)
                    else:
                        mzIndex = N.searchsorted(localMZ, mzValue)
                        localIntesnity = self.vars['intensity_values'].read()[i:localMaxIndex]
                        mzIntesnity = localIntesnity[mzIndex]
                        self.SIC.append(mzIntesnity)
                    m+=1

            self.SIC = N.array(self.SIC)
            self.sicOK = True
            #print "1D SIC Created"

    def make2DSIC(self):
        if self.sicOK:
            #print len(self.SIC)
            sicLayer = N.empty((self.rowPoints, self.colPoints), dtype = int)
            x = 0
            for j in xrange(len(self.SIC)):
                y=j%500
                sicLayer[x][y] = self.SIC[j]
                if j !=0 and (j%500) == 0:
                    x+=1
            print "SIC Layer Created"
            return sicLayer
        else:
            print "SIC Must be created first...."


    def make2DTIC(self):
        if self.loadOK:
            self.ticLayer = N.empty((self.rowPoints, self.colPoints), dtype = int)#  self.colPoints),  dtype=int)
            print self.ticLayer.shape
            x = 0
            for i in xrange(len(self.TIC)):
                y=i%self.colPoints
                self.ticLayer[x][y] = self.TIC[i]
                if i !=0 and (i%self.colPoints) == 0:
                    x+=1
#            for i in xrange(self.rowPoints):
#                for j in xrange(self.colPoints):
#                    startInd = self.scanIndex[i+j]
#                    ticPnt = sum(N.array(self.vars['intensity_values'].data[startInd:startInd+self.pntCount[i+j]]))
#                    self.ticLayer[i, j]=ticPnt
            self.ticOK = True
            print '2D TIC created'
            return True

    def get2DTIC(self):
        if self.ticOK:
            return self.ticLayer

    def close(self):
        self.file.close()



if __name__ == "__main__":

    import pylab as P

    #from scipy import ndimage
    #from matplotlib.lines import Line2D
    #app = QApplication(sys.argv)
    fn = 'TAi-R1.h5'#'TAi-R1.h5'#open_file()
    fn2 = 'TCiv-R1.h5'
    fn2OK = True#True
    saveOK = False
    sicOK = False
    ticOK = False
    imageOK = True#False

    if fn:
        t1 = time.clock()
        dataFile = ChromaTOF_Reader(fn,  fileType = 'HDF5')# or 'HDF5' or 'NetCDF'
        if fn2OK:
            dataFile2 = ChromaTOF_Reader(fn2,  fileType = 'HDF5')# or 'HDF5' or 'NetCDF'
        fig = P.figure()
        ax = fig.add_subplot(111)
        if imageOK:

            if dataFile.make2DTIC():
                TIC = dataFile.get2DTIC()
                t2 = time.clock()
                print t2-t1
                imAspect = dataFile.rowPoints/(dataFile.colPoints*1.0)
                #ax.imshow(TIC)
                #ax.imshow(N.transpose(TIC), aspect = imAspect,  alpha = 1,  origin = 'lower')#,  cmap = P.copper())
                ax.contour(N.transpose(TIC), alpha = 1,  origin = 'lower')#,  cmap = P.copper())
                if fn2OK:
                    if dataFile2.make2DTIC():
                        TIC2 = dataFile2.get2DTIC()
                        imAspect2 = dataFile2.rowPoints/(dataFile2.colPoints*1.0)
                        #ax.imshow(N.transpose(TIC2), aspect = imAspect2,  alpha = 0.6,  origin = 'lower',  cmap = P.hot())
                        ax.contour(N.transpose(TIC2),  alpha = 0.6,  origin = 'lower',  cmap = P.hot())
        if ticOK:
            print len(dataFile.TIC)
            print dataFile.rowPoints
            print dataFile.colPoints
            ax.plot(dataFile.TIC)

        P.show()
        if sicOK:
            t1 = time.clock()
            dataFile.makeSIC(41)
            if dataFile.sicOK:
                fig2 = P.figure()
                ax2 = fig2.add_subplot(111)
                SIC2D = dataFile.make2DSIC()
                ax2.imshow(N.transpose(SIC2D), origin = 'lower')
                #ax2.plot(dataFile.SIC)

                t2=time.clock()
                P.show()
                print t2-t1,  "SIC Create Time"
        if saveOK:
            t3 = time.clock()
            try:
                dataFile.vars.pop('error_log')
            except:
                print "Error caught trying to pop 'error_log'"
                pass
    #        for item in dataFile.vars.iteritems():
    #            print item[0], item[1].data
            saveDict(dataFile.vars, 'Hexane.h5')
            t4 = time.clock()
            print t4-t3

        dataFile.close()
        if fn2OK:
            dataFile2.close()
    #sys.exit(app.exec_())
    #sys.exit()



