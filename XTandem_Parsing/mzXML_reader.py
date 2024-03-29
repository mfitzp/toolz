# -------------------------------------------------------------------------
#     This file is part of mMass - the spectrum analysis tool for MS.
#     Copyright (C) 2005-07 Martin Strohalm <mmass@biographics.cz>

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

# Function: Load and parse data from mzXML format.

########################
'''Modified in July 2008 by Brian Clowers to include the cElement Tree
for a faster parsing of the XML file.  Additional functions were added
to allow the primary program to access fragment ion spectra'''


########################

from PyQt4.QtGui import QFileDialog,  QApplication
import numpy as N

import os.path
#import xml.dom.minidom
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import base64
import struct

# load modules
#from dlg_select_msscan import dlgSelectScan

def open_file():
    filename = str(QFileDialog.getOpenFileName())
    if filename:
        print "Opened: ", filename
        return filename


class mzXMLDoc:
    """ Get and format data from mzXML document. """


    def __init__(self, path, parent=None, sumBool = False):
        if parent:
            self.parent = parent
        self.data = {
                    'docType':'mzXML',
                    'scanID':'',
                    'date':'',
                    'operator':'',
                    'institution':'',
                    'contact':'',
                    'instrument':'',
                    'notes':'',
                    'peaklist':[],
                    'spectrum':[],
                    'totalScans':'',
                    'expTime':[],
                    'BPC':[],
                    'TIC':[],
                    'XIC':{},
                    'xicVal':''
                    }
        self.filename = path
        self.ns = None #namespace
        self.elmName = None
        self.scanList = None
        self.getDocument(self.filename, sumBool)

    def getDocument(self, path, sumBool = False):
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

        self.data['totalScans'] = int(element.get('scanCount'))
        if element:
            self.scanList = element.findall(self.ns+'scan')
            status = self.handleSpectrumList(self.scanList, sumBool = sumBool)
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

        # get description
        instrument = element.find(self.ns+'msInstrument')
        #element = document.getElementsByTagName('msInstrument')
        #if element:
        #    self.handleDescription(element[0])
        if instrument:
            self.handleDescription(instrument)

        #return self.data

    def getElement(self, name, path):
        """ Read and parse selected elements' data from document. """

        self.elmName = name

        # parse XML
        try:
            document = xml.dom.minidom.parse(path)
        except:
            return False

        # get data
        if name == 'description':
            element = document.getElementsByTagName('msInstrument')
        elif name == 'spectrum' or name == 'peaklist':
            element = document.getElementsByTagName('msRun')

        if element:

            # get description
            if name == 'description':
                if self.handleDescription(element[0]) == False:
                    return False

            # get spectrum
            elif name == 'spectrum' or name == 'peaklist':
                status = self.handleSpectrumList(element[0])

                # error in data
                if status == False:
                    return False

                # no spectrum selected
                elif status == None:
                    return None

        #return self.data

    def handleDescription(self, elements):
        """ Get document description from <msInstrument> element. """

        # msManufacturer
        msManufacturer = elements.find(self.ns+'msManufacturer')
        #msManufacturer = elements.getElementsByTagName('msManufacturer')
        if msManufacturer:
            #self.data['instrument'] = msManufacturer[0].getAttribute('value')
            self.data['instrument'] = msManufacturer.get('value')

        # msModel
        msModel = elements.find(self.ns+'msModel')
        #msModel = elements.getElementsByTagName('msModel')
        if msModel:
            #self.data['instrument'] += msModel[0].getAttribute('value')
            self.data['instrument'] += msModel.get('value')

        # msIonisation
        msIonisation = elements.find(self.ns+'msIonisation')
        #msIonisation = elements.getElementsByTagName('msIonisation')
        if msIonisation:
            #self.data['instrument'] += msIonisation[0].getAttribute('value')
            self.data['instrument'] += msIonisation.get('value')

        # msMassAnalyzer
        msMassAnalyzer = elements.find(self.ns+'msMassAnalyzer')
        #msMassAnalyzer = elements.getElementsByTagName('msMassAnalyzer')
        if msMassAnalyzer:
            #self.data['instrument'] += msMassAnalyzer[0].getAttribute('value')
            self.data['instrument'] += msMassAnalyzer.get('value')

        # operator
        operator = elements.find(self.ns+'operator')
        #operator = elements.getElementsByTagName('operator')
        if operator:
            self.data['operator'] = '%s %s' % (operator.get('first'), operator.get('last'))
            self.data['contact'] = '%s %s %s' % (operator.get('phone'), operator.get('email'), operator.get('URI'))
            #self.data['operator'] = '%s %s' % (operator[0].getAttribute('first'), operator[0].getAttribute('last'))
            #self.data['contact'] = '%s %s %s' % (operator[0].getAttribute('phone'), operator[0].getAttribute('email'), operator[0].getAttribute('URI'))

        return True

    def handleSpectrumList(self, elements, sumBool = False):
        """ Get list of spectra from <spectrumList> element. """

        # get all spectra
        spectra = elements
        if not spectra:
            return False

        # get one spectrum
        #if len(spectra) == 1:
        #    print "Single Scan"
        if sumBool:
            self.sumMZ(spectra)
            return True
        else:
            self.handleSpectrum(spectra[0])
            self.getChrom(spectra)
            return True


    def getChrom(self, spectra):
        '''Create the chromatogram, Base Peak, and Total Ion'''
        xTime = self.data.get('expTime')
        BPC = self.data.get('BPC')
        TIC = self.data.get('TIC')
        for scan in spectra:
            if scan.find(self.ns+'precursorMz') is None:
                xTime.append(scan.get('num'))
                if N.float(scan.get('peaksCount'))>0:
                    BPC.append(N.float(scan.get('basePeakIntensity')))
                    TIC.append(N.float(scan.get('totIonCurrent')))
                #                print scan.get('num'), type(scan)
