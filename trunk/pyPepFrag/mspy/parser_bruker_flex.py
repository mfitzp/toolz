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
import os
import re
import struct
import math

# load configuration
import config

# register essential objects
import objects


# PARSE BRUKER FLEX-SERIES DATA
# -----------------------------

class parseBRUKERFLEX():
    """Parse data from Bruker's flex-series instruments."""
    
    def __init__(self, path):
        self.path = path
        
        # search for fid in folder
        if os.path.isdir(path):
            spectra = self.foundSpectra(path)
            if spectra:
                self.path = spectra[0]
    # ----
    
    
    def getSpectrum(self):
        """Get spectrum from document."""
        
        # parse data
        spectrum = self._parseSpectrum()
        if not spectrum:
            return False
        
        return spectrum
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
        
        # get info
        params = self._parseParams()
        if params:
            if params.has_key('OpId'):
                info['operator'] = params['OpId'][1:-1]
            if params.has_key('AQ_DATE'):
                info['date'] = params['AQ_DATE'][1:-1]
            if params.has_key('CMT1') and params['CMT1'][1:-1]:
                info['notes'] += '%s\n' % params['CMT1'][1:-1]
            if params.has_key('CMT2') and params['CMT2'][1:-1]:
                info['notes'] += '%s\n' % params['CMT2'][1:-1]
            if params.has_key('CMT3') and params['CMT3'][1:-1]:
                info['notes'] += '%s\n' % params['CMT3'][1:-1]
        
        return info
    # ----
    
    
    def foundSpectra(self, path):
        """Found fid files in the folder."""
        
        spectra = []
        for dirpath, dirnames, filenames in os.walk(path):
            for name in filenames:
                if name.lower() == 'fid':
                    spectra.append(os.path.join(dirpath, name))
        
        return spectra
    # ----
    
    
    def _parseSpectrum(self):
        """Parse spectrum data."""
        
        # get acquisition parames
        params = self._parseParams()
        if not params:
            return False
        
        # open spectrum
        try:
            document = file(self.path, 'rb')
            rawData = document.read()
            document.close()
        except IOError:
            return False
        
        # convert to list
        try:
            count = len(rawData)/struct.calcsize('i')
            start, end = 0, len(rawData)
            points = struct.unpack('i' * count, rawData[start:end])
        except:
            return False
        
        # check data length
        if len(points) != int(params['TD']):
            return False
        
        # shift X-axis
        if params['SPTYPE'] == 'psd':
            shift = float(params['ML1'])
            interval = float(params['DW'])
        else:
            shift = float(params['DELAY'])
            interval = float(params['DW'])
        
        buff = []
        for x in points:
            buff.append([shift, x])
            shift += interval
        points = buff
        
        # convert X-axis to m/z
        if params['SPTYPE'] == 'tof':
            points = self._convertTimeToMZ(points, float(params['ML1']), float(params['ML2']), float(params['ML3']))
        
        # convert to scan object
        spectrum = objects.scan(points)
        
        # set additional parameters
        spectrum.msLevel = 1
        if params['SPTYPE'] == 'psd':
            spectrum.msLevel = 2
            if 'Parent' in params:
                spectrum.precursorMZ = params['Parent']
        
        return spectrum
    # ----
    
    
    def _parseParams(self):
        """Parse acquisition params."""
        
        # get acquisition file
        dirname = os.path.dirname(self.path)
        if os.path.exists(dirname + '/acqus'):
            path = dirname + '/acqus'
        elif os.path.exists(dirname + '/ACQUS'):
            path = dirname + '/ACQUS'
        else:
            return False
        
        # load data
        try:
            document = file(path)
            rawData = document.readlines()
            document.close()
        except IOError:
            return False
        
        # get params
        params = {}
        pattern = re.compile('^##\$([1-9a-zA-Z_]+)=(.*)$')
        for line in rawData:
            line = line.strip()
            parts = pattern.match(line)
            if parts:
                key = parts.group(1)
                value = parts.group(2).strip()
                params[key] = value
        
        # get spectrum type
        params['SPTYPE'] = self._getSpectrumType()
        if not params['SPTYPE']:
            return False
        
        # check important params
        if params['SPTYPE'] == 'tof':
            for key in ('TD', 'DELAY', 'DW', 'ML1', 'ML2', 'ML3'):
                if not key in params:
                    return False
        elif params['SPTYPE'] == 'psd':
            for key in ('TD', 'DW', 'ML1', 'ML2'):
                if not key in params:
                    return False
        else:
            return False
        
        return params
    # ----
    
    
    def _convertTimeToMZ(self, data, c1, c2, c3):
        """Convert time to m/z according to calibration constants."""
        
        cropIndex = None
        
        # linear calibration
        # t = c2 + sqrt(10^12 * M / c1)
        # M = (t - c2) * (t - c2) * c1 / math.pow(10,12)
        if not c3:
            con = c1 / math.pow(10,12)
            for x in range(len(data)):
                if data[x][0] <= c2:
                    cropIndex = x
                else:
                    data[x][0] = (data[x][0] - c2) * (data[x][0] - c2) * con
        
        # quadratic calibration
        # t = c2 + sqrt(10^12 * M / c1) + c3 * M
        # a = c3 * c3
        # b = -math.pow(10.0, 12.0) / c1 - 2 * (t - c2) * c3
        # c = (t - c2) * (t - c2)
        else:
            a = c3 * c3
            b1 = -math.pow(10.0, 12.0) / c1
            for x in range(len(data)):
                b = b1 - 2 * (data[x][0] - c2) * c3
                c = (data[x][0] - c2) * (data[x][0] - c2)
                if data[x][0] <= c2:
                    cropIndex = x
                else:
                    data[x][0] = (-b - math.sqrt(b*b - 4*a*c)) / (2*a)
        
        # crop "negativ" data
        if cropIndex:
            del data[0:cropIndex+1]
        
        return data
    # ----
    
    
    def _getSpectrumType(self):
        """Get spectrum type."""
        
        # get spectrum type file
        dirname = os.path.dirname(self.path)
        if os.path.exists(dirname + '/sptype'):
            path = dirname + '/sptype'
        elif os.path.exists(dirname + '/SPTYPE'):
            path = dirname + '/SPTYPE'
        else:
            return False
        
        # load data
        try:
            document = file(path)
            rawData = document.read()
            document.close()
        except IOError:
            return False
        
        # get type
        sptype = str(rawData)
        sptype = sptype.strip()
        sptype = sptype.lower()
        
        return sptype
    # ----
    
    