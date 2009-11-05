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

# Function: Load and parse spectrum data from Bruker Daltonics Flex series.
#modified by BH Clowers Aug 2008

import math
import re
import string
import os
import os.path
import xml.dom.minidom
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
import base64
import struct
import sys

from PyQt4.QtGui import QFileDialog,  QApplication
import numpy as N

import time as T

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"


def open_file():
    filename = str(QFileDialog.getOpenFileName())
    if filename:
        print "Opened: ", filename
        return filename

class brukerFlexDoc:
    """ Load and parse spectrum data from Bruker Daltonics Flex series. """

    # ----
    def __init__(self,  path):
        self.data = {
                    'docType': 'Bruker Flex Series',
                    'operator':'',
                    'date':'',
                    'analyzer':'',
                    'notes':'',
                    'runID':'',
                    'msManufacturer':'Bruker Daltonics',
                    'msModel':'autoFlex TOF-TOF',
                    'ionization':'MALDI',
                    'acqSoft':'',
                    'polarity':'',
                    'spectrum':[],
                    'peaklist':None,
                    'basePeak':None,
                    'basePeakInt':None
                    }
        self.filename = path
        self.ns = None #namespace
        self.elmName = None
        self.scanList = None
        self.fragScan = False
        if ".LIFT" in self.filename:
            self.fragScan = True
        self.getDocument(self.filename)
    # ----

    def encodeSpec(self):
        #t1 = T.clock()
        specList = self.data.get('spectrum')
        if len(specList) > 0:
            # decode data
            if type(specList[0]) is N.ndarray:
                subspec = N.column_stack(specList)
                if sys.byteorder != 'big':
                    subspec.byteswap()
                data = subspec.flatten()
                try:
                    endian = '!'
                    pointsCount = len(data)#/struct.calcsize(endian+'f')

                    data = struct.pack(endian+'f'*pointsCount, *data)#data[start:end])
                    data64 = base64.b64encode(data)
                except:
                    raise
                    return False

                t2 = T.clock()
                #print t2-t1
                return data64


    # ----
    def getDocument(self, path):
        """ Load and process data. """

        # get spectrum from raw data
        if not self.handleSpectrum(path):
            return False

        # get peaklist data
        self.handlePeaklist(path)

        return self.data
    # ----


    # ----
    def getElement(self, name, path):
        """ Load and process selected data part. """

        # get peaklist
        if name == 'peaklist':
            if not self.handlePeaklist(path):
                return False

        # get spectrum
        elif name == 'spectrum':
            if not self.handleSpectrum(path):
                return False

        return self.data
    # ----


    # ----
    def handleSpectrum(self, path):
        """ Convert spectrum data to list of points. """

        # get acquisition parameters
        acquData = self.handleAcquParams(path)
        if not acquData:
            return False

        # load spectrum data from file
        try:
            spectrumFile = file(path, 'rb')
            spectrumData = spectrumFile.read()
            spectrumFile.close()
        except IOError:
            return False

        # convert spectrum data from binary file
        spectrum = self.spectrumConvertFromBinary(spectrumData)
        if not spectrum:
            return False

        # check data length
        if len(spectrum) != int(acquData['TD']):
            return False

        # get X-axis for FAST spectrum
        if acquData['SPTYPE'] == 'psd':
            print  'psd'
            spectrum = self.spectrumAddFastAxis(spectrum, float(acquData['ML1']), float(acquData['DW']))

        # get X-axis for normal TOF spectrum
        elif acquData['SPTYPE'] == 'tof':
