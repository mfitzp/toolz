import os,sys, traceback
import rpy2
import rpy2.robjects as ro
import rpy2.rinterface as ri
from eicClass import EIC
import time
from PyQt4 import QtCore, QtGui


class StdOutFaker:
    def __init__(self, parent):
        self.P = parent
    def write(self, string):
#        print string
        if string != '\n' and string != ' ' and string != '':
#            pass
            self.P.emitUpdate(string)

class XCMSThread(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.parent = None
        if parent != None:
            self.parent = parent
        self.finished = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.ready = False
        self.numSteps = 0
        self.Rliblist = ['xcms']
        self.Rlibs = self.initRlibs(self.Rliblist)
        self.rtWidth = 200
        self.corType = 'corrected'
        self.useRetCor = False#perform retention time alignment
        self.maxMZ = None#use to truncate the range of peaks extracted
        self.fillPeaksOK = False
        self.curDir = os.getcwd()
        retcorImageName = 'image.png'
        self.imageName = os.path.join(self.curDir, retcorImageName)
        self.matchedFilterParams = {'fwhm':30.,
                                    'sigma':30/2.3548,
                                    'max': 5.,
                                    'snthresh':10.,
                                    'step':0.1,
                                    'steps':2.,
                                    'mzdiff':0.1,
                                    }

        self.matchedFilterTypes = {'fwhm':float,
                                   'sigma':float,
                                   'max':float,
                                   'snthresh':float,
                                   'step':float,
                                   'steps':float,
                                   'mzdiff':float
                                    }

        ##########################
        #this method is not working well yet for the ORBITRAP DATA ACQUIRED AT PNNL
        self.centWaveParams = {'ppm': 10.,
                               'peakwidth': str([20,50]),#this needs to be fixed, the new version of PyQt4 handles this better
                               'snthresh':10.,
                               'prefilter':str([3,100]),
                               'mzdiff':-0.001,
                               }
        self.centWaveTypes = {'ppm': float,
                               'peakwidth': str,
                               'snthresh':float,
                               'prefilter':str,
                               'mzdiff':float,
                               }
        ################################

        self.groupParams = {'bw':30.,
                            'minfrac':0.1,
                            'mzwid':0.1,
                            'max':3
                            }

        self.groupTypes = {'bw':float,
                            'minfrac':float,
                            'mzwid':float,
                            'max':int
                            }
        ##############################
#        'mdevden'
        self.retcorParams = {'extra':2,
                             'span':0.5,
                             'f':'symmetric',
                             'plottype':'none',
                             'missing':2
                             }
        self.retcorTypes = {'extra':int,
                            'span':float,
                            'f':str,
                            'plottype':str,
                            'missing':str
                            }

        #########################
        self.xcmsParamDict = {'Matched Filter':self.matchedFilterParams,
                              'Group Params':self.groupParams,
                              'Retcor Params':self.retcorParams,
                              'CentWave':self.centWaveParams}

        self.xcmsTypeDict = {'Matched Filter':self.matchedFilterTypes,
                             'Group Params':self.groupTypes,
                             'Retcor Params':self.retcorTypes,
                             'CentWave':self.centWaveTypes}


    def updateParamDict(self, paramDict):
        for subKey in paramDict.iterkeys():
            parentDict = paramDict[subKey]
            threadDict = self.xcmsParamDict[subKey]
#            print parentDict
#            print threadDict
            for key in threadDict.iterkeys():
                threadDict[key] = parentDict[key]

    def updateThread(self, fileList, paramDict, rtWidth, fillPeaksBool, corType = 'corrected',\
                     useRetcor = False, maxMZ = None):
        self.fileList = fileList
        self.updateParamDict(paramDict)
        self.rtWidth = rtWidth
        self.numSteps = 3
        self.ready = True
        self.corType = corType
        self.fillPeaksOK = fillPeaksBool
        self.useRetCor = useRetcor
        self.maxMZ = maxMZ
        return True

    def add2ROutput(self, rVector):
        for item in rVector:
            self.emitUpdate(item)
        self.emitUpdate('_\n')

    def setRString(self, xStr = None):
        self.buf = []
        if xStr != None:
            # function that append its argument to the list 'buf'
            self.buf.append(xStr)
            #print buf


    def emitUpdate(self, updateStr):
#        print "OK"
        self.emit(QtCore.SIGNAL("xcmsOutUpdate(PyQt_PyObject)"),updateStr)
#        self.numSteps += -1
#        self.emit(QtCore.SIGNAL("xcmsProgress(PyQt_PyObject)"),self.numSteps)

    def run(self):
        if self.ready:
            try:
                t1 = time.clock()
#                self.Rliblist = ['xcms']
#                self.Rlibs = self.initRlibs(self.Rliblist)
                #sys.stdout = StdOutFaker(self)
                r = ro.r
                #a = r('cdfpath = system.file("cdf", package = "faahKO")')
                #cdfpath = ri.globalEnv.get("cdfpath")
                #r('cdffiles = list.files(cdfpath, recursive = TRUE, full.names = TRUE)')
                #r('cdffiles = cdffiles[1:3]')
                #cdffiles = ri.globalEnv.get("cdffiles")
                self.add2ROutput(self.fileList)
                time.sleep(0.5)
                rfileList = ri.StrSexpVector(self.fileList)
                xset = r.xcmsSet(rfileList, step=self.matchedFilterParams['step'],
                                 mzdiff=self.matchedFilterParams['mzdiff'],
                                 snthresh=self.matchedFilterParams['snthresh'])
                ri.globalEnv["xset"] = xset
#                if self.maxMZ != None:
#                    print type(self.maxMZ)
#                    r('xset@peaks <- xset@peaks[xset@peaks[,"mz"] < %.2f, ]'%self.maxMZ)
#                    self.emitUpdate('max m/z truncated at %.2f\n'%self.maxMZ)

                xset = r.group(xset, bw=self.groupParams['bw'],
                               mzwid=self.groupParams['mzwid'],
                               minfrac=self.groupParams['minfrac'],
                               max=self.groupParams['max'])


                self.emitUpdate('\n\nXSET')
                self.emitUpdate(str(xset)+'\n')
                #ri.setWriteConsole(self.setRString)

                time.sleep(0.5)
#                if self.retcorParams['plottype'] != None:
##                    print self.retcorParams['plottype']self.retcorParams['plottype']
#                    r.png(file=self.imageName)
#                    r('dev.off')


                if self.useRetCor:

                    xset2 = r.retcor(xset,
                                     family=self.retcorParams['f'],
                                     plottype=self.retcorParams['plottype'],
                                     missing=self.retcorParams['missing'],
                                     extra=self.retcorParams['extra'],
                                     span=self.retcorParams['span'])

                    if self.retcorParams['plottype'] == 'mdevden':
                        r.savePlot(file=self.imageName, type = 'png')
                        r('dev.off()')
                    elif self.retcorParams['plottype'] == 'deviation':
                        r.savePlot(file=self.imageName, type = 'png')
                        r('dev.off()')
                else:
                    xset2 = xset
                    retCorStr = "Retention Time Alignment Not Used in Processing!\n"
                    self.emitUpdate(retCorStr)

                ri.globalEnv["xset2"] = xset2
                self.emitUpdate('\n\nXSET2')
                self.emitUpdate(str(xset2)+'\n')
                time.sleep(0.5)
                xset2 = r.group(xset2, bw=self.groupParams['bw'],
                               mzwid=self.groupParams['mzwid'],
                               minfrac=self.groupParams['minfrac'],
                               max=self.groupParams['max'])
                xset3 = r.fillPeaks(xset2)
                self.emitUpdate('\n\nXSET3')
                self.emitUpdate(str(xset3)+'\n')
                time.sleep(0.5)
                ri.globalEnv["xset3"] = xset3
#                gt = r.group(xset3, bw=self.groupParams['bw'],
#                               mzwid=self.groupParams['mzwid'],
#                               minfrac=self.groupParams['minfrac'],
#                               max=self.groupParams['max'])
                tsidx = r.groupnames(xset3)
                ri.globalEnv["tsidx"] = tsidx
                eicmax = r.length(tsidx)
                eic = r.getEIC(xset3, rtrange = self.rtWidth, groupidx = tsidx, rt = self.corType)
#                print self.buf
                eicClass = EIC(eic)
                self.emit(QtCore.SIGNAL("xcmsGetEIC(PyQt_PyObject)"),eicClass)
#                self.emit(QtCore.SIGNAL("xcmsSet(PyQt_PyObject)"),xset2)
                #if this is False then the peak table without the filled peaks will be returned and written to csv
                if self.fillPeaksOK:
                    self.emit(QtCore.SIGNAL("xcmsSet(PyQt_PyObject)"),xset3)
                else:
                    self.emit(QtCore.SIGNAL("xcmsSet(PyQt_PyObject)"),xset2)
                t2 = time.clock()
                self.emitUpdate('\nProcessing Time: %s seconds'%t2)
    #            self.updateGUI()
                sys.stdout=sys.__stdout__
#                ri.endr()
            except:
                self.stop()
                sys.stdout=sys.__stdout__
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
    #                    print 'Error saving figure data'
                errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
#                if self.parent != None:
#                    return QtGui.QMessageBox.warning(self.parent, "R Source Error", errorMsg)
                print errorMsg
                self.emitUpdate(errorMsg)

        else:
            print "Parameters not set or there is an error"



##                if self.loadmzXML:
##                    while not self.finished and self.numItems > 0:
##                        for item in self.loadList:
###                            print os.path.basename(item)
##                            tempmzXML =  mzXMLR(item)
##                            tempSpec = tempmzXML.data['spectrum']
##                            if len(tempSpec)>0:
###                                print 'Spec OK', os.path.basename(item)
##                                data2plot = DataPlot(tempSpec[0],  tempSpec[1],  name = os.path.basename(item), path = item)
##                                data2plot.setPeakList(tempmzXML.data['peaklist'])
##                                #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
##                                #note PyQt_PyObject
##                                self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)
##                            else:
##                                print 'Empty spectrum: ', item
##
##                            self.numItems -=1
##                else:
##                    while not self.finished and self.numItems > 0:
##                        for item in self.loadList:
##                            tempFlex = FR(item)
##                            tempSpec = tempFlex.data['spectrum']
##                            data2plot = DataPlot(tempSpec[:, 0],  tempSpec[:, 1], name = item.split(os.path.sep)[-4], path = item)#the -4 index is to handle the Bruker File Structure
##                            data2plot.setPeakList(tempFlex.data['peaklist'])
##                            #this following line is key to pass python object via the SIGNAL/SLOT mechanism of PyQt
##                            self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),data2plot)#note PyQt_PyObject
##                            self.numItems -=1

    def stop(self):
        print "stop try"
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        print "stop try"
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()

    def __del__(self):
        self.exiting = True
        self.wait()

    def initRlibs(self,libList):
        libDict = {}

        for lib in libList:
            try:
                libDict[lib] = ro.r('library(%s)'%lib)
            except:
                errorMsg ='Error loading R library %s\nCheck Library Installation\n'%lib
                errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg

        return libDict

    def list2rpyFuntions(self,strList):
        funcDict = {}
        for entry in strList:
            try:
                funcDict[entry] = ro.r['%s'%entry]
            except:
                errorMsg ='Error creating function %s'%entry
                errorMsg += "Sorry: %s\n\n:%s\n"%(sys.exc_type, sys.exc_value)
                print errorMsg

        return funcDict