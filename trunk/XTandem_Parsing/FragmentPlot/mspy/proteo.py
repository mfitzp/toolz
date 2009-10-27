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
from copy import deepcopy

# load configuration
import config

# register essential objects
import blocks
import objects


# COMMON PROTEOMICS RELATED FUNCTIONS
# -----------------------------------

def digest(protein, enzyme, miscleavage=0, allowMods=False, strict=True):
    """Digest given protein by specified enzyme.
        protein: (mspy.sequence) protein to by digested
        enzyme: (str) enzyme name - must b defined in mspy.enzymes
        miscleavage: (int) number of allowed misscleavages
        allowMods: do not care about modifications in cleavage site
        strict: do not cleave even if variable modification is in cleavage site
    """
    
    # check chain
    if len(protein) == 0:
        return []
    
    # get enzyme
    enzyme = blocks.enzymes[enzyme]
    expression = re.compile(enzyme.expression+'$')
    
    # get digest indices
    peptide = ''
    slices = [] # from | to | miscl
    lastIndex = 0
    for x, aa in enumerate(protein.chain):
        peptide += aa
        if expression.search(peptide):
            
            # skip not allowed modifications
            if not allowMods and protein.isModified(x-1, strict) and not enzyme.modsBefore:
                continue
            elif not allowMods and protein.isModified(x, strict) and not enzyme.modsAfter:
                continue
            else:
                slices.append((lastIndex, x, 0))
                lastIndex = x
    
    # add last peptide
    slices.append((lastIndex, x+1, 0))
    
    # add indices for partials
    indices = len(slices)
    for x in range(indices):
        for y in range(1, miscleavage+1):
            if x+y < indices:
                slices.append((slices[x][0], slices[x+y][1], y))
            else:
                break
    
    # get peptides slices from protein
    peptides = []
    for indices in slices:
        peptide = protein[indices[0]:indices[1]]
        peptide.miscleavages = indices[2]
        
        # add terminal groups
        if indices[0] == 0:
            peptide.nTermFormula = protein.nTermFormula
        else:
            peptide.nTermFormula = enzyme.nTermFormula
        if indices[1] == len(protein):
            peptide.cTermFormula = protein.cTermFormula
        else:
            peptide.cTermFormula = enzyme.cTermFormula
        
        peptides.append(peptide)
    
    return peptides
# ----


def fragment(peptide, serie):
    """Generate list of neutral peptide fragments from given peptide.
        peptide: (mspy.sequence) peptide to be fragmented
        serie: (str) fragment serie name - must be defined in mspy.fragments
    """
    
    frags = []
    length = len(peptide)
    
    # get serie definition
    if serie in blocks.fragments:
        serie = blocks.fragments[serie]
    else:
        raise KeyError, 'Unknown fragment type! -> ' + serie
    
    # N-terminal fragments
    if serie.terminus == 'N':
        for x in range(length):
            frag = peptide[:x+1]
            frag.cTermFormula = serie.cTermFormula
            frag.lossFormula = serie.lossFormula
            frag.fragmentSerie = serie.name
            frag.fragmentIndex = (x+1)
            frags.append(frag)
    
    # C-terminal fragments
    elif serie.terminus == 'C':
        for x in range(length):
            frag = peptide[length-(x+1):]
            frag.nTermFormula = serie.nTermFormula
            frag.lossFormula = serie.lossFormula
            frag.fragmentSerie = serie.name
            frag.fragmentIndex = (x+1)
            frags.append(frag)
    
    # internal fragments
    elif serie.terminus == 'I':
        for x in range(1,length-1):
            for y in range(2,length-x):
                frag = peptide[x:x+y]
                frag.nTermFormula = serie.nTermFormula
                frag.cTermFormula = serie.cTermFormula
                frag.lossFormula = serie.lossFormula
                frag.fragmentSerie = serie.name
                frag.fragmentIndex = ((x+1), (x+y))
                frags.append(frag)
    else:
        raise ValueError, 'Unknown fragment terminus! -> ' + serie.terminus
        
    # check fragment specifity
    for x in range(len(frags)):
        frags[x].fragFiltered = True
        for aa in serie.specifity:
            if aa in frags[x].chain:
                frags[x].fragFiltered = False
                break
    
    # filter nonsense fragments
    if frags and serie.terminus == 'N':
        if serie.termFilter[0]:
            frags[0].fragFiltered = True
        if serie.termFilter[1]:
            frags[-1].fragFiltered = True
    elif frags and serie.terminus == 'C':
        if serie.termFilter[0]:
            frags[-1].fragFiltered = True
        if serie.termFilter[1]:
            frags[0].fragFiltered = True
    
    return frags