##                print scan.get('basePeakIntensity'), type(scan.get('basePeakIntensity'))
#                if type(scan.get('basePeakIntensity')) == None:
#
                else:
                    BPC.append(0.0)
                    TIC.append(0.0)

    def sumMZ(self, spectra):
        for i,scan in enumerate(spectra):
            if i == 0:
                self.handleSpectrum(scan)
            else:
                self.handleSpectrum(scan, sumBool = True)

    def getXIC(self, spectra, mzValLo, mzValHi):
        '''Create the chromatogram, Base Peak, and Total Ion'''
        xicDict = self.data.get('XIC')
        curXIC = []
        curXICKey = '%.2f - %.2f'%(mzValLo,mzValHi)
        print 'curXICKey: ',curXICKey
        xicDict[curXICKey] = curXIC#store xic as a key of the high and low mzVals
        for scan in spectra:
            if scan.find(self.ns+'precursorMz') is None:#case for msLevel == 1 scan
                if N.float(scan.get('peaksCount'))>0:
                    xicVal, xicBool = self.handleXIC(scan, mzValLo, mzValHi)
                    if xicBool:
                        curXIC.append(xicVal)
                    else:
                        curXIC.append(0.0)
                #                print scan.get('num'), type(scan)
##                print scan.get('basePeakIntensity'), type(scan.get('basePeakIntensity'))
#                if type(scan.get('basePeakIntensity')) == None:
#
                else:
                    curXIC.append(0.0)


    def handleXIC(self, spectrum, mzValLo, mzValHi, sum = True):
        """
        Get spectrum data from <spectrum> element.
        Needs to be a parent ion scan
        use numpy.where
        return intensity val for that range (use sum?)

        Get GUI and code from SimpleViewer
        """

        # get data element
        peaks = spectrum.find(self.ns+'peaks')

        if peaks == None:
            return None, False

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
            #print data[0:20]
            #print type(data[0:20])
            data = base64.b64decode(data)
        except:
            return None, False

        # convert from binary format
        try:
#            print len(data)
            pointsCount = len(data)/struct.calcsize(endian+'f')
            start, end = 0, len(data)
            data = struct.unpack(endian+'f'*pointsCount, data[start:end])
            #print data[0:5]
            #print type(data[0:5])
        except:
            return None, False
#        print type(data)
#        for i in xrange(20):
#            print data[i]

        # split data to m/z and intensity
        mzData = data[::2]
        #print type(mzData)
        intData = data[1::2]

        # check data
        if not mzData or not intData or (len(mzData) != len(intData)):
            return None, False

        mzArray = N.array(mzData)
        intArray = N.array(intData)

        criteria = (mzArray >= mzValLo) & (mzArray <= mzValHi)
        validInd = N.where(criteria)[0]
        if len(validInd)>0:
            if sum:
                intVal = intArray[validInd].sum()
            else:
                intVal = intArray[validInd].max()
            return intVal, True
        else:
            return 0.0, True

        return True

    def handleSpectrum(self, spectrum, sumBool = False):
        """ Get spectrum data from <spectrum> element. """

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
            #print data[0:20]
            #print type(data[0:20])
            data = base64.b64decode(data)
        except:
            return False

        # convert from binary format
        try:
            print len(data)
            pointsCount = len(data)/struct.calcsize(endian+'f')
            start, end = 0, len(data)
            data = struct.unpack(endian+'f'*pointsCount, data[start:end])
            #print data[0:5]
            #print type(data[0:5])
        except:
            return False