#            print acquData['DELAY']
#            print acquData['DW']
#            print acquData['ML1']
#            print acquData['ML2']
#            print acquData['ML3']
            spectrum = self.spectrumAddTimeAxis(spectrum, float(acquData['DELAY']), float(acquData['DW']))
            #spectrum = N.array(spectrum)#temproary usage to make TOF axis in a format to write to disk
            spectrum = self.spectrumConvertTimeAxis(spectrum, float(acquData['ML1']), float(acquData['ML2']), float(acquData['ML3']))

        # get X-axis for ICR spectrum
        elif acquData['SPTYPE'] == 'icr':
            # not implemented yet
            spectrum = False

        if type(spectrum) is N.ndarray:
            self.data['spectrum'] = spectrum
            return True
        else:
            return False
    # ----


    # ----
    def handlePeaklist(self, path):
        """ Search for peaklist XML file and get peaklist data. """

        # get peaklist file
        dirname = os.path.dirname(path)
        if os.path.exists(dirname+'/pdata/1/peaklist.xml'):
            path = dirname+'/pdata/1/peaklist.xml'
        else:
            return False

        # parse XML
        try:
            document = ET.parse(path).getroot()
            self.ns = document.tag
            #print self.ns
            #document = xml.dom.minidom.parse(path)
        except:
            return False

        # get peaklist
        peaklist = []
        #peaks = document.getElementsByTagName('pk')
        peaks = document.findall('pk')#self.ns+
        if peaks:
            for peak in peaks:

                # get mass
                massNode = peak.find('mass')
                mass = massNode.text

                # get intensity
                intensNode = peak.find('absi')
                intens = intensNode.text

                # check mass and intensity
                try:
                    mass = float(mass)
                    intens = float(intens)
                except ValueError:
                    return False

                # add peak to peaklist
                peaklist.append([mass, intens])

        peaklist = N.array(peaklist)
        #intenseArray = peaklist[:,1]
        #print intenseArray.argmax()
        if len(peaklist) > 0:
            bploc = peaklist[:,1].argmax()
            self.data['basePeak'] = float(peaklist[bploc][0])
            self.data['basePeakInt'] = float(peaklist[bploc][1])
            self.data['peaklist'] = peaklist
        #print peaklist

        return True
    # ----


    # ----
    def handleAcquParams(self, path):
        """ Parse acquisition file and get params. """

        # get acquisition file (Howgh Brukers' programmers...)
        dirname = os.path.dirname(path)
        if os.path.exists(dirname+'/acqus'):
            path = dirname+'/acqus'
        elif os.path.exists(dirname+'/ACQUS'):
            path = dirname+'/ACQUS'
        else:
            return False

        # load acquisition params
        try:
            acquFile = file(path)
            data = acquFile.readlines()
            acquFile.close()
        except IOError:
            return False

        # parse lines
        acquParams = {}
        pattern = re.compile('^##\$([1-9a-zA-Z_]+)=(.*)$')
        for line in data:
            line = string.strip(line)

            # get key and value
            parts = pattern.match(line)
            if parts:
                key = parts.group(1)
                value = string.strip(parts.group(2))
                acquParams[key] = value

        # get spectrum type
        acquParams['SPTYPE'] = self.getSpectrumType(dirname)
        if not acquParams['SPTYPE']:
            return False

        # check important params for normal or FAST spectrum
        if acquParams['SPTYPE'] == 'tof':
            keys = ['TD', 'DELAY', 'DW', 'ML1', 'ML2', 'ML3']
        elif acquParams['SPTYPE'] == 'psd':
            keys = ['TD', 'DW', 'ML1', 'ML2']
        elif acquParams['SPTYPE'] == 'icr':
            # not implemented yet
            return False
        else:
            return False
        for key in keys:
            if not key in acquParams:
                return False

        # get and remember spectrum description
        if acquParams.has_key('Parent'):
            parentMZ = float(acquParams['Parent'])
            if parentMZ != 0:
                #print parentMZ
                self.data['precursorMZ'] = parentMZ

        if acquParams.has_key('SPTYPE'):
            self.data['analyzer'] = acquParams['SPTYPE']
        if acquParams.has_key('POLARI'):
            polarity = int(acquParams['POLARI'])
            if polarity == 1:
                self.data['polarity'] = '+'
            else:
                self.data['polarity'] = '-'

        if acquParams.has_key('FCVer'):
            self.data['acqSoft'] = acquParams['FCVer'][1:-1]
        if acquParams.has_key('SPOTNO'):
            self.data['runID'] = acquParams['SPOTNO'][1:-1]
        if acquParams.has_key('OpId'):
            self.data['operator'] = acquParams['OpId'][1:-1]
        if acquParams.has_key('AQ_DATE'):
            self.data['date'] = acquParams['AQ_DATE'][1:-1]
        if acquParams.has_key('CMT1') and acquParams['CMT1'][1:-1]:
            self.data['notes'] += 'CMT1: %s\n' % acquParams['CMT1'][1:-1]
        if acquParams.has_key('CMT2') and acquParams['CMT2'][1:-1]:
            self.data['notes'] += 'CMT2: %s\n' % acquParams['CMT2'][1:-1]
        if acquParams.has_key('CMT3') and acquParams['CMT3'][1:-1]:
            self.data['notes'] += 'CMT3: %s\n' % acquParams['CMT3'][1:-1]

        return acquParams
    # ----


    # ----
    def spectrumConvertFromBinary(self, data):
        """ Convert binary data to list of values. """

        # get data
        try:
            pointsCount = len(data)/struct.calcsize('i')
            start, end = 0, len(data)
            points = struct.unpack('i'*pointsCount, data[start:end])
            return points
        except:
            return False
    # ----


    # ----
    def spectrumAddTimeAxis(self, data, delay, interval):
        """ Count time values (raw X-axis) for normal spectrum from start-time and interval. """

        # add X-axis time
        spectrum = []
        time = delay
        for x in range(len(data)):
            spectrum.append([time, data[x]])
            time += interval

        return spectrum
    # ----


    # ----
    def spectrumAddFastAxis(self, data, start, interval):
        """ Count time values (raw X-axis) for FAST spectrum from start-stop-time and interval. """

        # add X-axis time
        spectrum = []
        mass = start
        for x in range(len(data)):
            spectrum.append([mass, data[x]])
            mass += interval

        return spectrum
    # ----


    # ----
    def spectrumConvertTimeAxis(self, data, c1, c2, c3):
        """ Convert time to mass according to calibration constants. """

        cropIndex = None

        #print type(data)
        if type(data) is list:
            data = N.array(data)
        else:
            return False

        # linear calibration
        # t = c2 + sqrt(10^12 * M / c1)
        # M = (t - c2) * (t - c2) * c1 / math.pow(10,12)
        if c3 == 0:
            con = c1 / math.pow(10,12)
            data[:, 0] = ((data[:, 0]-c2)**2)*con


        # quadratic calibration
        # t = c2 + sqrt(10^12 * M / c1) + c3 * M
        # a = c3 * c3
        # b = -math.pow(10.0, 12.0) / c1 - 2 * (t - c2) * c3
        # c = (t - c2) * (t - c2)
        else:
