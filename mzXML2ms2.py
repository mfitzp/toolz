# -------------------------------------------------------------------------
#     This file was modified from mMass - the spectrum analysis tool for MS.
#     Copyright (C) 2005-07 Martin Strohalm <mmass@biographics.cz> by 
#     Brian H. Clowers 2008.

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------


########################
'''CONVERTS mxXML FILE TO MS2 FILE USED BY THE CRUX PEPTIDE SEARCHING
SOFTWARE written by Mike Macoss and William Noble at UW.

Modified in July 2008 by Brian Clowers to include the cElement Tree
for a faster parsing of the XML file.  Additional functions were added
to allow the primary program to access fragment ion spectra.'''


########################

import sys
import os
import os.path

from PyQt4 import QtGui
from PyQt4 import QtCore

import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import base64
import struct

import numpy as N

# load modules



class mzXMLDoc:
    """ Get and format data from mzXML document. """

    # ----
    def __init__(self, path, minPeakCount = None, minmass=None,  maxmass=None,  parent=None):
        if parent:
            self.parent = parent
        if minPeakCount:
            self.minPeakCount = minPeakCount
        else:
            self.minPeakCount = 0
        
        if minmass:
            self.minmass = minmass
        
        if maxmass:
            self.maxmass = maxmass
        
        self.data = {
                    'docType':'mzXML',
                    'scanID':'',
                    'date':None,
                    'operator':None,
                    'institution':None,
                    'contact':None,
                    'manufacturer':None,
                    'msModel':None,
                    'msType': None, 
                    'ionization':None, 
                    'notes':'',
                    'peaklist':[],
                    'spectrum':[],
                    'totalScans':'', 
                    'expTime':[]
                    }
        
        self.Hmass=1.007276
        self.conversion = False
        self.curScanWrite = 0
        
        self.filename = path
        self.ns = None #namespace
        self.elmName = None
        self.scanList = None
        self.header = None
        self.precursorList = []
        self.getDocument(self.filename)
        self.initiateMS2File(self.filename)
        self.writeScans()  
    # ----

    def initiateMS2File(self,  filename):
        if self.filename:
            if os.sys.platform == 'win32':
                self.path2write = (self.filename.split('\\'))[-1].replace(".mzXML", "")+'.ms2'
            else:
                self.path2write = (self.filename.split('//'))[-1].replace(".mzXML", "")+'.ms2'#assumes linux2 and or OSX (win32 uses the 'bad' kind of slash)
            ms2write = file(self.path2write,  'w')
            if self.data.get('date'):
                ms2write.write('H\t%s\n' %(self.data.get('date')))
            if self.data.get('operator'):
                ms2write.write('H\t%s\n'%(self.data.get('operator')))
            if self.data.get('institution'):
                ms2write.write('H\t%s\n'%(self.data.get('institution')))
            if self.data.get('contact'):
                ms2write.write('H\t%s\n'%(self.data.get('contact')))
            if self.data.get('manufacturer'):
                ms2write.write('H\t%s\n'%(self.data.get('manufacturer')))
            if self.data.get('msModel'):
                ms2write.write('H\t%s\n'%(self.data.get('msModel')))
            if self.data.get('msType'):
                ms2write.write('H\t%s\n'%(self.data.get('msType')))
            if self.data.get('ionization'):
                ms2write.write('H\t%s\n'%(self.data.get('ionization')))
            ms2write.write('H\tMinimum # of Peaks per spectrum: %d\n'%(self.minPeakCount))
            ms2write.write('H\tComments: Converted using mzXML2MS2 by Brian H. Clowers\n')
            #ms2write.write('H\t'+self.data.get('notes')+'\n')
            #print self.data
            ms2write.close()
            self.HWritten = True

    def writeScans(self):
        if self.HWritten:
            ms2write = file(self.path2write,  'a')
            #print type(self.precursorList)
            if len(self.precursorList) == 0:
                raise "There are no scans in the file...try again slick!\n"
            pb = ProgressBar(len(self.precursorList))
            pb.show()
            self.curScanWrite = 0
            

            
            for scan in self.precursorList:
                ms2write.write('S\t%s\t%s\t%s\n' % (scan['scanID'], scan['scanID'], scan['precursor']))
                ms2write.write('I\tRTime\t%s\n' % (scan['RT']))
                ###This is a hack
                mz1 = float(scan['precursor'])
                ms2write.write('Z\t1\t%.2f\n' % (mz1))
                mz2 = 2*float(scan['precursor'])-(1*self.Hmass)
                ms2write.write('Z\t2\t%.2f\n' % (mz2))
                mz3 = 3*float(scan['precursor'])-(2*self.Hmass)
                ms2write.write('Z\t3\t%.2f\n' % (mz3))
                ##
                
                if len(scan['spectrum']) > 0:
                    mz_vector = scan['spectrum'][0]
                    int_vector = scan['spectrum'][1]
                    i = 0
                    for i in xrange(len(mz_vector)):
                        ms2write.writelines('%.4f %.f\n'%(mz_vector[i], int_vector[i]))
                
                self.curScanWrite+=1
                pb.barUpdate(self.curScanWrite)
                
            ms2write.close()
            self.conversion = True
            print "Converion of %s is done."%self.filename
        
        else:
            print "No file initiated"
                        
    
    def getDocument(self, path):
        """ Read and parse all data from document. """

        # parse XML
        try:
            #self.filename = path
            document = ET.parse(path).getroot()
            self.ns = document.tag.split('}')[0]+'}' #makes a string '{some namespace}'
            #document = xml.dom.minidom.parse(path)
        except:
            return False

        # get spectrum
        element = document.find(self.ns+'msRun')
        
        instrument = element.find(self.ns+'msInstrument')
        #print instrument.getchildren()

        if instrument:
            self.handleDescription(instrument)
        


        self.data['totalScans'] = int(element.get('scanCount'))
        #print self.data['totalScans']
        if element:
            self.scanList = element.findall(self.ns+'scan')
            status = self.handleSpectrumList(self.scanList)
            #status = self.handleSpectrumList(element[0])

            # error in data
            if status == False:
                return False

            # no spectrum selected
            elif status == None:
                return None

        # no msRun tag found
        else:
            return False

        # # get description
        # instrument = element.find(self.ns+'msInstrument')
        # #element = document.getElementsByTagName('msInstrument')

        # if instrument:
            # self.handleDescription(instrument)

        # #return self.data
    # ----

    # ----
    def handleDescription(self, elements):
        """ Get document description from <msInstrument> element. """

        # msManufacturer
        msManufacturer = elements.find(self.ns+'msManufacturer')
        #print msManufacturer.get('value')
        if msManufacturer != None:
            self.data['manufacturer'] = msManufacturer.get('value')

        # msModel
        msModel = elements.find(self.ns+'msModel')

        if msModel != None:
            self.data['msModel'] = msModel.get('value')

        # msIonisation
        msIonisation = elements.find(self.ns+'msIonisation')

        if msIonisation != None:
            self.data['ionization'] = msIonisation.get('value')

        # msMassAnalyzer
        msMassAnalyzer = elements.find(self.ns+'msMassAnalyzer')

        if msMassAnalyzer != None:
            self.data['msType'] = msMassAnalyzer.get('value')

        # operator
        operator = elements.find(self.ns+'operator')

        if operator != None:
            self.data['operator'] = '%s %s' % (operator.get('first'), operator.get('last'))
            self.data['contact'] = '%s %s %s' % (operator.get('phone'), operator.get('email'), operator.get('URI'))


        return True
    # ----

    def handleSpectrumList(self, elements):
        """ Get list of spectra from <spectrumList> element. """
        spectra = elements
        if not spectra:
            return False

        self.getMS2Scans(spectra)
        return True
    # ----

    def getMS2Scans(self, spectra):
        '''Get Precursor Ion Scans'''
        for scan in spectra:
            fragspec = scan.findall(self.ns+'scan')
            if fragspec:
                for subscan in fragspec:
                    #print type(subscan.get('msLevel'))
                    if int(subscan.get('msLevel')) == 2 and int(subscan.get('peaksCount')) >= self.minPeakCount:
                        #print self.getSpectrum(subscan)
                        self.precursorList.append(self.getSpectrum(subscan))
        
                  
        

    def getSpectrum(self, spectrum):
        """ Get spectrum data from <spectrum> element. """
        curScan = {
                        'scanID':'', 
                        'precursor':'', 
                        'RT':'', 
                        'Z':'', 
                        'spectrum':''
                        }
        # get data element
        peaks = spectrum.find(self.ns+'peaks')
        
        if peaks == None:
            return False

        # get endian or use default(!)
        if peaks.get('byteOrder') == 'network':
            endian = '!'
        elif peaks.get('byteOrder') == 'little':
            endian = '<'
        elif peaks.get('byteOrder') == 'big':
            endian = '>'
        else:
            endian = '!'

        # get raw data
        data = peaks.text

        # decode data
        try:
            data = base64.b64decode(data)
        except:
            return False

        # convert from binary format
        try:
          pointsCount = len(data)/struct.calcsize(endian+'f')
          start, end = 0, len(data)
          data = struct.unpack(endian+'f'*pointsCount, data[start:end])
        except:
            return False
        #print type(data)

        # split data to m/z and intensity
        mzData = data[::2]
        #print type(mzData)
        intData = data[1::2]

        # check data
        if not mzData or not intData or (len(mzData) != len(intData)):
            return False

        curScan['spectrum'] = [N.array(mzData), N.array(intData)]
        scanInfo = self.getScanInfo(spectrum)
        curScan['scanID']=scanInfo['id'] 
        curScan['precursor'] = scanInfo['mz']
        curScan['Z'] = scanInfo['charge']
        curScan['RT'] =scanInfo['time']
            
        return curScan


    # ----
    def getScanInfo(self, scan):
        """ Get basic info about selected scan. """
        
        scanInfo = {}
        scanInfo['type'] = '---'
        scanInfo['level'] = '---'
        scanInfo['range'] = '---'
        scanInfo['points'] = '---'
        scanInfo['polarity'] = '---'
        scanInfo['time'] = '---'
        scanInfo['mz'] = '---'
        scanInfo['charge'] = '---'
        scanInfo['method'] = '---'
        
        # get ID
        scanInfo['id'] = scan.get('num')
        
        # get msLevel
        scanInfo['level'] = scan.get('msLevel')

        # get number of points
        scanInfo['points'] = scan.get('peaksCount')

        # get polarity
        scanInfo['polarity'] = scan.get('polarity')

        # get retention time
        scanInfo['time'] = scan.get('retentionTime')

        # get range
        lowMz = scan.get('lowMz')
        highMz = scan.get('highMz')
        
        
        try:
            scanInfo['range'] = '%d - %d' % (float(lowMz), float(highMz))
        except:
            scanInfo['range'] = '%s - %s' % (lowMz, highMz)

        # find precursor params
        if scanInfo['level'] and scanInfo['level'] != '1':
            precursorMz = scan.find(self.ns+'precursorMz')

            scanInfo['mz'] = precursorMz.text


        return scanInfo
    # ----

