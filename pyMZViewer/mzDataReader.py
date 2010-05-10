#---------------------------------------------------------------------
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
#---------------------------------------------------------------------

# Function: Load and parse data from mzData format.
'''
Modified by BHC.
I believe there is a newer version of the mzData format that
contains the basepeak intensity already as a parameter but
I don't have one of those files to test as of 5.10.2010
'''

# load libs
#import wx
import os.path
#import xml.dom.minidom
import numpy as N
import xml.etree.cElementTree as ET
import base64
import struct

import matplotlib.pyplot as P

# load modules
#from dlg_select_msscan import dlgSelectScan


class mzDataDoc:
    """ Get and format data from mzData document. """


    def __init__(self, path,  parent = None):
        if parent:
            self.parent = parent
        self.data = {
                    'docType':'mzData',
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
                    'TIC':[]
                    }
        self.filename = path
        self.ns = None #namespace
        self.elmName = None
        self.scanList = None
        self.getDocument(self.filename)
#        if not self.getDocument(self.filename):
#            "Failure to load %s"%self.filename




    def getDocument(self, path):
        """ Read and parse all data from document. """

        # parse XML
        #try:
        document = ET.parse(path).getroot()
        self.ns = document.tag.split('}')[0]
        #print document.tag.split('}')
        #print self.ns
        #self.ns = document.tag#.split('}')[0]+'}'
        #document = xml.dom.minidom.parse(path)
        #return True
        #except:
            #return False

        # check document type
#        element = document.find(self.ns)
#        #element = document.find(self.ns+'mzData')
#        if not element:
#            return False

        # get description
        #element = document.find('description')
        #print int(element.get('count'))
#        if element:
#            self.handleDescription(element)

        # get spectrum
        element = document.find('spectrumList')
        self.data['totalScans'] = int(element.get('count'))
        if element:
            self.scanList = element.findall('spectrum')
            status = self.handleSpectrumList(self.scanList)

            # error in data
            if status == False:
                return False

            # no spectrum selected
            elif status == None:
                return None

        return self.data




    def getElement(self, name, path):
        """ Read and parse selected elements' data from document. """

        # parse XML
        try:
            document = xml.dom.minidom.parse(path)
        except:
            return False

        # check document type
        element = document.find(self.ns+'mzData')
        if not element:
            return False

        # get data
        if name == 'description':
            element = document.find(self.ns+'description')
        elif name == 'spectrum' or name == 'peaklist':
            element = document.find(self.ns+'spectrumList')

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

        return self.data




    def handleDescription(self, elements):
        """ Get document description from <description> element. """

        # admin
        admin = elements.find('admin')
        #admin = elements.find(self.ns+'admin')
        if admin:

            # sampleName
            #sampleName = admin.find(self.ns+'sampleName')
            sampleName = admin.find('sampleName')
            if sampleName:
                self.data['notes'] =  sampleName.text

            # contact
            contact = admin.find('contact')
            if contact:

                # name
                name = contact.find('name')
                if name:
                    self.data['operator'] = name.text

                # institution
                institution = contact.find('institution')
                if institution:
                    self.data['institution'] = institution.text

                # contactInfo
                contactInfo = contact.find('contactInfo')
                if contactInfo:
                    self.data['contact'] = contactInfo.text

        # instrument
        instrument = elements.find('instrument')
        if instrument:

            # instrumentName
            instrumentName = instrument.find('instrumentName')
            if instrumentName:
                self.data['instrument'] = instrumentName.text

        return True




    def handleSpectrumList(self, elements):
        """ Get list of spectra from <spectrumList> element. """

        # get all spectra
        spectra = elements#elements.find(self.ns+'spectrum')
        if not spectra:
            return False

        # get one spectrum
        #if len(spectra) == 1:
        #print len(spectra)
        for scan in spectra:
            #print type(scan.get("id")), int(scan.get("id")), type(int(scan.get("id")))
            if int(scan.get("id")) == 283:
                self.handleSpectrum(scan)
                print scan.get("id")
#        self.handleSpectrum(spectra[0])
        self.getChrom(spectra)
        return True

    def getChrom(self, spectra):
        '''Create the chromatogram, Base Peak, and Total Ion'''
        xTime = self.data.get('expTime')
        BPC = self.data.get('BPC')
        TIC = self.data.get('TIC')
        for scan in spectra:
            '''
            <spectrumDesc>
                    <spectrumSettings>
                      <acqSpecification spectrumType="discrete" methodOfCombination="average" count="1">
                        <acquisition acqNumber="0" />
                      </acqSpecification>
                      <spectrumInstrument
            '''
            description = scan.find('spectrumDesc')
            specSettings = description.find('spectrumSettings')
#            spectrumInstrument = specSettings.find('spectrumInstrument')# v1.05
            if specSettings:
                spectrumInstrument = specSettings.find('spectrumInstrument')# v1.04

                if spectrumInstrument:

                # get MS level
                    scanLevel = int(spectrumInstrument.get('msLevel'))
                    if scanLevel == 1:
                        xTime.append(scan.get('id'))
                        #print scan.get('id')
