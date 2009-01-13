#%
#% calculate isotopic distributions of molecules using the FFT
#%
#% (c) Magnus Palmblad, 1999
#%


import sys
import numpy as N
import numpy.fft.fftpack as F
import pylab as P


MAX_ELEMENTS = 5
MAX_MASS = 2**13      #% fast radix-2 fast-Fourier transform algorithm is used

M = N.array([378,234,65,75,6])               #% empirical formula, e.g. bovine insulin

A = N.zeros((MAX_ELEMENTS,MAX_MASS))#                 % isotopic abundancies stored in A

A[0,1:3]=[0.9998443,0.0001557]#                 % H
A[1,12:14]=[0.98889,0.01111]#                   % C
A[2,14:16]=[0.99634,0.00366]#                   % N
A[3,16:19]=[0.997628,0.000372,0.002000]#        % O
A[4,32:37]=[0.95018,0.00750,0.04215,0,0.00017]# % S (extend to other elements as needed)

tA=F.fft(A,axis=1)#                     % FFT along each element's isotopic distribution

ptA=N.ones(MAX_MASS);
for i in xrange(MAX_ELEMENTS-1):
    ptA = ptA*(tA[i,:]**M[i])#;         % multiply transforms (elementwise)


riptA=F.ifft(ptA).real#              % inverse FFT to get convolutions

id=N.zeros(MAX_MASS)
id[0:MAX_MASS-1]=riptA[1:MAX_MASS]#; % shift to real mass

print id.argmax(), id.max()
P.plot(riptA)
P.show()