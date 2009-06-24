# -*- coding: utf-8 -*-
"""
Pydee Editor

This temporary script file is located here:
C:\Documents and Settings\d3p483\.pydee\.temp.py
"""

import xml.etree.cElementTree as ET
import os, sys, traceback

fragType = ['a','b','c','x','y','z']

xtInputDict = {}
xtInputDict['maxCharge']='spectrum, maximum parent charge'
xtInputDict['defaultPath'] = "list path, default parameters"
xtInputDict['taxonomyPath'] = "list path, taxonomy information"
xtInputDict['fragSpecError'] = "spectrum, fragment monoisotopic mass error"
xtInputDict['parentErrPos'] = "spectrum, parent monoisotopic mass error plus"
xtInputDict['parentErrNeg'] = "spectrum, parent monoisotopic mass error minus"
xtInputDict['isotopeErr'] = "spectrum, parent monoisotopic mass isotope error"#use isotope error?
xtInputDict['fragUnits'] = "spectrum, fragment monoisotopic mass error units"#Daltons or ppm
xtInputDict['parentUnits'] = "spectrum, parent monoisotopic mass error units"#Daltons or ppm
xtInputDict['fragMassType'] = "spectrum, fragment mass type"#monoisotopic or average
xtInputDict['totalPeaks'] = "spectrum, total peaks"
xtInputDict['maxCharge'] = "spectrum, maximum parent charge"
xtInputDict['noiseSupress'] = "spectrum, use noise suppression"
xtInputDict['minParentMZ'] = "spectrum, minimum parent m+h"
xtInputDict['minFragMZ'] = "spectrum, minimum fragment mz"
xtInputDict['minPeaks'] = "spectrum, minimum peaks"
xtInputDict['threads'] = "spectrum, threads"
xtInputDict['aaModStr'] = "residue, modification mass"
'''
The format of this parameter is m@X, where m is the modfication
        mass in Daltons and X is the appropriate residue to modify. Lists of
        modifications are separated by commas. For example, to modify M and C
        with the addition of 16.0 Daltons, the parameter line would be
        +16.0@M,+16.0@C
'''

xtInputDict['potentialModMass'] = "residue, potential modification mass"
'''
    xtInputDict['"residue, potential modification motif"></note>
        <note>The format of this parameter is similar to residue, modification mass,
        with the addition of a modified PROSITE notation sequence motif specification.
        For example, a value of 80@[ST!]PX[KR] indicates a modification
        of either S or T when followed by P, and residue and the a K or an R.
        A value of 204@N!{P}[ST]{P} indicates a modification of N by 204, if it
        is NOT followed by a P, then either an S or a T, NOT followed by a P.
        Positive and negative values are allowed.
        </note>
'''
xtInputDict['potentialModMotif'] = "residue, potential modification motif"

xtInputDict['taxon'] = "protein, taxon"
'''
    xtInputDict['"protein, cleavage site">[RK]|{P}</note>
        <note>this setting corresponds to the enzyme trypsin. The first characters
        in brackets represent residues N-terminal to the bond - the '|' pipe -
        and the second set of characters represent residues C-terminal to the
        bond. The characters must be in square brackets (denoting that only
        these residues are allowed for a cleavage) or french brackets (denoting
        that these residues cannot be in that position). Use UPPERCASE characters.
        To denote cleavage at any residue, use [X]|[X] and reset the
        scoring, maximum missed cleavage site parameter (see below) to something like 50.
        </note>
'''
xtInputDict['cleavageSite'] = "protein, cleavage site"

xtInputDict['protCTermChange'] = "protein, cleavage C-terminal mass change"#>+17.002735</note>
xtInputDict['protNTermChange'] = "protein, cleavage N-terminal mass change"#>+1.007825</note>
xtInputDict['protNModMass'] = "protein, N-terminal residue modification mass"#>0.0</note>
xtInputDict['protCModMass'] = "protein, C-terminal residue modification mass"#>0.0</note>

xtInputDict['refine'] = "refine"#>yes</note>
xtInputDict['refineModMass'] = "refine, modification mass"#></note>
#xtInputDict[''] = "refine, sequence path"#></note>
xtInputDict['ticPercent'] = "refine, tic percent"#>20</note>
xtInputDict['synthesizeSpec'] = "refine, spectrum synthesis"#>yes</note>
xtInputDict['maxEValue'] = "refine, maximum valid expectation value"#>0.1</note>
xtInputDict['refinePotNTermMod'] = "refine, potential N-terminus modifications"#>+42.010565@[</note>
xtInputDict['refinePotCTermMod'] = "refine, potential C-terminus modifications"#></note>
xtInputDict['refineUnanticipated'] = "refine, unanticipated cleavage"#>yes</note>
#xtInputDict[''] = "refine, potential modification mass"#></note>
xtInputDict['pointMutations1'] = "refine, point mutations"#>no</note>
xtInputDict['useModsforFull'] = "refine, use potential modifications for full refinement"#>no</note>
xtInputDict['pointMutations2'] = "refine, point mutations"#>no</note>
xtInputDict['refinePotModMotif'] = "refine, potential modification motif"#></note>
'''
<note>The format of this parameter is similar to residue, modification mass,
    with the addition of a modified PROSITE notation sequence motif specification.
    For example, a value of 80@[ST!]PX[KR] indicates a modification
    of either S or T when followed by P, and residue and the a K or an R.
    A value of 204@N!{P}[ST]{P} indicates a modification of N by 204, if it
    is NOT followed by a P, then either an S or a T, NOT followed by a P.
    Positive and negative values are allowed.
    </note>
'''
xtInputDict['minIonCount'] = "scoring, minimum ion count"
xtInputDict['maxMissedCleavages'] = "scoring, maximum missed cleavage sites"
xtInputDict['xIons'] = "scoring, x ions"
xtInputDict['yIons'] = "scoring, y ions"
xtInputDict['zIons'] = "scoring, z ions"
xtInputDict['aIons'] = "scoring, a ions"
xtInputDict['bIons'] = "scoring, b ions"
xtInputDict['cIons'] = "scoring, c ions"



def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent(child, level+1)
        if not child.tail or not child.tail.strip():
            child.tail = i
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def getTaxonomyList(fileName='taxonomy.xml'):
    taxa = []
    try:

        root = ET.parse(fileName).getroot()
        children = root.getchildren()
        for child in children:
            taxa.append(child.get('label'))

        return taxa

    except:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
        errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
        #return QtGui.QMessageBox.warning(self, "Save Preferences Error", errorMsg)
        print errorMsg
        return []



def testETree():
    root = ET.Element('xml', version = '1.0')
    head = ET.SubElement(root, "bioml")
    note = ET.SubElement(head, "note")
    note.text = "GO Joe"
    note1 = ET.SubElement(head, "note", type = "input", label = "protein, taxon")
    note1.text = 'yeast'
    note2 = ET.SubElement(head, "note", type = "input", label = "list path, default parameters")
    note2.text='default_input.xml'
    note3 = ET.SubElement(head, "note", type = "input", label = "list path, taxonomy information")
    note3.text='taxonomy.xml'
    note4 = ET.SubElement(head, "note", type = "input", label = "spectrum, path")
    note4.text='test_spectra.mgf'
    note5 = ET.SubElement(head, "note", type = "input", label = "output, path")
    note5.text='test_spectra.mgf'
    note5.text = 'clowers.xml'
    indent(root)
    tree = ET.ElementTree(root)
    tree.write("test1.xml", encoding = 'utf-8')

if __name__ == "__main__":
    print xtInputDict
    taxa = getTaxonomyList()
    if len(taxa)>0:
        print taxa
    testETree()