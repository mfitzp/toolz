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

#load libs
import re
import numpy
from copy import copy, deepcopy

# load configuration
import config

# register essential objects
import blocks

# register essential modules
import basics
import pattern
import peakpicking

# compile basic patterns
formulaPattern = re.compile(r'''
    ^(
        ([\(][\d]*)* # start parenthesis
        (
            ([A-Z][a-z]{0,2}) # atom symbol
            (\{[\d]+\})? # isotope
            (([\-][\d]+)|[\d]*) # atom count
        )+
        ([\)][\d]*)* # end parenthesis
    )*$
''', re.X)

elementPattern = re.compile(r'''
            ([A-Z][a-z]{0,2}) # atom symbol
            (?:\{([\d]+)\})? # isotope
            ([\-]?[\d]*) # atom count
''', re.X)


# BASIC OBJECTS DEFINITION
# ------------------------

class formula:
    """Formula object definition."""
    
    def __init__(self, string):
        
        self.string = string
        self.mass = None
        self.composition = None
        
        # check formula
        if not formulaPattern.match(self.string):
            raise ValueError, 'Wrong formula! --> ' + self.string
        
        # check elements and isotopes
        for atom in elementPattern.findall(self.string):
            if not atom[0] in blocks.elements:
                raise ValueError, 'Unknown element in formula! --> ' + atom[0]
            elif atom[1] and not atom[1] in blocks.elements[atom[0]].isotopes:
                raise ValueError, 'Unknown isotope in formula! --> ' + atom[0] + atom[1]
        
        # check brackets
        if self.string.count(')') != self.string.count('('):
            raise ValueError, 'Wrong number of brackets in formula! --> ' + self.string
    # ----
    
    
    def getFormula(self):
        """Make formula."""
        
        # get composition
        composition = self.getComposition()
        
        # format composition
        buff = ''
        for el in sorted(composition.keys()):
            if composition[el] == 1:
                buff += el
            else:
                buff += '%s%d' % (el, composition[el])
        
        return buff
    # ----
    
    
    def getComposition(self):
        """Get elemental composition of current formula."""
        
        # check mass buffer
        if self.composition != None:
            return self.composition
        
        # unfold brackets
        unfoldedFormula = _unfoldBrackets(self.string)
        
        # group same elements
        self.composition = {}
        for symbol, isotop, count in elementPattern.findall(unfoldedFormula):
            
            # make atom
            if isotop:
                atom = '%s{%s}' % (symbol, isotop)
            else:
                atom = symbol
            
            # convert counting
            if count:
                count = int(count)
            else:
                count = 1
            
            # add atom
            if atom in self.composition:
                self.composition[atom] += count
            else:
                self.composition[atom] = count
        
        # remove zeros
        for atom in self.composition.keys():
            if self.composition[atom] == 0:
                del self.composition[atom]
        
        return self.composition
    # ----
    
    
    def getMass(self):
        """Get mass of current formula."""
        
        # check mass buffer
        if self.mass != None:
            return self.mass
        
        massMo = 0
        massAv = 0
        
        # get composition
        composition = self.getComposition()
        
        # get mass for each atom
        for atom in composition:
            count = composition[atom]
            
            # check specified isotope and mass
            match = elementPattern.match(atom)
            symbol, massNumber, tmp = match.groups()
            if massNumber:
                isotope = blocks.elements[symbol].isotopes[massNumber]
                atomMass = (isotope[0], isotope[0])
            else:
                atomMass = blocks.elements[symbol].mass
            
            # multiply atom
            massMo += atomMass[0]*count
            massAv += atomMass[1]*count
        
        # store mass in buffer
        self.mass = (massMo, massAv)
        
        return (massMo, massAv)
    # ----
    
    
    def getMZ(self, charge, agentFormula='H', agentCharge=1):
        """Get m/z of current formula. Charge, agent formula and agent charge can be set."""
        
        # get current mass and calculate mz
        return basics.mz(self.getMass(), charge, agentFormula=agentFormula, agentCharge=agentCharge)
    # ----
    
    
    def getNMD(self):
        """Get normalized mass defect."""
        
        # calc NMD
        mo, av = self.getMass()
        nm = int(0.5 + (mo * (1999.0/2000.0)))
        return 1000 * (mo - nm)/mo
    # ----
    
    
    def getNIS(self):
        """Get normalized isotopic shift."""
        
        # calc NMD
        mo, av = self.getMass()
        return 1000 * (av - mo)/mo
    # ----
    
    
    def getPattern(self, fwhm=0.1, relIntTreshold=0.01, charge=0, agentFormula='H', agentCharge=1, rounding=7):
        """Get isotopic pattern of current formula."""
        
        return pattern.isoPattern(self, \
            fwhm=fwhm, \
            relIntTreshold=relIntTreshold, \
            charge=charge, \
            agentFormula=agentFormula, \
            agentCharge=agentCharge, \
            rounding=rounding)
    # ----
    


