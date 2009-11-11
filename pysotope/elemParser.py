#########################################################################
# Author: Toni Lee with the help of Guilherme Freitas and Becky Tucker
# Copyright: This module has been placed in the public domain
#########################################################################

#Import regular expressions
import re
from pyelements import elemDict

#Create the dictionary (From Becky with a value of 0 inserted for Uus(mass not measurable))
TableofElements ={ 'H':1.00794,'He':4.002602,'Li':6.941,'Be':9.012182,
                        'B':10.811,'C':12.0107,'N':14.0067,'O':15.9994,'F':18.9984032,'Ne':20.1797,
                        'Na':22.98976928,'Mg':24.3050,'Al':26.9815386,'Si':28.0855,
                        'P':30.973762,'S':32.065,'Cl':35.453,'Ar':39.948,'K':39.0983,'Ca':40.078,
                        'Sc':44.955912,'Ti':47.867,'V':50.9415,'Cr':51.9961,'Mn':54.938045,
                        'Fe':55.845,'Ni':58.6934,'Co':58.933195,'Cu':63.546,'Zn':65.38,'Ga':69.723,
                        'Ge':72.64,'As':74.92160,'Se':78.96,'Br':79.904,'Kr':83.798,'Rb':85.4678,
                        'Sr':87.62,'Y':88.90585,'Zr':91.224,'Nb':92.90638,'Mo':95.96,'Tc':98,
                        'Ru':101.07,'Rh':102.90550,'Pd':106.42,'Ag':107.8682,'Cd':112.411,
                        'In':114.818,'Sn':118.710,'Sb':121.760,'Te':127.60,'I':126.90447,
                        'Xe':131.293,'Cs':132.9054519,'Ba':137.327,'La':138.90547,'Ce':140.116,
                        'Pr':140.90765,'Nd':144.242,'Pm':145,'Sm':150.36,'Eu':151.964,'Gd':157.25,
                        'Tb':158.92535,'Dy':162.500,'Ho':164.93032,'Er':167.259,'Tm':168.93421,
                        'Yb':173.054,'Lu':174.9668,'Hf':178.49,'Ta':180.94788,'W':183.84,
                        'Re':186.207,'Os':190.23,'Ir':192.217,'Pt':195.084,'Au':196.966569,
                        'Hg':200.59,'Tl':204.3833,'Pb':207.2,'Bi':208.98040,'Po':210,'At':210,
                        'Rn':220,'Fr':223,'Ra':226,'Ac':227,'Th':232.03806,'Pa':231.03588,
                        'U':238.02891,'Np':237,'Pu':244,'Am':243,'Cm':247,'Bk':247,'Cf':251,
                        'Es':252,'Fm':257,'Md':258,'No':259,'Lr':262,'Rf':261,'Db':262,'Sg':266,
                        'Bh':264,'Hs':277,'Mt':268,'Ds':271,'Rg':272, 'Uus':0
}

TableofElementsList=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl',\
                     'Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Ni','Co','Cu','Zn','Ga','Ge','As',\
                     'Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In',\
                     'Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb',\
                     'Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl',\
                     'Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk',\
                     'Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg', 'Uus']


#######################################
#Computes the MW of an atom-number pair
#######################################
def getMass(x):
    atom=re.findall('[A-Z][a-z]*',x)
    number=re.findall('[0-9]+', x)
    if len(number) == 0:
        multiplier = 1
    else:
        multiplier = float(number[0])
    if elemDict.has_key(atom[0]):
#        atomic_mass=TableofElements[atom[0]]
        atomic_mass=elemDict[atom[0]].mass#TableofElements[atom[0]]
    else:
        atomic_mass = 0.0

    return (atomic_mass*multiplier)

################################################################
#Segments formula into atom-number sections (i.e. 'H3' or 'N10')
################################################################
def parseFormula(fragment):
    segments=re.findall('[A-Z][a-z]*[0-9]*',fragment)
    return (segments)

##################################################################################
#Computes total mass of both parenthetical and nonparenthetical formula components
##################################################################################
def molmass(formula):
    formula = validateStr(formula)
    if '))' in formula:
        return 0
    parenMass=0
    nonparenMass=0
    while (len(formula)>0):
        #First computes the molecular weight of all parenthetical formulas from left to right
        while (len(re.findall('\(\w*\)[0-9]+', formula))!=0):
            parenthetical=re.findall('\(\w*\)[0-9]+',formula)
            for i in range(0,len(parenthetical)):
                parenMult1 = re.findall('\)[0-9]+', parenthetical[i])
