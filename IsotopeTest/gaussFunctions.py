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
    p1, success = optimize.leastsq(errfuncG, p0[:], args=(xArray, yArray), full_output = 0)
    p1G = fitfuncG(p1,xArray)
    #print "Params: ", p1
    return [success, p1, p1G]