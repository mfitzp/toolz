import os, sys, traceback
import numpy as N
import supportFunc as SF
import getBaseline as GB
import time


class DataClass(object):
    def __init__(self, xdata,  ydata,  name = None, path = None, interp = False, normOk = False):
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
        self.isoProfileDict = None
        self.isoProfileOk = False
        self.peakParams = None
        self.mplAx = None
        self.plotModVal = 1
        self.noiseEst = None
        self.minNoiseEst = None
        self.noiseOK = False
        self.normFactor = self.y.max()
        self.interpOk = False
        self.mzPad = None#this value is used for peak picking and is equal to the number of points in 0.5 mz units
#        if interp:
#            self.interpOk = True
#        else:
#            self.interpData()
        self.normOk = normOk
        if not self.normOk:
            self.normalize()

    def normalize(self):
        self.y = SF.normalize(self.y)
        self.normOk = True

    def savePkList(self):
        if self.pkListOk:
            t1 = time.clock()
#            print self.name
            #print self.path
            try:
                peakListFN = self.path.replace('.mzXML', '_pks.csv')
#                if os.path.isfile(peakListFN):
                N.savetxt(peakListFN, self.peakList, delimiter = ',', fmt='%.4f')
                print "Peak List Save Time: ", time.clock()-t1

            except:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
    #                    print 'Error saving figure data'
                errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
    #            return QtGui.QMessageBox.warning(self, "Interpolation Error", errorMsg)
                print errorMsg
                print self.path

    def getEICVal(self, mzLo, mzHi, type = 'sum'):#the other type is 'max'
        if mzHi == -1:
            crit = (self.x >= mzLo)
        else:
            crit = (self.x >= mzLo) & (self.x <= mzHi)
        range = N.where(crit)[0]
        if len(range) != 0:
            if type == 'sum':
                return self.y[range].sum()
            elif type == 'max':
                return self.y[range].max()

    def setAxis(self,  mplAxInstance):
        self.axSet = True
        self.mplAx = mplAxInstance

    def setPeakParams(self, paramDict):
        if type(paramDict) == dict:
            self.peakParams = paramDict

    def setIsotopeProfiles(self, isoCentroids, isoListX, isoListY):
        '''
        Used to store the isotope profiles from fitting routine
        '''
        tempDict = {}
        for i,cent in enumerate(isoCentroids):
            tempDict['%.5f'%cent] = [isoListX[i], isoListY[i]]

        self.isoProfileDict = tempDict
        self.isoProfileOk = True
#        print "set isotope patterns"

    def getIsotopeProfiles(self):
        '''
        Calculates isotope profiles of the picked peaks
        '''
        print 'get isotope profiles'


    def setPeakList(self, peakList, normalized = True):
        #reset this feature as different peak picking routines may be used
        self.isoProfileOk = False
        self.isoProfileDict = {}
        #peak list is two arrays peakLoc and intensity

        if normalized:
            if peakList != None:
                if len(peakList)>0:
                    self.pkListOk = True#CHANGE ME True
                    if type(peakList[0]) == N.ndarray:
                        self.peakList = peakList
                    elif type(peakList[0]) == N.float64:
                        self.peakList = N.array([peakList[0],peakList[1]])
        else:
            if peakList != None:
                if len(peakList)>0:
                    self.pkListOk = True#CHANGE ME True
                    if type(peakList[0]) == N.ndarray:
                        self.peakList = peakList
                        self.peakList[:,1] = SF.normalize(self.peakList[:,1])
                    elif type(peakList[0]) == N.float64:
                        self.peakList = N.array([[peakList[0],100.0]])
        #print self.peakList

    def applyTopHat(self):
        self.y = SF.topHat(self.y, 0.01)
        #need to normalize after topHat
        self.normalize()

    def interpData(self):
        #this of course slows loading down but is necessary for the peak picking using CWT
        try:
            newX, newY = SF.interpolate_spectrum_XY(self.x, self.y)

            meanMZ = N.round(newX.mean())
            crit = (newX >= meanMZ) & (newX <= (meanMZ+0.5))#CHECK ME
            #MZ Pad is a windowing factor to find the maximum of the peak rather than a valley.
            #This also must be done after interpolation
            self.mzPad = len(N.where(crit)[0])
#            print "MZ Pad", self.mzPad

            self.x = newX
            self.y = newY

            self.interpOk = True
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
#                    print 'Error saving figure data'
            errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
#            return QtGui.QMessageBox.warning(self, "Interpolation Error", errorMsg)
            print self.name
            print errorMsg

        if self.interpOk:
            self.x = newX
            self.y = newY

    def getNoise(self, numSegs, minSNR):
        noiseEst, minNoiseEst = GB.SplitNSmooth(self.y,numSegs, minSNR)
        if noiseEst != None:
            if len(noiseEst) == len(self.x):
                self.noiseEst = noiseEst
                self.minNoiseEst = minNoiseEst
                self.noiseOK = True
#                print "Get Noise Ok"

    def plot(self, mplAxInstance, pColor = 'r', scatter = False, labelPks = False, plotPks = True,\
             invert = False, plotNoise = False, usrAlpha = 1):
        #if self.axSet:
        self.labelPks = labelPks
        self.mplAx = mplAxInstance
        if self.y != None:
            if invert:
                self.plotModVal = -1
            else:
                self.plotModVal = 1

            if scatter:
                self.mplAx.scatter(self.x,  self.y,  label = self.name)
            else:
                self.mplAx.plot(self.x,  self.y*self.plotModVal,  label = self.name,  picker = 5,  color = pColor, alpha = usrAlpha)
                if plotNoise:
                    if self.noiseOK:
                        self.mplAx.plot(self.x,  self.noiseEst,  label = '_nolegend_',  color = 'r', alpha = 0.6)
                    else:
                        print "No noise to plot"
                if self.pkListOk and plotPks:
                    try:
                        if type(self.peakList[0]) == N.ndarray:
                            self.mplAx.vlines(self.peakList[:, 0], 0, self.peakList[:, 1]*1.15*self.plotModVal,  color = 'r',  label = '_nolegend_')
                            if self.labelPks:
                                for peak in self.peakList:
                                    self.mplAx.text(peak[0], peak[1]*1.1*self.plotModVal, '%.4f'%peak[0],  fontsize=8, rotation = 45)
                        elif type(self.peakList[0]) == N.float64:
                            #this is the case where there is only one value in the peaklist
                            self.mplAx.vlines(self.peakList[[0]], 0, self.peakList[[1]]*1.1*self.plotModVal,  color = 'r',  label = '_nolegend_')
                            if self.labelPks:
                                self.mplAx.text(self.peakList[0], self.peakList[1]*1.1*self.plotModVal, '%.4f'%self.peakList[0],  fontsize=8, rotation = 45)

                        else:
                            print 'Type of First peakList element', type(self.peakList[0])
                            print "Error plotting peak list"

                    except:
                        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
                        errorMsg = "Peak Plot Error:\n\t %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
                        print self.name
                        print errorMsg



        else:
            self.mplAx.plot(self.x,  label = self.name)
#    else:
#        errMsg = 'axis must be set before attempting to plot'
#        raise errMsg
