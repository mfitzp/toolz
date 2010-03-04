# -------------------------------------------------------------------------
#     Copyright (C) 2008-2010 Martin Strohalm <mmass@biographics.cz>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE in the
#     main directory of the program
# -------------------------------------------------------------------------

# load libs
import xml.sax
import base64
import struct

# load configuration
import config

# register essential objects
import objects


# PARSE mzData DATA
# -----------------

class parseMZDATA():
    """Parse data from mzData."""
    
    def __init__(self, path):
        self.path = path
    # ----
    
    
    def getSpectrum(self, scanNumber=None):
        """Get spectrum from document."""
        
        # init parser
        handler = scanHandler(scanNumber)
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        # parse document
        try:
            document = file(self.path)
            parser.parse(document)
            document.close()
            scan = handler.scan
        except stopParsing:
            scan = handler.scan
        except xml.sax.SAXException:
            return False
        
        # check data
        if not scan:
            return False
        
        # parse peaks
        try:
            points = self._parsePoints(scan)
        except:
            return False
        
        # parse data as peaklist (discrete points)
        if scan['spectrumType'] == 'discrete':
            for x, p in enumerate(points):
                points[x] = objects.peak(p[0], p[1])
            spectrum = objects.scan(peaks=points)
        
        # parse data as spectrum (continuous line)
        else:
            spectrum = objects.scan(points=points)
        
        # set metadata
        if scan['scanNumber']:
            spectrum.scanNumber = int(scan['scanNumber'])
        if scan['parentScanNumber']:
            spectrum.parentScanNumber = int(scan['parentScanNumber'])
        if scan['msLevel']:
            spectrum.msLevel = int(scan['msLevel'])
        if scan['polarity']:
            spectrum.polarity = scan['polarity']
        if scan['retentionTime']:
            spectrum.retentionTime = scan['retentionTime']
        if scan['totIonCurrent']:
            spectrum.totIonCurrent = float(scan['totIonCurrent'])
        if scan['basePeakMz']:
            spectrum.basePeakMZ = float(scan['basePeakMz'])
        if scan['basePeakIntensity']:
            spectrum.basePeakIntensity = float(scan['basePeakIntensity'])
        if scan['precursorMz']:
            spectrum.precursorMZ = float(scan['precursorMz'])
        if scan['precursorIntensity']:
            spectrum.precursorIntensity = float(scan['precursorIntensity'])
        
        return spectrum
    # ----
    
    
    def getScanList(self):
        """Get list of all scans in the document."""
        
        # init parser
        handler = scanListHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        # parse document
        try:
            document = file(self.path)
            parser.parse(document)
            document.close()
        except xml.sax.SAXException:
            return False
        
        return handler.scans
    # ----
    
    
    def getInfo(self):
        """Get document info."""
        
        info = {
            'title': '',
            'operator': '',
            'contact': '',
            'institution': '',
            'date': '',
            'instrument': '',
            'notes': '',
        }
        
        # init parser
        handler = infoHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        
        # parse document
        try:
            document = file(self.path)
            parser.parse(document)
            document.close()
        except stopParsing:
            info = handler.info
            return info
        except xml.sax.SAXException:
            return info
        
        return info
    # ----
    
    
    def _parsePoints(self, scan):
        """Parse spectrum data."""
        
        # decode data
        mzData = base64.b64decode(scan['mzData'])
        intData = base64.b64decode(scan['intData'])
        
        # get endian
        mzEndian = '!'
        intEndian = '!'
        if scan['mzEndian'] == 'little':
            mzEndian = '<'
        elif scan['mzEndian'] == 'big':
            mzEndian = '>'
        if scan['intEndian'] == 'little':
            intEndian = '<'
        elif scan['intEndian'] == 'big':
            intEndian = '>'
        
        # get precision
        mzPrecision = 'f'
        intPrecision = 'f'
        if scan['mzPrecision'] == '64':
            mzPrecision = 'd'
        if scan['intPrecision'] == '64':
            intPrecision = 'd'
        
        # convert from binary
        count = len(mzData) / struct.calcsize(mzEndian + mzPrecision)
        mzData = struct.unpack(mzEndian + mzPrecision * count, mzData[0:len(mzData)])
        count = len(intData) / struct.calcsize(intEndian + intPrecision)
        intData = struct.unpack(intEndian + intPrecision * count, intData[0:len(intData)])
        
        # format
        data = map(list, zip(mzData, intData))
        
        return data
    # ----
    
    

