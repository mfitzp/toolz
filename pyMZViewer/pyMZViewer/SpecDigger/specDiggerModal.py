from PyQt4 import QtCore, QtGui
import os, sys, traceback
import time

import numpy as N
import scipy as S
from mpl_pyqt4_widget import MPL_Widget
#from pepFragMain import pepFrag

from DistanceTable.distanceTable import DiffTable
from mzXMLReader import mzXMLDoc
from xtandemParser import XT_RESULTS

my_array = [['00','01','50'],
            ['10','11','12'],
            ['20','21','22'],
            ['30','31','32']]

def main():
    app = QtGui.QApplication(sys.argv)
    w = SpecDiggerModal()
    w.show()
    sys.exit(app.exec_())

class SpecDiggerModal(QtGui.QWidget):
    def __init__(self, mzXMLResult = None, xtResult = None, title = None, annotation = None, colHeaderList = None, rowHeaderList = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if title != None:
            self.setWindowTitle(title)
        else:
            self.setWindowTitle('Spectrum Digger')

        self.resize(660, 600)

        self.vLayout = QtGui.QVBoxLayout(self)
        self.tabWidget = QtGui.QTabWidget(self)

        self.plotTab = QtGui.QWidget()
#        self.plotWidget = MPL_Widget(self.tab2, enableAutoScale = True, enableCSV = True, enableEdit = True)
        self.plotWidget = MPL_Widget(parent = self, enableAutoScale = False, doublePlot = True, enableEdit = True, shareAxis = True)
        self.plotLayout = QtGui.QHBoxLayout(self.plotTab)
        self.plotLayout.addWidget(self.plotWidget)
        self.tabWidget.addTab(self.plotTab, "Plot")        
        
        self.tableTab = QtGui.QWidget()
        self.tableWidget = DiffTable(self.tableTab)
        self.tabLayout = QtGui.QHBoxLayout(self.tableTab)
        self.tabLayout.addWidget(self.tableWidget)

        self.tabWidget.addTab(self.tableTab, "Table")

        self.vLayout.addWidget(self.tabWidget)
        self.tabWidget.setCurrentIndex(0)
        
        self.startup()
        
        ################################################
        self.annotation = None
        
        self.mzXMLOk = False
        self.xtOk = False
        
        if mzXMLResult != None:
            self.mzXMLOk = self.setDataFile(dataFileInstance = mzXMLResult)
        else:
            #if this fails need to abort
            #self.setDataFile(fileName = self.__getFileName__())
            self.mzXMLOk = self.setDataFile(fileName = 'R19.mzXML')

            
        if xtResult != None:
            self.xtOk = self.setXTResults(xtInstance = xtResult)
        else:
            self.xtOk = self.setXTResults(fileName = self.__getFileName__())
#            self.setXTResults(fileName = 'R19.xml')
            
            
        if annotation != None:
            self.annotation = annotation
            
        if self.xtOk and self.mzXMLOk:
            self.__testFunc__()
        ######################

#        if data != None:
#            self.data = data
#            self.tableWidget.addData(self.data)

        ######################

#        if type(colHeaderList) == list:
#            self.tableWidget.setHorizontalHeaderLabels(colHeaderList)
#        if type(rowHeaderList) == list:
#            self.tableWidget.setVerticalHeaderLabels(rowHeaderList)
#        self.tableWidget.resizeColumnsToContents()
#        self.tableWidget.setSortingEnabled(True)
#        self.tableWidget.setCurrentCell(0, 0)#needed so selectedRanges does not fail initially


    def __testFunc__(self):
        self.plotMZXML()
        self.plotXTVals()
        self.updatePlotWidget()


    def getXTResult(self):
        fn = self.__getFileName__()
        if fn != None:
            self.setXTResults()
    
    
    def startup(self):

        self.mzXMLax = self.plotWidget.canvas.ax
        self.XTax = self.plotWidget.canvas.ax2

        self.BPC = None#base peak chromatogram from the mzXML file
        self.expTime = None#experiment time


        self.xtScanVals = None#indices from the main scan where a DB hit was found
        self.hitScans = None#indices from the main scan where a DB hit was found
        self.scanScores = None#primary score values from the DB
        self.nextScores = None#the next closets score from the DB
        
        self.__curDir = os.getcwd()
        self.__setMessages__()

    def __getFileName__(self):
#        if self.firstLoad:
        dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                         self.OpenDataText,\
                                                         self.__curDir, 'XML (*.xml)')
        if dataFileName != None:
            if os.path.isfile(os.path.abspath(str(dataFileName))):
                return os.path.abspath(str(dataFileName))


