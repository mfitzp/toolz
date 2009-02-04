import re
#import wx
import operator
import os
import sys
import datetime

from PyQt4.QtCore import QString

#from tables.node import filenode
from tables import *
import numpy as N

localVarTypes = [float,int,str,tuple,list,N.ndarray,datetime.date]

##class workspaceIO:
##
##    def __init__(self,hd5FileName):
##        self.__theFileName = hd5FileName
class intTable(IsDescription):
    name = StringCol(32)
    value = Int32Col()

class floatTable(IsDescription):
    name = StringCol(32)
    value = Float64Col()

class dateTable(IsDescription):
    name = StringCol(32)
    value = StringCol(32)

def save_workspace(filename, publicVarDict, scratchPadDict = None,  plotScriptDict = None):

    if type(publicVarDict) is not dict:
        print "Incorrect data type submitted, variables not stored in a Dictionary"
    else:
        createIntTbl = True
        createFloatTbl = True

        hdf = openFile(filename, mode = "w", title = 'SubPlot Data File')
        varGroup = hdf.createGroup("/", 'pubVars', 'Public Variables')

        for entry in publicVarDict.iteritems():
            valuetype = type(entry[1])
            if valuetype is int:
                if createIntTbl:
                    intTbl = hdf.createTable(varGroup, 'IntVars', intTable, "Integer Variables")
                    createIntTbl = False
                intTbl_row = intTbl.row
                intTbl_row['name'] = entry[0]
                intTbl_row['value'] = entry[1]
                intTbl_row.append()

            elif valuetype is float:
                if createFloatTbl:
                    floatTbl = hdf.createTable(varGroup, 'FloatVars', floatTable, "Float Variables")
                    createFloatTbl = False
                floatTbl_row = floatTbl.row
                floatTbl_row['name'] = entry[0]
                floatTbl_row['value'] = entry[1]
                floatTbl_row.append()

##            elif valuetype is date:
##                dateTbl_row = dateTbl.row
##                dateTbl_row['name'] = entry[0]
##                dateTbl_row['value'] = entry[1]
##                dateTbl_row.append()

            if valuetype is str:
                hdf.createArray(varGroup, entry[0], entry[1], title=entry[0])

            if valuetype is N.ndarray:
                hdf.createArray(varGroup, entry[0], entry[1], title=entry[0])

            elif valuetype is list:
                hdf.createArray(varGroup, entry[0], entry[1], title=entry[0])

            elif valuetype is tuple:
                hdf.createArray(varGroup, entry[0], entry[1], title=entry[0])

            elif valuetype is dict:
                process_dict(hdf, entry[0], entry[1], ("/" + varGroup._v_hdf5name))

        if createFloatTbl is False:
            floatTbl.flush()

        if createIntTbl is False:
            intTbl.flush()

        if len(scratchPadDict) != 0:
            scratchGroup = hdf.createGroup("/",  'scratch',  'Scratch Pad Scripts')
            for script in scratchPadDict.iteritems():
                scriptname = str(script[0])
                strScript = str(script[1])
                valuetype = type(strScript)
                if valuetype is str:
                    hdf.createArray(scratchGroup, scriptname, strScript, title=scriptname)

        if len(plotScriptDict) != 0:
            plotScriptGroup = hdf.createGroup("/",  'plotScripts',  'Plot Scripts')
            for script in plotScriptDict.iteritems():
                valuetype = type(script[1][0])#the script is a list because this is the easiest way to pass things to the interp.
                if valuetype is str:
                    hdf.createArray(plotScriptGroup, script[0], script[1][0], title=script[0])

        hdf.close()

#tuples, lists, and arrays will be stored as table.array
def load_workspace(filename):
    if os.path.isfile(filename):
        scriptDict ={}
        plotDict = {}
        loadedVars = []
        hdf = openFile(filename, mode = "r")
        groupDict = hdf.root._v_groups
        if groupDict.has_key('pubVars'):
            for node in hdf.root.pubVars._f_iterNodes():
