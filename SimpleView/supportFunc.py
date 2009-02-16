import numpy as N
import scipy as S
from scipy import ndimage#used for tophat filter
from scipy.interpolate import interp1d

def topHat(data, factor):
    '''
    data -- numpy array
    pntFactor determines how finely the filter is applied to data.
    A point factor of 0.01 is appropriate for the tophat filter of Bruker MALDI mass spectra.
    A smaller number is faster but a trade-off is imposed
    '''
    pntFactor = factor
    struct_pts = int(round(data.size*pntFactor))
    str_el = N.repeat([1], struct_pts)
    tFil = ndimage.white_tophat(data, None, str_el)

    return tFil

def derivative(y_data):
    '''calculates the 1st derivative'''
    y = (y_data[1:]-y_data[:-1])
    dy = y/2 #((x_data[1:]-x_data[:-1])/2)
    return N.append(dy,dy.mean())

def normalize(data):
    data/=data.max()
    data*=100
    return data

def roundLen(data):
    dl = len(data)
    place = 2
    newdl = N.round(dl,-place)#rounds to nearest tenth use -1, hundredth use -2
    if newdl > dl:
        newdl -= N.power(10,place)
#    print newdl,dl
    return data[0:newdl]

def interpolate_spectrum_XY(X, Y): #data array contains two columns. x & y, respectively
    x=X
    y=Y
    f=interp1d(x,y)
    x_new = N.arange(x.min(), x.max(), ((x.max()-x.min())/(2*len(x))))
    y_new=f(x_new)
    return (x_new, y_new)

def flattenX(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flattenX(el))
        else:
            result.append(el)
    return result

#def saveCSV(self,  path):
#    spectrum = self.data.get('spectrum')
#    if spectrum != None:
#        path+='.csv'
#        #t1 = T.clock()
#        N.savetxt(path, N.transpose(spectrum), delimiter = ',', fmt='%.4f')
#        #t2 = T.clock()
#        #print t2-t1