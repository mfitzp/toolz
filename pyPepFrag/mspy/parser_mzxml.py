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
import zlib
import struct

# load configuration
import config

# register essential objects
import objects


# PARSE mzXML DATA
# ----------------

class parseMZXML():
    """Parse data from mzXML."""
    
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
        
        # get precision
        precision = 'f'
        if scan['precision'] == '32':
            precision = 'f'
        elif scan['precision'] == '64':
            precision = 'd'
        
        # get endian
        endian = '!'
        if scan['byteOrder'] == 'little':
            endian = '<'
        elif scan['byteOrder'] == 'big':
            endian = '>'
        
        # decode data
        data = base64.b64decode(scan['points'])
        
        # decompress data
        if scan['compression']:
            data = zlib.decompress(data)
        
        # convert from binary
        count = len(data) / struct.calcsize(endian + precision)
        data = struct.unpack(endian + precision * count, data[0:len(data)])
        
        # format
        data = map(list, zip(data[::2], data[1::2]))
        
        return data
    # ----
    
    

class scanListHandler(xml.sax.handler.ContentHandler):
    """Get list of all scans in the document."""
    
    def __init__(self):
        self.scans = []
        self._isPrecursor = False
        self._scanHierarchy = ['']
        self._spectrumType = 'continuous'
    # ----
    
    
    def startElement(self, name, attrs):
        """Element started."""
        
        # get data type
        if name == 'dataProcessing':
            if attrs.get('centroided', False):
                self._spectrumType = 'discrete'
        
        # get scan metadata
        elif name == 'scan':
            scanNumber = attrs.get('num','')
            scan = {
                'scanNumber': scanNumber,
                'parentScanNumber': self._scanHierarchy[-1],
                'msLevel': attrs.get('msLevel',"1"),
                'pointsCount': attrs.get('peaksCount',''),
                'polarity': attrs.get('polarity',''),
                'retentionTime': attrs.get('retentionTime',''),
                'lowMz': attrs.get('lowMz',''),
                'highMz': attrs.get('highMz',''),
                'basePeakMz': attrs.get('basePeakMz',''),
                'basePeakIntensity': attrs.get('basePeakIntensity',''),
                'totIonCurrent': attrs.get('totIonCurrent',''),
                'precursorMz': '',
                'precursorIntensity': '',
                'spectrumType': self._spectrumType,
            }
            self.scans.append(scan)
            
            # add scan to hierarchy
            self._scanHierarchy.append(scanNumber)
        
        # get precursor data
        elif name == 'precursorMz':
            self._isPrecursor = True
            self.scans[-1]['precursorIntensity'] = attrs.get('precursorIntensity','')
    # ----
    
    
    def endElement(self, name):
        """Element ended."""
        
        # remove scan from hierarchy
        if name == 'scan':
            del self._scanHierarchy[-1]
        
        # stop reading precursor data
        elif name == 'precursorMz':
            self._isPrecursor = False
    # ----
    
    
    def characters(self, ch):
        """Grab characters."""
        
        # get precursor mz
        if self._isPrecursor:
            self.scans[-1]['precursorMz'] += ch
    # ----
    
    

class scanHandler(xml.sax.handler.ContentHandler):
    """Get scan data."""
    
    def __init__(self, scanNumber):
        self.scanNumber = scanNumber
        
        self._isMatch = False
        self._isPeaks = False
        self._isPrecursor = False
        self._scanHierarchy = ['']
        self._spectrumType = 'continuous'
        
        self.scan = False
    # ----
    
    
    def startElement(self, name, attrs):
        """Element started."""
        
        # get data type
        if name == 'dataProcessing':
            centroided = attrs.get('centroided', False)
            if centroided and centroided!='0':
                self._spectrumType = 'discrete'
        
        # get scan metadata
        elif name == 'scan':
            scanNumber = attrs.get('num','')
            self._isMatch = False
            
            # selected scan
            if self.scanNumber==None or scanNumber == str(self.scanNumber):
                self._isMatch = True
                self.scan = {
                    'points': '',
                    'scanNumber': scanNumber,
                    'parentScanNumber': self._scanHierarchy[-1],
                    'msLevel': attrs.get('msLevel',"1"),
                    'pointsCount': attrs.get('peaksCount',''),
                    'polarity': attrs.get('polarity',''),
                    'retentionTime': attrs.get('retentionTime',''),
                    'lowMz': attrs.get('lowMz',''),
                    'highMz': attrs.get('highMz',''),
                    'basePeakMz': attrs.get('basePeakMz',''),
                    'basePeakIntensity': attrs.get('basePeakIntensity',''),
                    'totIonCurrent': attrs.get('totIonCurrent',''),
                    'precursorMz': '',
                    'precursorIntensity': '',
                    'spectrumType': self._spectrumType,
                    'byteOrder': '',
                    'compression': '',
                    'precision': '',
                }
            
            # add scan to hierarchy
            self._scanHierarchy.append(scanNumber)
        
        # get peaks data
        elif name == 'peaks' and self._isMatch:
            self._isPeaks = True
            self.scan['byteOrder'] = attrs.get('byteOrder','network')
            self.scan['compression'] = attrs.get('compressionType','')
            self.scan['precision'] = attrs.get('precision','32')
        
        # get precursor data
        elif name == 'precursorMz' and self._isMatch:
            self._isPrecursor = True
            self.scan['precursorIntensity'] = attrs.get('precursorIntensity',"")
    # ----
    
    
    def endElement(self, name):
        """Element ended."""
        
        # stop parsing
        if name == 'scan' and self._isMatch:
            raise stopParsing()
        
        # remove scan from hierarchy
        elif name == 'scan':
            del self._scanHierarchy[-1]
        
        # stop reading peaks data
        elif name == 'peaks':
            self._isPeaks = False
        
        # stop reading precursor data
        elif name == 'precursorMz':
            self._isPrecursor = False
    # ----
    
    
    def characters(self, ch):
        """Grab characters."""
        
        # get peaks
        if self._isPeaks:
            self.scan['points'] += ch
        
        # get precursor
        if self._isPrecursor:
            self.scan['precursorMz'] += ch
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
    # ----
    
    
    def startElement(self, name, attrs):
        """Element started."""
        
        # get instrument
        if name == 'msManufacturer':
             self.info['instrument'] += attrs.get('value', '') + ' '
        elif name == 'msModel':
             self.info['instrument'] += attrs.get('value', '') + ' '
        elif name == 'msIonisation':
             self.info['instrument'] += attrs.get('value', '') + ' '
        elif name == 'msMassAnalyzer':
             self.info['instrument'] += attrs.get('value', '') + ' '
    # ----
    
    
    def endElement(self, name):
        """Element ended."""
        
        # stop parsing
        if name == 'msInstrument':
            raise stopParsing()
    # ----
    
    

class stopParsing(Exception):
    """Exeption to stop parsing XML data."""
    pass