class scanListHandler(xml.sax.handler.ContentHandler):
    """Get list of all scans in the document."""
    
    def __init__(self):
        self.scans = []
    # ----
    
    
    def startElement(self, name, attrs):
        """Element started."""
        
        # get scan metadata
        if name == 'spectrum':
            scanNumber = attrs.get('id','')
            scan = {
                'scanNumber': scanNumber,
                'parentScanNumber': '',
                'msLevel': '',
                'pointsCount': '',
                'polarity': '',
                'retentionTime': '',
                'lowMz': '',
                'highMz': '',
                'basePeakMz': '',
                'basePeakIntensity': '',
                'totIonCurrent': '',
                'precursorMz' : '',
                'precursorIntensity' : '',
                'spectrumType': '',
            }
            self.scans.append(scan)
        
        # get spectrum type
        elif name == 'acqSpecification':
            self.scans[-1]['spectrumType'] = attrs.get('spectrumType','continuous')
        
        # get other params
        elif name == 'spectrumInstrument':
            self.scans[-1]['msLevel'] = attrs.get('msLevel','1')
            self.scans[-1]['lowMz'] = attrs.get('mzRangeStart','')
            self.scans[-1]['highMz'] = attrs.get('mzRangeStop','')
        
        # get other params
        elif name == 'userParam' or name == 'cvParam':
            n = attrs.get('name','')
            if n == 'basePeakMz':
                self.scans[-1]['basePeakMz'] = attrs.get('value','')
            elif n == 'basePeakIntensity':
                self.scans[-1]['basePeakIntensity'] = attrs.get('value','')
            elif n == 'TimeInMinutes':
                self.scans[-1]['retentionTime'] = attrs.get('value','')
            elif n == 'totIonCurrent':
                self.scans[-1]['totIonCurrent'] = attrs.get('value','')
            elif n == 'MassToChargeRatio':
                self.scans[-1]['precursorMz'] = attrs.get('value','')
            elif n == 'Polarity':
                if attrs.get('value','') == 'Positive':
                    self.scans[-1]['polarity'] = '+'
                elif attrs.get('value','') == 'Negative':
                    self.scans[-1]['polarity'] = '-'
                else:
                    self.scans[-1]['polarity'] = attrs.get('value','')
        
        # get spectrum length
        elif name == 'data':
            self.scans[-1]['pointsCount'] = attrs.get('length','')
        
        # get parent scan
        elif name == 'precursor':
            self.scans[-1]['parentScanNumber'] = attrs.get('spectrumRef','')
    # ----
    
    
    def endElement(self, name):
        """Element ended."""
        pass
    # ----
    
    
    def characters(self, ch):
        """Grab characters."""
        pass
    # ----
    
    