#        else:
##            if self.__askConfirm__("Data Reset",self.ResetAllDataText):
#            self.startup()
#            dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
#                                                                 self.OpenDataText,\
#                                                                 self.__curDir, 'mzXML (*.mzXML);;mzML (*.mzML)')
#            if dataFileName:
#                self.loadFile(dataFileName)

    def updatePlotWidget(self):
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()

    def plotXTVals(self):
        self.XTax.vlines(self.xtScanVals, 0, self.scanScores*-1, color='k', lw = 2.0, linestyles='solid')#, alpha = 0.1)
        self.XTax.vlines(self.xtScanVals, 0, self.nextScores*-1, color='r', lw = 2.0, linestyles='solid')#, alpha = 0.7)
        self.XTax.set_ylim((-100,0))
        self.XTax.grid(True)

    def plotMZXML(self):
        if len(self.BPC)>=1:
            self.mzXMLax.plot(self.scanVals, self.BPC, '-ob', ms =2, picker = 5, alpha = 0.5)
            hitIND = []
            for scan in self.xtScanVals:
                curHit = N.where(self.scanVals<scan)[0][-1]#xtXML.dataDict['scanID'] == scanVals)
                #print 'CurHit', curHit
                hitIND.append(curHit)
            self.handleA,  = self.mzXMLax.plot([0], [0], 'o', ms=8, alpha=0.5, color='yellow', visible=False, label = 'Cursor A')
            self.mzXMLax.plot(self.xtScanVals, self.BPC[N.array(hitIND)], 'og', ms = 5, alpha = 0.6)
            self.mzXMLax.grid(True)

    def setDataFile(self, fileName = None, dataFileInstance = None):
        '''
        Sets the main mzXML instance for this interface.  Either a single valid file name
        should be passed or an already loaded mzXML instance...not both
        '''
        if fileName != None and dataFileInstance != None:
            print "Pick one mzXML instance, not a file to load and an instance"
            return False
        
        if fileName != None:
#            self.curDataFileName = 'R19.mzXML'
            self.curDataFileName = fileName
            if os.path.isfile(self.curDataFileName):
 
        #        try:
                t0 = time.clock()
                self.curDataFile = mzXMLDoc(self.curDataFileName, sumBool = False)
                print "%s Load Time: %.4f s"%(self.curDataFileName, time.clock()-t0)
                self.BPC = N.array(self.curDataFile.data.get('BPC'))
                self.scanVals = N.array(self.curDataFile.data.get('expTime'), dtype = N.int32)
                return True
        #        except:
        #            print "mzXML Failure"
            else:
                print "%s is not a File"%self.curDataFileName
        elif dataFileInstance != None:
            self.curDataFile = dataFileInstnace
            self.BPC = N.array(self.curDataFile.data.get('BPC'))
            self.scanVals = N.array(self.curDataFile.data.get('expTime'), dtype = N.int32)
            return True
            

    def setXTResults(self, fileName= None, xtInstance = None):
        '''
        Sets the main X!Tandem result instance for this interface.  Either a single valid file name
        should be passed or an already loaded xtResult instance...not both
        '''
        if fileName != None and xtInstance != None:
            print "Pick one XT Result instance, not a file to load and an instance"
            return False        
        
        t0 = time.clock()
        if fileName != None:
            self.curXTFileName = 'R19.xml'
            self.curXTResults = XT_RESULTS(self.curXTFileName)
        if xtInstance != None:
            self.curXTResults = xtInstance
        
        self.xtScanVals = self.curXTResults.dataDict['scanID']
        self.scanScores = self.curXTResults.dataDict['hScore']
        self.nextScores = self.curXTResults.dataDict['deltaH']
        print "%s Load Time %.4f s"%(self.curXTFileName, time.clock()-t0)
        return True


    def __exitProgram__(self):
        if self.okToExit():
            self.close()

    def okToExit(self):
        reply = QtGui.QMessageBox.question(self, "Confirm Quit", "Exit now?",\
                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    def __askConfirm__(self,title,message):
        clickedButton = QtGui.QMessageBox.question(self,\
                                                   title,message,\
                                                   QtGui.QMessageBox.Yes,QtGui.QMessageBox.Cancel)
        if clickedButton == QtGui.QMessageBox.Yes: return True
        return False

    def __showHints__(self):
        return QtGui.QMessageBox.information(self,
                                             ("Hints and Known Issues"),
                                             ("<p> 1.    For files that contain spectra with a high degree of detail (i.e. not centroided (stick) mass spectra) use the profile mode for drawing (Ctrl+D).  Otherwise, the plotting will be slow.</p>"
                                             "<p> 2. I haven't incorporated MS^n (where n >= 3) spectrum views at this point--I didn't have an example file to test.</p>"
                                             "<p>3.  If the program is too slow, remember python is not or ever intended to be C.</p>"
                                             "<p>4.  I have not incorporated a reader for mzData files as this format does not explictly store base peak and TIC values for chromatogram generation.  In order to do this each scan must be read simply to construct the TIC/BPC.  This is very slow.  The new mzML format will be supported in the very near future.</p>"
                                             "<p>4.  Ctrl+Z enables/disables zooming, Ctrl+A zooms out entirely (i.e. autoscale).  These shortcuts are by far the easiest way to navigate</p>"
                                             ""))

    def __showAbout__(self):
        return QtGui.QMessageBox.information(self,
                                            ("mzViewer V.0.5, October, 2009"),
                                            ("<p><b>mzViewer</b> was written in Python by Brian H. Clowers (bhclowers@gmail.com).</p>"
        "<p>Please keep in mind that the entire effort is very much a"
        " work in progress and that Brian won't quit his day job for programming."
        " The original purpose of mzViewer was to provide a user-friendly, open-source tool"
        " for examining common mass spectrometry data formats (e.g. mzXML and mzML* (*in the future)"
        " using numpy and matplotlib.  Feel free to update"
        " (preferably with documentation) mzViewer and please share your contributions"
        " with the rest of the community.</p>"))
    
    def __setMessages__(self):
        '''This function is obvious'''
        self.SaveDataText = "Choose a name for the data file to save:"
        self.ScratchSavePrompt = "Choose file name to save the scratch pad:"
        self.OpenDataText = "Choose a data file to open:"
        self.ResetAllDataText = "This operation will reset all your data.\nWould you like to continue?"


if __name__ == "__main__":
    main()