#        print type(data)
#        for i in xrange(20):
#            print data[i]

        # split data to m/z and intensity
        mzData = data[::2]
        #print type(mzData)
        intData = data[1::2]

        # check data
        if not mzData or not intData or (len(mzData) != len(intData)):
            return False

        # "zip" mzData and intData
        formatedData = [N.array(mzData), N.array(intData)]
        #formatedData = zip(mzData, intData)

        # set data as spectrum or peaklist
        if not self.elmName:
            if sumBool:
                self.data['spectrum'][0]+=formatedData[0]
                self.data['spectrum'][1]+=formatedData[1]
            else:
                self.data['spectrum'] = formatedData
            # else:
                # self.data['peaklist'] = self.convertSpectrumToPeaklist(formatedData)
        elif self.elmName == 'spectrum':
            if sumBool:
                self.data['spectrum'][0]+=formatedData[0]
                self.data['spectrum'][1]+=formatedData[1]
            else:
                self.data['spectrum'] = formatedData
        # elif self.elmName == 'peaklist':
            # self.data['peaklist'] = self.convertSpectrumToPeaklist(formatedData)

        # get precursor info for MS/MS data
        scanInfo = self.getScanInfo(spectrum)
        if scanInfo['time'] != '---':
            self.data['notes'] += '\n-----\nTime: %s' % (scanInfo['time'])
        if scanInfo['level'] and scanInfo['level'] != '1':
            self.data['notes'] += '\nMS Level: %s' % (scanInfo['level'])
            self.data['notes'] += '\nPrecursor Mass: %s' % (scanInfo['mz'])
            self.data['notes'] += '\nPrecursor Charge: %s' % (scanInfo['charge'])
            self.data['notes'] += '\nPrecursor Polarity: %s' % (scanInfo['polarity'])
            self.data['notes'] += '\nBase Peak Intensity: %s' % (scanInfo['basePeakIntensity'])

        return True

    def getScans(self, spectra):
        """ Get basic info about all the ms scans. """

        # get list of scans
        scans = []
        for x, scan in enumerate(spectra):

            # get scan info
            scanInfo = self.getScanInfo(scan)

            # ID, time, range, MS level, prec.mass, pre.charge, spec. type
            scans.append(['---', '---', '---', '---', '---', '---', '---', '---', '---'])
            scans[x][0] = scanInfo['id']
            scans[x][1] = scanInfo['time']
            scans[x][2] = scanInfo['range']
            scans[x][3] = scanInfo['points']
            scans[x][4] = scanInfo['level']
            scans[x][5] = scanInfo['mz']
            scans[x][6] = scanInfo['charge']
            scans[x][7] = scanInfo['type']
            scans[x][8] = scanInfo['basePeakIntensity']

        return scans

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
        scanInfo['basePeakIntensity'] = '---'

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

        #get base peak intensity
        scanInfo['basePeakIntensity'] = scan.get('basePeakIntensity')

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
            #if precursorMz:

                # get m/z
            scanInfo['mz'] = precursorMz.text#self.getText(precursorMz[0].childNodes)
            #pscanInfo['intensity'] = precursorMz.get('basePeakIntensity')

        return scanInfo


##########################################
    def getPreSpectrum(self, spectrum):
        """ Get spectrum data from <spectrum> element. """

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
        #data = self.getText(peaks[0].childNodes)
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
#        for i in xrange(20):
#            print data[i]

        # split data to m/z and intensity
        mzData = data[::2]
        #print type(mzData)
        intData = data[1::2]

        # check data
        if not mzData or not intData or (len(mzData) != len(intData)):
            return False

        # "zip" mzData and intData
        formatedData = [N.array(mzData), N.array(intData)]
        #formatedData = zip(mzData, intData)
        scanInfo = self.getScanInfo(spectrum)
        if scanInfo['time'] != '---':
            self.data['notes'] += '\n-----\nTime: %s' % (scanInfo['time'])
        if scanInfo['level'] and scanInfo['level'] != '1':
            self.data['notes'] += '\nMS Level: %s' % (scanInfo['level'])
            self.data['notes'] += '\nPrecursor Mass: %s' % (scanInfo['mz'])
            self.data['notes'] += '\nPrecursor Charge: %s' % (scanInfo['charge'])
            self.data['notes'] += '\nPrecursor Polarity: %s' % (scanInfo['polarity'])

        return formatedData,  scanInfo


