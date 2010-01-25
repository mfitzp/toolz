#!/usr/bin/python

import os

DEBUG = True

if os.sys.platform == 'win32':
    print "Win32"
    ROOTDIR = "C:\ChemBio"
    DBDIR = 'db'
    if DEBUG:
        WATCHDIR = 'C:\ChemBio\Data'
    else:
        WATCHDIR = 'Z:\ChemBio\Data'
else:
    ROOTDIR = '/usr/local/PNL/ChemBio'
    DBDIR = 'db'
    WATCHDIR = '/usr/local/PNL/ChemBio/Data'

STATUSIDS = [0,1,2,3,4]
STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']
STATUSDICT = {0:'Queued', 1:'Processing', 2:'Finished', 3:'Failed', 4:'Waiting for User Action'}

JOBKEYS = [0,1,2,3,4,5,6]
JOBTYPES = ['X!Tandem', 'RAW File Conversion', 'Bruker File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified', 'Ignored']
JOBDICT = {'X!Tandem':0, 'RAW File Conversion':1, 'Bruker File Conversion':2, 'Peak Picking':3, 'Polygraph':4, 'Unspecified':5, 'Ignored':6}

#WATCHDB = 'watchList.db'
QUEUEDB = os.path.join(ROOTDIR,DBDIR,'labqueue.db')
QUEUEDIR = '/workspace/DaQueue'
QUEUETABLE = 'queueTable'
WATCHTABLE = 'watchTable'

CONFIGEXTENSION = '.cfgXML'#, '.db']

#1SRef is a Bruker File Folder Structure that should be ignored
EXCLUDE = ['.svn', '.db', '.cfgXML']
INCLUDED = ['.RAW', '.raw', '1SRef', '.mzXML', '.mzxml']

DBNAME = QUEUEDB#'labqueue.db'
ROOTUSER = 'clowers'

XT_EXE_PATH = ''

try:
    USERNAME = os.login()
except:
    USERNAME = 'TestUser'


if __name__ == "__main__":
    print QUEUEDB, WATCHDIR
    print os.path.isfile(QUEUEDB), os.path.isdir(WATCHDIR)