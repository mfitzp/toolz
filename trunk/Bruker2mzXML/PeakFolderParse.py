import os
from os import walk, path

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog

import time

#try:
#    import psyco
#    psyco.full()
#except:
#    print "Pysco not installed, try easy_install psyco at your command prompt"

def convert2mgf(dataList, newFileName = 'Generic.mgf', msType = 'MALDI'):

    if len(dataList) == 0:
        print "No Data Present"
        return False

    if msType == 'MALDI':
        chargeOK = True
        charge = 1
    else:
        chargeOK = False

    newFile = os.path.abspath(os.path.join(os.path.dirname(dataList[0][0]),newFileName))#mgf = mascot general format
    f = open(newFile, 'w')
    try:
        writeStr = 'MASS=Monoisotopic\n\n'
        f.write(writeStr)
        status = ''
        for item in dataList:
            dataPath = item[0]
            if '.LIFT_pks' in dataPath:
                if os.path.isfile(dataPath):
                    f.write('BEGIN IONS\n')
                    f.write('TITLE=%s\n'%dataPath)
                    if chargeOK:
                        f.write('CHARGE=%s+\n'%charge)
                    nominalMass = dataPath.split('.')[-4]
                    defectMass = dataPath.split('.')[-3]
                    massStr = nominalMass+'.'+defectMass
                    f.write('PEPMASS=%s\n'%massStr)
                    readFile = open(dataPath, 'r')
                    for line in readFile.readlines():
                        lineData = line.split(',')
                        f.write(lineData[0]+' '+lineData[1])



                    readFile.close()
                    f.write('END IONS\n\n')
                    status+='%s read and written\n'%dataPath
                    print '%s read and written'%dataPath
        f.close()
        print "FINISHED WRITING %s"%newFile
        status+="FINISHED WRITING %s\n"%newFile
        return status
    except:
        f.close()



def getPeakFiles(directory):

    if directory == None:
        return []
#        directory= str(QFileDialog.getExistingDirectory())

    print directory

    dirList = []
    i=0
    for root, dirs, files in walk(directory):
        for tempFile in files:
            if 'LIFT_pks.csv' in tempFile:
#                    print root, tempFile
                mzXML = tempFile.replace('_pks.csv','.mzXML')
#                    print mzXML
                tempMZXML = path.abspath(path.join(root, mzXML))
                if os.path.isfile(tempMZXML):
                    temptime = time.clock()
                    i+=1
                    dataPath = path.abspath(path.join(root, tempFile))

                    dirList.append((dataPath, tempFile))

    return dirList

def run_main():
    import sys
#    app = QtGui.QApplication(sys.argv)

    dirList = getPeakFiles('Z:/data/Clowers/051909/LB1_YP_W1_S4')
#    dirList = getPeakFiles('C:/Test')
#    dirList = getPeakFiles()
    print dirList
    convert2mgf(dirList)
    print "Done"
#    sys.exit(app.exec_())



if __name__ == "__main__":
    run_main()
