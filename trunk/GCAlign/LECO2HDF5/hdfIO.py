'''
Need to write some of the attributes of the LECO file into the
netCDF file.
'''

import os
import sys
import tables as T
import numpy as N
import time


def saveDict(arrayDict, filename):
    '''
    Saves the original netCDF arrays in a compressed HDF5 format
    '''

    filters = T.Filters(complevel=5, complib='zlib')
    atom = T.Int32Atom()
    hdf = T.openFile(filename, mode = "w", title = 'Data_Array')
    varGroup = hdf.createGroup("/", 'Data_Arrays', 'Data_Arrays')
    for item in arrayDict.iteritems():
        data = N.array(item[1].data)
        shape = data.shape
        ca = hdf.createCArray(varGroup, item[0], atom, shape,  filters = filters)
        ca[0:shape[0]] = data
        ca.flush()
        print "%s written"%item[0]

    hdf.close()

def saveChromaTOF(fileName,  cdf, numCols=None,  numRows = None, dataType = 'NetCDF'):
    t1 = time.clock()

    mzMax = 401 #rows
    colCount = len(cdf.scanIndex)
    hdf = T.openFile(fileName, mode = "w", title = 'Data_Array')
    filters = T.Filters(complevel=5, complib='zlib')
    atom = T.Int32Atom()
    chunkS = (400, 5)
    #chunkMZ = (20, 401)
    dataCube = hdf.createEArray(hdf.root, 'dataCube', atom, (0,mzMax), filters = filters,  expectedrows = colCount)#,  chunkshape = chunkMZ)
    dataCube.attrs.rowPoints = cdf.rowPoints
    dataCube.attrs.colPoints = cdf.colPoints

    data = cdf.TIC
    shape = data.shape
    ca = hdf.createCArray(hdf.root, 'TIC', atom, shape,  filters = filters)
    ca[0:shape[0]] = data
    ca.flush()
    print "TIC written"


    #sicCube = hdf.createEArray(hdf.root, 'sicCube', atom, (mzMax,0), filters = filters,  expectedrows = mzMax)#,  chunkshape = chunkS)
    #print "Sic Chunk", sicCube.chunkshape
    #print "MZ Chunk",  dataCube.chunkshape

    try:
        if dataType == 'NetCDF':
            m=0
            for i in cdf.scanIndex:

                localMaxIndex = i+cdf.pntCount[m]
                mz2Write = N.zeros(mzMax)#ADDING 1 so that indicies work out!!!!!!!!!!!!!!!DOUBLE CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                mzLocal = N.array(cdf.vars['mass_values'].data[i:localMaxIndex])
                mzLocal +=1 #!!!!!!!!!!!!!!DOUBLE CHECK THIS
                intLocal = cdf.vars['intensity_values'].data[i:localMaxIndex]
                N.put(mz2Write,  mzLocal, intLocal)
                dataCube.append(mz2Write[N.newaxis,:])
                dataCube.flush()

                if m%10000 == 0:
#                    self.emit(QtCore.SIGNAL("itemLoaded(PyQt_PyObject)"),self.msg)
                    print m
                m+=1
            print time.clock()-t1, 'seconds'
            hdf.close()

        if dataType == 'HDF5':
            m=0
            for i in cdf.scanIndex:

                localMaxIndex = i+cdf.pntCount[m]
                mz2Write = N.zeros(mzMax)#ADDING 1 so that indicies work out!!!!!!!!!!!!!!!DOUBLE CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                mzLocal = N.array(cdf.vars['mass_values'][i:localMaxIndex])
                mzLocal +=1 #!!!!!!!!!!!!!!DOUBLE CHECK THIS
                intLocal = cdf.vars['intensity_values'][i:localMaxIndex]
                N.put(mz2Write,  mzLocal, intLocal)
                dataCube.append(mz2Write[N.newaxis,:])
                dataCube.flush()

                if m%10000 == 0:
                    print m
                m+=1
            print time.clock()-t1, 'seconds'
            hdf.close()


    except:
        errorMsg = "Error: %s\n\n%s\n"%(sys.exc_type, sys.exc_value)
        print errorMsg
        hdf.close()



def loadHDF5(filename):
    if os.path.isfile(filename):
        loadedVars = []
        hdf = T.openFile(filename, mode = "r")
        groupDict = hdf.root._v_groups
        if groupDict.has_key('Data_Arrays'):
            for node in hdf.root.Data_Arrays._f_iterNodes():
                if node._c_classId is 'CARRAY':
                    loadedVars.append((node._v_hdf5name,node))


        #hdf.close()
        return hdf, dict(loadedVars)#remember to close the file when you are done


if __name__ == "__main__":
    from LECO_IO import ChromaTOF_Reader
    fn = 'C:/TCiv-R1.h5'
    f2write = 'C:/TCiv-R1_T.h5'
    if fn:
        cdf = ChromaTOF_Reader(fn, fileType = 'HDF5')
        saveChromaTOF(f2write, cdf, dataType = 'HDF5')



