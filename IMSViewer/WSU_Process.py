#!/usr/bin/env python
###################################
'''
'''
###################################
import os, sys, traceback
from PyQt4 import QtCore, QtGui
import pylab as P
import numpy as N
import supportFunc as SF
import getBaseline as GB
import SG_Filter as SG
import time


class WSUDataClass(object):
    def __init__(self, x, y, mzX, mzY, name = None, path = None, normOk = False):

        if name:
            self.name = name
        else:
            self.name = 'None'

        if path:
            self.path = path
        else:
            self.path = 'None'

        self.x = x
        self.y = y
        self.mzX = mzX
        self.mzY = mzY

        self.axSet = False
        self.peakList = None
        self.pkListOk = False
        self.labelPks = False
        self.peakList = None
        self.peakParams = None
        self.mplAx = None
        self.plotModVal = 1
        self.noiseEst = None
        self.minNoiseEst = None
        self.noiseOK = False
        self.normFactor = self.y.max()
        self.filterOK = False
        self.filter = None
        self.filterFactor = 1
        self.filterVal = 0#used to check if this value already exists
        self.info = ''
        self.filterType = 'None'
        self.initExpParams()
#        self.setData()

        self.normOk = normOk
        if not self.normOk:
            self.normalize()

    def setData(self):
        if os.path.isfile(self.path):
            f = open(self.path, 'r')
            header = []
            for i in xrange(15):
                header.append(f.readline())
            f.close()

            mobX = header[-1]
            mobX = mobX.split(' ')
            mobX.pop(0)
            mobX = N.array(mobX, dtype = float)

            wsu = P.load(self.path, skiprows = 15)
            mzX = wsu[:,0]#extracts the m/z domain
            wsu = wsu[:,1:]#gets rid of first column which is the m/z values

            mobY = wsu.sum(axis = 0)


            mzY = wsu.sum(axis = 1)
            #clean up and assign to class
            header.pop(-1)
            self.info = header
            self.x = mobX
            self.y = mobY
            self.mzX = mzX
            self.mzY = mzY

    def initExpParams(self):
        '''
        WSU Data Header similar to below:

        Mobility v2.2 (beta) compiled Jun 24 2003 14:20:54
        This data was saved on 12/11/08 17:03:35
        ID:
        # of Extractions = 700 ; # of Interleaves = 1
        TDC Resolution: 2.500 nsec
        TDC Active Time: 35.800 usec
        Drift Time = 5.000 msec
        Histogram length: 13201 cells
        TOF start delay = 2.8 usec
        Extraction Frequency = 25 kHz
        Extraction Pulse Width = 2.00 usec ; # of Laser Pulses = 14610
        Laser Frequency = 25 Hz
        Mass1: 35.000 Time1: 7.3500
        Mass2: 289.090 Time2: 20.6575
        '''
        self.temperature = None #in degrees C
        self.pressure = None #in Torr
        self.voltage = None #volts
        self.gasType = 'N2'#He, Argon, CO2, SF6, Air

    def setExpParams(self):
        if "Mass Counts" not in self.info:#case for a IMS spectrum from a PCP instrument
            paramSplit = self.info.split("=")
            #temperature index = 1, pressure index = 2, voltage index = 3
            self.temperature = 1.0#N.float(paramSplit[1].split(' ')[2])
            self.pressure = 1.0#N.float(paramSplit[2].split(' ')[2])
            self.voltage = 1.0#N.float(paramSplit[3].split(' ')[2])
#           print temperature, type(temperature)
#           print pressure, type(pressure)
#           print voltage, type(voltage)

    def setInfo(self, info):
        if type(info) == str:
            self.info = info
            self.setExpParams()
        elif type(info) == list:
            self.info = info

    def setFiltered(self, filterArray, filterVal):
        if filterVal != self.filterVal:
            self.filterVal = filterVal
            self.filterFactor = filterArray.max()
            self.filter = SF.normalize(filterArray)
            self.filterType = "Low Pass Freq %.2f Hz"%filterVal
            self.filterOK = True

    def normalize(self):
        self.y = SF.normalize(self.y)
        self.normOk = True

    def setAxis(self,  mplAxInstance):
        self.axSet = True
        self.mplAx = mplAxInstance

    def applyTopHat(self):
        self.y = SF.topHat(self.y, 0.01)

    def applySGFilter(self, usrKernel = 17, usrOrder = 3):
        try:
            self.filter = SG.savitzky_golay(self.y, kernel = usrKernel, order = usrOrder)
        except:
            usrKernel = 17
            usrOrder = 3
            self.filter = SG.savitzky_golay(self.y, kernel = usrKernel, order = usrOrder)
            print "Param Error, reverting to default"
        self.filterFactor = 100
        self.filterType = "SG K = %s, O = %s"%(usrKernel,usrOrder)
        self.filterOK = True

    def getNoise(self, numSegs, minSNR):
        noiseEst, minNoiseEst = GB.SplitNSmooth(self.y,numSegs, minSNR)
        if noiseEst != None:
            if len(noiseEst) == len(self.x):
                self.noiseEst = noiseEst
                self.minNoiseEst = minNoiseEst
                self.noiseOK = True
