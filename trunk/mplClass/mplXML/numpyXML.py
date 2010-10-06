import struct
import base64
import numpy as N
import matplotlib.pyplot as P

'''
Handlers to convert numpy arrays back and forth between the bloated XML format
'''

def encodeArray(numpyArray):
    # decode data
    if type(numpyArray) is N.ndarray:
        data = numpyArray
        multiDim = False
        dims = 1
        if len(data.shape)>1:
            multiDim = True		
            dims = data.shape[1]
		
    try:
        endian = '!'
        pointsCount = len(data)#data.size#/struct.calcsize(endian+'f')
        start, end = 0, len(data)
        #print "Points Count Encode:",  pointsCount
        #print "Length of encodeData",  len(data)
        #print "Type of encodeData",  type(data)
        #problem arises with multidimensional arrays
        #using the method below it flattens the array
        # if multiDim:
            # s = ''
            # for i in data:
                # pointsCount = len(i)
                # print i
                # s+=struct.pack(endian+'f'*pointsCount, *i)
            # data = s
        # else:
        data = struct.pack(endian+'f'*pointsCount, *data)#data[start:end])
        #data = struct.pack('f', data[start:end])
        
    except:
        print data
        raise
        return False

    # convert from binary format
    try:
        data = base64.b64encode(data)
    except:
        raise
        return False

    return N.array(data)


def decodeArray(data):
    # decode data
    try:
        data = base64.b64decode(data)
        endian = '!'
    except:
        return False

    # convert from binary format
    try:
      pointsCount = len(data)/struct.calcsize(endian+'f')
      start, end = 0, len(data)
      data = struct.unpack(endian+'f'*pointsCount, data[start:end])
    except:
        raise
        return False
    #print type(data)
#    for i in xrange(20):
#        print data[i]

    # split data to m/z and intensity
    #mzData = data[::2]
    #print type(mzData)
    #intData = data[1::2]

    return N.array(data)#[mzData, intData]	