#                        BPC.append(scan.get('basePeakIntensity'))
                        BPC.append(self.handleSpectrum(scan, getBPC=True))
                        #TIC.append(scan.get('totIonCurrent'))


    def handleSpectrum(self, spectrum, getBPC = False):
        """ Get spectrum data from <spectrum> element. """

        mzArray = None
        intArray = None

        # get spectrum type
        description = spectrum.find('spectrumDesc')
        specSettings = description.find('spectrumSettings')
        acqSpecification = specSettings.find('acqSpecification')
        #acqSpecification = spectrum.find(self.ns+'acqSpecification')
        specType = acqSpecification.get('spectrumType')
        #specType = acqSpecification.get('spectrumType')

        # get mzArray

        mzArrayBinary = spectrum.find('mzArrayBinary')
        #mzArrayBinary = spectrum.find(self.ns+'mzArrayBinary')
        mzPrec = 'f'
        if mzArrayBinary:

            # get data
            mzArrayData = mzArrayBinary.find('data')
            #mzArrayData = mzArrayBinary.find(self.ns+'data')
            #mzArray = self.getText(mzArrayData.childNodes)
            mzArray = mzArrayData.text
#            mzArray = self.getText(mzArrayData.text)

            # get endian
            mzEndian = '<'
            if mzArrayData.get('endian') == 'big':
#            if mzArrayData.get('endian') == 'big':
                mzEndian = '>'

            if mzArrayData.get('precision') == '64':
                mzPrec = 'd'
            elif mzArrayData.get('precision') == '32':
                mzPrec = 'f'

        # get intArray
        intenArrayBinary = spectrum.find('intenArrayBinary')
        #intenArrayBinary = spectrum.find(self.ns+'intenArrayBinary')
        intPrec = 'f'
        if intenArrayBinary:

            # get data
            #intenArrayData = intenArrayBinary.find(self.ns+'data')
            intenArrayData = intenArrayBinary.find('data')
            intArray = intenArrayData.text
            #intArray = self.getText(intenArrayData.text)
            #intArray = self.getText(intenArrayData.childNodes)

            # get endian
            intEndian = '<'
            if intenArrayData.get('endian') == 'big':
            #if intenArrayData.get('endian') == 'big':
                intEndian = '>'

            if intenArrayData.get('precision') == '64':
                intPrec = 'd'
            elif intenArrayData.get('precision') == '32':
                intPrec = 'f'
        # check data
        if not mzArray or not intArray:
            print "SCAN DATA READ FAILED"
            return False

        # decode data
        try:
            mzData = base64.b64decode(mzArray)
            intData = base64.b64decode(intArray)
#            if mzBits == 64:
#                mzData = base64.b64decode(mzArray)
#            elif mzBits == 32:
#                mzData = base64.b32decode(mzArray)
#
#            if intBits == 64:
#                intData = base64.b64decode(intArray)
#            elif intBits == 32:
#                intData = base64.b32decode(intArray)
        except:
            print "DECODE FAILED"
            return False

        # convert from binary format
        mzData = self.convertFromBinary(mzData, mzEndian, mzPrec)
        intData = self.convertFromBinary(intData, intEndian, intPrec)
#        print mzData, intData
#        print len(mzData), len(intData)
        mzData = N.array(mzData)#doing this because there seems to be two values returned?
        intData = N.array(intData)

        if getBPC:
            return intData.max()


        # check data
        if len(mzData) != len(intData):
            print "LENGTH MISMATCH"
            return False