class sequence:
    """Sequence object definition."""
    
    def __init__(self, chain, title=''):
        
        # get chain
        chain = chain.upper()
        for char in ('\t','\n','\r','\f','\v', ' ', '-', '*', '.'):
                chain = chain.replace(char, '')
        self.chain = chain.upper()
        
        self.nTermFormula = 'H'
        self.cTermFormula = 'OH'
        self.modifications = [] # [[name, position=[#|symbol], state[f|v]], ] (f-fixed, v-variable)
        self.labels = [] # [[name, position=[#|symbol], state[f|v]], ] (f-fixed, v-variable)
        self.mass = None # (monoisotopic, average)
        self.composition = None
        
        # for proteins
        self.accession = ''
        self.title = title
        self.orgName = ''
        
        # for peptides
        self.userRange = []
        self.aaBefore = ''
        self.aaAfter = ''
        self.miscleavages = 0
        
        # for fragments
        self.fragmentSerie = ''
        self.fragmentIndex = 0
        self.fragFiltered = False
        self.lossFormula = ''
        
        # check amino acids
        for amino in self.chain:
            if not amino in blocks.aminoacids:
                raise ValueError, 'Unknown amino acid in sequence! --> ' + amino
    # ----
    
    
    def __len__(self):
        """Get sequence length."""
        return len(self.chain)
    # ----
    
    
    def __getslice__(self, start, stop):
        """Get slice of the sequence."""
        
        # check slice
        if stop < start:
            raise ValueError, 'Invalid sequence slice definition!'
        
        # brake the links
        parent = deepcopy(self)
        
        # check slice
        start = max(start, 0)
        stop = min(stop, len(parent.chain))
        
        # make new sequence object
        seq = parent.chain[start:stop]
        peptide = sequence(seq)
        
        # add modifications
        for mod in parent.modifications:
            if type(mod[1]) == int and mod[1] >= start and mod[1] < stop:
                mod[1] -= start
                peptide.modifications.append(mod)
            elif type(mod[1]) in (str, unicode) and mod[1] in peptide.chain:
                peptide.modifications.append(mod)
        
        # add labels
        for mod in parent.labels:
            if type(mod[1]) == int and mod[1] >= start and mod[1] < stop:
                mod[1] -= start
                peptide.labels.append(mod)
            elif type(mod[1]) in (str, unicode) and mod[1] in peptide.chain:
                peptide.labels.append(mod)
        
        # set range in user coordinates
        peptide.userRange = [start+1, stop]
        
        # set adjacent amino acids
        if start > 0:
            peptide.aaBefore = parent.chain[start-1]
        if stop < len(parent.chain):
            peptide.aaAfter = parent.chain[stop]
        
        # add terminal modifications
        if start == 0:
            peptide.nTermFormula = parent.nTermFormula
        if stop >= len(parent.chain):
            peptide.cTermFormula = parent.cTermFormula
        
        return peptide
    # ----
    
    
    def __setslice__(self, start, stop, value):
        """Insert sequence object."""
        
        # check slice
        if stop < start:
            raise ValueError, 'Invalid slice!'
        
        # check value
        if not isinstance(value, sequence):
            raise TypeError, 'Invalid object to instert!'
        
        # brake the links
        value = deepcopy(value)
        
        # delete slice
        if stop != start:
            del(self[start:stop])
        
        # insert sequence
        self.chain = self.chain[:start] + value.chain + self.chain[start:]
        
        # shift modifications
        for x, mod in enumerate(self.modifications):
            if type(mod[1]) == int and mod[1] >= start:
                self.modifications[x][1] += (len(value))
        
        # shift labels
        for x, mod in enumerate(self.labels):
            if type(mod[1]) == int and mod[1] >= start:
                self.labels[x][1] += (len(value))
        
        # insert modifications
        for mod in value.modifications:
            if type(mod[1]) == int:
                mod[1] += start
            self.modifications.append(mod)
        
        # insert labels
        for mod in value.labels:
            if type(mod[1]) == int:
                mod[1] += start
            self.labels.append(mod)
        
        # clear
        self.mass = None
        self.composition = None
        self.userRange = []
        self.aaBefore = ''
        self.aaAfter = ''
        self.miscleavages = 0
    # ----
    
    
    def __delslice__(self, start, stop):
        """Delete slice of the sequence"""
        
        # check slice
        if stop < start:
            raise ValueError, 'Invalid slice!'
        
        # remove sequence
        self.chain = self.chain[:start] + self.chain[stop:]
        
        # remove modifications
        keep = []
        for mod in self.modifications:
            if type(mod[1]) == int and (mod[1] < start or mod[1] >= stop):
                if mod[1] >= stop:
                    mod[1] -= (stop - start)
                keep.append(mod)
            elif type(mod[1]) in (str, unicode) and mod[1] in self.chain:
                keep.append(mod)
        self.modifications = keep
        
        # remove labels
        keep = []
        for mod in self.labels:
            if type(mod[1]) == int and (mod[1] < start or mod[1] >= stop):
                if mod[1] >= stop:
                    mod[1] -= (stop - start)
                keep.append(mod)
            elif type(mod[1]) in (str, unicode) and mod[1] in self.chain:
                keep.append(mod)
        self.labels = keep
        
        # clear
        self.mass = None
        self.composition = None
        self.userRange = []
        self.aaBefore = ''
        self.aaAfter = ''
        self.miscleavages = 0
    #----
    
    
    def __add__(self, value):
        """Join sequences and return result."""
        
        # check value
        if not isinstance(value, sequence):
            raise TypeError, 'Invalid object to join with sequence!'
        
        # join sequences
        result = self[:]
        result[len(result):] = value
        
        # set C terminus
        result.cTermFormula = value.cTermFormula
        
        # set neutral loss
        result.lossFormula = value.lossFormula
        
        # clear
        result.mass = None
        result.composition = None
        result.userRange = []
        result.aaBefore = ''
        result.aaAfter = ''
        result.miscleavages = 0
        
        return result
    # ----
    
    
    def getFormula(self):
        """Make formula."""
        
        # get composition
        composition = self.getComposition()
        
        # format composition
        buff = ''
        for el in sorted(composition.keys()):
            if composition[el] == 1:
                buff += el
            else:
                buff += '%s%d' % (el, composition[el])
        
        return buff
    # ----
    
    
    def getComposition(self):
        """Get elemental composition of current sequence."""
        
        # check mass buffer
        if self.composition != None:
            return self.composition
        
        plusFormula = ''
        minusFormula = ''
        
        # add amino acids to formula
        for amino in self.chain:
            plusFormula += blocks.aminoacids[amino].formula
        
        # add modifications and labels
        mods = self.modifications + self.labels
        for name, position, state in mods:
            count = 1
            if type(position) == str and position !='':
                count = self.chain.count(position)
            plusFormula += count*blocks.modifications[name].gainFormula
            minusFormula += count*blocks.modifications[name].lossFormula
        
        # add terminal modifications
        plusFormula += self.nTermFormula + self.cTermFormula
        
        # subtract neutral loss for fragments
        minusFormula += self.lossFormula
        
        # get compositions
        self.composition = formula(plusFormula).getComposition()
        minusComposition = formula(minusFormula).getComposition()
        
        # subtract minus formula
        for atom in minusComposition:
            if atom in self.composition:
                self.composition[atom] -= minusComposition[atom]
            else:
                self.composition[atom] = minusComposition[atom]
        
        # remove zeros
        for atom in self.composition.keys():
            if self.composition[atom] == 0:
                del self.composition[atom]
        
        return self.composition
    # ----
    
    
    def getMass(self):
        """Get mass of current sequence."""
        
        # check mass buffer
        if self.mass != None:
            return self.mass
        
        # get mass
        composition = self.getFormula()
        compound = formula(composition)
        mass = compound.getMass()
        
        # store mass in buffer
        self.mass = (mass[0], mass[1])
        
        return (mass[0], mass[1])
    # ----
    
    
    def getMZ(self, charge, agentFormula='H', agentCharge=1):
        """Get m/z of current sequence. Charge, agent formula and agent charge can be set."""
        
        # get current mass and calculate mz
        return basics.mz(self.getMass(), charge, agentFormula=agentFormula, agentCharge=agentCharge)
    # ----
    
    
    def getNMD(self):
        """Get normalized mass defect."""
        
        # calc NMD
        mo, av = self.getMass()
        nm = int(0.5 + (mo * (1999.0/2000.0)))
        return 1000 * (mo - nm)/mo
    # ----
    
    
    def getNIS(self):
        """Get normalized isotopic shift."""
        
        # calc NMD
        mo, av = self.getMass()
        return 1000 * (av - mo)/mo
    # ----
    
    
    def getPattern(self, fwhm=0.1, relIntTreshold=0.01, charge=0, agentFormula='H', agentCharge=1, rounding=7):
        """Get isotopic pattern of current sequence."""
        
        return pattern.isoPattern(self, \
            fwhm=fwhm, \
            relIntTreshold=relIntTreshold, \
            charge=charge, \
            agentFormula=agentFormula, \
            agentCharge=agentCharge, \
            rounding=rounding)
    # ----
    
    
    def getFormated(self, format='S [m]'):
        """Get formated sequence."""
        
        # make keys
        keys = {}
        keys['s'] = self.chain.lower()
        keys['S'] = self.chain
        keys['n'] = self.nTermFormula
        keys['c'] = self.cTermFormula
        keys['b'] = self.aaBefore.lower()
        keys['B'] = self.aaBefore
        keys['a'] = self.aaAfter.lower()
        keys['A'] = self.aaAfter
        keys['m'] = self._formatModifications()
        keys['p'] = self.miscleavages
        
        if self.userRange:
            keys['r'] = '%s-%s' % tuple(self.userRange)
        
        if self.fragmentSerie:
            if type(self.fragmentIndex) in (tuple, list):
                keys['f'] = '%s %s-%s' % (self.fragmentSerie, self.fragmentIndex[0], self.fragmentIndex[1])
            else:
                keys['f'] = '%s %s' % (self.fragmentSerie, self.fragmentIndex)
        
        # format
        buff = ''
        for char in format:
            if char in keys:
                buff += keys[char]
            else:
                buff += char
        
        # clear format
        buff = buff.replace('[]', '')
        buff = buff.replace('()', '')
        buff = buff.strip()
        
        return buff
    # ----
    
    
    def modify(self, name, position, state='f'):
        """Add new modification to sequence."""
        
        # check modification
        if not name in blocks.modifications:
            raise KeyError, 'Unknown modification! --> ' + name
        
        # add modification
        self.modifications.append([name, position, state])
        self.mass = None
        self.composition = None
    # ----
    
    
    def removeModification(self, mod):
        """Remove modification from sequence."""
        
        # remove modification
        if mod in self.modifications:
            i = self.modifications.index(mod)
            del self.modifications[i]
        
        self.mass = None
        self.composition = None
    # ----
    
    
    def setTerminalFormula(self, term, mod):
        """Set terminal modification."""
        
        if term == 'N':
            self.nTermFormula = mod
        elif term == 'C':
            self.cTermFormula = mod
        
        self.mass = None
        self.composition = None
    # ----
    
    
    def label(self, name, position, state='f'):
        """Add new label modification to sequence."""
        
        # check modification
        if not name in blocks.modifications:
            raise KeyError, 'Unknown modification! --> ' + name
        
        # add modification
        
        self.labels.append([name, position, state])
        self.mass = None
        self.composition = None
    # ----
    
    
    def isModified(self, position=None, strict=False):
        """Check if selected amino or whole sequence has any modification."""
        
        # check specified position only
        if position != None:
            for mod in self.modifications:
                if (strict or mod[2]=='f') and (mod[1] == position or mod[1] == self.chain[position]):
                    return True
        
        # check whole sequence
        else:
            for mod in self.modifications:
                if strict or mod[2]=='f':
                    return True
        
        # not modified
        return False
    # ----
    
    
    def _formatModifications(self):
        """Format modifications."""
        
        # get modifications
        modifs = {}
        for mod in self.modifications:
            
            # count modification
            if mod[1] == '' or type(mod[1]) == int:
                count = 1
            elif type(mod[1]) in (str, unicode):
                count = self.chain.count(mod[1])
            
            # add modification to dic
            if count and mod[0] in modifs:
                modifs[mod[0]] += count
            elif count:
                modifs[mod[0]] = count
        
        # format modifications
        if modifs:
            mods = ''
            for mod in sorted(modifs.keys()):
                mods += '%sx%s; ' % (modifs[mod], mod)
            return '%s' % mods[:-2]
        else:
            return ''
    # ----
    


