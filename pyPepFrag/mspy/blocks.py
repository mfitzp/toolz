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
import xml.dom.minidom

# load configuration
import config

# register essential objects
import objects


# BASIC OBJECTS DEFINITIONS
# -------------------------

class element:
    """Element object definition"""
    
    def __init__(self, name='', symbol='', atomicNumber='', isotopes={}):
        self.name = name
        self.symbol = symbol
        self.atomicNumber = atomicNumber
        self.mass = None # (monoisotopic, average)
        self.isotopes = isotopes # {mass number:(mass, abundance)}
        
        # init masses
        self.initMasses()
    # ----
    
    
    def initMasses(self):
        """Initialize masses."""
        
        isotopes = self.isotopes.values()
        massMo = 0
        massAv = 0
        maxAbundance = 0
        for isotop in isotopes:
            massAv += isotop[0]*isotop[1]
            if maxAbundance < isotop[1]:
                massMo = isotop[0]
                maxAbundance = isotop[1]
        if massMo == 0 or massAv == 0:
            massMo = isotopes[0][0]
            massAv = isotopes[0][0]
        self.mass = (massMo, massAv)
    # ----
    


class aminoacid:
    """Amino acid object definition"""
    
    def __init__(self, name='', symbol='', formula='', abbr=''):
        self.name = name
        self.symbol = symbol
        self.formula = formula
        self.mass = None # (monoisotopic, average)
        self.abbr = abbr
        
        # init masses
        self.initMasses()
    # ----
    
    
    def initMasses(self):
        """Initialize masses."""
        
        self.mass = objects.formula(self.formula).getMass()
    # ----
    


class enzyme:
    """Enzyme object definition."""
    
    def __init__(self, name='', expression='', nTermFormula='', cTermFormula='', modsBefore=True, modsAfter=True):
        self.name = name
        self.expression = expression
        self.nTermFormula = nTermFormula
        self.cTermFormula = cTermFormula
        self.cTermMass = None # (monoisotopic, average)
        self.nTermMass = None # (monoisotopic, average)
        self.modsBefore = modsBefore
        self.modsAfter = modsAfter
        
        # init masses
        self.initMasses()
    # ----
    
    
    def initMasses(self):
        """Initialize masses."""
        
        self.nTermMass = objects.formula(self.nTermFormula).getMass()
        self.cTermMass = objects.formula(self.cTermFormula).getMass()
    # ----
    


class modification:
    """Modification object definition."""
    
    def __init__(self, name='', gainFormula='', lossFormula='', aminoSpecifity='', termSpecifity='', description=''):
        self.name = name
        self.gainFormula = gainFormula
        self.lossFormula = lossFormula
        self.mass = None # (monoisotopic, average)
        self.aminoSpecifity = aminoSpecifity
        self.termSpecifity = termSpecifity
        self.description = description
        
        # init masses
        self.initMasses()
    # ----
    
    
    def initMasses(self):
        """Initialize masses."""
        
        gain = objects.formula(self.gainFormula).getMass()
        loss = objects.formula(self.lossFormula).getMass()
        self.mass = (gain[0]-loss[0], gain[1]-loss[1])
    # ----
    


class fragment:
    """Peptide ion fragment object definition."""
    
    def __init__(self, name='', terminus='', specifity='', cTermFormula='', nTermFormula='', lossFormula='', termFilter=(False,False)):
        self.name = name
        self.terminus = terminus
        self.specifity = specifity
        self.cTermFormula = cTermFormula # C-term gain/loss
        self.nTermFormula = nTermFormula # N-term gain/loss
        self.lossFormula = lossFormula # neutral loss
        self.cTermMass = None # (monoisotopic, average)
        self.nTermMass = None # (monoisotopic, average)
        self.lossMass = None # (monoisotopic, average)
        self.termFilter = termFilter # (N,C)
        
        # init masses
        self.initMasses()
    # ----
    
    
    def initMasses(self):
        """Initialize masses."""
        
        self.nTermMass = objects.formula(self.nTermFormula).getMass()
        self.cTermMass = objects.formula(self.cTermFormula).getMass()
        self.lossMass = objects.formula(self.lossFormula).getMass()
    # ----
    



# BLOCKS LOADING FUNCTIONS
# ------------------------

