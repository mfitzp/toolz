# -*- coding: utf-8 -*-
# elements.py

# Copyright (c) 2006-2007, Christoph Gohlke
# Copyright (c) 2006-2007, The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the copyright holders nor the names of any
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Properties of the Chemical Elements.

Author:
    Christoph Gohlke, http://www.lfd.uci.edu/~gohlke/
    Laboratory for Fluorescence Dynamics, University of California, Irvine

References:
    http://physics.nist.gov/PhysRefData/Compositions/
    http://physics.nist.gov/PhysRefData/IonEnergy/tblNew.html
    http://en.wikipedia.org/wiki/%(element.name)s

"""

class Element(object):
    """Chemical Element.

    Class attributes:
    number -- atomic number
    symbol -- element symbol
    name -- element name in english
    group -- group in the periodic table
    period -- period in the periodic table
    block -- block in the periodic table
    protons -- number of protons
    neutron -- number of neutrons in the most abundant isotope
    electrons -- number of electrons
    mass -- relative atomic mass
    en -- electronegativity (Pauling scale)
    covrad -- Covalent radius (in A)
    atmrad -- Atomic radius (in A)
    vdwrad -- Van der Waals radius (in A)
    tboil -- boiling temperature (in K)
    tmelt -- melting temperature (in K)
    density -- density at 295K (g/cm^3 respectively g/L)
    phase -- 'solid/liquid' or 'gas' at 295K
    acidity -- acidic behaviour
    oxistates -- oxidation states
    eleaffin -- electron affinity (in eV)
    eleshells -- number of electrons per shell
    eleconfig -- ground state electron configuration
    ionenergy -- list of ionization energies (in eV)
    isotopes -- list of isotopes (mass number, rel. atomic mass, fraction)
    maxiso -- index of the most abundant isotope
    puremass -- rel. atomic mass of the most abundant isotope
    purefrac -- fraction of the most abundant isotope

    """

    def __init__(self, number, symbol, name, **kwargs):
        self.number = number
        self.symbol = symbol
        self.name = name

        self.__dict__.update(kwargs)

        elements.add(self)
        groups.add(self)
        periods.add(self)
        blocks.add(self)

        # properties the most abundant isotope
        mass = frac = 0.0; maxf = 0
        for i, (n, m, f) in enumerate(self.isotopes):
            mass += m*f
            frac += f
            if f > maxf:
                maxf = f
                self.isomax = i
                self.puremass = m
                self.purefrac = f
                self.neutrons = n - number

        self.protons = number
        self.electrons = number
        self.massnumber = self.protons+self.neutrons

        assert(abs(frac-1.0) < 1e-9,
            "%s - Isotope fractions must add up to 1.0" % self.symbol)
        assert(abs(mass-self.mass) < 0.03,
            "%s - Mean of isotope masses must equal mass" % self.symbol)
        assert(self.number == self.protons,
            "%s - Atomic number must equal number of protons" % self.symbol)
        assert(self.protons == sum(self.eleshells),
            "%s - Number of protons must equal electrons" % self.symbol)

    def __str__(self):
        return self.symbol

    def add(self, **kwargs):
        """Add any properties."""
        self.__dict__.update(kwargs)

    def export(self, format='text'):
        """Return element properties in specifed format."""
        if format=='xml':
            raise NotImplementedError()
        elif format=='list':
            result = [self.symbol, self.name]
        elif format=='python':
            result = """%(symbol)s = Element(""" \
    """%(number)s, '%(symbol)s', '%(name)s',
    group=%(group)s, period=%(period)s, block='%(block)s',
    mass=%(mass)s, en=%(en)s,
    covrad=%(covrad).3f, atmrad=%(atmrad).3f, vdwrad=%(vdwrad).3f,
    tboil=%(tboil).3f, tmelt=%(tmelt).3f, density=%(density).4f,
    phase='%(phase)s', acidity='%(acidity)s',
    eleaffin=%(eleaffin).8f,
    eleshells=%(eleshells)s,
    eleconfig='%(eleconfig)s',
    oxistates='%(oxistates)s',
    ionenergy=(%%s),
    isotopes=(%%s),)\n""" % self.__dict__
            ion = []
            for i,j in enumerate(self.ionenergy):
                if i and (i%4==0):
                    ion.append("\n"+" "*15)
                ion.append(" %9.4f," % j)
            iso = []
            for i in self.isotopes:
                iso.append("(%-3i, %14.10f, %10.8f)," % (i[0], i[1], i[2]))
            result = result % ("".join(ion),"\n              ".join(iso))
        else:
            result = '\n'.join([
            "%-22s : %s"    % ("Name", self.name),
            "%-22s : %s"    % ("Symbol", self.symbol),
            "%-22s : %i"    % ("Atomic Number", self.number),
            "%-22s : %i"    % ("Group", self.group),
            "%-22s : %i"    % ("Period", self.period),
            "%-22s : %s"    % ("Block", self.block),
            "%-22s : %.10g" % ("Atomic Weight", self.mass),
            "%-22s : %.10g" % ("Atomic Radius", self.atmrad),
            "%-22s : %.10g" % ("Covalent Radius", self.covrad),
            "%-22s : %.10g" % ("Van der Waals Radius", self.vdwrad),
            "%-22s : %.10g" % ("Electronegativity", self.en),
            "%-22s : %s"    % ("Electron Configuration", self.eleconfig),
            "%-22s : %s"    % ("Electron per Shell", ', '.join(
                "%i" % i for i in self.eleshells)),
            "%-22s : %s"    % ("Oxidation States", self.oxistates),
            "%-22s : %s"    % ("Isotopes", ', '.join(
                "(%i, %.10g, %.10g)" % (a,b,c*100.0) for a,b,c in \
                                                            self.isotopes)),
            "%-22s : %s"   % ("Ionization Potentials", ', '.join(
                "%.10g" % ion for ion in self.ionenergy)),
            ""])
        return result


class _Elements(object):
    """List of Chemical Elements."""

    def __init__(self):
        self.__list = []
        self.__dict = {}

    def add(self, element):
        """Add element."""
        self.__list.append(element)
        self.__dict[element.number] = element
        self.__dict[element.symbol] = element
        self.__dict[element.name] = element

    def __str__(self):
        return "[%s]" % ", ".join(e.symbol for e in self.__list)

    def __contains__(self, item):
        return self.__dict.__contains__(item)

    def __iter__(self):
        return iter(self.__list)

    def __len__(self):
        return len(self.__list)

    def __getitem__(self, key):
        return self.__dict[key]


class _Blocks(object):
    """List of Blocks of Chemical Elements."""

    def __init__(self):
        self.__dict = {'s': [], 'p': [], 'd': [], 'f': []}

    def add(self, element):
        """Add element."""
        self.__dict[element.block].append(element)

    def __str__(self):
        l = []
        for i in 'spdf':
            b = self.__dict[i]
            l.append("%2s [%s]" % (i, ", ".join(e.symbol for e in b)))
        return "\n".join(l)

    def __iter__(self):
        return iter(self.__dict[i] for i in 'spdf')

    def __getitem__(self, key):
        return self.__dict[key]


class _Periods(object):
    """List of Periods of Chemical Elements."""

    def __init__(self):
        self.__list = [[] for i in range(8)]

    def add(self, element):
        """Add element."""
        self.__list[element.period].append(element)

    def __str__(self):
        l = []
        for i, g in enumerate(self.__list[1:]):
            l.append("%2i [%s]" % (i+1, ", ".join(e.symbol for e in g)))
        return "\n".join(l)

    def __iter__(self):
        return iter(self.__list[1:])

    def __getitem__(self, key):
        return self.__list[key]


class _Group(list):
    """Group of Chemical Elements."""

    def __init__(self, old, description):
        self. description = description
        self.oldname = old
        list.__init__(self)


class _Groups(object):
    """List of Groups of Chemical Elements."""

    __list = [[],
        _Group('IA',    'Alkali metals'),
        _Group('IIA',   'Alkaline earths'),
        _Group('IIIB',  ''),
        _Group('IVB',   ''),
        _Group('VB',    ''),
        _Group('VIB',   ''),
        _Group('VIIB',  ''),
        _Group('VIIIB', ''),
        _Group('VIIIB', ''),
        _Group('VIIIB', ''),
        _Group('IB',    'Coinage Metals'),
        _Group('IIB',   ''),
        _Group('IIIA',  'Boron Group'),
        _Group('IVA',   'Carbon Group'),
        _Group('VA',    'Pnictogens'),
        _Group('VIA',   'Chalcogens'),
        _Group('VIIA',  'Halogens'),
        _Group('VIIIA', 'Noble gases')]

    def add(self, element):
        """Add element."""
        self.__list[element.group].append(element)

    def __str__(self):
        l = []
        for i, g in enumerate(self.__list[1:]):
            l.append("%2i [%s]" % (i+1, ", ".join(e.symbol for e in g)))
        return "\n".join(l)

    def __iter__(self):
        return iter(self.__list[1:])

    def __getitem__(self, key):
        return self.__list[key]


elements = _Elements()
groups = _Groups()
periods = _Periods()
blocks = _Blocks()

elemDict = {}

elemDict['H']= Element(1, 'H', 'Hydrogen',
    group=1, period=1, block='s',
    mass=1.00794, en=2.2,
    covrad=0.320, atmrad=0.790, vdwrad=1.200,
    tboil=20.280, tmelt=13.810, density=0.0840,
    phase='gas', acidity='basic',
    eleaffin=0.75420375,
    eleshells=(1,),
    eleconfig='1s',
    oxistates='1*, -1',
    ionenergy=(   13.5984,),
    isotopes=((1  ,   1.0078250321, 0.99988500),
              (2  ,   2.0141017780, 0.00011500),),)

elemDict['He']= Element(2, 'He', 'Helium',
    group=18, period=1, block='s',
    mass=4.002602, en=0.0,
    covrad=0.930, atmrad=0.490, vdwrad=1.400,
    tboil=4.216, tmelt=0.950, density=0.1785,
    phase='gas', acidity='basic',
    eleaffin=0.00000000,
    eleshells=(2,),
    eleconfig='1s^2',
    oxistates='*',
    ionenergy=(   24.5874,   54.4160,),
    isotopes=((3  ,   3.0160293097, 0.00000137),
              (4  ,   4.0026032497, 0.99999863),),)

elemDict['Li']= Element(3, 'Li', 'Lithium',
    group=1, period=2, block='s',
    mass=6.941, en=0.98,
    covrad=1.230, atmrad=2.050, vdwrad=1.820,
    tboil=1615.000, tmelt=453.700, density=0.5300,
    phase='solid', acidity='acidic',
    eleaffin=0.61804900,
    eleshells=(2, 1),
    eleconfig='[He] 2s',
    oxistates='1*',
    ionenergy=(    5.3917,   75.6380,  122.4510,),
    isotopes=((6  ,   6.0151223000, 0.07590000),
              (7  ,   7.0160040000, 0.92410000),),)

elemDict['Be']= Element(4, 'Be', 'Beryllium',
    group=2, period=2, block='s',
    mass=9.012182, en=1.57,
    covrad=0.900, atmrad=1.400, vdwrad=0.000,
    tboil=3243.000, tmelt=1560.000, density=1.8500,
    phase='solid', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 2),
    eleconfig='[He] 2s^2',
    oxistates='2*',
    ionenergy=(    9.3227,   18.2110,  153.8930,  217.7130,),
    isotopes=((9  ,   9.0121821000, 1.00000000),),)

elemDict['B'] = Element(5, 'B', 'Boron',
    group=13, period=2, block='p',
    mass=10.811, en=2.04,
    covrad=0.820, atmrad=1.170, vdwrad=0.000,
    tboil=4275.000, tmelt=2365.000, density=2.4600,
    phase='solid', acidity='amphoteric',
    eleaffin=0.27972300,
    eleshells=(2, 3),
    eleconfig='[He] 2s^2 2p',
    oxistates='3*',
    ionenergy=(    8.2980,   25.1540,   37.9300,   59.3680,
                 340.2170,),
    isotopes=((10 ,  10.0129370000, 0.19900000),
              (11 ,  11.0093055000, 0.80100000),),)

elemDict['C']= Element(6, 'C', 'Carbon',
    group=14, period=2, block='p',
    mass=12.0107, en=2.55,
    covrad=0.770, atmrad=0.910, vdwrad=1.700,
    tboil=5100.000, tmelt=3825.000, density=3.5100,
    phase='solid', acidity='amphoteric',
    eleaffin=1.26211800,
    eleshells=(2, 4),
    eleconfig='[He] 2s^2 2p^2',
    oxistates='4*, 2, -4*',
    ionenergy=(   11.2603,   24.3830,   47.8770,   64.4920,
                 392.0770,  489.9810,),
    isotopes=((12 ,  12.0000000000, 0.98930000),
              (13 ,  13.0033548378, 0.01070000),),)

elemDict['N']= Element(7, 'N', 'Nitrogen',
    group=15, period=2, block='p',
    mass=14.0067, en=3.04,
    covrad=0.750, atmrad=0.750, vdwrad=1.550,
    tboil=77.344, tmelt=63.150, density=1.1700,
    phase='gas', acidity='amphoteric',
    eleaffin=-0.07000000,
    eleshells=(2, 5),
    eleconfig='[He] 2s^2 2p^3',
    oxistates='5, 4, 3, 2, -3*',
    ionenergy=(   14.5341,   39.6010,   47.4880,   77.4720,
                  97.8880,  522.0570,  667.0290,),
    isotopes=((14 ,  14.0030740052, 0.99632000),
              (15 ,  15.0001088984, 0.00368000),),)

elemDict['O']= Element(8, 'O', 'Oxygen',
    group=16, period=2, block='p',
    mass=15.9994, en=3.44,
    covrad=0.730, atmrad=0.650, vdwrad=1.520,
    tboil=90.188, tmelt=54.800, density=1.3300,
    phase='gas', acidity='amphoteric',
    eleaffin=1.46111200,
    eleshells=(2, 6),
    eleconfig='[He] 2s^2 2p^4',
    oxistates='-2*, -1',
    ionenergy=(   13.6181,   35.1160,   54.9340,   54.9340,
                  77.4120,  113.8960,  138.1160,  739.3150,
                 871.3870,),
    isotopes=((16 ,  15.9949146221, 0.99757000),
              (17 ,  16.9991315000, 0.00038000),
              (18 ,  17.9991604000, 0.00205000),),)

elemDict['F'] = Element(9, 'F', 'Fluorine',
    group=17, period=2, block='p',
    mass=18.9984032, en=3.98,
    covrad=0.720, atmrad=0.570, vdwrad=1.470,
    tboil=85.000, tmelt=53.550, density=1.5800,
    phase='gas', acidity='amphoteric',
    eleaffin=3.40118870,
    eleshells=(2, 7),
    eleconfig='[He] 2s^2 2p^5',
    oxistates='-1*',
    ionenergy=(   17.4228,   34.9700,   62.7070,   87.1380,
                 114.2400,  157.1610,  185.1820,  953.8860,
                1103.0890,),
    isotopes=((19 ,  18.9984032000, 1.00000000),),)

elemDict['Ne']= Element(10, 'Ne', 'Neon',
    group=18, period=2, block='p',
    mass=20.1797, en=0.0,
    covrad=0.710, atmrad=0.510, vdwrad=1.540,
    tboil=27.100, tmelt=24.550, density=0.8999,
    phase='gas', acidity='basic',
    eleaffin=0.00000000,
    eleshells=(2, 8),
    eleconfig='[He] 2s^2 2p^6',
    oxistates='*',
    ionenergy=(   21.5645,   40.9620,   63.4500,   97.1100,
                 126.2100,  157.9300,  207.2700,  239.0900,
                1195.7970, 1362.1640,),
    isotopes=((20 ,  19.9924401759, 0.90480000),
              (21 ,  20.9938467400, 0.00270000),
              (22 ,  21.9913855100, 0.09250000),),)

elemDict['Na']= Element(11, 'Na', 'Sodium',
    group=1, period=3, block='s',
    mass=22.98977, en=0.93,
    covrad=1.540, atmrad=2.230, vdwrad=2.270,
    tboil=1156.000, tmelt=371.000, density=0.9700,
    phase='solid', acidity='acidic',
    eleaffin=0.54792600,
    eleshells=(2, 8, 1),
    eleconfig='[Ne] 3s',
    oxistates='1*',
    ionenergy=(    5.1391,   47.2860,   71.6400,   98.9100,
                 138.3900,  172.1500,  208.4700,  264.1800,
                 299.8700, 1465.0910, 1648.6590,),
    isotopes=((23 ,  22.9897696700, 1.00000000),),)

elemDict['Mg']= Element(12, 'Mg', 'Magnesium',
    group=2, period=3, block='s',
    mass=24.305, en=1.31,
    covrad=1.360, atmrad=1.720, vdwrad=1.730,
    tboil=1380.000, tmelt=922.000, density=1.7400,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 2),
    eleconfig='[Ne] 3s^2',
    oxistates='2*',
    ionenergy=(    7.6462,   15.0350,   80.1430,  109.2400,
                 141.2600,  186.5000,  224.9400,  265.9000,
                 327.9500,  367.5300, 1761.8020, 1962.6130,),
    isotopes=((24 ,  23.9850419000, 0.78990000),
              (25 ,  24.9858370200, 0.10000000),
              (26 ,  25.9825930400, 0.11010000),),)

elemDict['Al']= Element(13, 'Al', 'Aluminium',
    group=13, period=3, block='p',
    mass=26.981538, en=1.61,
    covrad=1.180, atmrad=1.820, vdwrad=0.000,
    tboil=2740.000, tmelt=933.500, density=2.7000,
    phase='solid', acidity='neutral',
    eleaffin=0.43283000,
    eleshells=(2, 8, 3),
    eleconfig='[Ne] 3s^2 3p',
    oxistates='3*',
    ionenergy=(    5.9858,   18.8280,   28.4470,  119.9900,
                 153.7100,  190.4700,  241.4300,  284.5900,
                 330.2100,  398.5700,  442.0700, 2085.9830,
                2304.0800,),
    isotopes=((27 ,  26.9815384400, 1.00000000),),)

elemDict['Si']= Element(14, 'Si', 'Silicon',
    group=14, period=3, block='p',
    mass=28.0855, en=1.9,
    covrad=1.110, atmrad=1.460, vdwrad=2.100,
    tboil=2630.000, tmelt=1683.000, density=2.3300,
    phase='solid', acidity='amphoteric',
    eleaffin=1.38952100,
    eleshells=(2, 8, 4),
    eleconfig='[Ne] 3s^2 3p^2',
    oxistates='4*, -4',
    ionenergy=(    8.1517,   16.3450,   33.4920,   45.1410,
                 166.7700,  205.0500,  246.5200,  303.1700,
                 351.1000,  401.4300,  476.0600,  523.5000,
                2437.6760, 2673.1080,),
    isotopes=((28 ,  27.9769265327, 0.92229700),
              (29 ,  28.9764947200, 0.04683200),
              (30 ,  29.9737702200, 0.03087100),),)

elemDict['P']= Element(15, 'P', 'Phosphorus',
    group=15, period=3, block='p',
    mass=30.973761, en=2.19,
    covrad=1.060, atmrad=1.230, vdwrad=1.800,
    tboil=553.000, tmelt=317.300, density=1.8200,
    phase='solid', acidity='amphoteric',
    eleaffin=0.74650000,
    eleshells=(2, 8, 5),
    eleconfig='[Ne] 3s^2 3p^3',
    oxistates='5*, 3, -3',
    ionenergy=(   10.4867,   19.7250,   30.1800,   51.3700,
                  65.0230,  220.4300,  263.2200,  309.4100,
                 371.7300,  424.5000,  479.5700,  560.4100,
                 611.8500, 2816.9430, 3069.7620,),
    isotopes=((31 ,  30.9737615100, 1.00000000),),)

elemDict['S']= Element(16, 'S', 'Sulfur',
    group=16, period=3, block='p',
    mass=32.065, en=2.58,
    covrad=1.020, atmrad=1.090, vdwrad=1.800,
    tboil=717.820, tmelt=392.200, density=2.0600,
    phase='solid', acidity='amphoteric',
    eleaffin=2.07710290,
    eleshells=(2, 8, 6),
    eleconfig='[Ne] 3s^2 3p^4',
    oxistates='6*, 4, 2, -2',
    ionenergy=(   10.3600,   23.3300,   34.8300,   47.3000,
                  72.6800,   88.0490,  280.9300,  328.2300,
                 379.1000,  447.0900,  504.7800,  564.6500,
                 651.6300,  707.1400, 3223.8360, 3494.0990,),
    isotopes=((32 ,  31.9720706900, 0.94930000),
              (33 ,  32.9714585000, 0.00760000),
              (34 ,  33.9678668300, 0.04290000),
              (36 ,  35.9670808800, 0.00020000),),)

elemDict['Cl']= Element(17, 'Cl', 'Chlorine',
    group=17, period=3, block='p',
    mass=35.453, en=3.16,
    covrad=0.990, atmrad=0.970, vdwrad=1.750,
    tboil=239.180, tmelt=172.170, density=2.9500,
    phase='gas', acidity='amphoteric',
    eleaffin=3.61272400,
    eleshells=(2, 8, 7),
    eleconfig='[Ne] 3s^2 3p^5',
    oxistates='7, 5, 3, 1, -1*',
    ionenergy=(   12.9676,   23.8100,   39.6100,   53.4600,
                  67.8000,   98.0300,  114.1930,  348.2800,
                 400.0500,  455.6200,  529.9700,  591.9700,
                 656.6900,  749.7500,  809.3900, 3658.4250,
                3946.1930,),
    isotopes=((35 ,  34.9688527100, 0.75780000),
              (37 ,  36.9659026000, 0.24220000),),)

elemDict['Ar']= Element(18, 'Ar', 'Argon',
    group=18, period=3, block='p',
    mass=39.948, en=0.0,
    covrad=0.980, atmrad=0.880, vdwrad=1.880,
    tboil=87.450, tmelt=83.950, density=1.6600,
    phase='gas', acidity='basic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 8),
    eleconfig='[Ne] 3s^2 3p^6',
    oxistates='*',
    ionenergy=(   15.7596,   27.6290,   40.7400,   59.8100,
                  75.0200,   91.0070,  124.3190,  143.4560,
                 422.4400,  478.6800,  538.9500,  618.2400,
                 686.0900,  755.7300,  854.7500,  918.0000,
                4120.7780, 4426.1140,),
    isotopes=((36 ,  35.9675462800, 0.00336500),
              (38 ,  37.9627322000, 0.00063200),
              (40 ,  39.9623831230, 0.99600300),),)

elemDict['K']= Element(19, 'K', 'Potassium',
    group=1, period=4, block='s',
    mass=39.0983, en=0.82,
    covrad=2.030, atmrad=2.770, vdwrad=2.750,
    tboil=1033.000, tmelt=336.800, density=0.8600,
    phase='solid', acidity='acidic',
    eleaffin=0.50145900,
    eleshells=(2, 8, 8, 1),
    eleconfig='[Ar] 4s',
    oxistates='1*',
    ionenergy=(    4.3407,   31.6250,   45.7200,   60.9100,
                  82.6600,  100.0000,  117.5600,  154.8600,
                 175.8140,  503.4400,  564.1300,  629.0900,
                 714.0200,  787.1300,  861.7700,  968.0000,
                1034.0000, 4610.9550, 4933.9310,),
    isotopes=((39 ,  38.9637069000, 0.93258100),
              (40 ,  39.9639986700, 0.00011700),
              (41 ,  40.9618259700, 0.06730200),),)

elemDict['Ca']= Element(20, 'Ca', 'Calcium',
    group=2, period=4, block='s',
    mass=40.078, en=1.0,
    covrad=1.740, atmrad=2.230, vdwrad=0.000,
    tboil=1757.000, tmelt=1112.000, density=1.5400,
    phase='solid', acidity='acidic',
    eleaffin=0.02455000,
    eleshells=(2, 8, 8, 2),
    eleconfig='[Ar] 4s^2',
    oxistates='2*',
    ionenergy=(    6.1132,   11.7100,   50.9080,   67.1000,
                  84.4100,  108.7800,  127.7000,  147.2400,
                 188.5400,  211.2700,  591.2500,  656.3900,
                 726.0300,  816.6100,  895.1200,  974.0000,
                1087.0000, 1157.0000, 5129.0450, 5469.7380,),
    isotopes=((40 ,  39.9625912000, 0.96941000),
              (42 ,  41.9586183000, 0.00647000),
              (43 ,  42.9587668000, 0.00135000),
              (44 ,  43.9554811000, 0.02086000),
              (46 ,  45.9536928000, 0.00004000),
              (48 ,  47.9525340000, 0.00187000),),)

elemDict['Sc']= Element(21, 'Sc', 'Scandium',
    group=3, period=4, block='d',
    mass=44.95591, en=1.36,
    covrad=1.440, atmrad=2.090, vdwrad=0.000,
    tboil=3109.000, tmelt=1814.000, density=2.9900,
    phase='solid', acidity='acidic',
    eleaffin=0.18800000,
    eleshells=(2, 8, 9, 2),
    eleconfig='[Ar] 3d 4s^2',
    oxistates='3*',
    ionenergy=(    6.5615,   12.8000,   24.7600,   73.4700,
                  91.6600,   11.1000,  138.0000,  158.7000,
                 180.0200,  225.3200,  225.3200,  685.8900,
                 755.4700,  829.7900,  926.0000,),
    isotopes=((45 ,  44.9559102000, 1.00000000),),)

elemDict['Ti']= Element(22, 'Ti', 'Titanium',
    group=4, period=4, block='d',
    mass=47.867, en=1.54,
    covrad=1.320, atmrad=2.000, vdwrad=0.000,
    tboil=3560.000, tmelt=1935.000, density=4.5100,
    phase='solid', acidity='neutral',
    eleaffin=0.08400000,
    eleshells=(2, 8, 10, 2),
    eleconfig='[Ar] 3d^2 4s^2',
    oxistates='4*, 3',
    ionenergy=(    6.8281,   13.5800,   27.4910,   43.2660,
                  99.2200,  119.3600,  140.8000,  168.5000,
                 193.5000,  193.2000,  215.9100,  265.2300,
                 291.4970,  787.3300,  861.3300,),
    isotopes=((46 ,  45.9526295000, 0.08250000),
              (47 ,  46.9517638000, 0.07440000),
              (48 ,  47.9479471000, 0.73720000),
              (49 ,  48.9478708000, 0.05410000),
              (50 ,  49.9447921000, 0.05180000),),)

elemDict['V']= Element(23, 'V', 'Vanadium',
    group=5, period=4, block='d',
    mass=50.9415, en=1.63,
    covrad=1.220, atmrad=1.920, vdwrad=0.000,
    tboil=3650.000, tmelt=2163.000, density=6.0900,
    phase='solid', acidity='neutral',
    eleaffin=0.52500000,
    eleshells=(2, 8, 11, 2),
    eleconfig='[Ar] 3d^3 4s^2',
    oxistates='5*, 4, 3, 2, 0',
    ionenergy=(    6.7462,   14.6500,   29.3100,   46.7070,
                  65.2300,  128.1200,  150.1700,  173.7000,
                 205.8000,  230.5000,  255.0400,  308.2500,
                 336.2670,  895.5800,  974.0200,),
    isotopes=((50 ,  49.9471628000, 0.00250000),
              (51 ,  50.9439637000, 0.99750000),),)

elemDict['Cr']= Element(24, 'Cr', 'Chromium',
    group=6, period=4, block='d',
    mass=51.9961, en=1.66,
    covrad=1.180, atmrad=1.850, vdwrad=0.000,
    tboil=2945.000, tmelt=2130.000, density=7.1400,
    phase='solid', acidity='neutral',
    eleaffin=0.67584000,
    eleshells=(2, 8, 13, 1),
    eleconfig='[Ar] 3d^5 4s',
    oxistates='6, 3*, 2, 0',
    ionenergy=(    6.7665,   16.5000,   30.9600,   49.1000,
                  69.3000,   90.5600,  161.1000,  184.7000,
                 209.3000,  244.4000,  270.8000,  298.0000,
                 355.0000,  384.3000, 1010.6400,),
    isotopes=((50 ,  49.9460496000, 0.04345000),
              (52 ,  51.9405119000, 0.83789000),
              (53 ,  52.9406538000, 0.09501000),
              (54 ,  53.9388849000, 0.02365000),),)

elemDict['Mn']= Element(25, 'Mn', 'Manganese',
    group=7, period=4, block='d',
    mass=54.938049, en=1.55,
    covrad=1.170, atmrad=1.790, vdwrad=0.000,
    tboil=2235.000, tmelt=1518.000, density=7.4400,
    phase='solid', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 13, 2),
    eleconfig='[Ar] 3d^5 4s^2',
    oxistates='7, 6, 4, 3, 2*, 0, -1',
    ionenergy=(    7.4340,   15.6400,   33.6670,   51.2000,
                  72.4000,   95.0000,  119.2700,  196.4600,
                 221.8000,  248.3000,  286.0000,  314.4000,
                 343.6000,  404.0000,  435.3000, 1136.2000,),
    isotopes=((55 ,  54.9380496000, 1.00000000),),)

elemDict['Fe']= Element(26, 'Fe', 'Iron',
    group=8, period=4, block='d',
    mass=55.845, en=1.83,
    covrad=1.170, atmrad=1.720, vdwrad=0.000,
    tboil=3023.000, tmelt=1808.000, density=7.8740,
    phase='solid', acidity='neutral',
    eleaffin=0.15100000,
    eleshells=(2, 8, 14, 2),
    eleconfig='[Ar] 3d^6 4s^2',
    oxistates='6, 3*, 2, 0, -2',
    ionenergy=(    7.9024,   16.1800,   30.6510,   54.8000,
                  75.0000,   99.0000,  125.0000,  151.0600,
                 235.0400,  262.1000,  290.4000,  330.8000,
                 361.0000,  392.2000,  457.0000,  485.5000,
                1266.1000,),
    isotopes=((54 ,  53.9396148000, 0.05845000),
              (56 ,  55.9349421000, 0.91754000),
              (57 ,  56.9353987000, 0.02119000),
              (58 ,  57.9332805000, 0.00282000),),)

elemDict['Co']= Element(27, 'Co', 'Cobalt',
    group=9, period=4, block='d',
    mass=58.9332, en=1.88,
    covrad=1.160, atmrad=1.670, vdwrad=0.000,
    tboil=3143.000, tmelt=1768.000, density=8.8900,
    phase='solid', acidity='neutral',
    eleaffin=0.66330000,
    eleshells=(2, 8, 15, 2),
    eleconfig='[Ar] 3d^7 4s^2',
    oxistates='3, 2*, 0, -1',
    ionenergy=(    7.8810,   17.0600,   33.5000,   51.3000,
                  79.5000,  102.0000,  129.0000,  157.0000,
                 186.1300,  276.0000,  305.0000,  336.0000,
                 376.0000,  411.0000,  444.0000,  512.0000,
                 546.8000, 1403.0000,),
    isotopes=((59 ,  58.9332002000, 1.00000000),),)

elemDict['Ni']= Element(28, 'Ni', 'Nickel',
    group=10, period=4, block='d',
    mass=58.6934, en=1.91,
    covrad=1.150, atmrad=1.620, vdwrad=1.630,
    tboil=3005.000, tmelt=1726.000, density=8.9100,
    phase='solid', acidity='acidic',
    eleaffin=1.15716000,
    eleshells=(2, 8, 16, 2),
    eleconfig='[Ar] 3d^8 4s^2',
    oxistates='3, 2*, 0',
    ionenergy=(    7.6398,   18.1680,   35.1700,   54.9000,
                  75.5000,  108.0000,  133.0000,  162.0000,
                 193.0000,  224.5000,  321.2000,  352.0000,
                 384.0000,  430.0000,  464.0000,  499.0000,
                 571.0000,  607.2000, 1547.0000,),
    isotopes=((58 ,  57.9353479000, 0.68076900),
              (60 ,  59.9307906000, 0.26223100),
              (61 ,  60.9310604000, 0.01139900),
              (62 ,  61.9283488000, 0.03634500),
              (64 ,  63.9279696000, 0.00925600),),)

elemDict['Cu']= Element(29, 'Cu', 'Copper',
    group=11, period=4, block='d',
    mass=63.546, en=1.9,
    covrad=1.170, atmrad=1.570, vdwrad=1.400,
    tboil=2840.000, tmelt=1356.600, density=8.9200,
    phase='solid', acidity='acidic',
    eleaffin=1.23578000,
    eleshells=(2, 8, 18, 1),
    eleconfig='[Ar] 3d^10 4s',
    oxistates='2*, 1',
    ionenergy=(    7.7264,   20.2920,   26.8300,   55.2000,
                  79.9000,  103.0000,  139.0000,  166.0000,
                 199.0000,  232.0000,  266.0000,  368.8000,
                 401.0000,  435.0000,  484.0000,  520.0000,
                 557.0000,  633.0000,  671.0000, 1698.0000,),
    isotopes=((63 ,  62.9296011000, 0.69170000),
              (65 ,  64.9277937000, 0.30830000),),)

elemDict['Zn']= Element(30, 'Zn', 'Zinc',
    group=12, period=4, block='d',
    mass=65.409, en=1.65,
    covrad=1.250, atmrad=1.530, vdwrad=1.390,
    tboil=1180.000, tmelt=692.730, density=7.1400,
    phase='solid', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 2),
    eleconfig='[Ar] 3d^10 4s^2',
    oxistates='2*',
    ionenergy=(    9.3942,   17.9640,   39.7220,   59.4000,
                  82.6000,  108.0000,  134.0000,  174.0000,
                 203.0000,  238.0000,  274.0000,  310.8000,
                 419.7000,  454.0000,  490.0000,  542.0000,
                 579.0000,  619.0000,  698.8000,  738.0000,
                1856.0000,),
    isotopes=((64 ,  63.9291466000, 0.48630000),
              (66 ,  65.9260368000, 0.27900000),
              (67 ,  66.9271309000, 0.04100000),
              (68 ,  67.9248476000, 0.18750000),
              (70 ,  69.9253250000, 0.00620000),),)

elemDict['Ga']= Element(31, 'Ga', 'Gallium',
    group=13, period=4, block='p',
    mass=69.723, en=1.81,
    covrad=1.260, atmrad=1.810, vdwrad=1.870,
    tboil=2478.000, tmelt=302.920, density=5.9100,
    phase='solid', acidity='neutral',
    eleaffin=0.41000000,
    eleshells=(2, 8, 18, 3),
    eleconfig='[Ar] 3d^10 4s^2 4p',
    oxistates='3*',
    ionenergy=(    5.9993,   20.5100,   30.7100,   64.0000,),
    isotopes=((69 ,  68.9255810000, 0.60108000),
              (71 ,  70.9247050000, 0.39892000),),)

elemDict['Ge'] = Element(32, 'Ge', 'Germanium',
    group=14, period=4, block='p',
    mass=72.64, en=2.01,
    covrad=1.220, atmrad=1.520, vdwrad=0.000,
    tboil=3107.000, tmelt=1211.500, density=5.3200,
    phase='solid', acidity='neutral',
    eleaffin=1.23271200,
    eleshells=(2, 8, 18, 4),
    eleconfig='[Ar] 3d^10 4s^2 4p^2',
    oxistates='4*',
    ionenergy=(    7.8994,   15.9340,   34.2200,   45.7100,
                  93.5000,),
    isotopes=((70 ,  69.9242504000, 0.20840000),
              (72 ,  71.9220762000, 0.27540000),
              (73 ,  72.9234594000, 0.07730000),
              (74 ,  73.9211782000, 0.36280000),
              (76 ,  75.9214027000, 0.07610000),),)

elemDict['As'] = Element(33, 'As', 'Arsenic',
    group=15, period=4, block='p',
    mass=74.9216, en=2.18,
    covrad=1.200, atmrad=1.330, vdwrad=1.850,
    tboil=876.000, tmelt=1090.000, density=5.7200,
    phase='solid', acidity='neutral',
    eleaffin=0.81400000,
    eleshells=(2, 8, 18, 5),
    eleconfig='[Ar] 3d^10 4s^2 4p^3',
    oxistates='5, 3*, -3',
    ionenergy=(    9.7886,   18.6330,   28.3510,   50.1300,
                  62.6300,  127.6000,),
    isotopes=((75 ,  74.9215964000, 1.00000000),),)

elemDict['Se'] = Element(34, 'Se', 'Selenium',
    group=16, period=4, block='p',
    mass=78.96, en=2.55,
    covrad=1.160, atmrad=1.220, vdwrad=1.900,
    tboil=958.000, tmelt=494.000, density=4.8200,
    phase='solid', acidity='amphoteric',
    eleaffin=2.02067000,
    eleshells=(2, 8, 18, 6),
    eleconfig='[Ar] 3d^10 4s^2 4p^4',
    oxistates='6, 4*, -2',
    ionenergy=(    9.7524,   21.9000,   30.8200,   42.9440,
                  68.3000,   81.7000,  155.4000,),
    isotopes=((74 ,  73.9224766000, 0.00890000),
              (76 ,  75.9192141000, 0.09370000),
              (77 ,  76.9199146000, 0.07630000),
              (78 ,  77.9173095000, 0.23770000),
              (80 ,  79.9165218000, 0.49610000),
              (82 ,  81.9167000000, 0.08730000),),)

elemDict['Br'] = Element(35, 'Br', 'Bromine',
    group=17, period=4, block='p',
    mass=79.904, en=2.96,
    covrad=1.140, atmrad=1.120, vdwrad=1.850,
    tboil=331.850, tmelt=265.950, density=3.1400,
    phase='solid', acidity='amphoteric',
    eleaffin=3.36358800,
    eleshells=(2, 8, 18, 7),
    eleconfig='[Ar] 3d^10 4s^2 4p^5',
    oxistates='7, 5, 3, 1, -1*',
    ionenergy=(   11.8138,   21.8000,   36.0000,   47.3000,
                  59.7000,   88.6000,  103.0000,  192.8000,),
    isotopes=((79 ,  78.9183376000, 0.50690000),
              (81 ,  80.9162910000, 0.49310000),),)

elemDict['Kr'] = Element(36, 'Kr', 'Krypton',
    group=18, period=4, block='p',
    mass=83.798, en=0.0,
    covrad=1.120, atmrad=1.030, vdwrad=2.020,
    tboil=120.850, tmelt=116.000, density=4.4800,
    phase='gas', acidity='basic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 8),
    eleconfig='[Ar] 3d^10 4s^2 4p^6',
    oxistates='2*',
    ionenergy=(   13.9996,   24.3590,   36.9500,   52.5000,
                  64.7000,   78.5000,  110.0000,  126.0000,
                 230.3900,),
    isotopes=((78 ,  77.9203860000, 0.00350000),
              (80 ,  79.9163780000, 0.02280000),
              (82 ,  81.9134846000, 0.11580000),
              (83 ,  82.9141360000, 0.11490000),
              (84 ,  83.9115070000, 0.57000000),
              (86 ,  85.9106103000, 0.17300000),),)

elemDict['Rb'] = Element(37, 'Rb', 'Rubidium',
    group=1, period=5, block='s',
    mass=85.4678, en=0.82,
    covrad=2.160, atmrad=2.980, vdwrad=0.000,
    tboil=961.000, tmelt=312.630, density=1.5300,
    phase='solid', acidity='acidic',
    eleaffin=0.48591600,
    eleshells=(2, 8, 18, 8, 1),
    eleconfig='[Kr] 5s',
    oxistates='1*',
    ionenergy=(    4.1771,   27.2800,   40.0000,   52.6000,
                  71.0000,   84.4000,   99.2000,  136.0000,
                 150.0000,  277.1000,),
    isotopes=((85 ,  84.9117893000, 0.72170000),
              (87 ,  86.9091835000, 0.27830000),),)

elemDict['Sr'] = Element(38, 'Sr', 'Strontium',
    group=2, period=5, block='s',
    mass=87.62, en=0.95,
    covrad=1.910, atmrad=2.450, vdwrad=0.000,
    tboil=1655.000, tmelt=1042.000, density=2.6300,
    phase='solid', acidity='acidic',
    eleaffin=0.05206000,
    eleshells=(2, 8, 18, 8, 2),
    eleconfig='[Kr] 5s^2',
    oxistates='2*',
    ionenergy=(    5.6949,   11.0300,   43.6000,   57.0000,
                  71.6000,   90.8000,  106.0000,  122.3000,
                 162.0000,  177.0000,  324.1000,),
    isotopes=((84 ,  83.9134250000, 0.00560000),
              (86 ,  85.9092624000, 0.09860000),
              (87 ,  86.9088793000, 0.07000000),
              (88 ,  87.9056143000, 0.82580000),),)

elemDict['Y'] = Element(39, 'Y', 'Yttrium',
    group=3, period=5, block='d',
    mass=88.90585, en=1.22,
    covrad=1.620, atmrad=2.270, vdwrad=0.000,
    tboil=3611.000, tmelt=1795.000, density=4.4700,
    phase='solid', acidity='acidic',
    eleaffin=0.30700000,
    eleshells=(2, 8, 18, 9, 2),
    eleconfig='[Kr] 4d 5s^2',
    oxistates='3*',
    ionenergy=(    6.2173,   12.2400,   20.5200,   61.8000,
                  77.0000,   93.0000,  116.0000,  129.0000,
                 146.5200,  191.0000,  206.0000,  374.0000,),
    isotopes=((89 ,  88.9058479000, 1.00000000),),)

elemDict['Zr'] = Element(40, 'Zr', 'Zirconium',
    group=4, period=5, block='d',
    mass=91.224, en=1.33,
    covrad=1.450, atmrad=2.160, vdwrad=0.000,
    tboil=4682.000, tmelt=2128.000, density=6.5100,
    phase='solid', acidity='neutral',
    eleaffin=0.42600000,
    eleshells=(2, 8, 18, 10, 2),
    eleconfig='[Kr] 4d^2 5s^2',
    oxistates='4*',
    ionenergy=(    6.6339,   13.1300,   22.9900,   34.3400,
                  81.5000,),
    isotopes=((90 ,  89.9047037000, 0.51450000),
              (91 ,  90.9056450000, 0.11220000),
              (92 ,  91.9050401000, 0.17150000),
              (94 ,  93.9063158000, 0.17380000),
              (96 ,  95.9082760000, 0.02800000),),)

elemDict['Nb'] = Element(41, 'Nb', 'Niobium',
    group=5, period=5, block='d',
    mass=92.90638, en=1.6,
    covrad=1.340, atmrad=2.080, vdwrad=0.000,
    tboil=5015.000, tmelt=2742.000, density=8.5800,
    phase='solid', acidity='neutral',
    eleaffin=0.89300000,
    eleshells=(2, 8, 18, 12, 1),
    eleconfig='[Kr] 4d^4 5s',
    oxistates='5*, 3',
    ionenergy=(    6.7589,   14.3200,   25.0400,   38.3000,
                  50.5500,  102.6000,  125.0000,),
    isotopes=((93 ,  92.9063775000, 1.00000000),),)

elemDict['Mo'] = Element(42, 'Mo', 'Molybdenum',
    group=6, period=5, block='d',
    mass=95.94, en=2.16,
    covrad=1.300, atmrad=2.010, vdwrad=0.000,
    tboil=4912.000, tmelt=2896.000, density=10.2800,
    phase='solid', acidity='neutral',
    eleaffin=0.74720000,
    eleshells=(2, 8, 18, 13, 1),
    eleconfig='[Kr] 4d^5 5s',
    oxistates='6*, 5, 4, 3, 2, 0',
    ionenergy=(    7.0924,   16.1500,   27.1600,   46.4000,
                  61.2000,   68.0000,  126.8000,  153.0000,),
    isotopes=((92 ,  91.9068100000, 0.14840000),
              (94 ,  93.9050876000, 0.09250000),
              (95 ,  94.9058415000, 0.15920000),
              (96 ,  95.9046789000, 0.16680000),
              (97 ,  96.9060210000, 0.09550000),
              (98 ,  97.9054078000, 0.24130000),
              (100,  99.9074770000, 0.09630000),),)

elemDict['Tc'] = Element(43, 'Tc', 'Technetium',
    group=7, period=5, block='d',
    mass=97.907216, en=1.9,
    covrad=1.270, atmrad=1.950, vdwrad=0.000,
    tboil=4538.000, tmelt=2477.000, density=11.4900,
    phase='solid', acidity='neutral',
    eleaffin=0.55000000,
    eleshells=(2, 8, 18, 13, 2),
    eleconfig='[Kr] 4d^6 5s',
    oxistates='7*',
    ionenergy=(    7.2800,   15.2600,   29.5400,),
    isotopes=((98 ,  97.9072160000, 1.00000000),),)

elemDict['Ru'] = Element(44, 'Ru', 'Ruthenium',
    group=8, period=5, block='d',
    mass=101.07, en=2.2,
    covrad=1.250, atmrad=1.890, vdwrad=0.000,
    tboil=4425.000, tmelt=2610.000, density=12.4500,
    phase='solid', acidity='neutral',
    eleaffin=1.04638000,
    eleshells=(2, 8, 18, 15, 1),
    eleconfig='[Kr] 4d^7 5s',
    oxistates='8, 6, 4*, 3*, 2, 0, -2',
    ionenergy=(    7.3605,   16.7600,   28.4700,),
    isotopes=((96 ,  95.9075980000, 0.05540000),
              (98 ,  97.9052870000, 0.01870000),
              (99 ,  98.9059393000, 0.12760000),
              (100,  99.9042197000, 0.12600000),
              (101, 100.9055822000, 0.17060000),
              (102, 101.9043495000, 0.31550000),
              (104, 103.9054300000, 0.18620000),),)

elemDict['Rh'] = Element(45, 'Rh', 'Rhodium',
    group=9, period=5, block='d',
    mass=102.9055, en=2.28,
    covrad=1.250, atmrad=1.830, vdwrad=0.000,
    tboil=3970.000, tmelt=2236.000, density=12.4100,
    phase='solid', acidity='acidic',
    eleaffin=1.14289000,
    eleshells=(2, 8, 18, 16, 1),
    eleconfig='[Kr] 4d^8 5s',
    oxistates='5, 4, 3*, 1*, 2, 0',
    ionenergy=(    7.4589,   18.0800,   31.0600,),
    isotopes=((103, 102.9055040000, 1.00000000),),)

elemDict['Pd'] = Element(46, 'Pd', 'Palladium',
    group=10, period=5, block='d',
    mass=106.42, en=2.2,
    covrad=1.280, atmrad=1.790, vdwrad=1.630,
    tboil=3240.000, tmelt=1825.000, density=12.0200,
    phase='solid', acidity='acidic',
    eleaffin=0.56214000,
    eleshells=(2, 8, 18, 18, 0),
    eleconfig='[Kr] 4d^10',
    oxistates='4, 2*, 0',
    ionenergy=(    8.3369,   19.4300,   32.9300,),
    isotopes=((102, 101.9056080000, 0.01020000),
              (104, 103.9040350000, 0.11140000),
              (105, 104.9050840000, 0.22330000),
              (106, 105.9034830000, 0.27330000),
              (108, 107.9038940000, 0.26460000),
              (110, 109.9051520000, 0.11720000),),)

elemDict['Ag'] = Element(47, 'Ag', 'Silver',
    group=11, period=5, block='d',
    mass=107.8682, en=1.93,
    covrad=1.340, atmrad=1.750, vdwrad=1.720,
    tboil=2436.000, tmelt=1235.100, density=10.4900,
    phase='solid', acidity='acidic',
    eleaffin=1.30447000,
    eleshells=(2, 8, 18, 18, 1),
    eleconfig='[Kr] 4d^10 5s',
    oxistates='2, 1*',
    ionenergy=(    7.5762,   21.4900,   34.8300,),
    isotopes=((107, 106.9050930000, 0.51839000),
              (109, 108.9047560000, 0.48161000),),)

elemDict['Cd'] = Element(48, 'Cd', 'Cadmium',
    group=12, period=5, block='d',
    mass=112.411, en=1.69,
    covrad=1.480, atmrad=1.710, vdwrad=1.580,
    tboil=1040.000, tmelt=594.260, density=8.6400,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 18, 2),
    eleconfig='[Kr] 4d^10 5s^2',
    oxistates='2*',
    ionenergy=(    8.9938,   16.9080,   37.4800,),
    isotopes=((106, 105.9064580000, 0.01250000),
              (108, 107.9041830000, 0.00890000),
              (110, 109.9030060000, 0.12490000),
              (111, 110.9041820000, 0.12800000),
              (112, 111.9027572000, 0.24130000),
              (113, 112.9044009000, 0.12220000),
              (114, 113.9033581000, 0.28730000),
              (116, 115.9047550000, 0.07490000),),)

elemDict['In'] = Element(49, 'In', 'Indium',
    group=13, period=5, block='p',
    mass=114.818, en=1.78,
    covrad=1.440, atmrad=2.000, vdwrad=1.930,
    tboil=2350.000, tmelt=429.780, density=7.3100,
    phase='solid', acidity='neutral',
    eleaffin=0.40400000,
    eleshells=(2, 8, 18, 18, 3),
    eleconfig='[Kr] 4d^10 5s^2 5p',
    oxistates='3*',
    ionenergy=(    5.7864,   18.8690,   28.0300,   28.0300,),
    isotopes=((113, 112.9040610000, 0.04290000),
              (115, 114.9038780000, 0.95710000),),)

elemDict['Sn'] = Element(50, 'Sn', 'Tin',
    group=14, period=5, block='p',
    mass=118.71, en=1.96,
    covrad=1.410, atmrad=1.720, vdwrad=2.170,
    tboil=2876.000, tmelt=505.120, density=7.2900,
    phase='solid', acidity='neutral',
    eleaffin=1.11206600,
    eleshells=(2, 8, 18, 18, 4),
    eleconfig='[Kr] 4d^10 5s^2 5p^2',
    oxistates='4*, 2*',
    ionenergy=(    7.3439,   14.6320,   30.5020,   40.7340,
                  72.2800,),
    isotopes=((112, 111.9048210000, 0.00970000),
              (114, 113.9027820000, 0.00660000),
              (115, 114.9033460000, 0.00340000),
              (116, 115.9017440000, 0.14540000),
              (117, 116.9029540000, 0.07680000),
              (118, 117.9016060000, 0.24220000),
              (119, 118.9033090000, 0.08590000),
              (120, 119.9021966000, 0.32580000),
              (122, 121.9034401000, 0.04630000),
              (124, 123.9052746000, 0.05790000),),)

elemDict['Sb'] = Element(51, 'Sb', 'Antimony',
    group=15, period=5, block='p',
    mass=121.76, en=2.05,
    covrad=1.400, atmrad=1.530, vdwrad=0.000,
    tboil=1860.000, tmelt=903.910, density=6.6900,
    phase='solid', acidity='neutral',
    eleaffin=1.04740100,
    eleshells=(2, 8, 18, 18, 5),
    eleconfig='[Kr] 4d^10 5s^2 5p^3',
    oxistates='5, 3*, -3',
    ionenergy=(    8.6084,   16.5300,   25.3000,   44.2000,
                  56.0000,  108.0000,),
    isotopes=((121, 120.9038180000, 0.57210000),
              (123, 122.9042157000, 0.42790000),),)

elemDict['Te'] = Element(52, 'Te', 'Tellurium',
    group=16, period=5, block='p',
    mass=127.6, en=2.1,
    covrad=1.360, atmrad=1.420, vdwrad=2.060,
    tboil=1261.000, tmelt=722.720, density=6.2500,
    phase='solid', acidity='neutral',
    eleaffin=1.97087500,
    eleshells=(2, 8, 18, 18, 6),
    eleconfig='[Kr] 4d^10 5s^2 5p^4',
    oxistates='6, 4*, -2',
    ionenergy=(    9.0096,   18.6000,   27.9600,   37.4100,
                  58.7500,   70.7000,  137.0000,),
    isotopes=((120, 119.9040200000, 0.00090000),
              (122, 121.9030471000, 0.02550000),
              (123, 122.9042730000, 0.00890000),
              (124, 123.9028195000, 0.04740000),
              (125, 124.9044247000, 0.07070000),
              (126, 125.9033055000, 0.18840000),
              (128, 127.9044614000, 0.31740000),
              (130, 129.9062228000, 0.34080000),),)

elemDict['I'] = Element(53, 'I', 'Iodine',
    group=17, period=5, block='p',
    mass=126.90447, en=2.66,
    covrad=1.330, atmrad=1.320, vdwrad=1.980,
    tboil=457.500, tmelt=386.700, density=4.9400,
    phase='solid', acidity='amphoteric',
    eleaffin=3.05903800,
    eleshells=(2, 8, 18, 18, 7),
    eleconfig='[Kr] 4d^10 5s^2 5p^5',
    oxistates='7, 5, 1, -1*',
    ionenergy=(   10.4513,   19.1310,   33.0000,),
    isotopes=((127, 126.9044680000, 1.00000000),),)

elemDict['Xe'] = Element(54, 'Xe', 'Xenon',
    group=18, period=5, block='p',
    mass=131.293, en=0.0,
    covrad=1.310, atmrad=1.240, vdwrad=2.160,
    tboil=165.100, tmelt=161.390, density=4.4900,
    phase='gas', acidity='basic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 18, 8),
    eleconfig='[Kr] 4d^10 5s^2 5p^6',
    oxistates='2, 4, 6',
    ionenergy=(   12.1298,   21.2100,   32.1000,),
    isotopes=((124, 123.9058958000, 0.00090000),
              (126, 125.9042690000, 0.00090000),
              (128, 127.9035304000, 0.01920000),
              (129, 128.9047795000, 0.26440000),
              (130, 129.9035079000, 0.04080000),
              (131, 130.9050819000, 0.21180000),
              (132, 131.9041545000, 0.26890000),
              (134, 133.9053945000, 0.10440000),
              (136, 135.9072200000, 0.08870000),),)

elemDict['Cs'] = Element(55, 'Cs', 'Caesium',
    group=1, period=6, block='s',
    mass=132.90545, en=0.79,
    covrad=2.350, atmrad=3.340, vdwrad=0.000,
    tboil=944.000, tmelt=301.540, density=1.9000,
    phase='solid', acidity='acidic',
    eleaffin=0.47162600,
    eleshells=(2, 8, 18, 18, 8, 1),
    eleconfig='[Xe] 6s',
    oxistates='1*',
    ionenergy=(    3.8939,   25.1000,),
    isotopes=((133, 132.9054470000, 1.00000000),),)

elemDict['Ba'] = Element(56, 'Ba', 'Barium',
    group=2, period=6, block='s',
    mass=137.327, en=0.89,
    covrad=1.980, atmrad=2.780, vdwrad=0.000,
    tboil=2078.000, tmelt=1002.000, density=3.6500,
    phase='solid', acidity='acidic',
    eleaffin=0.14462000,
    eleshells=(2, 8, 18, 18, 8, 2),
    eleconfig='[Xe] 6s^2',
    oxistates='2*',
    ionenergy=(    5.2117,  100.0040,),
    isotopes=((130, 129.9063100000, 0.00106000),
              (132, 131.9050560000, 0.00101000),
              (134, 133.9045030000, 0.02417000),
              (135, 134.9056830000, 0.06592000),
              (136, 135.9045700000, 0.07854000),
              (137, 136.9058210000, 0.11232000),
              (138, 137.9052410000, 0.71698000),),)

elemDict['La'] = Element(57, 'La', 'Lanthanum',
    group=3, period=6, block='f',
    mass=138.9055, en=1.1,
    covrad=1.690, atmrad=2.740, vdwrad=0.000,
    tboil=3737.000, tmelt=1191.000, density=6.1600,
    phase='solid', acidity='acidic',
    eleaffin=0.47000000,
    eleshells=(2, 8, 18, 18, 9, 2),
    eleconfig='[Xe] 5d 6s^2',
    oxistates='3*',
    ionenergy=(    5.5769,   11.0600,   19.1750,),
    isotopes=((138, 137.9071070000, 0.00090000),
              (139, 138.9063480000, 0.99910000),),)

elemDict['Ce'] = Element(58, 'Ce', 'Cerium',
    group=3, period=6, block='f',
    mass=140.116, en=1.12,
    covrad=1.650, atmrad=2.700, vdwrad=0.000,
    tboil=3715.000, tmelt=1071.000, density=6.7700,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 19, 9, 2),
    eleconfig='[Xe] 4f 5d 6s^2',
    oxistates='4, 3*',
    ionenergy=(    5.5387,   10.8500,   20.2000,   36.7200,),
    isotopes=((136, 135.9071400000, 0.00185000),
              (138, 137.9059860000, 0.00251000),
              (140, 139.9054340000, 0.88450000),
              (142, 141.9092400000, 0.11114000),),)

elemDict['Pr'] = Element(59, 'Pr', 'Praseodymium',
    group=3, period=6, block='f',
    mass=140.90765, en=1.13,
    covrad=1.650, atmrad=2.670, vdwrad=0.000,
    tboil=3785.000, tmelt=1204.000, density=6.4800,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 21, 8, 2),
    eleconfig='[Xe] 4f^3 6s^2',
    oxistates='4, 3*',
    ionenergy=(    5.4730,   10.5500,   21.6200,   38.9500,
                  57.4500,),
    isotopes=((141, 140.9076480000, 1.00000000),),)

elemDict['Nd'] = Element(60, 'Nd', 'Neodymium',
    group=3, period=6, block='f',
    mass=144.24, en=1.14,
    covrad=1.640, atmrad=2.640, vdwrad=0.000,
    tboil=3347.000, tmelt=1294.000, density=7.0000,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 22, 8, 2),
    eleconfig='[Xe] 4f^4 6s^2',
    oxistates='3*',
    ionenergy=(    5.5250,   10.7200,),
    isotopes=((142, 141.9077190000, 0.27200000),
              (143, 142.9098100000, 0.12200000),
              (144, 143.9100830000, 0.23800000),
              (145, 144.9125690000, 0.08300000),
              (146, 145.9131120000, 0.17200000),
              (148, 147.9168890000, 0.05700000),
              (150, 149.9208870000, 0.05600000),),)

elemDict['Pm'] = Element(61, 'Pm', 'Promethium',
    group=3, period=6, block='f',
    mass=144.912744, en=1.13,
    covrad=1.630, atmrad=2.620, vdwrad=0.000,
    tboil=3273.000, tmelt=1315.000, density=7.2200,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 23, 8, 2),
    eleconfig='[Xe] 4f^5 6s^2',
    oxistates='3*',
    ionenergy=(    5.5820,   10.9000,),
    isotopes=((145, 144.9127440000, 1.00000000),),)

elemDict['Sm'] = Element(62, 'Sm', 'Samarium',
    group=3, period=6, block='f',
    mass=150.36, en=1.17,
    covrad=1.620, atmrad=2.590, vdwrad=0.000,
    tboil=2067.000, tmelt=1347.000, density=7.5400,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 24, 8, 2),
    eleconfig='[Xe] 4f^6 6s^2',
    oxistates='3*, 2',
    ionenergy=(    5.6437,   11.0700,),
    isotopes=((144, 143.9119950000, 0.03070000),
              (147, 146.9148930000, 0.14990000),
              (148, 147.9148180000, 0.11240000),
              (149, 148.9171800000, 0.13820000),
              (150, 149.9172710000, 0.07380000),
              (152, 151.9197280000, 0.26750000),
              (154, 153.9222050000, 0.22750000),),)

elemDict['Eu'] = Element(63, 'Eu', 'Europium',
    group=3, period=6, block='f',
    mass=151.964, en=1.2,
    covrad=1.850, atmrad=2.560, vdwrad=0.000,
    tboil=1800.000, tmelt=1095.000, density=5.2500,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 25, 8, 2),
    eleconfig='[Xe] 4f^7 6s^2',
    oxistates='3*, 2',
    ionenergy=(    5.6704,   11.2500,),
    isotopes=((151, 150.9198460000, 0.47810000),
              (153, 152.9212260000, 0.52190000),),)

elemDict['Gd'] = Element(64, 'Gd', 'Gadolinium',
    group=3, period=6, block='f',
    mass=157.25, en=1.2,
    covrad=1.610, atmrad=2.540, vdwrad=0.000,
    tboil=3545.000, tmelt=1585.000, density=7.8900,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 25, 9, 2),
    eleconfig='[Xe] 4f^7 5d 6s^2',
    oxistates='3*',
    ionenergy=(    6.1498,   12.1000,),
    isotopes=((152, 151.9197880000, 0.00200000),
              (154, 153.9208620000, 0.02180000),
              (155, 154.9226190000, 0.14800000),
              (156, 155.9221200000, 0.20470000),
              (157, 156.9239570000, 0.15650000),
              (158, 157.9241010000, 0.24840000),
              (160, 159.9270510000, 0.21860000),),)

elemDict['Tb'] = Element(65, 'Tb', 'Terbium',
    group=3, period=6, block='f',
    mass=158.92534, en=1.2,
    covrad=1.590, atmrad=2.510, vdwrad=0.000,
    tboil=3500.000, tmelt=1629.000, density=8.2500,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 27, 8, 2),
    eleconfig='[Xe] 4f^9 6s^2',
    oxistates='4, 3*',
    ionenergy=(    5.8638,   11.5200,),
    isotopes=((159, 158.9253430000, 1.00000000),),)

elemDict['Dy'] = Element(66, 'Dy', 'Dysprosium',
    group=3, period=6, block='f',
    mass=162.5, en=1.22,
    covrad=1.590, atmrad=2.490, vdwrad=0.000,
    tboil=2840.000, tmelt=1685.000, density=8.5600,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 28, 8, 2),
    eleconfig='[Xe] 4f^10 6s^2',
    oxistates='3*',
    ionenergy=(    5.9389,   11.6700,),
    isotopes=((156, 155.9242780000, 0.00060000),
              (158, 157.9244050000, 0.00100000),
              (160, 159.9251940000, 0.02340000),
              (161, 160.9269300000, 0.18910000),
              (162, 161.9267950000, 0.25510000),
              (163, 162.9287280000, 0.24900000),
              (164, 163.9291710000, 0.28180000),),)

elemDict['Ho'] = Element(67, 'Ho', 'Holmium',
    group=3, period=6, block='f',
    mass=164.93032, en=1.23,
    covrad=1.580, atmrad=2.470, vdwrad=0.000,
    tboil=2968.000, tmelt=1747.000, density=8.7800,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 29, 8, 2),
    eleconfig='[Xe] 4f^11 6s^2',
    oxistates='3*',
    ionenergy=(    6.0215,   11.8000,),
    isotopes=((165, 164.9303190000, 1.00000000),),)

elemDict['Er'] = Element(68, 'Er', 'Erbium',
    group=3, period=6, block='f',
    mass=167.259, en=1.24,
    covrad=1.570, atmrad=2.450, vdwrad=0.000,
    tboil=3140.000, tmelt=1802.000, density=9.0500,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 30, 8, 2),
    eleconfig='[Xe] 4f^12 6s^2',
    oxistates='3*',
    ionenergy=(    6.1077,   11.9300,),
    isotopes=((162, 161.9287750000, 0.00140000),
              (164, 163.9291970000, 0.01610000),
              (166, 165.9302900000, 0.33610000),
              (167, 166.9320450000, 0.22930000),
              (168, 167.9323680000, 0.26780000),
              (170, 169.9354600000, 0.14930000),),)

elemDict['Tm'] = Element(69, 'Tm', 'Thulium',
    group=3, period=6, block='f',
    mass=168.93421, en=1.25,
    covrad=1.560, atmrad=2.420, vdwrad=0.000,
    tboil=2223.000, tmelt=1818.000, density=9.3200,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 31, 8, 2),
    eleconfig='[Xe] 4f^13 6s^2',
    oxistates='3*, 2',
    ionenergy=(    6.1843,   12.0500,   23.7100,),
    isotopes=((169, 168.9342110000, 1.00000000),),)

elemDict['Yb'] = Element(70, 'Yb', 'Ytterbium',
    group=3, period=6, block='f',
    mass=173.04, en=1.1,
    covrad=1.740, atmrad=2.400, vdwrad=0.000,
    tboil=1469.000, tmelt=1092.000, density=9.3200,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 32, 8, 2),
    eleconfig='[Xe] 4f^14 6s^2',
    oxistates='3*, 2',
    ionenergy=(    6.2542,   12.1700,   25.2000,),
    isotopes=((168, 167.9338940000, 0.00130000),
              (170, 169.9347590000, 0.03040000),
              (171, 170.9363220000, 0.14280000),
              (172, 171.9363777000, 0.21830000),
              (173, 172.9382068000, 0.16130000),
              (174, 173.9388581000, 0.31830000),
              (176, 175.9425680000, 0.12760000),),)

elemDict['Lu'] = Element(71, 'Lu', 'Lutetium',
    group=3, period=6, block='d',
    mass=174.967, en=1.27,
    covrad=1.560, atmrad=2.250, vdwrad=0.000,
    tboil=3668.000, tmelt=1936.000, density=9.8400,
    phase='solid', acidity='acidic',
    eleaffin=0.50000000,
    eleshells=(2, 8, 18, 32, 9, 2),
    eleconfig='[Xe] 4f^14 5d 6s^2',
    oxistates='3*',
    ionenergy=(    5.4259,   13.9000,),
    isotopes=((175, 174.9407679000, 0.97410000),
              (176, 175.9426824000, 0.02590000),),)

elemDict['Hf'] = Element(72, 'Hf', 'Hafnium',
    group=4, period=6, block='d',
    mass=178.49, en=1.3,
    covrad=1.440, atmrad=2.160, vdwrad=0.000,
    tboil=4875.000, tmelt=2504.000, density=13.3100,
    phase='solid', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 10, 2),
    eleconfig='[Xe] 4f^14 5d^2 6s^2',
    oxistates='4*',
    ionenergy=(    6.8251,   14.9000,   23.3000,   33.3000,),
    isotopes=((174, 173.9400400000, 0.00160000),
              (176, 175.9414018000, 0.05260000),
              (177, 176.9432200000, 0.18600000),
              (178, 177.9436977000, 0.27280000),
              (179, 178.9458151000, 0.13620000),
              (180, 179.9465488000, 0.35080000),),)

elemDict['Ta'] = Element(73, 'Ta', 'Tantalum',
    group=5, period=6, block='d',
    mass=180.9479, en=1.5,
    covrad=1.340, atmrad=2.090, vdwrad=0.000,
    tboil=5730.000, tmelt=3293.000, density=16.6800,
    phase='solid', acidity='neutral',
    eleaffin=0.32200000,
    eleshells=(2, 8, 18, 32, 11, 2),
    eleconfig='[Xe] 4f^14 5d^3 6s^2',
    oxistates='5*',
    ionenergy=(    7.5496,),
    isotopes=((180, 179.9474660000, 0.00012000),
              (181, 180.9479960000, 0.99988000),),)

elemDict['W'] = Element(74, 'W', 'Tungsten',
    group=6, period=6, block='d',
    mass=183.84, en=2.36,
    covrad=1.300, atmrad=2.020, vdwrad=0.000,
    tboil=5825.000, tmelt=3695.000, density=19.2600,
    phase='solid', acidity='neutral',
    eleaffin=0.81500000,
    eleshells=(2, 8, 18, 32, 12, 2),
    eleconfig='[Xe] 4f^14 5d^4 6s^2',
    oxistates='6*, 5, 4, 3, 2, 0',
    ionenergy=(    7.8640,),
    isotopes=((180, 179.9467060000, 0.00120000),
              (182, 181.9482060000, 0.26500000),
              (183, 182.9502245000, 0.14310000),
              (184, 183.9509326000, 0.30640000),
              (186, 185.9543620000, 0.28430000),),)

elemDict['Re'] = Element(75, 'Re', 'Rhenium',
    group=7, period=6, block='d',
    mass=186.207, en=1.9,
    covrad=1.280, atmrad=1.970, vdwrad=0.000,
    tboil=5870.000, tmelt=3455.000, density=21.0300,
    phase='solid', acidity='neutral',
    eleaffin=0.15000000,
    eleshells=(2, 8, 18, 32, 13, 2),
    eleconfig='[Xe] 4f^14 5d^5 6s^2',
    oxistates='7, 6, 4, 2, -1',
    ionenergy=(    7.8335,),
    isotopes=((185, 184.9529557000, 0.37400000),
              (187, 186.9557508000, 0.62600000),),)

elemDict['Os'] = Element(76, 'Os', 'Osmium',
    group=8, period=6, block='d',
    mass=190.23, en=2.2,
    covrad=1.260, atmrad=1.920, vdwrad=0.000,
    tboil=5300.000, tmelt=3300.000, density=22.6100,
    phase='solid', acidity='neutral',
    eleaffin=1.07780000,
    eleshells=(2, 8, 18, 32, 14, 2),
    eleconfig='[Xe] 4f^14 5d^6 6s^2',
    oxistates='8, 6, 4*, 3, 2, 0, -2',
    ionenergy=(    8.4382,),
    isotopes=((184, 183.9524910000, 0.00020000),
              (186, 185.9538380000, 0.01590000),
              (187, 186.9557479000, 0.01960000),
              (188, 187.9558360000, 0.13240000),
              (189, 188.9581449000, 0.16150000),
              (190, 189.9584450000, 0.26260000),
              (192, 191.9614790000, 0.40780000),),)

elemDict['Ir'] = Element(77, 'Ir', 'Iridium',
    group=9, period=6, block='d',
    mass=192.217, en=2.2,
    covrad=1.270, atmrad=1.870, vdwrad=0.000,
    tboil=4700.000, tmelt=2720.000, density=22.6500,
    phase='solid', acidity='acidic',
    eleaffin=1.56436000,
    eleshells=(2, 8, 18, 32, 15, 2),
    eleconfig='[Xe] 4f^14 5d^7 6s^2',
    oxistates='6, 4*, 3, 2, 1*, 0, -1',
    ionenergy=(    8.9670,),
    isotopes=((191, 190.9605910000, 0.37300000),
              (193, 192.9629240000, 0.62700000),),)

elemDict['Pt'] = Element(78, 'Pt', 'Platinum',
    group=10, period=6, block='d',
    mass=195.078, en=2.28,
    covrad=1.300, atmrad=1.830, vdwrad=1.750,
    tboil=4100.000, tmelt=2042.100, density=21.4500,
    phase='solid', acidity='acidic',
    eleaffin=2.12510000,
    eleshells=(2, 8, 18, 32, 17, 1),
    eleconfig='[Xe] 4f^14 5d^9 6s',
    oxistates='4*, 2*, 0',
    ionenergy=(    8.9588,   18.5630,),
    isotopes=((190, 189.9599300000, 0.00014000),
              (192, 191.9610350000, 0.00782000),
              (194, 193.9626640000, 0.32967000),
              (195, 194.9647740000, 0.33832000),
              (196, 195.9649350000, 0.25242000),
              (198, 197.9678760000, 0.07163000),),)

elemDict['Au'] = Element(79, 'Au', 'Gold',
    group=11, period=6, block='d',
    mass=196.96655, en=2.54,
    covrad=1.340, atmrad=1.790, vdwrad=1.660,
    tboil=3130.000, tmelt=1337.580, density=19.3200,
    phase='solid', acidity='acidic',
    eleaffin=2.30861000,
    eleshells=(2, 8, 18, 32, 18, 1),
    eleconfig='[Xe] 4f^14 5d^10 6s',
    oxistates='3*, 1',
    ionenergy=(    9.2255,   20.5000,),
    isotopes=((197, 196.9665520000, 1.00000000),),)

elemDict['Hg'] = Element(80, 'Hg', 'Mercury',
    group=12, period=6, block='d',
    mass=200.59, en=2.0,
    covrad=1.490, atmrad=1.760, vdwrad=0.000,
    tboil=629.880, tmelt=234.310, density=13.5500,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 18, 2),
    eleconfig='[Xe] 4f^14 5d^10 6s^2',
    oxistates='2*, 1',
    ionenergy=(   10.4375,   18.7560,   34.2000,),
    isotopes=((196, 195.9658150000, 0.00150000),
              (198, 197.9667520000, 0.09970000),
              (199, 198.9682620000, 0.16870000),
              (200, 199.9683090000, 0.23100000),
              (201, 200.9702850000, 0.13180000),
              (202, 201.9706260000, 0.29860000),
              (204, 203.9734760000, 0.06870000),),)

elemDict['Tl'] = Element(81, 'Tl', 'Thallium',
    group=13, period=6, block='p',
    mass=204.3833, en=2.04,
    covrad=1.480, atmrad=2.080, vdwrad=1.960,
    tboil=1746.000, tmelt=577.000, density=11.8500,
    phase='solid', acidity='neutral',
    eleaffin=0.37700000,
    eleshells=(2, 8, 18, 32, 18, 3),
    eleconfig='[Xe] 4f^14 5d^10 6s^2 6p',
    oxistates='3, 1*',
    ionenergy=(    6.1082,   20.4280,   29.8300,),
    isotopes=((203, 202.9723290000, 0.29524000),
              (205, 204.9744120000, 0.70476000),),)

elemDict['Pb'] = Element(82, 'Pb', 'Lead',
    group=14, period=6, block='p',
    mass=207.2, en=2.33,
    covrad=1.470, atmrad=1.810, vdwrad=2.020,
    tboil=2023.000, tmelt=600.650, density=11.3400,
    phase='solid', acidity='neutral',
    eleaffin=0.36400000,
    eleshells=(2, 8, 18, 32, 18, 4),
    eleconfig='[Xe] 4f^14 5d^10 6s^2 6p^2',
    oxistates='4, 2*',
    ionenergy=(    7.4167,   15.0320,   31.9370,   42.3200,
                  68.8000,),
    isotopes=((204, 203.9730290000, 0.01400000),
              (206, 205.9744490000, 0.24100000),
              (207, 206.9758810000, 0.22100000),
              (208, 207.9766360000, 0.52400000),),)

elemDict['Bi'] = Element(83, 'Bi', 'Bismuth',
    group=15, period=6, block='p',
    mass=208.98038, en=2.02,
    covrad=1.460, atmrad=1.630, vdwrad=0.000,
    tboil=1837.000, tmelt=544.590, density=9.8000,
    phase='solid', acidity='acidic',
    eleaffin=0.94236300,
    eleshells=(2, 8, 18, 32, 18, 5),
    eleconfig='[Xe] 4f^14 5d^10 6s^2 6p^3',
    oxistates='5, 3*',
    ionenergy=(    7.2855,   16.6900,   25.5600,   45.3000,
                  56.0000,   88.3000,),
    isotopes=((209, 208.9803830000, 1.00000000),),)

elemDict['Po'] = Element(84, 'Po', 'Polonium',
    group=16, period=6, block='p',
    mass=208.982416, en=2.0,
    covrad=1.460, atmrad=1.530, vdwrad=0.000,
    tboil=0.000, tmelt=527.000, density=9.2000,
    phase='solid', acidity='neutral',
    eleaffin=1.90000000,
    eleshells=(2, 8, 18, 32, 18, 6),
    eleconfig='[Xe] 4f^14 5d^10 6s^2 6p^4',
    oxistates='6, 4*, 2',
    ionenergy=(    8.4140,),
    isotopes=((209, 208.9824160000, 1.00000000),),)

elemDict['At'] = Element(85, 'At', 'Astatine',
    group=17, period=6, block='p',
    mass=209.9871, en=2.2,
    covrad=1.450, atmrad=1.430, vdwrad=0.000,
    tboil=610.000, tmelt=575.000, density=0.0000,
    phase='unknown', acidity='amphoteric',
    eleaffin=2.80000000,
    eleshells=(2, 8, 18, 32, 18, 7),
    eleconfig='[Xe] 4f^14 5d^10 6s^2 6p^5',
    oxistates='7, 5, 3, 1, -1*',
    ionenergy=(    0.000,),
    isotopes=((210, 209.9871310000, 1.00000000),),)

elemDict['Rn'] = Element(86, 'Rn', 'Radon',
    group=18, period=6, block='p',
    mass=222.0176, en=0.0,
    covrad=0.000, atmrad=1.340, vdwrad=0.000,
    tboil=211.400, tmelt=202.000, density=9.2300,
    phase='gas', acidity='basic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 18, 8),
    eleconfig='[Xe] 4f^14 5d^10 6s^2 6p^6',
    oxistates='2*',
    ionenergy=(   10.7485,),
    isotopes=((222, 222.0175705000, 1.00000000),),)

elemDict['Fr'] = Element(87, 'Fr', 'Francium',
    group=1, period=7, block='s',
    mass=223.0197307, en=0.7,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=950.000, tmelt=300.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 18, 8, 1),
    eleconfig='[Rn] 7s',
    oxistates='1*',
    ionenergy=(    4.0727,),
    isotopes=((223, 223.0197307000, 1.00000000),),)

elemDict['Ra'] = Element(88, 'Ra', 'Radium',
    group=2, period=7, block='s',
    mass=226.025403, en=0.9,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=1413.000, tmelt=973.000, density=5.5000,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 18, 8, 2),
    eleconfig='[Rn] 7s^2',
    oxistates='2*',
    ionenergy=(    5.2784,   10.1470,),
    isotopes=((226, 226.0254026000, 1.00000000),),)

elemDict['Ac'] = Element(89, 'Ac', 'Actinium',
    group=3, period=7, block='f',
    mass=227.027747, en=1.1,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=3470.000, tmelt=1324.000, density=10.0700,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 18, 9, 2),
    eleconfig='[Rn] 6d 7s^2',
    oxistates='3*',
    ionenergy=(    5.1700,   12.1000,),
    isotopes=((227, 227.0277470000, 1.00000000),),)

elemDict['Th'] = Element(90, 'Th', 'Thorium',
    group=3, period=7, block='f',
    mass=232.0381, en=1.3,
    covrad=1.650, atmrad=0.000, vdwrad=0.000,
    tboil=5060.000, tmelt=2028.000, density=11.7200,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 18, 10, 2),
    eleconfig='[Rn] 6d^2 7s^2',
    oxistates='4*',
    ionenergy=(    6.3067,   11.5000,   20.0000,   28.8000,),
    isotopes=((232, 232.0380504000, 1.00000000),),)

elemDict['Pa'] = Element(91, 'Pa', 'Protactinium',
    group=3, period=7, block='f',
    mass=231.03588, en=1.5,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=4300.000, tmelt=1845.000, density=15.3700,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 20, 9, 2),
    eleconfig='[Rn] 5f^2 6d 7s^2',
    oxistates='5*, 4',
    ionenergy=(    5.8900,),
    isotopes=((231, 231.0358789000, 1.00000000),),)

elemDict['U'] = Element(92, 'U', 'Uranium',
    group=3, period=7, block='f',
    mass=238.02891, en=1.38,
    covrad=1.420, atmrad=0.000, vdwrad=1.860,
    tboil=4407.000, tmelt=1408.000, density=18.9700,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 21, 9, 2),
    eleconfig='[Rn] 5f^3 6d 7s^2',
    oxistates='6*, 5, 4, 3',
    ionenergy=(    6.1941,),
    isotopes=((234, 234.0409456000, 0.00005500),
              (235, 235.0439231000, 0.00720000),
              (238, 238.0507826000, 0.99274500),),)

elemDict['Np'] = Element(93, 'Np', 'Neptunium',
    group=3, period=7, block='f',
    mass=237.048167, en=1.36,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=4175.000, tmelt=912.000, density=20.4800,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 22, 9, 2),
    eleconfig='[Rn] 5f^4 6d 7s^2',
    oxistates='6, 5*, 4, 3',
    ionenergy=(    6.2657,),
    isotopes=((237, 237.0481673000, 1.00000000),),)

elemDict['Pu'] = Element(94, 'Pu', 'Plutonium',
    group=3, period=7, block='f',
    mass=244.064198, en=1.28,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=3505.000, tmelt=913.000, density=19.7400,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 24, 8, 2),
    eleconfig='[Rn] 5f^6 7s^2',
    oxistates='6, 5, 4*, 3',
    ionenergy=(    6.0260,),
    isotopes=((244, 244.0641980000, 1.00000000),),)

elemDict['Am'] = Element(95, 'Am', 'Americium',
    group=3, period=7, block='f',
    mass=243.061373, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=2880.000, tmelt=1449.000, density=13.6700,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 25, 8, 2),
    eleconfig='[Rn] 5f^7 7s^2',
    oxistates='6, 5, 4, 3*',
    ionenergy=(    5.9738,),
    isotopes=((243, 243.0613727000, 1.00000000),),)

elemDict['Cm'] = Element(96, 'Cm', 'Curium',
    group=3, period=7, block='f',
    mass=247.070347, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1620.000, density=13.5100,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 25, 9, 2),
    eleconfig='[Rn] 5f^7 6d 7s^2',
    oxistates='4, 3*',
    ionenergy=(    5.9914,),
    isotopes=((247, 247.0703470000, 1.00000000),),)

elemDict['Bk'] = Element(97, 'Bk', 'Berkelium',
    group=3, period=7, block='f',
    mass=247.070299, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1258.000, density=13.2500,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 27, 8, 2),
    eleconfig='[Rn] 5f^9 7s^2',
    oxistates='4, 3*',
    ionenergy=(    6.1979,),
    isotopes=((247, 247.0702990000, 1.00000000),),)

elemDict['Cf'] = Element(98, 'Cf', 'Californium',
    group=3, period=7, block='f',
    mass=251.07958, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1172.000, density=15.1000,
    phase='solid', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 28, 8, 2),
    eleconfig='[Rn] 5f^10 7s^2',
    oxistates='4, 3*',
    ionenergy=(    6.2817,),
    isotopes=((251, 251.0795800000, 1.00000000),),)

elemDict['Es'] = Element(99, 'Es', 'Einsteinium',
    group=3, period=7, block='f',
    mass=252.08297, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1130.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 29, 8, 2),
    eleconfig='[Rn] 5f^11 7s^2',
    oxistates='3*',
    ionenergy=(    6.4200,),
    isotopes=((252, 252.0829700000, 1.00000000),),)

elemDict['Fm'] = Element(100, 'Fm', 'Fermium',
    group=3, period=7, block='f',
    mass=257.095099, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1800.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 30, 8, 2),
    eleconfig='[Rn] 5f^12 7s^2',
    oxistates='3*',
    ionenergy=(    6.5000,),
    isotopes=((257, 257.0950990000, 1.00000000),),)

elemDict['Md']= Element(101, 'Md', 'Mendelevium',
    group=3, period=7, block='f',
    mass=258.098425, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1100.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 31, 8, 2),
    eleconfig='[Rn] 5f^13 7s^2',
    oxistates='3*',
    ionenergy=(    6.5800,),
    isotopes=((258, 258.0984250000, 1.00000000),),)

elemDict['No']= Element(102, 'No', 'Nobelium',
    group=3, period=7, block='f',
    mass=259.10102, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1100.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 8, 2),
    eleconfig='[Rn] 5f^14 7s^2',
    oxistates='3, 2*',
    ionenergy=(    6.6500,),
    isotopes=((259, 259.1010200000, 1.00000000),),)

elemDict['Lr']= Element(103, 'Lr', 'Lawrencium',
    group=3, period=7, block='d',
    mass=262.10969, en=1.3,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=1900.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 9, 2),
    eleconfig='[Rn] 5f^14 6d 7s^2',
    oxistates='3*',
    ionenergy=(    4.9000,),
    isotopes=((262, 262.1096900000, 1.00000000),),)

elemDict['Rf'] = Element(104, 'Rf', 'Rutherfordium',
    group=4, period=7, block='d',
    mass=261.10875, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 10, 2),
    eleconfig='[Rn] 5f^14 6d^2 7s^2',
    oxistates='*',
    ionenergy=(    6.0000,),
    isotopes=((261, 261.1087500000, 1.00000000),),)

elemDict['Db']= Element(105, 'Db', 'Dubnium',
    group=5, period=7, block='d',
    mass=262.11415, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 11, 2),
    eleconfig='[Rn] 5f^14 6d^3 7s^2',
    oxistates='*',
    ionenergy=(    0.000,),
    isotopes=((262, 262.1141500000, 1.00000000),),)

elemDict['Sg']= Element(106, 'Sg', 'Seaborgium',
    group=6, period=7, block='d',
    mass=266.12193, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 12, 2),
    eleconfig='[Rn] 5f^14 6d^4 7^s2',
    oxistates='*',
    ionenergy=(    0.000,),
    isotopes=((266, 266.1219300000, 1.00000000),),)

elemDict['Bh']= Element(107, 'Bh', 'Bohrium',
    group=7, period=7, block='d',
    mass=265.12473, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 13, 2),
    eleconfig='[Rn] 5f^14 6d^5 7^s2',
    oxistates='*',
    ionenergy=(    0.000,),
    isotopes=((265, 265.1247300000, 1.00000000),),)#Mod BHC

elemDict['Hs']= Element(108, 'Hs', 'Hassium',
    group=8, period=7, block='d',
    mass=269.13411, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='neutral',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 14, 2),
    eleconfig='[Rn] 5f^14 6d^6 7s^2',
    oxistates='*',
    ionenergy=(    0.000,),
    isotopes=((269, 269.1341100000, 1.00000000),),)

elemDict['Mt']= Element(109, 'Mt', 'Meitnerium',
    group=9, period=7, block='d',
    mass=268.13882, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 15, 2),
    eleconfig='[Rn] 5f^14 6d^7 7s^2',
    oxistates='*',
    ionenergy=(    0.000,),
    isotopes=((268, 268.1388200000, 1.00000000),),)

elemDict['Ds'] = Element(110, 'Ds', 'Darmstadtium',
    group=10, period=7, block='d',
    mass=271.1460, en=0.0,
    covrad=0.000, atmrad=0.000, vdwrad=0.000,
    tboil=0.000, tmelt=0.000, density=0.0000,
    phase='unknown', acidity='acidic',
    eleaffin=0.00000000,
    eleshells=(2, 8, 18, 32, 32, 17, 1),
    eleconfig='[Rn] 5f^14 6d^9 7s^1',
    oxistates='*',
    ionenergy=(    0.000,),
    isotopes=((271, 271.14600000, 1.00000000),),)

#elemDict['Rg'] = 111 272.154
#elemDict['Uub'] = 112 277.164

#Not Confirmed
#elemDict['Uut'] = 113 287.181
#elemDict['Uuq'] = 114 289.187
#elemDict['Uup'] = 115 291.194
#elemDict['Uuh'] = 116 ?
#elemDict['Uus'] = 117 ?
#elemDict['Uuo'] = 118 ?


def test_elements_module():
    """Test elements module."""
    #for i in (elements, groups, periods, blocks):
        #print i, "\n"
    for e in elements:
        e.export('python')

    m = 0.0
    for e in 'HBCNOFPSKVYIU':
        m += elements[e].mass
    assert(abs(m-680)<1)

    m = 0.0
    for e in elements:
        m += e.mass
    assert(abs(m-14659)<1)

    assert('Xe' in elements)
    assert('Xu' not in elements)
    for b in blocks:
        pass

if __name__ == "__main__":
    C = elemDict['C']
    print C.isotopes
    print C.__dict__
#    test_elements_module()