class peak:
    """Peak object definition"""
    
    def __init__(self, mz, intensity=0., baseline=0., sn=None, charge=None, isotope=None):
        self.mz = float(mz)
        self.intensity = float(intensity)
        self.baseline = float(baseline)
        self.sn = sn
        self.charge = charge
        self.isotope = isotope
        self.relIntensity = 1.
    # ----
    
    


class peaklist:
    """Peaklist object definition."""
    
    def __init__(self, peaks=[]):
        
        self._basePeak = None
        
        # check data
        self.peaks = []
        for item in peaks:
            self._check(item)
            self.peaks.append(item)
        
        # add data
        self._sort()
        self._setBasePeak()
        self.refresh()
    # ----
    
    
    def __len__(self):
        return len(self.peaks)
    # ----
    
    
    def __setitem__(self, i, item):
        
        # check item
        self._check(item)
        
        # check relint and add
        if self.peaks[i] is self._basePeak:
            self.peaks[i] = item
            self._sort()
            self._setBasePeak()
            self.refresh()
        elif item.intensity - item.baseline > self._basePeak.intensity - self._basePeak.baseline:
            self.peaks[i] = item
            self._sort()
            self._basePeak = item
            self.refresh()
        else:
            item.relIntensity = (item.intensity - item.baseline)/(self._basePeak.intensity - self._basePeak.baseline)
            self.peaks[i] = item
            self._sort()
    # ----
    
    
    def __getitem__(self, i):
        return self.peaks[i]
    # ----
    
    
    def __delitem__(self, i):
        
        # recalculate relative intensity
        if self.peaks[i] is self._basePeak:
            del self.peaks[i]
            self._setBasePeak()
            self.refresh()
        else:
            del self.peaks[i]
    # ----
    
    
    def __iter__(self):
        self._index = 0
        return self
    # ----
    
    
    def next(self):
        if self._index < len(self.peaks):
            self._index += 1
            return self.peaks[self._index-1]
        else:
            raise StopIteration
    # ----
    
    
    def append(self, item):
        
        # check peak
        self._check(item)
        
        # add peak and sort peaklist
        if self.peaks and self.peaks[-1].mz > item.mz:
            self.peaks.append(item)
            self._sort()
        else:
            self.peaks.append(item)
        
        # recalc relative intensity
        if not self._basePeak:
            self._setBasePeak()
        if item.intensity - item.baseline > self._basePeak.intensity - self._basePeak.baseline:
            self._basePeak = item
            self.refresh()
        else:
            item.relIntensity = (item.intensity - item.baseline)/(self._basePeak.intensity - self._basePeak.baseline)
    # ----
    
    
    def _check(self, item):
        """Check each item to be a peak"""
        
        if not isinstance(item, peak):
            raise TypeError, 'Item must be a peak object!'
    # ----
    
    
    def _sort(self):
        """Sort data according to mass."""
        
        buff = []
        for item in self.peaks:
            buff.append((item.mz, item))
        buff.sort()
        
        self.peaks = []
        for item in buff:
            self.peaks.append(item[1])
    # ----
    
    
    def _setBasePeak(self):
        """Get most intensive peak."""
        
        if not self.peaks:
            self._basePeak = None
            return
        
        self._basePeak = self.peaks[0]
        maxInt = self._basePeak.intensity - self._basePeak.baseline
        
        for item in self.peaks[1:]:
            intensity = item.intensity-item.baseline
            if intensity > maxInt:
                self._basePeak = item
                maxInt = intensity
    # ----
    
    
    def getBasePeak(self):
        """Get most intens peak."""
        return self._basePeak
    # ---
    
    
    def refresh(self):
        """Recalculate relative intensity."""
        
        if not self._basePeak:
            self._setBasePeak()
            if not self._basePeak:
                return
        
        maxInt = self._basePeak.intensity - self._basePeak.baseline
        for item in self.peaks:
            if maxInt:
                item.relIntensity = (item.intensity - item.baseline)/maxInt
            else:
                item.relIntensity = 1.
    # ----
    
    
    def delete(self, indexes=None):
        """Delete peaks by indexes."""
        
        # delete all
        if indexes==None:
            self.empty()
        
        # delete by indexes
        else:
            indexes.sort()
            indexes.reverse()
            relint = False
            for i in indexes:
                if self.peaks[i] is self._basePeak:
                    relint = True
                del self.peaks[i]
            if relint:
                self._setBasePeak()
                self.refresh()
    # ----
    
    
    def empty(self):
        """Delete all peaks."""
        
        # delete all
        del self.peaks[:]
        self._basePeak = None
    # ----
    


