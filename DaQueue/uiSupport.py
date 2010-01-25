#!/usr/bin/python

import os

STATUSIDS = [0,1,2,3,4]
STATUSTYPES = ['Queued', 'Processing', 'Finished', 'Failed', 'Waiting for User Action']
STATUSDICT = {0:'Queued', 1:'Processing', 2:'Finished', 3:'Failed', 4:'Waiting for User Action'}

JOBKEYS = [0,1,2,3,4,5,6]
JOBTYPES = ['X!Tandem', 'RAW File Conversion', 'Bruker File Conversion', 'Peak Picking', 'Polygraph', 'Unspecified', 'Ignored']
JOBDICT = {'X!Tandem':0, 'RAW File Conversion':1, 'Bruker File Conversion':2, 'Peak Picking':3, 'Polygraph':4, 'Unspecified':5, 'Ignored':6}

#WATCHDB = 'watchList.db'
QUEUEDB = 'labqueue.db'
QUEUEDIR = '/workspace/DaQueue'
QUEUETABLE = 'queueTable'
WATCHTABLE = 'watchTable'
CONFIGEXTENSION = '.cfgXML'#, '.db']

#1SRef is a Bruker File Folder Structure that should be ignored
EXCLUDE = ['.svn', '.db', '.cfgXML']
INCLUDED = ['.RAW', '.raw','.mzXML', '1SRef']

DBNAME = 'labqueue.db'
QUEUETABLE = 'queueTable'
ROOTUSER = 'clowers'

XT_EXE_PATH = ''

try:
    USERNAME = os.login()
except:
    USERNAME = 'TestUser'