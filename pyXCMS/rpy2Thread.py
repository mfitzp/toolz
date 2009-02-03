import sys
import rpy2.robjects as ro
import rpy2.rinterface as ri
from eicClass import EIC

from PyQt4 import QtCore, QtGui


class StdOutFaker:
    def __init__(self, parent):
        self.P = parent
    def write(self, string):
#        print string
        if string != '\n' and string != ' ' and string != '':
            pass
#            self.P.emitUpdate(string)

class XCMSThread(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.finished = False
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.ready = True
        self.numSteps = 25
        self.Rliblist = ['xcms']
        self.Rlibs = self.initRlibs(self.Rliblist)

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

        self.groupTypes = {}
        ##############################

        self.retcorParams = {'extra':2,
                             'span':.5,
                             'f':'symmetric',
                             'plottype':"mdevden",
                             'missing':2,
                             }
        self.retcorTypes = {}

        #########################
        self.xcmsParamDict = {'Matched Filter':self.matchedFilterParams,
                               'CentWave':self.centWaveParams}
        self.xcmsTypeDict = {'Matched Filter':self.matchedFilterTypes,
                               'CentWave':self.centWaveTypes}


    def updateParamDict(self, paramDict):
        for subKey in paramDict.iterkeys():
            parentDict = paramDict[subKey]
            threadDict = self.xcmsParamDict[subKey]
            for key in threadDict.iterkeys():
                threadDict[key] = paramDict[key]

    def updateThread(self, fileList, paramDict):
        self.fileList = fileList
        self.updateParamDict(paramDict)
        self.numSteps = 3
        self.ready = True
        return True

    def add2ROutput(self, rVector):
        for item in rVector:
            self.emitUpdate(item)
        self.emitUpdate('_\n')

    def emitUpdate(self, updateStr):
#        print "OK"
        self.emit(QtCore.SIGNAL("xcmsOutUpdate(PyQt_PyObject)"),updateStr)
#        self.numSteps += -1
#        self.emit(QtCore.SIGNAL("xcmsProgress(PyQt_PyObject)"),self.numSteps)

    def run(self):
        try:
            sys.stdout = StdOutFaker(self)
            r = ro.r
            a = r('cdfpath = system.file("cdf", package = "faahKO")')
            cdfpath = ri.globalEnv.get("cdfpath")
            r('cdffiles = list.files(cdfpath, recursive = TRUE, full.names = TRUE)')
            r('cdffiles = cdffiles[1:2]')
            cdffiles = ri.globalEnv.get("cdffiles")
#                if len(cdffiles) == 0:
#                    rMsg = 'Open R and enter the following:\nsource("http://bioconductor.org/biocLite.R")\nbiocLite("faahKO")'
#                    return QtGui.QMessageBox.warning(self, "Error with Test Data", rMsg )
            self.add2ROutput(cdffiles)
            xset = r.xcmsSet(cdffiles)
            ri.globalEnv["xset"] = xset
            xset = r.group(xset)
            self.emitUpdate('\n\nXSET')
            self.emitUpdate(str(xset)+'\n')


            xset2 = r.retcor(xset, family = "symmetric", plottype = "mdevden")
            ri.globalEnv["xset2"] = xset2
            self.emitUpdate('\n\nXSET2')
            self.emitUpdate(str(xset2)+'\n')
            xset2 = r.group(xset2, bw = 10)
            xset3 = r.fillPeaks(xset2)
            self.emitUpdate('\n\nXSET3')
            self.emitUpdate(str(xset3)+'\n')
            ri.globalEnv["xset3"] = xset3
            gt = r.groups(xset3)
            tsidx = r.groupnames(xset3)
            ri.globalEnv["tsidx"] = tsidx
            eicmax = r.length(tsidx)
            eic = r.getEIC(xset3, rtrange = 150, groupidx = tsidx, rt = "corrected")
            eicClass = EIC(eic)
            self.emit(QtCore.SIGNAL("xcmsGetEIC(PyQt_PyObject)"),eicClass)
#            self.updateGUI()
            sys.stdout=sys.__stdout__
        except:
            sys.stdout=sys.__stdout__



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