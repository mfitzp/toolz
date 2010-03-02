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

# Function: Load and parse data from mzData format.

# load libs
#import wx
import os.path
#import xml.dom.minidom
import numpy as N
import xml.etree.cElementTree as ET
import base64
import struct

# load modules
#from dlg_select_msscan import dlgSelectScan


class mzDataDoc:
    """ Get and format data from mzData document. """

    # ----
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
    # ----


    # ----
    def getDocument(self, path):
        """ Read and parse all data from document. """

        # parse XML
        try:
            document = ET.parse(path).getroot()
            self.ns = document.tag#.split('}')[0]+'}'
            #document = xml.dom.minidom.parse(path)
        except:
            return False

        # check document type
#        element = document.find(self.ns)
#        #element = document.getElementsByTagName('mzData')
#        if not element:
#            return False

        # get description
        element = document.find('description')
        if element:
            self.handleDescription(element)

        # get spectrum
        element = document.find('spectrumList')
        if element:
            self.scanList = element.getchildren()
            status = self.handleSpectrumList(self.scanList)

            # error in data
            if status == False:
                return False

            # no spectrum selected
            elif status == None:
                return None

        return self.data
    # ----


    # ----
    def getElement(self, name, path):
        """ Read and parse selected elements' data from document. """

        # parse XML
        try:
            document = xml.dom.minidom.parse(path)
        except:
            return False

        # check document type
        element = document.getElementsByTagName('mzData')
        if not element:
            return False

        # get data
        if name == 'description':
            element = document.getElementsByTagName('description')
        elif name == 'spectrum' or name == 'peaklist':
            element = document.getElementsByTagName('spectrumList')

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
    # ----


    # ----
    def handleDescription(self, elements):
        """ Get document description from <description> element. """

        # admin
        admin = elements.find('admin')
        #admin = elements.getElementsByTagName('admin')
        if admin:

            # sampleName
            #sampleName = admin[0].getElementsByTagName('sampleName')
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
    # ----


    # ----
    def handleSpectrumList(self, elements):
        """ Get list of spectra from <spectrumList> element. """

        # get all spectra
        spectra = elements#elements.getElementsByTagName('spectrum')
        if not spectra:
            return False

        # get one spectrum
        #if len(spectra) == 1:
        self.handleSpectrum(spectra[0])
        self.getChrom(spectra)
        return True
    # ----
    def getChrom(self, spectra):
        '''Create the chromatogram, Base Peak, and Total Ion'''
        xTime = self.data.get('expTime')
        BPC = self.data.get('BPC')
        TIC = self.data.get('TIC')
        for scan in spectra:
            if scan.find(self.ns+'precursorMz') is None:
                xTime.append(scan.get('num'))
                BPC.append(scan.get('basePeakIntensity'))
                TIC.append(scan.get('totIonCurrent'))

    # ----
    def handleSpectrum(self, spectrum):
        """ Get spectrum data from <spectrum> element. """

        mzArray = None
        intArray = None

        # get spectrum type
        acqSpecification = spectrum.getElementsByTagName('acqSpecification')
        specType = acqSpecification[0].getAttribute('spectrumType')

        # get mzArray
        mzArrayBinary = spectrum.getElementsByTagName('mzArrayBinary')
        if mzArrayBinary:

            # get data
            mzArrayData = mzArrayBinary[0].getElementsByTagName('data')
            mzArray = self.getText(mzArrayData[0].childNodes)

            # get endian
            mzEndian = '<'
            if mzArrayData[0].getAttribute('endian') == 'big':
                mzEndian = '>'

        # get intArray
        intenArrayBinary = spectrum.getElementsByTagName('intenArrayBinary')
        if intenArrayBinary:

            # get data
            intenArrayData = intenArrayBinary[0].getElementsByTagName('data')
            intArray = self.getText(intenArrayData[0].childNodes)

            # get endian
            intEndian = '<'
            if intenArrayData[0].getAttribute('endian') == 'big':
                intEndian = '>'

        # check data
        if not mzArray or not intArray:
            return False

        # decode data
        try:
            mzData = base64.b64decode(mzArray)
            intData = base64.b64decode(intArray)
        except:
            return False

        # convert from binary format
        mzData = self.convertFromBinary(mzData, mzEndian)
        intData = self.convertFromBinary(intData, intEndian)

        # check data
        if not mzData or not intData or (len(mzData) != len(intData)):
            return False

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
    # ----


    # ----
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
    # ----


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
        scanInfo['id'] = scan.getAttribute('id')

        # get spectrum type
        acqSpecification = scan.getElementsByTagName('acqSpecification')
        if acqSpecification:
            scanInfo['type'] = acqSpecification[0].getAttribute('spectrumType')

        # get number of points
        mzArrayBinaryData = scan.getElementsByTagName('data')
        if mzArrayBinaryData:
            scanInfo['points'] = mzArrayBinaryData[0].getAttribute('length')

        # find instrument's params
        spectrumInstrument = scan.getElementsByTagName('spectrumInstrument')# v1.05
        if not spectrumInstrument:
            spectrumInstrument = scan.getElementsByTagName('acqInstrument')# v1.04

        if spectrumInstrument:

            # get MS level
            scanInfo['level'] = spectrumInstrument[0].getAttribute('msLevel')

            # get range
            mzRangeStart = spectrumInstrument[0].getAttribute('mzRangeStart')
            mzRangeStop = spectrumInstrument[0].getAttribute('mzRangeStop')
            try:
                scanInfo['range'] = '%d - %d' % (float(mzRangeStart), float(mzRangeStop))
            except:
                scanInfo['range'] = '%s - %s' % (mzRangeStart, mzRangeStop)

            # get params
            cvParams = spectrumInstrument[0].getElementsByTagName('cvParam')
            for cvParam in cvParams:

                # get polarity
                if cvParam.getAttribute('name') in ('Polarity', 'polarity'):
                    scanInfo['polarity'] = cvParam.getAttribute('value')

                # get retention time
                elif cvParam.getAttribute('name') in ('TimeInMinutes', 'time.min'):
                    try:
                        time = float(cvParam.getAttribute('value'))
                        scanInfo['time'] = str(round(time, 3))
                    except:
                        scanInfo['time'] = cvParam.getAttribute('value')

        # find precursor params
        ionSelection = scan.getElementsByTagName('ionSelection')
        if ionSelection:

            # get params
            cvParams = ionSelection[0].getElementsByTagName('cvParam')
            for cvParam in cvParams:

                # get m/z
                if cvParam.getAttribute('name') in ('MassToChargeRatio', 'mz'):
                    scanInfo['mz'] = cvParam.getAttribute('value')

                # get charge
                elif cvParam.getAttribute('name') in ('ChargeState', 'charge'):
                    scanInfo['charge'] = cvParam.getAttribute('value')

        # find activation params
        activation = scan.getElementsByTagName('activation')
        if activation:

            # get params
            cvParams = activation[0].getElementsByTagName('cvParam')
            for cvParam in cvParams:

                # get method
                if cvParam.getAttribute('name') in ('Method', 'method'):
                    scanInfo['method'] = cvParam.getAttribute('value')

        return scanInfo
    # ----


    # ----
    def getText(self, nodelist):
        """ Get text from node list. """

        # get text
        buff = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                buff += node.data

        return buff
    # ----


    # ----
    def convertFromBinary(self, data, endian):
        """ Convert binary data to the list of values. """

        try:
          pointsCount = len(data)/struct.calcsize(endian+'f')
          start, end = 0, len(data)
          points = struct.unpack(endian+'f'*pointsCount, data[start:end])
          return points
        except:
            return None
    # ----


    # ----
    def convertSpectrumToPeaklist(self, spectrum):
        """ Convert spectrum to peaklist. """

        peaklist = []
        for point in spectrum:
            peaklist.append([point[0], point[1], '', 0])

        return peaklist
    # ----
