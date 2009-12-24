#!/usr/bin/python
import os, sys, traceback
import xml.etree.ElementTree as ET#need to use correctly with py2exe
import xml.etree.cElementTree as ET#I know seems redundant but is needed by py2exe



def readXML(fileName):
    if os.path.isfile(fileName):
        xml = open(fileName, 'r')
        xmlText = xml.read()
        xml.close()
        print xmlText
#        self.setOutputText(QtCore.QString(xmlText))

def modXML(fileName, inputFile, outputPath):
    '''
    modifies a standard x!tandem input file to utilize a different input and output path
    '''
    outPathKey = "output, path"
    dataPathKey = "spectrum, path"
    coreName = ''
    if os.path.isfile(inputFile):
        coreName = os.path.basename(inputFile)

    xml = open(fileName, 'r')
    r = ET.parse(xml).getroot()
    rr = r[0]
    if 'bioml' in rr.tag:
        for node in rr:
            if node.get('label') == outPathKey:
                if os.path.isdir(outputPath):
                    fullOutPath = os.path.join(outputPath, coreName)
                    node.text = fullOutPath
            elif node.get('label') == dataPathKey:
                if os.path.isfile(inputFile):
                    node.text = inputFile
            print node.get('label'), node.text
    xml.close()
    tree = ET.ElementTree(r)
    tree.write('queueXTInput.xml', encoding = 'utf-8')


if __name__ == "__main__":
#    readXML('pyInput.xml')
    modXML('/home/clowers/workspace/DaQueue/pyInput.xml', '/home/clowers/workspace/DaQueue/modXT.py', '/home/clowers/Sandbox')