def loadElements(path=config.blocksPath+'/elements.xml'):
    """Parse elements XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get elements
    container = {}
    elementTags = document.getElementsByTagName('element')
    for x, elementTag in enumerate(elementTags):
        
        # get symbol, name and atomic number
        name = elementTag.getAttribute('name')
        symbol = str(elementTag.getAttribute('symbol'))
        atomicNumber = elementTag.getAttribute('atomicNumber')
        
        # get masses
        massTags = elementTag.getElementsByTagName('mass')
        massMo = float(massTags[0].getAttribute('monoisotopic'))
        massAv = float(massTags[0].getAttribute('average'))
        mass = (massMo, massAv)
        
        # get isotopes
        isotopes = {}
        isotopeTags = elementTag.getElementsByTagName('isotope')
        for isotopeTag in isotopeTags:
            massNumber = isotopeTag.getAttribute('massNumber')
            imass = float(isotopeTag.getAttribute('mass'))
            abundance = float(isotopeTag.getAttribute('abundance'))
            isotopes[massNumber] = (imass,abundance)
        
        # make object
        container[symbol] = element( \
                name=name, \
                symbol=symbol, \
                atomicNumber=atomicNumber, \
                isotopes=isotopes \
            )
        
    return container
# ----


def loadAminoacids(path=config.blocksPath+'/aminoacids.xml'):
    """Parse amino acid XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get aminoacids
    container = {}
    aminoacidTags = document.getElementsByTagName('aminoacid')
    for x, aminoacidTag in enumerate(aminoacidTags):
        
        # get basic data
        name = aminoacidTag.getAttribute('name')
        symbol = aminoacidTag.getAttribute('symbol')
        abbr = aminoacidTag.getAttribute('abbr')
        formula = aminoacidTag.getAttribute('formula')
        
        # make object
        container[symbol] = aminoacid( \
                name=name, \
                symbol=symbol, \
                formula=formula, \
                abbr=abbr \
            )
        
    return container
# ----


def loadEnzymes(path=config.blocksPath+'/enzymes.xml'):
    """Parse enzymes XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get enzymes
    container = {}
    enzymeTags = document.getElementsByTagName('enzyme')
    for x, enzymeTag in enumerate(enzymeTags):
        
        # get name
        name = str(enzymeTag.getAttribute('name'))
        
        # get expression
        expressionTags = enzymeTag.getElementsByTagName('expression')
        expression = str(expressionTags[0].childNodes[0].data)
        
        # get formula
        formulaTags = enzymeTag.getElementsByTagName('formula')
        cTermFormula = str(formulaTags[0].getAttribute('cTerm'))
        nTermFormula = str(formulaTags[0].getAttribute('nTerm'))
        
        # allowed modifications
        allowModsTags = enzymeTag.getElementsByTagName('allowMods')
        modsBefore = bool(int(allowModsTags[0].getAttribute('before')))
        modsAfter = bool(int(allowModsTags[0].getAttribute('after')))
        
        # add enzyme to dico
        container[name] = enzyme( \
                name=name, \
                expression=expression, \
                cTermFormula=cTermFormula, \
                nTermFormula=nTermFormula, \
                modsBefore=modsBefore, \
                modsAfter=modsAfter \
            )
        
    return container
# ----


def loadModifications(path=config.blocksPath+'/modifications.xml'):
    """Parse modifications XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get modifications
    container = {}
    modificationTags = document.getElementsByTagName('modification')
    for x, modificationTag in enumerate(modificationTags):
        
        # get name
        name = str(modificationTag.getAttribute('name'))
        
        # get formulas
        formulaTags = modificationTag.getElementsByTagName('formula')
        gainFormula = str(formulaTags[0].getAttribute('gain'))
        lossFormula = str(formulaTags[0].getAttribute('loss'))
        
        # get specifity
        specifityTags = modificationTag.getElementsByTagName('specifity')
        aminoSpecifity = str(specifityTags[0].getAttribute('amino'))
        termSpecifity = str(specifityTags[0].getAttribute('terminus'))
        
        # get description
        descriptionTags = modificationTag.getElementsByTagName('description')
        description = _getNodeText(descriptionTags[0])
        
        # add modification
        container[name] = modification( \
                name=name, \
                gainFormula=gainFormula, \
                lossFormula=lossFormula, \
                aminoSpecifity=aminoSpecifity, \
                termSpecifity=termSpecifity, \
                description=description \
            )
        
    return container
# ----


def loadFragments(path=config.blocksPath+'/fragments.xml'):
    """Parse fragments XML and get data."""
    
    # parse XML
    document = xml.dom.minidom.parse(path)
    
    # get fragments
    container = {}
    fragmentTags = document.getElementsByTagName('fragment')
    for x, fragmentTag in enumerate(fragmentTags):
        
        # get basic data
        name = fragmentTag.getAttribute('name')
        terminus = fragmentTag.getAttribute('terminus')
        specifity = fragmentTag.getAttribute('specifity')
        
        # get formula
        formulaTags = fragmentTag.getElementsByTagName('formula')
        cTermFormula = str(formulaTags[0].getAttribute('cTerm'))
        nTermFormula = str(formulaTags[0].getAttribute('nTerm'))
        lossFormula = str(formulaTags[0].getAttribute('neutralLoss'))
        
        # get filter
        termFilterTags = fragmentTag.getElementsByTagName('termFilter')
        nTerm = bool(int(termFilterTags[0].getAttribute('nTerm')))
        cTerm = bool(int(termFilterTags[0].getAttribute('cTerm')))
        termFilter = (nTerm, cTerm)
        
        # make object
        container[name] = fragment(
                name=name, \
                terminus=terminus, \
                specifity=specifity, \
                cTermFormula=cTermFormula, \
                nTermFormula=nTermFormula, \
                lossFormula=lossFormula, \
                termFilter=termFilter \
            )
        
    return container
# ----