class scan:
    """Scan object definition."""
    
    def __init__(self, points=[], peaks=[]):
        
        self.scanNumber = None
        self.parentScanNumber = None
        self.polarity = None
        self.msLevel = None
        self.retentionTime = None
        self.totIonCurrent = None
        self.basePeakMZ = None
        self.basePeakIntensity = None
        self.precursorMZ = None
        self.precursorIntensity = None
        
        # convert points to numPy array
        self.points = numpy.array(points)
        
        # convert peaks to peaklist
        if isinstance(peaks, peaklist):
            self.peaklist = peaks
        else:
            self.peaklist = peaklist(peaks)
    # ----
    
    
    def __len__(self):
        return len(self.points)
    # ----
    
    
    def getPointsRange(self, minX, maxX):
        """Get X range of points."""
        
        # crop points
        i1 = _getIndex(self.points, minX)
        i2 = _getIndex(self.points, maxX)
        return self.points[i1:i2]
    # ----
    
    
    def getIntensity(self, mz):
        """Get interpolated intensity for given m/z."""
        
        # check data
        if len(self.points) == 0:
            return None
        
        # get mass index
        index = _getIndex(self.points, mz)
        if not index or index == len(self.points):
            return None
        
        # interpolate between two points
        x1, y1 = self.points[index-1]
        x2, y2 = self.points[index]
        intensity = y1 + ((mz - x1) * (y2 - y1)/(x2 - x1))
        
        return intensity
    # ----
    
    
    def getNoise(self, minX=None, maxX=None, mz=None, deviation=0.1):
        """Get baseline for selection or mz."""
        
        # check data
        if len(self.points) == 0:
            return None, None
        
        return peakpicking.getNoise(self.points, minX=minX, maxX=maxX, mz=mz, deviation=deviation)
    # ----
    
    
    def crop(self, minX, maxX):
        """Crop data points and peaklist."""
        
        # crop spectrum data
        i1 = _getIndex(self.points, minX)
        i2 = _getIndex(self.points, maxX)
        self.points = self.points[i1:i2]
        
        # crop peaklist data
        indexes = []
        for x, peak in enumerate(self.peaklist):
            if peak.mz < minX or peak.mz > maxX:
                indexes.append(x)
        self.peaklist.delete(indexes)
    # ----
    
    
    def calibrate(self, fce, params):
        """Re-calibrate data points and peaklist."""
        
        # calibrate spectrum data
        for x, point in enumerate(self.points):
            self.points[x][0] = fce(params, point[0])
        
        # calibrate peaklist data
        for x, peak in enumerate(self.peaklist):
            self.peaklist[x].mz = fce(params, peak.mz)
    # ----
    
    
    def normalize(self):
        """Normalize scan data."""
        
        # get spectrum maximum
        spectrumMax = 0
        if len(self.points) > 0:
            maxXY = numpy.maximum.reduce(self.points)
            spectrumMax = maxXY[1]
        
        # get peaklist maximum
        peaklistMax = 0
        if len(self.peaklist) > 0:
            basePeak = self.peaklist.getBasePeak()
            peaklistMax = basePeak.intensity
        
        f = max(spectrumMax, peaklistMax)/100
        
        # normalize spectrum points
        if len(self.points) > 0:
            self.points = self.points / numpy.array((1, f))
        
        # normalize peaklist
        for peak in self.peaklist:
            peak.intensity /= f
            peak.baseline /= f
        self.peaklist.refresh()
    # ----
    