#                print "Get Noise Ok"

    def plot(self, mplAxInstance, pColor = 'r', scatter = False, labelPks = False, plotPks = False,\
             invert = False, plotNoise = False, plotFilter = False, ignoreRaw = False, ignoreNorm = True,\
             usrAlpha = 1):
        #if self.axSet:
        self.labelPks = labelPks
        self.mplAx = mplAxInstance
        normFactor = self.normFactor/100
        filterFactor = normFactor*self.filterFactor/100#/self.normFactor
        if ignoreNorm:
            normFactor = 1
            filterFactor = 1
        if self.y != None:
            if invert:
                self.plotModVal = -1
            else:
                self.plotModVal = 1

            if scatter:
                self.mplAx.scatter(self.x,  self.y,  label = self.name)
            else:
                filterColor = 'r'
                filterLabel = '_nolegend_'
                filterAlpha = 0.6
                filterPicker = None
                if ignoreRaw:
                    if self.filterOK:
                        plotFilter = True
                        filterColor = pColor
                        filterLabel = self.name
                        filterAlpha = 1
                        filterPicker = 5
                        pass
                    else:
                        self.mplAx.plot(self.x,  self.y*self.plotModVal*normFactor,  label = self.name,  picker = 5,  color = pColor, alpha = usrAlpha)
                else:
                    self.mplAx.plot(self.x,  self.y*self.plotModVal*normFactor,  label = self.name,  picker = 5,  color = pColor, alpha = usrAlpha)

                if plotNoise:
                    if self.noiseOK:
                        self.mplAx.plot(self.x,  self.noiseEst,  label = '_nolegend_',  color = 'r', alpha = 0.6)
                    else:
                        print "No noise to plot"
                if plotFilter:
                    if self.filterOK:
                        self.mplAx.plot(self.x, self.filter*filterFactor, label = filterLabel,  picker = filterPicker, color = filterColor, alpha = filterAlpha)



        else:
            self.mplAx.plot(self.x,  label = self.name)




if __name__ == "__main__":
    import sys
    import gzip
    import time
    from mpl_pyqt4_widget import MPL_Widget
    app = QtGui.QApplication(sys.argv)
    w = MPL_Widget()
    w2 = MPL_Widget()
    t1 = time.clock()
    f = open('C:\Sandbox\WSU_IMS.txt', 'r')
#    f = gzip.open('C:\Sandbox\WSU_IMS.txt.gz', 'rb')
    header = []
    for i in xrange(15):
        header.append(f.readline())
    f.close()

    mobX = header[-1]
#    header.pop(len(header)-1)
    dummyHeader = ''
    header.pop(-1)
    for entry in header:
        dummyHeader+=entry
#    dummyHeader.join(header)
    header = dummyHeader
    print type(header)
    print header

    mobX = mobX.split(' ')
    mobX.pop(0)
    mobX = N.array(mobX, dtype = float)

#    wsu = P.load('C:\Sandbox\WSU_IMS.txt.gz', skiprows = 15)
    wsu = P.load('C:\Sandbox\WSU_IMS.txt', skiprows = 15)
    mzX = wsu[:,0]#extracts the m/z domain
    wsu = wsu[:,1:]#gets rid of first column which is the m/z values

    mobY = wsu.sum(axis = 0)
    print "mobY", len(mobY)

    mzY = wsu.sum(axis = 1)
    print "mzY", len(mzY)
    print time.clock()-t1
    w.canvas.ax.plot(mobX, mobY)
#    w2.canvas.ax.plot(mzX, mzY)
    w.show()
#    w2.show()
    sys.exit(app.exec_())