def _getNodeText(node):
    """Get text from node list."""
    
    buff = ''
    for node in node.childNodes:
        if node.nodeType == node.TEXT_NODE:
            buff += node.data
    
    return buff
# ----



# BLOCKS SAVING FUNCTIONS
# -----------------------

def saveElements(path=config.blocksPath+'/elements.xml'):
    """Make and save elements XML."""
    
    data = makeElementsXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def saveAminoacids(path=config.blocksPath+'/aminoacids.xml'):
    """Make and save aminoacids XML."""
    
    data = makeAminoacidsXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def saveEnzymes(path=config.blocksPath+'/enzymes.xml'):
    """Make and save enzymes XML."""
    
    data = makeEnzymesXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def saveModifications(path=config.blocksPath+'/modifications.xml'):
    """Make and save modifications XML."""
    
    data = makeModificationsXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def saveFragments(path=config.blocksPath+'/fragments.xml'):
    """Make and save fragments XML."""
    
    data = makeFragmentsXML()
    try:
        save = file(path, 'w')
        save.write(data.encode("utf-8"))
        save.close()
        return True
    except:
        return False
# ----


def makeElementsXML():
    """Format elements to XML"""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mspyElements version="1.0">\n'
    
    symbols = elements.keys()
    symbols.sort()
    for symbol in symbols:
        buff += '  <element symbol="%s" name="%s" atomicNumber="%s">\n' % (elements[symbol].symbol, elements[symbol].name, elements[symbol].atomicNumber)
        buff += '    <mass monoisotopic="%s" average="%s" />\n' % elements[symbol].mass
        buff += '    <isotopes>\n'
        
        isotopes = elements[symbol].isotopes.keys()
        isotopes.sort()
        for isotope in isotopes:
            buff += '      <isotope massNumber="%s" mass="%s" abundance="%s" />\n' % (isotope, elements[symbol].isotopes[isotope][0], elements[symbol].isotopes[isotope][1])
        
        buff += '    </isotopes>\n'
        buff += '  </element>\n'
        
    buff += '</mspyElements>'
    return buff
# ----


def makeAminoacidsXML():
    """Format aminoacids to XML"""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mspyAminoacids version="1.0">\n'
    
    symbols = aminoacids.keys()
    symbols.sort()
    for symbol in symbols:
        buff += '  <aminoacid symbol="%s" name="%s" abbr="%s" formula="%s" />\n' % (aminoacids[symbol].symbol, aminoacids[symbol].name, aminoacids[symbol].abbr, aminoacids[symbol].formula)
        
    buff += '</mspyAminoacids>'
    return buff
# ----


def makeEnzymesXML():
    """Format enzymes to XML"""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mspyEnzymes version="1.0">\n'
    
    names = enzymes.keys()
    names.sort()
    for name in names:
        buff += '  <enzyme name="%s">\n' % (enzymes[name].name)
        buff += '    <expression><![CDATA[%s]]></expression>\n' % (enzymes[name].expression)
        buff += '    <formula nTerm="%s" cTerm="%s" />\n' % (enzymes[name].nTermFormula, enzymes[name].cTermFormula)
        buff += '    <allowMods before="%s" after="%s" />\n' % (int(enzymes[name].modsBefore), int(enzymes[name].modsAfter))
        buff += '  </enzyme>\n'
        
    buff += '</mspyEnzymes>'
    return buff
# ----


def makeModificationsXML():
    """Format modifications to XML"""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mspyModifications version="1.0">\n'
    
    names = modifications.keys()
    names.sort()
    for name in names:
        buff += '  <modification name="%s">\n' % (modifications[name].name)
        buff += '    <description>%s</description>\n' % (modifications[name].description)
        buff += '    <formula gain="%s" loss="%s" />\n' % (modifications[name].gainFormula, modifications[name].lossFormula)
        buff += '    <specifity amino="%s" terminus="%s" />\n' % (modifications[name].aminoSpecifity, modifications[name].termSpecifity)
        buff += '  </modification>\n'
        
    buff += '</mspyModifications>'
    return buff
# ----


def makeFragmentsXML():
    """Format fragments to XML"""
    
    buff = '<?xml version="1.0" encoding="utf-8" ?>\n'
    buff += '<mspyFragments version="1.0">\n'
    
    names = fragments.keys()
    names.sort()
    for name in names:
        buff += '  <fragment name="%s" terminus="%s" specifity="%s">\n' % (fragments[name].name, fragments[name].terminus, fragments[name].specifity)
        buff += '    <formula nTerm="%s" cTerm="%s" neutralLoss="%s" />\n' % (fragments[name].nTermFormula, fragments[name].cTermFormula, fragments[name].lossFormula)
        buff += '    <termFilter nTerm="%s" cTerm="%s" />\n' % (int(fragments[name].termFilter[0]), int(fragments[name].termFilter[1]))
        buff += '  </fragment>\n'
        
    buff += '</mspyFragments>'
    return buff
# ----



# LOAD BASIC BLOCKS
# -----------------

elements = loadElements()
aminoacids = loadAminoacids()
enzymes = loadEnzymes()
modifications = loadModifications()
fragments = loadFragments()