#######################################

    def getText(self, nodelist):
        """ Get text from node list. """

        # get text
        buff = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                buff += node.data

        return buff

    def convertSpectrumToPeaklist(self, spectrum):
        """ Convert spectrum to peaklist. """

        peaklist = []
        for point in spectrum:
            peaklist.append([point[0], point[1], '', 0])

        return peaklist

def encodeData(numpyArray):
    # decode data
    if type(numpyArray) is N.ndarray:
        data = numpyArray
    try:
        endian = '!'
        pointsCount = len(data)#/struct.calcsize(endian+'f')
        start, end = 0, len(data)
        print "Points Count Encode:",  pointsCount
        print "Length of encodeData",  len(data)
        print "Type of encodeData",  type(data)

        data = struct.pack(endian+'f'*pointsCount, *data)#data[start:end])
        #data = struct.pack('f', data[start:end])
    except:
        raise
        return False

    # convert from binary format
    try:
        data = base64.b64encode(data)
    except:
        raise
        return False

    return data


def decodeData(data):
    # decode data
    try:
        data = base64.b64decode(data)
        endian = '!'
    except:
        return False

    # convert from binary format
    try:
      pointsCount = len(data)/struct.calcsize(endian+'f')
      start, end = 0, len(data)
      data = struct.unpack(endian+'f'*pointsCount, data[start:end])
    except:
        raise
        return False
    #print type(data)
#    for i in xrange(20):
#        print data[i]

    # split data to m/z and intensity
    mzData = data[::2]
    #print type(mzData)
    intData = data[1::2]

    return [mzData, intData]

if __name__ == "__main__":
    
    
    import sys
    #import numpy as N
    from base64 import b64encode
    import pylab as P
    from matplotlib.lines import Line2D
    app = QApplication(sys.argv)
    fn = 'R19.mzXML'#open_file()
    xtFN = 'R19.xml'


    def convertScanNum(val):
        return val/60


    def OnPick(event):
        if not isinstance(event.artist, Line2D):
            return True

        line = event.artist
        indexA = event.ind[0]
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        print indexA,  xdata[indexA]
        selectHandleA.set_visible(True)
        selectHandleA.set_data([xdata[indexA]], [ydata[indexA]])
        fig.canvas.draw()

    if os.path.isfile(fn):

        mzx = mzXMLDoc(fn, True)
        #mzx.getDocument(fn)
#        spectrum = mzx.data.get('spectrum')
        BPC = mzx.data.get('BPC')
#        xvalues = mzx.data.get('expTime')

        fig = P.figure(figsize=(8,6))
        ax = fig.add_subplot(111, axisbg='#FFFFCC')
        ax.plot(BPC)
        
        if os.path.isfile(xtFN):
            print xtFN
            
        
#        ax2 = ax.twinx()
#
#        #x = npy.arange(0.0, 5.0, 0.01)
#        #y = npy.sin(2*npy.pi*x) + 0.5*npy.random.randn(len(x))
#        if len(BPC) >=1:
#            ax.plot(N.array(xvalues), N.array(BPC), 'r-', picker = 5)
#        #ax.set_ylim(-2,2)
#        #ax.set_title('Press left mouse button and drag to test')
#        mzValLo = 835.1
#        mzValHi = 875.1
#        xicKey1 = '%.2f% - .2f'%(mzValLo,mzValHi)
#        mzx.getXIC(mzx.scanList, mzValLo, mzValHi)
#
#        mzValLo = 600
#        mzValHi = 675
#        mzx.getXIC(mzx.scanList, mzValLo, mzValHi)
#
#        xicKey2 = '%.2f% -.2f'%(mzValLo,mzValHi)
#        #xicY = mzx.data.get('XIC')[xicKey]
#        xicDict = mzx.data.get('XIC')
#        for xic in xicDict.itervalues():
#            ax.plot(N.array(xvalues), N.array(xic))
#
##        def updateTwinAx(ax):
##           y1, y2 = ax.get_ylim()
##           ax2.set_ylim(convertTwinAx(y1), convertScanNum(y2))
##           ax2.figure.canvas.draw()
##
##    # automatically update ylim of ax2 when ylim of ax1 changes.
##        ax.callbacks.connect("ylim_changed", updateTwinAx)

        P.show()
    #print mzx.data
    sys.exit(app.exec_())

