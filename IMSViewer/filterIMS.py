import os, traceback
#import time

import numpy as N
#import pylab as P

from scipy import fftpack

#import Filter_By_Harmonic as FBH
import Interpolate_Spectrum_w_FFT as ISFFT
#import Stitch_Single as SS
import supportFunc as SF
#import Find_Peaks as FP
#import getBaseline as GB


'''
FROM PCP
Example IMS File Structure:

This is  c:\datamel\09300830.txt
IMS Cell Temp. =  58.500000  'C
Atmos Pressure =  750.000000  Torr
Cell  Voltage  =  3000.000000  Volts
Uo   Constant  =  53882.000000
Gas      Type  =  N2
Carrier  Flow  =  200.000000  ml/min
Drift    Flow  =  500.000000  ml/min
Start    Time  =  10.000000  msec
End      Time  =  50.000000  msec
Dwell          =  40.000000  usec for  1001.000000  Channels
#Scans         =  300.000000
Time(msec)   Data Value
 10.000000 656.000000
 10.040000 -198.000000
 10.080000 -2855.000000

'''

'''
09300830 Noisy IMS
10010817 Noisy IMS
10010825 IMS
10020807 IMS-MS
10150804 m/z spectrum
'''

def lowPassIMS(yVals, freq):
    fftResultDict = ISFFT.fft_spectrum(yVals)
    fft_mag = SF.normalize(fftResultDict['fft_mag'])
    fft_raw = fftResultDict['fft_result']
    cutoff = freq
    fft_raw[cutoff:]=0
    filSpec = fftpack.ifft(fft_raw)
    return filSpec.real
