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
import re

# load configuration
import config

# register essential objects
import objects


# PARSE SIMPLE ASCII XY
# ---------------------

class parseXY():
    """Parse data from ASCII XY."""
    
    def __init__(self, path):
        self.path = path
    # ----
    
    
    def getSpectrum(self, discrete=False):
        """Get spectrum from document."""
        
        # parse data
        data = self._parseData()
        if not data:
            return False
        
        # parse data as peaklist (discrete points)
        if discrete:
            for x, p in enumerate(data):
                data[x] = objects.peak(p[0], p[1])
            spectrum = objects.scan(peaks=data)
        
        # parse data as spectrum (continuous line)
        else:
            spectrum = objects.scan(points=data)
        
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
        
        return info
    # ----
    
    
    def _parseData(self):
        """Parse data."""
        
        # open document
        try:
            document = file(self.path)
            rawData = document.readlines()
            document.close()
        except IOError:
            return False
        
        pattern = re.compile('^([-0-9\.eE+]+)[ \t]*(;|,)?[ \t]*([-0-9\.eE+]*)$')
        
        # read lines
        data = []
        for line in rawData:
            line = line.strip()
            
            # discard comment lines
            if not line or line[0] == '#':
                continue
            
            # check pattern
            parts = pattern.match(line)
            if parts:
                try:
                    mass = float(parts.group(1))
                    intensity = float(parts.group(3))
                except ValueError:
                    return False
                data.append([mass, intensity])
            else:
                return False
        
        return data
    # ----
    
    
