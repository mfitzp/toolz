import numpy as N
import scipy.optimize as optimize

def getGauss(x, pos, wid, amp = 1):
    '''
    x -- numpy array
    pos -- centroid position
    wid -- width
    amp -- amplitude of peak

    Forumulas used:

    y = a * exp(-0.5 * (x-b)^2 / c^2) --traditional gaussian forumla
    '''
    gNorm = amp * N.exp(-0.5*((x-pos)/(wid))**2)
    return gNorm

def fitGauss(xArray, yArray, amp, centroid, width):
    p = [amp, centroid, width]

    # Fit the first set
    #p[0] -- amplitude, p[1] -- centroid, p[2] -- width
    fitfuncG = lambda p, x: p[0]*N.exp(-0.5*(x-p[1])**2/p[2]**2) # Target function
    errfuncG = lambda p, x, y: fitfuncG(p, x) - y # Distance to the target function
    out = optimize.leastsq(errfuncG, p[:], args=(xArray, yArray), full_output = 1)

    pfinal = out[0]
    covar = out[1]
    success = out[-1]
    #print pfinal
    #print "Cov Matrix\n", covar
    infodict = out[2]

    #print infodict

#    #indexErr = N.sqrt( covar[0][0] )
#    #ampErr = N.sqrt( covar[1][1] ) * pfinal[0]

#    #red_chi2 =(infodict["fvec"]**2).sum()/(infodict["fvec"].size)#-xArray.size)
#    #print red_chi2


    pFinalAns = fitfuncG(pfinal,xArray)
    return [success, pfinal, pFinalAns]