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
    p0 = [amp, centroid, width] # Initial guess for the parameters
    #p1, success = optimize.leastsq(errfuncG, p0[:], args=(xArray, yArray), full_output = 0)
    out = optimize.leastsq(errfuncG, p0[:], args=(xArray, yArray), full_output = 1)

    pfinal = out[0]
    covar = out[1]
    #print out[2]
    infodict = out[2]
    success = out[-1]

    indexErr = N.sqrt( covar[0][0] )
    ampErr = N.sqrt( covar[1][1] ) * pfinal[0]
    #print pfinal
    #print covar
    print indexErr
    print ampErr
    # calculate error estimation from covariance matrix
    red_chi2 =(infodict["fvec"]**2).sum()#/(infodict["fvec"].size-xArray.size)
    print red_chi2
    #print covx , red_chi2
#    if cov_x is not None :
#    print " parameters  and  errors "
#    print x, numpy . sqrt ( cov_x . diagonal ()* red_chi2 )
#    print " correlation   maxtrix "
#    print cov_x / numpy . outer ( numpy . sqrt ( cov_x . diagonal ()) ,
#    numpy . sqrt ( cov_x . diagonal ()))

    pFinalAns = fitfuncG(pfinal,xArray)
    return [success, pfinal, pFinalAns]