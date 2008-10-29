
import os
import sys

import numpy as N
import scipy as S
from scipy.interpolate import interp1d
import numpy.linalg.norm as norm

def evaluate(inter,  sid,  ff,  rr):
    inter = N.round(inter)
    sid = N.round(sid)

    if len(ff) > 0 and inter != 0:
        step = (len(ff)+inter)/len(rr)
        fff = interp1d(ff,  N.arange(0, len(ff), step))
        if len(fff) > len(rr):
            fff = ff[0:len(rr)]
        elif len(fff) <= len(rr):
            diff = len(rr) - len(fff)
            fff = N.append(fff,  N.ones(diff)*fff[len(fff)])
    elif len(ff) > 0 and inter == 0:
        fff = ff
    else:
        return False

    if len(fff) > 0:
        if sid > 0:
            sidtill = N.ones(sid)*fff[1]
            ffff = N.append(sidtill,  fff[0:(len(fff)-sid)])
        elif sid <= 0:
            sid = N.abs(sid)
            sidtill = N.ones(sid)*fff[len(fff)]
            ffff = N.append(fff[(sid+1):len(fff)],  sidtill)
        else:
            return False

    if rr == 0:
        rrs = 0
    else:
        rrs = rr.real/N.max(rr.real)

    if ffff == 0:
        fffs = 0
    else:
        fffs = ffff.real/N.max(ffff.real)

    meanR = N.mean(rrs)
    meanF = N.mean(fffs)

    if (LA.norm(rrs-meanR))*(LA.norm(fffs-meanF)) == 0:
       cc = -1e10
    else:
        cc = ((rrs-meanR)*(fffs-meanF)[N.newaxis,:])/((LA.norm(rrs-meanR))*(LA.norm(fffs-meanF)))
    end

    return cc



