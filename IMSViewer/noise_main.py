import os, traceback
import time

import numpy as N
import pylab as P

from scipy import fftpack

import Filter_By_Harmonic as FBH
import Interpolate_Spectrum_w_FFT as ISFFT
import Stitch_Single as SS
import supportFunc as SF
import Find_Peaks as FP
import getBaseline as GB


'''
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

#ims = P.load('10010817.TXT', skiprows = 13)#delimiter = ',',


#            P.plot(x,y)
#            P.show()

x,y = openIMSFile('10010817.TXT')
print type(x), type(y), type(y[0])

fig = P.figure()
ax = fig.add_subplot(111)
#ax2 = fig.add_subplot(212)
#ax3 = fig.add_subplot(313)

normY = SF.normalize(y)
ax.plot(x, normY, alpha = 0.4)

#newX, newY = SF.interpolate_spectrum_XY(ims[:,0], ims[:,1], factor = 4)

fftResultDict = ISFFT.fft_spectrum(normY)
fft_mag = SF.normalize(fftResultDict['fft_mag'])
fft_raw = fftResultDict['fft_result']

#thFFT = SF.topHat(fft_mag,0.01)
#noiseEst, minNoise = GB.SplitNSmooth(thFFT, len(thFFT)/10, sigThresh = 3)

cutoff = 85
#thFFTFil = thFFT*1
fft_raw[85:]=0
#thFFTFil[85:]=0

#for i,val in enumerate(thFFT[cutoff:]):
#    if val > noiseEst[i+cutoff]:
#        fft_raw[i+cutoff] = 0#noiseEst[i+cutoff]
#        thFFTFil[i+cutoff] = 0#noiseEst[i+cutoff]

filSpec = fftpack.ifft(fft_raw)
ax.plot(x, SF.normalize(filSpec), 'g')

#line2, = ax2.plot(fft_mag, 'r')

#ax2.plot(thFFT)
#ax2.plot(thFFTFil, '--g')
#
#ax3.hist(thFFT)



P.show()