##                print type(node.flavor)
                if node._c_classId is 'ARRAY':
                    #print node._v_hdf5name
                    #print node.flavor
                    #print ""
                    #print "Array"
                    loadedVars.append((node._v_hdf5name,node.read()))
                if node._c_classId is 'TABLE':
                    for row in node.iterrows():
                        loadedVars.append((row['name'], row['value']))
                        #print type(row['name'])
                        #print row['name']

        if groupDict.has_key('scratch'):
            for node in hdf.root.scratch._f_iterNodes():
                if node._c_classId is 'ARRAY':
                    scriptDict[QString(node._v_name)] = QString(node.read())

        if groupDict.has_key('plotScripts'):
            for node in hdf.root.plotScripts._f_iterNodes():
                if node._c_classId is 'ARRAY':
                    plotDict[node._v_name] = [node.read()]

        hdf.close()
        return dict(loadedVars),  scriptDict,  plotDict


def process_dict(hdfile, dictname, dict2process, currentGroup):

    createIntTbl = True
    createFloatTbl = True

    #print currentGroup
    dictGroup = hdfile.createGroup(currentGroup, dictname, 'Dict Variables')

    for entry in dict2process.iteritems():
        valuetype = type(entry[1])
        if valuetype is int:
            if createIntTbl:
                dictIntTbl = hdfile.createTable(dictGroup, 'IntVars', intTable, "Integer Variables")
                creatIntTbl = False
            dictIntTbl_row = dictIntTbl.row
            dictIntTbl_row['name'] = entry[0]
            dictIntTbl_row['value'] = entry[1]
            dictIntTbl_row.append()

        elif valuetype is float:
            if createFloatTbl:
                dictFloatTbl = hdfile.createTable(dictGroup, 'FloatVars', floatTable, "Float Variables")
                createFloatTbl = False
            dictFloatTbl_row = dictFloatTbl.row
            dictFloatTbl_row['name'] = entry[0]
            dictFloatTbl_row['value'] = entry[1]
            dictFloatTbl_row.append()

        if valuetype is str:
            hdfile.createArray(dictGroup, entry[0], entry[1], title=entry[0])

        if valuetype is N.ndarray:
            hdfile.createArray(dictGroup, entry[0], entry[1], title=entry[0])

        elif valuetype is list:
            hdfile.createArray(dictGroup, entry[0], entry[1], title=entry[0])

        elif valuetype is tuple:
            hdfile.createArray(dictGroup, entry[0], entry[1], title=entry[0])

        elif valuetype is dict:
                process_dict(hdfile, entry[0], entry[1], (currentGroup + "/" + dictGroup._v_hdf5name))

    if createIntTbl is False:
        dictIntTbl.flush()
    if createFloatTbl is False:
        dictFloatTbl.flush()










if __name__ == "__main__":

    x = N.arange(0,10, N.random.random())
    y = N.cos(x-N.random.random())
    y2 = N.sin(x-N.random.random())
    y3 = 2*N.sin(x-N.random.random())

    array_list = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
             "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
             "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi",
             "Lemon", "Nectarine", "Plum", "Raspberry", "Strawberry",
             "Orange"]

    int1 = 3
    int2 = 423
    int3 = 8342
    float1 = 3.1432
    float2 = 4.234
    float3 = 234.12311
    str1 = 'yahoo'
    str2 = 'joe'
    str3 = 'get out'
    longStr = 'x = N.arange(0,20, N.random.random())\r\
y = N.cos(x-N.random.random())\r\
y2 = 2*N.cos(x-N.random.random())\r\
y3 = 2*N.sin(x-N.random.random())\r\
a = "yahoo"\r\
b = 3.3241\r\
c = [3,2,6,4,1,3,9]\r'
    list_test2 = [2,3,24,23.25,12,3,'go joe']
    tuple_test = (23,123,52,'string',89,30.2341, )
    dict1 = dict(joe = 45.234, darray = N.arange(0,20,0.5))
    dict_test = dict(b = 1.234, c = 'string', d = [1,2,4,5,3], np = N.arange(0,10,0.1), d2 = dict1)
    varDict = {'fruit':array_list, 'x':x, 'y':y, 'y2':y2, 'y3':y3,\
                'int1':int1, 'int2':int2, 'int3':int3,\
                'float1':float1, 'float2':float2, 'float3':float3,\
                'str1':str1, 'str2':str2, 'str2':str2, 'longstr':longStr,\
                'tuple_test': tuple_test, 'dictTest': dict_test, 'list_test2':\
                list_test2}
    #print type(varDict)
    #save_workspace(varDict, File_Dialog())
    vars = load_workspace(File_Dialog())
    for value in vars.values():
        print value
        print type(value)

    #print vars.keys()
    #print vars.items()

