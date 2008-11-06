"""
Classes for reading manufacturer specific ANDI-MS data files
"""

 #############################################################################
 #                                                                           #
 #    PyMS software for processing of metabolomic mass-spectrometry data     #
 #    Copyright (C) 2005-8 Vladimir Likic                                    #
 #                                                                           #
 #    This program is free software; you can redistribute it and/or modify   #
 #    it under the terms of the GNU General Public License version 2 as      #
 #    published by the Free Software Foundation.                             #
 #                                                                           #
 #    This program is distributed in the hope that it will be useful,        #
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
 #    GNU General Public License for more details.                           #
 #                                                                           #
 #    You should have received a copy of the GNU General Public License      #
 #    along with this program; if not, write to the Free Software            #
 #    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.              #
 #                                                                           #
 #############################################################################


import sys, types

import numpy
from pycdf import CDF, CDFError

from pyms.IO import Class
from pyms.Utils.Error import error, stop
from pyms.Utils.Utils import is_str, is_int, is_float, is_number
from pyms.Utils.IO import save_data

class ANDIMS_reader(object):

    """
    @summary: Generic reader for ANDI-MS NetCDF files

    @author: Lewis Lee
    @author: Vladimir Likic
    """

    # the keys used to retrieve certain data from the NetCDF file
    __MASS_STRING = "mass_values"
    __INTENSITY_STRING = "intensity_values"
    __TIME_STRING = "scan_acquisition_time"

    def __init__(self, file_name):

        """
        @param file_name: The name of the ANDI-MS file
        @type file_name: StringType
        """

        if not is_str(file_name):
            error("'file_name' must be a string")

        try:
            file = CDF(file_name)
            self.__file_name = file_name
        except CDFError:
            error("Cannot open file '%s'" % file_name) 

        print " -> Processing netCDF file '%s'" % (self.__file_name)

        time = file.var(self.__TIME_STRING)
        mass = file.var(self.__MASS_STRING)
        intensity = file.var(self.__INTENSITY_STRING)

        time_list = time.get().tolist()
        mass_list = mass.get().tolist()
        intensity_list = intensity.get().tolist()

        if len(mass_list) == 0 or len(intensity_list) == 0:
            error("The file contains no useable data")

        if len(mass_list) != len(intensity_list):
            error("The mass values do not match intensities")

        min_mass = min(mass_list)
        max_mass = max(mass_list)

        if is_float(min_mass): min_mass = int(round(min_mass))
        if is_float(max_mass): max_mass = int(round(max_mass))

        intensity_matrix = []

        scan = numpy.repeat([0], max_mass - min_mass + 1)

        offset = min_mass
        mass_elem = int(round(mass_list[0]))
        intensity_elem = int(round(intensity_list[0]))

        # Calculate the index in the scan where the intensity value will
        # be inserted
        i = mass_elem - offset
        # If the calculated index is valid, add the intensity value to
        # the existing value at the specified index
        if 0 <= i and i < len(scan):
            scan[i] = scan[i] + intensity_elem

        # The next iteration of the data processing procedure will
        # depend on the length of the data lists
        if len(mass_list) != 1 and len(intensity_list) != 1:
            # Initialise the list index.  Since the first element (at
            # index 0) has already been retrieved, the index is
            # initialised to 1 rather than 0
            index = 1

            while index < len(mass_list) and index < len(intensity_list):
                mass_elem_prev = mass_elem
                intensity_elem_prev = intensity_elem
                mass_elem = int(round(mass_list[index]))
                intensity_elem = int(round(intensity_list[index]))
                # If the previous mass value is larger than the current
                # mass value, the current scan has ended.  As such,
                # append the current scan into the data list and create
                # a new scan
                if mass_elem_prev > mass_elem:
                    intensity_matrix.append(scan)
                    scan = numpy.repeat([0], max_mass - min_mass + 1)
                # Calculate the index in the scan to insert the
                # intensity value into
                i = mass_elem - offset
                # If the calculated index is valid, add the intensity
                # value to the existing value at the specified index
                if 0 <= i and i < len(scan):
                    scan[i] = scan[i] + intensity_elem
                index = index + 1

        # Append the final scan to the data
        intensity_matrix.append(scan)

        # Fix any differences in scan sizes between the time values'
        # array and the intensity values' matrix
        scan_size = len(intensity_matrix)
        if len(intensity_matrix) > len(time_list):
            scan_size = len(time_list)

        # Check if time array is sorted and raise error if it isn't
        if not (time_list[:scan_size] == sorted(time_list[:scan_size])):
            error("File input was not sorted in chronological order")

        self.__time_list = time_list[:scan_size]
        self.__intensity_matrix = numpy.array(intensity_matrix[:scan_size])

        self.__min_rt = self.__time_list[0]
        self.__max_rt = self.__time_list[-1]

        self.__min_mass = min_mass
        self.__max_mass = max_mass

        self.__mass_list = []

        for mass in range(min_mass, max_mass+1):
            self.__mass_list.append(mass)

        if len(self.__time_list) != len(self.__intensity_matrix):
            error("data inconsistent in time domain")

        if len(self.__mass_list) != len(self.__intensity_matrix[0]):
            error("data inconsistent in m/z domain")

        print "    [ %d scans, masses from %d to %d ]" % \
                (len(self.get_tic()), self.__min_mass, self.__max_mass)

    def get_filename(self):

        """
        @summary: Returns the name of the ANDI/MS NetCDF file used to
            construct this object

        @return: Name of a file used to construct the object
        @rtype: StringType
        """

        return self.__file_name

    def get_intensity_matrix(self):

        """
        @summary: Returns the full intensity matrix

        @return: Intensity matrix
        @rtype: numpy.ndarray
        """ 

        return self.__intensity_matrix

    def get_time_list(self):

        """
        @summary: Returns the array of time values

        @return: Array of time values in seconds
        @rtype: numpy.ndarray
        """ 

        return self.__time_list

    def get_tic(self):

        """
        @summary: Returns the total ion chromatogram

        @return: Total ion chromatogram
        @rtype: IonChromatogram
        """

        ia = numpy.sum(self.__intensity_matrix, 1)
        rt = self.__time_list
        tic = Class.IonChromatogram(ia, rt)

        return tic

    def get_mass_range(self):

        """
        @summary: Returns the minimum and the maximum mass from the
            mass range

        @return: Minimum and maximum mass from the mass range
        @rtype: TupleType
        """
        return (self.__min_mass, self.__max_mass)

    def get_ic_at_index(self, index):

        """
        @summary: Returns the ion chromatogram at the specified index

        @param index: Index of an ion chromatogram in the
            intensity data matrix
        @type index: IntType 

        @return: Ion chromatogram at given index
        @rtype: IonChromatogram
        """

        if not int(index):
            error("'index' must be an integer")
        try:
            intensity_array = self.__intensity_matrix[:,index]
        except IndexError:
            error("index out of bounds.")

        return Class.IonChromatogram(intensity_array, self.__time_list, \
                index + self.__min_mass)

    def get_ic_at_mass(self, mass):

        """
        @summary: Returns the ion chromatogram for the specified mass

        If no mass value is given, the function returns the total
        ion chromatogram.

        @param mass: Mass value of an ion chromatogram
        @type mass: IntType

        @return: Ion chromatogram for given mass
        @rtype: IonChromatogram
        """

        if not is_int(mass):
            error("'mass' must be an integer")

        if mass < self.__min_mass or mass > self.__max_mass:
            error("mass is out of range")
        
        return self.get_ic_at_index(mass - self.__min_mass)

    def get_mass_spectrum_at_index(self, index):

        """
        @summary: Returns mass spectrum at given index

        @param index: Index of an ion chromatogram
        @type index: IntType

        @return: Mass spectrum at given index
        @rtype: numpy.ndarray
        """

        if not is_int(index):
            error("'index' must be an integer")

        im = self.get_intensity_matrix()

        try:
            mass_spectrum = im[index]
        except IndexError:
            error("index out of bounds")

        return mass_spectrum 

    def get_mass_list(self):

        """
        @summary: Returns the m/z list

        @return: List of m/z
        @rtype: numpy.ndarray
        """

        return self.__mass_list

    def get_index_at_time(self, time):

        """
        @summary: Returns the index corresponding to given time

        @param time: Time in seconds
        @type time: FloatType

        @return: Index corresponding to given time
        @rtype: IntType
        """

        if not is_number(time):
            error("'time' must be a number.")

        if time < self.__min_rt or time > self.__max_rt:
            error("time %.2f is out of bounds (min: %.2f, max: %.2f)" %
                  (time, self.__min_rt, self.__max_rt))

        for index in range(len(self.__time_list)):
            if time <= self.__time_list[index]:
                return index 

    def null_mass(self, mass):

        """
        @summary: Zeroes the intensity of a given mass across the entire
            time range

        @param mass: The mass value of an ion chromatogram
        @type mass: IntType

        @return: none
        @rtype: NoneType
        """

        if not is_int(mass):
            error("'mass' must be an integer")

        if mass < self.__min_mass or mass > self.__max_mass:
            error("mass is out of range")
       
        index = mass - self.__min_mass
        rowlen = len(self.__intensity_matrix[:,index])
        self.__intensity_matrix[:,index] = numpy.zeros(rowlen)

        print " -> nulled mass %d" % (mass)

    def export_csv(self, root_name):

        """
        @summary: Exports data to the CSV format

        Calling object.export_csv("NAME") will create NAME.im.csv,
        NAME.rt.csv, and NAME.mz.csv where these are the intensity
        matrix, retention time vector, and m/z vector.

        @param root_name: Root name for the output files
        @type root_name: StringType

        @return: none
        @rtype: NoneType

        @author: Milica Ng
        """

        # export 2D matrix of intensities into CSV format
        i_matrix = self.get_intensity_matrix()
        save_data(root_name+'.im.csv', i_matrix, sep=",")

        # export 1D vector of m/z's, corresponding to rows of
        # the intensity matrix, into CSV format
        mz_vector = self.get_mass_list()
        save_data(root_name+'.mz.csv', mz_vector, sep=",")

        # export 1D vector of retention times, corresponding to
        # columns of the intensity matrix, into CSV format
        rt_vector = self.get_time_list()
        save_data(root_name+'.rt.csv', rt_vector, sep=",")

class ChemStation(ANDIMS_reader):

    """
    @summary: ANDI-MS reader for Agilent ChemStation NetCDF files

    @author: Lewis Lee
    @author: Vladimir Likic
    """

    pass

class Xcalibur(ANDIMS_reader):

    """
    @summary: ANDI-MS reader for Thermo Xcalibur NetCDF files

    @author: Tim Erwin
    @author: Vladimir Likic
    """

    pass

