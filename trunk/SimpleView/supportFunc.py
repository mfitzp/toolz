import numpy as N
import scipy as S
from scipy import ndimage#used for tophat filter

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

#def saveCSV(self,  path):
#    spectrum = self.data.get('spectrum')
#    if spectrum != None:
#        path+='.csv'
#        #t1 = T.clock()
#        N.savetxt(path, N.transpose(spectrum), delimiter = ',', fmt='%.4f')
#        #t2 = T.clock()
#        #print t2-t1