# ----


def coverage(peptides, length):
    """Calculate sequence coverage.
        peptides: (list of mspy.sequence or list of ranges (start,stop))
        length: (int) parent sequence length
    """
    
    # check data
    if not peptides:
        return 0.
    
    # make blank sequence
    blank = length*[0]
    
    # list of ranges
    if type(peptides) is list and type(peptides[0]) in (list, tuple):
        for peptide in peptides:
            for x in range(peptide[0]-1, peptide[1]):
                blank[x]=(1)
    
    # list of sequence objects
    elif type(peptides) is list and isinstance(peptides[0], objects.sequence):
        for peptide in peptides:
            for x in range(peptide.userRange[0]-1, peptide.userRange[1]):
                blank[x]=(1)
    
    # unknown object
    else:
        raise ValueError, 'List of sequence objects or ranges must be given! -> ' + str(type(peptides))
    
    # get sequence coverage
    return 100.0*blank.count(1)/length
# ----


def variateMods(peptide, position=True, maxMods=1, enzyme=None):
    """Calculate all possible combinations of variable modifications for given peptide.
        peptide: (mspy.sequence) peptide to be variated
        position: (bool) retain modifications positions (much slower)
        maxMods: (int) maximum modifications allowed per one residue
        enzyme: (str or None) enzyme name to ensure that modifications are not presented in cleavage site
    """
    
    variablePeptides = []
    
    # get modifications
    fixedMods = []
    variableMods = []
    for mod in peptide.modifications:
        if mod[2] == 'f':
            fixedMods.append(mod)
        elif type(mod[1]) == int:
            variableMods.append(mod)
        else:
            if not position:
                variableMods += [mod] * peptide.chain.count(mod[1])
            else:
                for x, amino in enumerate(peptide.chain):
                    if amino == mod[1]:
                        variableMods.append([mod[0], x, 'v'])
    
    # make combinations of variable modifications
    variableMods = _countUniqueModifications(variableMods)
    combinations = []
    for x in _uniqueCombinations(variableMods):
        combinations.append(x)
    
    # filter modifications on same amino
    if maxMods:
        buff = []
        for combination in combinations:
            valid = True
            indexes = []
            for mod in combination:
                indexes += [mod[0][1]]*mod[1]
                if not position and type(mod[0][1]) in (str, unicode):
                    maxMods = peptide.chain.count(mod[0][1])
                if indexes.count(mod[0][1])>maxMods:
                    valid = False
                    break
            if valid:
                buff.append(combination)
        combinations = buff
    
    # filter modifications by enzyme
    if enzyme:
        enz = blocks.enzymes[enzyme]
        if not enz.modsBefore or not enz.modsAfter:
            
            if position:
                amino = (0,len(peptide)-1)
            else:
                amino = (peptide.chain[0],peptide.chain[-1])
                count = (peptide.chain.count(amino[0]),peptide.chain.count(amino[1]))
            
            buff = []
            for combination in combinations:
                valid = True
                indexes = []
                for mod in combination:
                    indexes += [mod[0][1]]*mod[1]
                    
                    if not enz.modsBefore and peptide.aaAfter and mod[0][1]==amino[1]:
                        if position or indexes.count(mod[0][1])>=count[1]:
                            valid = False
                            break
                    elif not enz.modsAfter and peptide.aaBefore and mod[0][1]==amino[0]:
                        if position or indexes.count(mod[0][1])>=count[0]:
                            valid = False
                            break
                
                if valid:
                    buff.append(combination)
            combinations = buff
    
    # format modifications and filter same
    buff = []
    for combination in combinations:
        mods = []
        
        for mod in combination:
            if position:
                mods += [mod[0]]*mod[1]
            else:
                mods += [[mod[0][0],'',mod[0][2]]]*mod[1]
        
        mods.sort()
        if not mods in buff:
            buff.append(mods)
        
    combinations = buff
    
    # make new peptides
    for combination in combinations:
        variablePeptide = deepcopy(peptide)
        variablePeptide.modifications = fixedMods+combination
        variablePeptide.modifications.sort()
        variablePeptides.append(variablePeptide)
    
    return variablePeptides