#                print "ParenMult1", parenMult1, parenthetical[i]
                parenMult2 = re.findall('[0-9]+', parenMult1[0])
#                print "ParentMult2", parenMult2
                segments =parseFormula(parenthetical[i])
#                print "Segments", segments
                for i in range(0, len(segments)):
                    parenMass= parenMass + ((getMass(segments[i]))*(float(parenMult2[0])))
            formula=re.sub('\(\w*\)[0-9]+', '', formula)
        #Sums nonparenthetical molecular weights when all parenthetical molecular weights have been summed
        segments = parseFormula(formula)
#        print "Segments", segments
        for i in range(0, len(segments)):
            nonparenMass=nonparenMass + getMass(segments[i])
        formula=re.sub(formula, '', formula)

    Mass=parenMass+nonparenMass
    return Mass


def getAtoms(formula):
    formula = validateStr(formula)
    if '))' in formula:
        return False
    atoms = []
    numAtoms = []
    while (len(formula)>0):
        #First computes the molecular weight of all parenthetical formulas from left to right
        while (len(re.findall('\(\w*\)[0-9]+', formula))!=0):
            parenthetical=re.findall('\(\w*\)[0-9]+',formula)
            for i in range(0,len(parenthetical)):
                parenMult1 = re.findall('\)[0-9]+', parenthetical[i])
#                print "ParenMult1", parenMult1, parenthetical[i]
                parenMult2 = re.findall('[0-9]+', parenMult1[0])
#                print "ParentMult2", parenMult2
                segments =parseFormula(parenthetical[i])
#                print "Segments", segments
                for i in range(0, len(segments)):
                    multFactor = re.findall('[0-9]+', segments[i])
                    subSegs = re.findall('[A-Z][a-z]*',segments[i])
#                    print "MultiFactor: ", multFactor
#                    print "Subsegs: ", subSegs
                    for seg in subSegs:
                        atoms.append(seg)
                        if len(parenMult2)>0:
                            coreNum = int(parenMult2[0])
                        else:
                            coreNum = 1
                        if len(multFactor)>0:
                            multNum = int(multFactor[0])
                            numAtoms.append(coreNum*multNum)
                        else:
                            numAtoms.append(coreNum)

            formula=re.sub('\(\w*\)[0-9]+', '', formula)
        #Sums nonparenthetical molecular weights when all parenthetical molecular weights have been summed
        segments = parseFormula(formula)
#        print "Segments", segments
        for i in range(0, len(segments)):
            multFactor = re.findall('[0-9]+', segments[i])
            subSegs = re.findall('[A-Z][a-z]*',segments[i])
#            print "MultiFactor: ", multFactor
#            print "Subsegs: ", subSegs
            for seg in subSegs:
                atoms.append(seg)
                if len(multFactor)>0:
                    multNum = int(multFactor[0])
                    numAtoms.append(1*multNum)
                else:
                    numAtoms.append(1)

        formula=re.sub(formula, '', formula)


    return True, atoms, numAtoms


def validateStr(potentialStr):
    _NON_ASCII = re.compile('[^a-zA-Z0-9()]+')#re.compile('[^-~]')
    print _NON_ASCII.sub('', potentialStr)
    return _NON_ASCII.sub('', potentialStr)
    #re.findall(_NON_ASCII, potentialStr)#, string, flags)


if __name__ == '__main__':
    test = ['C', 'Na', 'NaCl', 'H2O', 'Ag14Uus3', 'CoFFeEs12']
    test_alt = ['CoFFeEs', 'BeNiCe', 'LiEr', 'GaIn', 'AmErICa', 'U2', \
            'UVRaY']
    test_paren= ['Co(FFeEs)2', 'Be(Ni)2Ce', '(LiEr)4', '(Ga)3In', '(AmErICa)4', '(U2)6', \
            'UVRaY', 'CO4(O2)3(BaH3)33']
#    for element in test:
#        print ('The mass of %(substance)s is %(Mass)f.' % {'substance': \
#                element, 'Mass': molmass(element)})
#    for element in test_alt:
#        print ('The mass of %(substance)s is %(Mass)f.' % {'substance': \
#                element, 'Mass': molmass(element)})
    for element in test_paren:
        print getAtoms(element)
        print " "
#        print ('The mass of %(substance)s is %(Mass)f.' % {'substance': \
#                element, 'Mass': molmass(element)})
#    print molmass('CO2')
#    validateStr('Joe@#$%@()._')
#    print type(molmass('3')), molmass('$@$#%#')