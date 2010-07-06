import os, sys, traceback
import numpy as N
import supportFunc as SF
import getBaseline as GB
import SG_Filter as SG
import time


class DataClass(object):
    def __init__(self, xdata,  ydata,  name = None, path = None, normOk = False):
        self.x = xdata
        if ydata != None:
            self.y = ydata
        else:
            self.y = None

        if name:
            self.name = name
        else:
            self.name = 'None'

        if path:
            self.path = path
        else:
            self.path = 'None'

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
        self.normOk = normOk
        if not self.normOk:
            self.normalize()

        self.filterOK = False
        self.filter = None
        self.filterFactor = 1
        self.filterVal = 0#used to check if this value already exists
        self.info = ''
        self.filterType = 'None'
        self.initExpParams()

    def initExpParams(self):
        '''
        This is  c:\datamel\10010825.txt
        IMS Cell Temp. =  97.000000  'C
        Atmos Pressure =  748.500000  Torr
        Cell  Voltage  =  3000.000000  Volts
        Uo   Constant  =  53882.000000
        Gas      Type  =  N2
        Carrier  Flow  =  200.000000  ml/min
        Drift    Flow  =  500.000000  ml/min
        Start    Time  =  0.000000  msec
        End      Time  =  40.000000  msec
        Dwell          =  40.000000  usec for  1001.000000  Channels
        Scans         =  200.000000
        '''
        self.temperature = None #in degrees C
        self.pressure = None #in Torr
        self.voltage = None #volts
        self.gasType = 'N2'#He, Argon, CO2, SF6, Air

    def setExpParams(self):
        if "IMS Cell Temp. =" in self.info:#case for a IMS spectrum from a PCP instrument
            paramSplit = self.info.split("=")
            #print paramSplit
#           print paramSplit
            #temperature index = 1, pressure index = 2, voltage index = 3
            self.temperature = N.float(paramSplit[1].split(' ')[2])
            self.pressure = N.float(paramSplit[2].split(' ')[2])
            self.voltage = N.float(paramSplit[3].split(' ')[2])
#           print temperature, type(temperature)
#           print pressure, type(pressure)
#           print voltage, type(voltage)

    def setInfo(self, info):
        if type(info) == str:
            self.info = info
            self.setExpParams()

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

