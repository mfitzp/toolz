import numpy as N
import scipy as S
import numpy.linalg as LA

from evaluate import evaluate

def beamSearch(r1,  r2,  ff,  rr,  option):
    opti = [0,  0,  evaluate(0, 0)]
    inter = 0
    sid = 0

    tempSol = 0
    pp = N.zeros((4, 2))
    intv1 = r1*2/3
    intv2 = r2*2/3

    bestSol = [0, 0, -1]
    secondBestSol=[0, 0, -1]
    while True:#True was while 1:
        if i == 1:
            beamWidth = 1
        else:
            beamWidth = option

        for j in xrange(beamWidth):
            sp = [[pp[j, 0],  pp[j, 1]],
                    [pp[j, 0]+intv2, pp[j, 1]],
                    [pp[j, 0]-intv2,  pp[j, 1]],
                    [pp[j, 0],  pp[j, 1]+intv1],
                    [pp[j, 0],  pp[j, 1]-intv1],
                    [pp[j, 0]+intv2,  pp[j, 1]+intv1],
                    [pp[j, 0]+intv2,  pp[j, 1]-intv1],
                    [pp[j, 0]-intv2,  pp[j, 1]+intv1],
                    [pp[j, 0]-intv2,  pp[j, 1]-intv1]]
            for m in xrange(len(sp)):
                tempSol = evaluate(sp[m, 0],  sp[m, 1])
                if tempSol > bestSol[2]:
                    secondBestSol = bestSol
                    bestSol = [sp[m, 0],  sp[m, 1], tempSol]
        pp[0] = [bestSol[0],  bestSol[1]]
        pp[1] = [secondBestSol[0],  secondBestSol[1]]
        intv1 = intv1/2*(2/3)
        intv2 = intv2/2*(2/3)
        i+=1
        if intv1 < 1 and intv2 < 1:
            break

    opti = [round(bestSol[0]), round(bestSol[1]),  bestSol[2]]
    return opti


def coco(r, f):
    if r == 0:
        r = 0
    else:
        r = N.real(r)/N.max(N.real(r))

    if f == 0:
        f = 0
    else:
        f = N.real(f)/N.max(N.real(f))

    if (LA.norm(r-N.mean(r)))*(LA.norm(f-N.mean(f)))==0:
        cc = -1e10
    else:
        cc = ((r-N.mean(r))*(f-N.mean(f))[N.newaxis,:])/((LA.norm(r-N.mean(r))*(LA.norm(f-N.mean(f)))))#there is a column descriptor in the MATLAB code....

    return cc