#            a = c3**2
#            b1 = -math.pow(10.0, 12.0) / c1
#            b = b1-2*(data[:, 0]-c2)*c3
#            c = (data[:, 0]-c2)**2
#            data[:, 0]=(-b-((b**2-4*a*c)**0.5))/(2*a)
            t = data[:, 0]
            data[:, 0]=((c1+c2*t+c3*t**2)**0.5)/math.pow(10, 12)

        return data
    # ----


    # ----
    def getSpectrumType(self, dirname):

        # get spectrum type file (Howgh Brukers' programmers...)
        if os.path.exists(dirname+'/sptype'):
            path = dirname+'/sptype'
        elif os.path.exists(dirname+'/SPTYPE'):
            path = dirname+'/SPTYPE'
        else:
            return False

        # load spectrum type params
        try:
            sptypeFile = file(path)
            sptype = sptypeFile.read()
            sptypeFile.close()
        except IOError:
            return False

        # check string
        sptype = str(sptype)
        sptype = sptype.strip()
        sptype = sptype.lower()

        return sptype
    # ----


    # ----
    def getNodeText(self, nodelist):
        """ Get text from node list. """

        # get text
        buff = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                buff += node.data

        return buff
    # ----
#if __name__ == "__main__":
#
#    import sys
#    import time
#    #import numpy as N
#    import pylab as P
#    from scipy import ndimage
#    from matplotlib.lines import Line2D
#    app = QApplication(sys.argv)
#    fn = open_file()
#
#    if fn:
#        t1 = time.clock()
#        flex = brukerFlexDoc(fn)
#        spectrum = flex.data.get('spectrum')
#        t2 = time.clock()
#        print t2-t1
##
#        struct_pts = int(round(spectrum[:, 1].size*0.005))
#        str_el = N.repeat([1], struct_pts)
#        tFil = ndimage.white_tophat(spectrum[:, 1], None, str_el)
##
#
#
#        #P.save('A10_TOF_LIFT.txt',  spectrum)
#        fig = P.figure()
#        ax = fig.add_subplot(111)
#        ax.plot(spectrum[:, 0],  spectrum[:, 1])
#        ax.plot(spectrum[:, 0], tFil, ':r')
#        #print flex.data['basePeak'], flex.data['basePeakInt']
#        if flex.data['basePeak'] != None:
#            peaklist = flex.data['peaklist']
#            for peak in peaklist:
#                ax.text(peak[0], peak[1]*1.05, '%.3f'%peak[0],  fontsize=9, rotation = 90)
#        P.show()
#    sys.exit(app.exec_())
