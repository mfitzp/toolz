from PyQt4 import QtCore, QtGui
import os, sys, traceback
import time

import numpy as N
import scipy as S
from matplotlib.lines import Line2D
from mpl_pyqt4_widget import MPL_Widget
#from pepFragMain import pepFrag

from DistanceTable.distanceTable import DiffTable
from mzXMLReader import mzXMLDoc
from xtandemParser import XT_RESULTS
from FragmentPlot import FragPlotWidgets

my_array = [['00','01','50'],
            ['10','11','12'],
            ['20','21','22'],
            ['30','31','32']]

def main():
    app = QtGui.QApplication(sys.argv)
    mzXMLAns = mzXMLDoc('R19.mzXML', sumBool = False)
    #xtAns = XT_RESULTS('R19.xml')
    xtAns = None
    w = SpecDiggerModal(mzXMLResult = mzXMLAns, xtResult = xtAns)
    w.show()
    sys.exit(app.exec_())

class SpecDiggerModal(QtGui.QWidget):
    def __init__(self, mzXMLResult = None, xtResult = None, title = None, annotation = None, colHeaderList = None, rowHeaderList = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
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
        
        if isinstance(mzXMLResult, mzXMLDoc):
            self.mzXMLOk = self.setDataFile(dataFileInstance = mzXMLResult)
        else:
            print "Not and mzXMLDoc"
            #if this fails need to abort TODO
            self.mzXMLOk = self.setDataFile(fileName = self.__getFileName__())
            #self.mzXMLOk = self.setDataFile(fileName = 'R19.mzXML')

            
        if isinstance(xtResult, XT_RESULTS):
            self.xtOk = self.setXTResults(xtInstance = xtResult)
        else:
            try:
                coreName = os.path.splitext(os.path.abspath(self.curDataFileName))[0]
                coreName = coreName+'.xml'
                print "Trying %s as a default X!Tandem Result File"%coreName
                self.xtOk = self.setXTResults(coreName)
            except:
                print "The Core X!Tandem file name is not the same"
                try:
                    self.xtOk = self.setXTResults(fileName = self.__getFileName__())
                except:
                    self.xtOk = False
#            self.setXTResults(fileName = 'R19.xml')


        if title != None:
            self.setWindowTitle(title)
        else:
            try:
                titleTemp = 'Spectrum Digger: %s'%self.curDataFileName
#                print "Temp Title: ", titleTemp
                self.setWindowTitle(titleTemp)
            except:
                self.setWindowTitle('Spectrum Digger')

                            
            
        if annotation != None:
            self.annotation = annotation
            
        if self.xtOk and self.mzXMLOk:#not sure this is working
            self.__updateGUI__()
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


    def __updateGUI__(self):
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
        self.openWindows = []

    def __getFileName__(self):
#        if self.firstLoad:
        dataFileName = QtGui.QFileDialog.getOpenFileName(self,\
                                                         self.OpenDataText,\
                                                         self.__curDir, 'mzXML (*.mzXML);;xml (*.xml);;All Files (*.*)')
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

    def OnPickChrom(self, event):
        if not isinstance(event.artist, Line2D):
            return True

        line = event.artist
        lineLabel = line.get_label()
        if lineLabel == 'X!Tandem Results':
            xVals = self.xtScanVals
            yVals = self.xtHitVals
            self.handleA.set_color('r')
            #print "Length of xVals", len(xVals)
            
        elif lineLabel == 'mzXML':
            xVals = self.scanVals
            yVals = self.BPC
            self.handleA.set_color('y')
        #print lineLabel, type(lineLabel)     
        self.curIndex = event.ind[0]
        curLim = self.mzXMLax.get_xlim()[0]
        lowInd = N.where(xVals<=curLim)[0]
        if len(lowInd)>0:
            lowInd = lowInd[-1]
        else:
            lowInd = 0
        pickInd = lowInd+self.curIndex
        #print "Pick Ind: ", pickInd
        xVal = xVals[pickInd]
        yVal = yVals[pickInd]
        #print "%s Scan #: %s"%(lineLabel, xVal)
        #########Interact with parent
        if lineLabel == 'mzXML':
            self.emit(QtCore.SIGNAL("specSelected(PyQt_PyObject)"),[pickInd, xVal, yVal, lineLabel])
        elif lineLabel == 'X!Tandem Results':
            self.getFragSpectrum(pickInd)
            print "HANDLE X!Tandem RESULTS LOAD FRAG PLOT\n"
        
        #########
#        xdata = line.get_xdata()
#        ydata = line.get_ydata()
        self.handleA.set_visible(True)
#        self.handleAline.set_visible(True)
        #self.handleA.set_data([xdata[self.curIndex], ydata[self.curIndex]])
        self.handleA.set_data([xVal, yVal])
        curXlim = self.mzXMLax.get_xlim()
        self.mzXMLax.set_xlim(curXlim)#needed to prevent autoscale of vline cursor
        self.plotWidget.canvas.draw()

    def getFragSpectrum(self, indexVal):
        try:
            try:
                self.openWindows[-1].close()#close and open children and respawn
            except:
                pass
            #indexVal +=-1#this is because we are counting from zero, but the index table counts from 1
            curSeq = self.curXTResults.dataDict['pepID'][indexVal]
            xData = self.curXTResults.dataDict['xFrags'][indexVal]#this is text and needs to be converted
            yData = self.curXTResults.dataDict['yFrags'][indexVal]
            eValText = str(self.curXTResults.dataDict['pep_eVal'][indexVal])
            theoMZText = '%.2f'%self.curXTResults.dataDict['theoMZ'][indexVal]
            ppmText = '%d'%self.curXTResults.dataDict['ppm_error'][indexVal]
            scanID = '%d'%self.curXTResults.dataDict['scanID'][indexVal]
            hScore = '%.2f'%self.curXTResults.dataDict['hScore'][indexVal]
            fragTitle = 'Index: '+str(indexVal)+', '+curSeq+', '+scanID
            textTag='\n'
            textTag+='e-Val: '
            textTag+= eValText
            textTag+='\nhScore: '
            textTag+=hScore
            textTag+='\n'
            textTag+='m/z: '
            textTag+=theoMZText
            textTag+='\n'
            textTag+='ppm error: '
            textTag+=ppmText

            tempXList = xData.split()
            tempYList = yData.split()
#                print type(tempXList), type(tempYList)
#                print tempXList
            xData = N.array(tempXList, dtype = N.float)#conver to array with dtype set or it will default to string types
            yData = N.array(tempYList, dtype = N.float)
            curFragPlot = FragPlotWidgets.FragPlot(curSeq, xData, yData, title = fragTitle, annotation = textTag)
            curFragPlot.show()
            self.openWindows.append(curFragPlot)
#                print indexVal
#                print curSeq
#                print xData
#                print yData

#                curType = self.infoMap[str(curItem.text())]
#                curVal = self.curSelectInfo[str(curItem.text())]
#                curTbl = self.curTbl
        except:
            raise


    def updatePlotWidget(self):
        self.plotWidget.canvas.mpl_connect('pick_event', self.OnPickChrom)
        self.plotWidget.canvas.format_labels()
        self.plotWidget.canvas.draw()

    def plotXTVals(self):
        self.XTax.vlines(self.xtScanVals, 0, self.scanScores*-1, color='k', lw = 2.0, linestyles='solid')#, alpha = 0.1)
        self.XTax.vlines(self.xtScanVals, 0, self.nextScores*-1, color='r', lw = 2.0, linestyles='solid')#, alpha = 0.7)
        self.XTax.set_ylim((-100,0))
        self.XTax.grid(True)

    def plotMZXML(self):
        if len(self.BPC)>=1:
            self.mzXMLax.plot(self.scanVals, self.BPC, '-ob', ms =2, picker = 3, alpha = 0.5, label = 'mzXML')
            hitIND = []
            for scan in self.xtScanVals:
                curHit = N.where(self.scanVals<scan)[0][-1]#xtXML.dataDict['scanID'] == scanVals)
                #print 'CurHit', curHit
                hitIND.append(curHit)
            self.xtHitVals = self.BPC[N.array(hitIND)]
            if self.xtHitVals != None:
                self.handleA,  = self.mzXMLax.plot([0], [0], 'o', ms=8, alpha=0.5, color='yellow', visible=False, label = 'Cursor A')
                self.mzXMLax.plot(self.xtScanVals, self.xtHitVals, 'og', ms = 5, picker = 3, alpha = 0.6, label = 'X!Tandem Results')
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
            self.curDataFile = dataFileInstance
            self.curDataFileName = self.curDataFile.fileName
            print "%s passed to SpecDigger"%self.curDataFileName
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
            #self.curXTFileName = 'R19.xml'
            self.curXTResults = XT_RESULTS(fileName)
        if xtInstance != None:
            self.curXTResults = xtInstance
        
        self.curXTFileName = self.curXTResults.fileName
        self.xtScanVals = self.curXTResults.dataDict['scanID']
        self.scanScores = self.curXTResults.dataDict['hScore']
        self.nextScores = self.curXTResults.dataDict['deltaH']
        
        xtOrderInd = self.xtScanVals.argsort()
        self.xtScanVals = self.xtScanVals[xtOrderInd]
        self.scanScores = self.scanScores[xtOrderInd]
        self.nextScores = self.nextScores[xtOrderInd]
        
        print "%s Load Time %.4f s"%(self.curXTFileName, time.clock()-t0)
        return True

    def closeEvent(self,  event = None):
        self.__exitProgram__()

    def __exitProgram__(self):
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