#        P.vlines(mzData, 0, intData)
#        P.show()
        # "zip" mzData and intData
        formatedData = zip(mzData, intData)

        # check spectrumType
        if specType == 'discrete':
            self.data['peaklist'] = self.convertSpectrumToPeaklist(formatedData)
        else:
            self.data['spectrum'] = formatedData

        # get precursor info for MS/MS data
        scanInfo = self.getScanInfo(spectrum)
        if scanInfo['time'] != '---':
            self.data['notes'] += '\n-----\nTime: %s' % (scanInfo['time'])
        if scanInfo['level'] and scanInfo['level'] != '1':
            self.data['notes'] += '\nMS Level: %s' % (scanInfo['level'])
            self.data['notes'] += '\nPrecursor Mass: %s' % (scanInfo['mz'])
            self.data['notes'] += '\nPrecursor Charge: %s' % (scanInfo['charge'])
            self.data['notes'] += '\nPrecursor Polarity: %s' % (scanInfo['polarity'])
            self.data['notes'] += '\nActivation Method: %s' % (scanInfo['method'])

        return True




    def getScans(self, spectra):
        """ Get basic info about all the ms scans. """

        # get list of scans
        scans = []
        for x, scan in enumerate(spectra):

            # get scan info
            scanInfo = self.getScanInfo(scan)

            # ID, time, range, MS level, prec.mass, pre.charge, spec. type
            scans.append(['---', '---', '---', '---', '---', '---', '---', '---'])
            scans[x][0] = scanInfo['id']
            scans[x][1] = scanInfo['time']
            scans[x][2] = scanInfo['range']
            scans[x][3] = scanInfo['points']
            scans[x][4] = scanInfo['level']
            scans[x][5] = scanInfo['mz']
            scans[x][6] = scanInfo['charge']
            scans[x][7] = scanInfo['type']

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

        # get ID
        #scanInfo['id'] = scan.getAttribute('id')
        scanInfo['id'] = int(scan.get('id'))
        #print int(scan.get('id'))

        # get spectrum type
        description = scan.find('spectrumDesc')
        specSettings = description.find('spectrumSettings')
        acqSpecification = specSettings.find('acqSpecification')
        #acqSpecification = scan.find('acqSpecification')
        if acqSpecification:
            scanInfo['type'] = acqSpecification.get('spectrumType')

        # get number of points
        mzArrayBinaryData = scan.find('mzArrayBinary')
        if mzArrayBinaryData:
            scanInfo['points'] = mzArrayBinaryData.get('length')

        # find instrument's params
        spectrumInstrument = specSettings.find('spectrumInstrument')# v1.05
        #print spectrumInstrument.getchildren()
        if not spectrumInstrument:
            spectrumInstrument = scan.find('acqInstrument')# v1.04
        if spectrumInstrument:

            # get MS level
            scanInfo['level'] = int(spectrumInstrument.get('msLevel'))

            # get range
            mzRangeStart = spectrumInstrument.get('mzRangeStart')
            mzRangeStop = spectrumInstrument.get('mzRangeStop')
            try:
                scanInfo['range'] = '%d - %d' % (float(mzRangeStart), float(mzRangeStop))
            except:
                scanInfo['range'] = '%s - %s' % (mzRangeStart, mzRangeStop)

            # get params
            cvParams = spectrumInstrument.findall('cvParam')
            #print "CVPARAMS",cvParams.get('name')
            for cvParam in cvParams:

                # get polarity
                #print "Parent cvParams", cvParam.get('name')
                if cvParam.get('name') == 'Polarity':
                    scanInfo['polarity'] = cvParam.get('value')

                # get retention time
                elif cvParam.get('name') == 'TimeInMinutes':
                    try:
                        time = float(cvParam.get('value'))
                        scanInfo['time'] = str(round(time, 3))
                    except:
                        scanInfo['time'] = cvParam.get('value')

        # find precursor params
        #precursorList


        precursorList = description.find('precursorList')
        if precursorList:
            precursor = precursorList.find('precursor')
            ionSelection = precursor.find('ionSelection')
            if ionSelection:

                # get params
                cvParams = ionSelection.findall('cvParam')
                for cvParam in cvParams:

                    # get m/z
                    #print cvParam.get("name"), cvParam.get("value")
                    if cvParam.get('name') == 'MassToChargeRatio':
                        scanInfo['mz'] = float(cvParam.get('value'))

                    # get charge
                    elif cvParam.get('name') == 'ChargeState':
                        scanInfo['charge'] = int(cvParam.get('value'))

            # find activation params
            activation = ionSelection.find('activation')
            if activation:

                # get params
                cvParams = activation.find('cvParam')
                for cvParam in cvParams:

                    # get method
                    if cvParam.get('name') == 'Method':
                        scanInfo['method'] = cvParam.get('value')
        #print scanInfo
        return scanInfo




    def getText(self, nodelist):
        """ Get text from node list. """

        # get text
        buff = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                buff += node.data

        return buff




    def convertFromBinary(self, data, endian, precision):
        """ Convert binary data to the list of values. """

        try:
          pointsCount = len(data)/struct.calcsize(endian+precision)
          start, end = 0, len(data)
          points = struct.unpack(endian+precision*pointsCount, data[start:end])
          return points
        except:
            return None




    def convertSpectrumToPeaklist(self, spectrum):
        """ Convert spectrum to peaklist. """

        peaklist = []
        for point in spectrum:
            peaklist.append([point[0], point[1], '', 0])

        return peaklist


if __name__ == "__main__":

    import sys
    #import numpy as N
    from base64 import b64encode
    import matplotlib.pyplot as P
    from matplotlib.lines import Line2D
#    app = QApplication(sys.argv)
#    fn = open_file()
#    fn = '/home/clowers/workspace/SimpleView/Blank_B.mzXML'
#    fn = 'C:/Data/Clowers/OrganicSignatures/BSATest/BSA.mzXML'
    fn = 'RnB10V_2.mzData'
    fn = '/home/clowers/Desktop/Froehlich/RnB10V_3.mzData'
    mzx = mzDataDoc(fn)
#    print mzx.data['BPC']
    P.plot(mzx.data['BPC'], '-ob', ms = 2)
    P.show()
    #mzx.getScans(mzx.scanList)
#    for i in mzx.getScans(mzx.scanList):
#        print i