# ----


def searchSequence(protein, mass, charge, tolerance, enzyme=None, tolUnits='Da', massType='Mo', maxMods=1, position=False):
    """Search sequence for specified mass.
        protein: (mspy.sequence) protein sequence to be searched
        mass: (float) m/z value to search for
        charge: (int) charge of the mass value
        tolerance: (float) mass tolerance
        tolUnits: ('Da', 'ppm') tolerance units
        enzyme: (str or None) enzyme used for peptides endings, if None H/OH is used
        massType: ('Mo' or 'Av') mass type of the mass value
        maxMods: (int) maximum number of modifications at one residue
        position: (bool) retain position for variable modifications (much slower)
    """
    
    matches = []
    
    # set mass type
    massType = 0
    if massType == 'Av':
        massType = 1
    
    # set terminal modifications
    if enzyme:
        enzyme = blocks.enzymes[enzyme]
        nTerm = enzyme.nTermFormula
        cTerm = enzyme.cTermFormula
    else:
        nTerm = 'H'
        cTerm = 'OH'
    
    # set mass limits
    if tolUnits == 'ppm':
        lowMass = mass - (tolerance * mass/1000000)
        highMass = mass + (tolerance * mass/1000000)
    else:
        lowMass = mass - tolerance
        highMass = mass + tolerance
    
    # search sequence
    length = len(protein)
    for i in range(length):
        for j in range(i+1, length+1):
            
            # get peptide
            peptide = protein[i:j]
            if enzyme:
                if i != 0:
                    peptide.setTerminalFormula('N', nTerm)
                if j != length:
                    peptide.setTerminalFormula('C', cTerm)
            
            # variate modifications
            variants = variateMods(peptide, position=position, maxMods=maxMods)
            
            # search
            skip = True
            for pep in variants:
                current = pep.getMZ(charge)[massType]
                if lowMass <= current <= highMass:
                    matches.append(pep)
                if current < highMass:
                    skip = False
            if skip:
                break
    
    return matches
# ----



# HELPER FUNCTIONS
# ----------------

def _uniqueCombinations(items):
    """Generate unique combinations of items"""
    
    for i in range(len(items)):
        for cc in _uniqueCombinations(items[i+1:]):
            for j in range(items[i][1]):
                yield [[items[i][0],items[i][1]-j]] + cc
    yield []
# ----


def _countUniqueModifications(mods):
    """Get list of unique modifications with counter"""
    
    uniqueMods = []
    modsCount = []
    for mod in mods:
        if mod in uniqueMods:
            modsCount[uniqueMods.index(mod)] +=1
        else:
            uniqueMods.append(mod)
            modsCount.append(1)
    
    modsList = []
    for x, mod in enumerate(uniqueMods):
        modsList.append([mod, modsCount[x]])
    
    return modsList
# ----