# HELPER FUNCTIONS
# ----------------

def _unfoldBrackets(string):
    """Unfold formula and count each atom."""
    
    unfoldedFormula = ''
    brackets = [0,0]
    enclosedFormula = ''
    
    i = 0
    while i < len(string):
        
        # handle brackets
        if string[i] == '(':
            brackets[0] += 1
        elif string[i] == ')':
            brackets[1] += 1
        
        # part outside brackets
        if brackets == [0,0]:
            unfoldedFormula += string[i]
        
        # part within brackets
        else:
            enclosedFormula += string[i]
            
            # unfold part within brackets
            if brackets[0] == brackets[1]:
                enclosedFormula = _unfoldBrackets(enclosedFormula[1:-1])
                
                # multiply part within brackets
                count = ''
                while len(string)>(i+1) and string[i+1].isdigit():
                    count += string[i+1]
                    i += 1
                if count:
                    enclosedFormula = enclosedFormula * int(count)
                
                # add and clear
                unfoldedFormula += enclosedFormula
                enclosedFormula = ''
                brackets = [0,0]
        
        i += 1
    return unfoldedFormula
# ----
    


def _getIndex(points, x):
    """Get nearest higher index for selected point."""
    
    lo = 0
    hi = len(points)
    while lo < hi:
        mid = (lo + hi) / 2
        if x < points[mid][0]:
            hi = mid
        else:
            lo = mid + 1
        
    return lo
# ----


        