class scanHandler(xml.sax.handler.ContentHandler):
    """Get scan data."""
    
    def __init__(self, scanNumber):
        self.scanNumber = scanNumber
        
        self._isMatch = False
        self._isMzArray = False
        self._isIntArray = False
        self._isData = False
        
        self.scan = False
    # ----
    
    
    def startElement(self, name, attrs):
        """Element started."""
        
        # get scan metadata
        if name == 'spectrum':
            scanNumber = attrs.get('id','')
            self._isMatch = False
            
            # selected scan
            if self.scanNumber==None or scanNumber == str(self.scanNumber):
                self._isMatch = True
                self.scan = {
                    'scanNumber': scanNumber,
                    'parentScanNumber': '',
                    'msLevel': '',
                    'pointsCount': '',
                    'polarity': '',
                    'retentionTime': '',
                    'lowMz': '',
                    'highMz': '',
                    'basePeakMz': '',
                    'basePeakIntensity': '',
                    'totIonCurrent': '',
                    'precursorMz' : '',
                    'precursorIntensity' : '',
                    'spectrumType': '',
                    'mzData': '',
                    'mzEndian': '',
                    'mzPrecision': '',
                    'intData': '',
                    'intEndian': '',
                    'intPrecision': '',
                }
        
        # get spectrum type
        elif name == 'acqSpecification' and self._isMatch:
            self.scan['spectrumType'] = attrs.get('spectrumType','continuous')
        
        # get other params
        elif name == 'spectrumInstrument' and self._isMatch:
            self.scan['msLevel'] = attrs.get('msLevel','')
            self.scan['lowMz'] = attrs.get('mzRangeStart','')
            self.scan['highMz'] = attrs.get('mzRangeStop','')
        
        # get other params
        elif (name == 'userParam' or name == 'cvParam') and self._isMatch:
            n = attrs.get('name','')
            if n == 'basePeakMz':
                self.scan['basePeakMz'] = attrs.get('value','')
            elif n == 'basePeakIntensity':
                self.scan['basePeakIntensity'] = attrs.get('value','')
            elif n == 'TimeInMinutes':
                self.scan['retentionTime'] = attrs.get('value','')
            elif n == 'totIonCurrent':
                self.scan['totIonCurrent'] = attrs.get('value','')
            elif n == 'Polarity':
                self.scan['polarity'] = attrs.get('value','')
            elif n == 'MassToChargeRatio':
                self.scan['precursorMz'] = attrs.get('value','')
        
        # get parent scan
        elif name == 'precursor' and self._isMatch:
            self.scan['parentScanNumber'] = attrs.get('spectrumRef','')
        
        # get mz data
        elif name == 'mzArrayBinary' and self._isMatch:
            self._isMzArray = True
        
        # get int data
        elif name == 'intenArrayBinary' and self._isMatch:
            self._isIntArray = True
        
        # get data
        elif name == 'data' and self._isMatch:
            self._isData = True
            if self._isMzArray:
                self.scan['mzEndian'] = attrs.get('endian','')
                self.scan['mzPrecision'] = attrs.get('precision','32')
            elif self._isIntArray:
                self.scan['intEndian'] = attrs.get('endian','')
                self.scan['intPrecision'] = attrs.get('precision','32')
    # ----
    
    
    def endElement(self, name):
        """Element ended."""
        
        # stop parsing
        if name == 'spectrum' and self._isMatch:
            raise stopParsing()
        
        # stop reading mz data
        elif name == 'mzArrayBinary':
            self._isMzArray = False
        
        # stop reading int data
        elif name == 'intenArrayBinary':
            self._isIntArray = False
        
        # stop reading data
        elif name == 'data':
            self._isData = False
    # ----
    
    
    def characters(self, ch):
        """Grab characters."""
        
        # get data
        if self._isData:
            if self._isMzArray:
                self.scan['mzData'] += ch
            elif self._isIntArray:
                self.scan['intData'] += ch
    # ----
    
    

class infoHandler(xml.sax.handler.ContentHandler):
    """Get info data."""
    
    def __init__(self):
        
        self.info = {
            'title': '',
            'operator': '',
            'contact': '',
            'institution': '',
            'date': '',
            'instrument': '',
            'notes': '',
        }
        
        self._isSampleName = False
        self._isContact = False
        self._isName = False
        self._isInstitution = False
        self._isContactInfo = False
        self._isInstrumentName = False
    # ----
    
    
    def startElement(self, name, attrs):
        """Element started."""
        
        # get instrument
        if name == 'sampleName':
             self._isSampleName = True
        if name == 'contact':
             self._isContact = True
        elif name == 'name' and self._isContact:
             self._isName = True
        elif name == 'institution':
             self._isInstitution = True
        elif name == 'contactInfo':
             self._isContactInfo = True
        elif name == 'instrumentName':
             self._isInstrumentName = True
    # ----
    
    
    def endElement(self, name):
        """Element ended."""
        
        # stop parsing
        if name == 'description':
            raise stopParsing()
        
        # stop elements
        if name == 'sampleName':
             self._isSampleName = False
        if name == 'contact':
             self._isContact = False
             self._isName = False
        elif name == 'name':
             self._isName = False
        elif name == 'institution':
             self._isInstitution = False
        elif name == 'contactInfo':
             self._isContactInfo = False
        elif name == 'instrumentName':
             self._isInstrumentName = False
    # ----
    
    
    def characters(self, ch):
        """Grab characters."""
        
        # get data
        if self._isSampleName:
            self.info['title'] += ch
        elif self._isName:
            self.info['operator'] += ch
        elif self._isInstitution:
            self.info['institution'] += ch
        elif self._isContactInfo:
            self.info['contact'] += ch
        elif self._isInstrumentName:
            self.info['instrument'] += ch
    # ----
    
    

class stopParsing(Exception):
    """Exeption to stop parsing XML data."""
    pass
