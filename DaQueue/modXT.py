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
    inputFile = Raw Data File
    outputPath = Output Path File Name
    returns Success and XT input file path
    '''
    #print 'fileName :', fileName
    #print 'inputFile :', inputFile
    print 'Processing :', outputPath

    outPathKey = "output, path"
    dataPathKey = "spectrum, path"
    coreName = ''
    if os.path.isfile(inputFile):
        coreName = os.path.basename(inputFile)

    outputPathDir = os.path.dirname(outputPath)

    modFileName = os.path.join(outputPathDir, 'queueXTInput.xml')

    xml = open(fileName, 'r')
    try:
        r = ET.parse(xml).getroot()
        rr = r[0]
        if 'bioml' in rr.tag:
            for node in rr:
                if node.get('label') == outPathKey:
                    fullOutPath = os.path.abspath(outputPath)
                    node.text = fullOutPath
                elif node.get('label') == dataPathKey:
                    if os.path.isfile(inputFile):
                        node.text = inputFile
                #print node.get('label'), node.text
        xml.close()
        tree = ET.ElementTree(r)
        tree.write(modFileName, encoding = 'utf-8')
        return [True, os.path.abspath(modFileName)]
    except:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
        errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
        print errorMsg
        return [False, None]

if __name__ == "__main__":
#    readXML('pyInput.xml')
    #modXML(fileName, inputFile, outputPath)
    print modXML('/home/clowers/workspace/DaQueue/pyInput.xml', '/home/clowers/workspace/DaQueue/modXT.py', '/home/clowers/Sandbox/id_rsa.pub')