##########################################

class ProgressBar(QtGui.QWidget):
    def __init__(self, maxRange, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('File Conversion Progress')

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.maxRange = maxRange
        self.pbar.setRange(0, self.maxRange)
        self.pbar.setValue(0)
        self.step = 0;
        
    def barUpdate(self, value):
        if self.step >= self.maxRange:
            return

        self.step +=1
        self.pbar.setValue(value)



class OpenFile(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Convert mzXML to MS2')
        self.centralwidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.vlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.label = QtGui.QLabel("Set the Minimum # of Peaks per Scan:")
        self.spinBox = QtGui.QSpinBox()
        self.spinBox.setValue(50)
        self.textEdit = QtGui.QTextEdit()
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.spinBox)
        self.vlayout.addWidget(self.textEdit)
        self.statusBar()
        self.setFocus()

        exit = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        exit.setShortcut('Ctrl+O')
        exit.setStatusTip('Open new File')
        self.connect(exit, QtCore.SIGNAL('triggered()'), self.showDialog)

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        self.curDir = os.getcwd()

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Select mzXML file to convert',self.curDir, 'mzXML (*.mzXML)')
        if filename:
            self.fileType= str(filename).split('.')[-1]
            if self.fileType == 'mzXML':
                try:
                    mzx = mzXMLDoc(filename, self.spinBox.value())
                    if mzx.conversion:
                        self.textEdit.setText("%s\nFile Successfully Converted"%(filename))
                except:
                    self.textEdit.setText("Sorry: %s:%s"%(sys.exc_type, sys.exc_value))


#######################################



if __name__ == "__main__":


    app = QtGui.QApplication(sys.argv)
    cd = OpenFile()
    cd.show()
    sys.exit(app.exec_())

        

