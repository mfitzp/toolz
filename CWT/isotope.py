'''
%
% Calculates isotopic distributions including isotopic fine structure
% of molecules using FFT and various scaling 'tricks'. Easily adopted
% to molecules of any elemental composition (by altering MAX_ELEMENTS
% and the nuclide matrix A). To simulate spectra, convolute with peak
% shape using FFT.
%
% (C) 1999 by Magnus Palmblad, Division of Ion Physics, Uppsala Univ.
% Acknowledgements:
% Lars Larsson-Cohn, Dept. of Mathematical Statistics, Uppsala Univ.,
% for help on theory of convolutions and FFT.
% Jan Axelsson, Div. of Ion Physics, Uppsala Univ. for comments and ideas
%
% Contact Magnus Palmblad at magnus.palmblad@gmail.com if you should
% have any questions or comments.
%

Converted to Python 1/10/08 by
Brian H. Clowers bhclowers@gmail.com
Required Modules:
numpy for the numerical calculations
matplotlib enables the plotting functions

-Keep in mind that the resolution will determine how finely
the isotopic calculation will be performed.
    --if it is too fine (i.e. < 0.00001)
      then the calculation will fail.
    --Besides, the ability to resolve differences of 0.00001 Da
      would allow differentiation of electronic states--a feat
      beyond even some of the best mass spectrometers (as of 2009).
--Also if the window size is huge and resolution small
  again this will create a huge array beyond the memory of simple desktop PC.

'''
import sys
import numpy as N
import numpy.fft.fftpack as F

from elements import ELEMENTS #A DICTIONARY OF ALL ELEMENTS
#USAGE: ELEMENTS['C'].isotopes returns as tuple containing the info for each isotope

import time
import pylab as P


def next2pow(x):
    return 2**int(N.ceil(N.log(float(x))/N.log(2.0)))

def getWindowSize():
    try:
        WINDOW_SIZE = int(raw_input("Window size (in Da) ---> "))
    except:
        print "Please enter an integer next time....defaulting to 10"
        WINDOW_SIZE = 10
    return WINDOW_SIZE

def getResolution():
    try:
        RESOLUTION = float(raw_input("Resolution (in Da) ----> "))
    except:
        print "Please enter an float next time....defaulting to 0.001"
        RESOLUTION = 0.001
    return RESOLUTION

#RESOLUTION=input('Resolution (in Da) ----> ');  % mass unit used in vectors

def getAveragineComp(peakMZ,charges):
    mwAvgine = 111.1254#average MW
    #C4.9384 H7.7583 N1.3577 O1.4773 S0.0417 Averagine, MWav = 111.1254 Da
    # of averagine units
    peakMZ*=charges
    numUnits = peakMZ/mwAvgine
    atoms = ['H','C','N','O','S',None]
    comp = N.array([7.7583,4.9384,1.3577,1.4773,0.0417,0]) #% empiric formula, e.g. averagine
    comp*=numUnits
    comp = N.round(comp)
    return atoms, comp





WINDOW_SIZE = getWindowSize()
#WINDOW_SIZE = 10

RESOLUTION = getResolution()
#RESOLUTION = 0.001

if RESOLUTION < 0.00001:#  % minimal mass step allowed
  RESOLUTION = 0.00001
elif RESOLUTION > 0.5:  # maximal mass step allowed
  RESOLUTION = 0.5

R=0.00001/RESOLUTION#  % R is used to scale nuclide masses (see below)

WINDOW_SIZE=WINDOW_SIZE/RESOLUTION;   # convert window size to new mass units
WINDOW_SIZE=next2pow(WINDOW_SIZE);  # fast radix-2 fast-Fourier transform algorithm

if WINDOW_SIZE < N.round(496708*R)+1:
  WINDOW_SIZE = nextpow2(N.round(496708*R)+1)  # just to make sure window is big enough

print 'Vector size: 1x%d'%WINDOW_SIZE

MAX_ELEMENTS=5+1  # add 1 due to mass correction 'element'
MAX_ISOTOPES=4    # maxiumum # of isotopes for one element
CUTOFF=1e-4       # relative intensity cutoff for plotting

massE = 5.4858E-4 #mass in Da
numCharges = 0
numProtons = 0

#H378 C254 N65 O75 S6
ATOMS = ['H','C','N','O','S',None]
ISOTOPES = []
for atom in ATOMS:
    if ELEMENTS.hasKey(atom):
        ISOTOPES.append(ELEMENTS[atom].isotopes)
    else:
        ISOTOPES.append(0)

for i,isotope in enumerate(ISOTOPES):
    print ATOMS[i], isotope


M=N.array([378+numProtons,254,65,75,6,0]) #% empiric formula, e.g. bovine insulin
print M

#C4.9384 H7.7583 N1.3577 O1.4773 S0.0417 Averagine, MWav = 111.1254 Da

#ATOMS, M = getAveragineComp(2000, 1)
#print atoms
#print comp

# isotopic abundances stored in matrix A (one row for each element)
'''
So here's the reasoning behind the units used:
The two STABLE isotopes of carbon are:
#Neutrons    Mass            Relative abundance
 12          12.0            0.98929999999999996)
 13          13.0033548378   0.010699999999999999)

'''

A=N.zeros((MAX_ELEMENTS,MAX_ISOTOPES,2));

A[0][0,:] = [100783,0.9998443]#                 % 1H
A[0][1,:] = [201410,0.0001557]#                 % 2H
A[1][0,:] = [100000,0.98889]#                   % 12C
A[1][1,:] = [200336,0.01111]#                   % 13C
A[2][0,:] = [100307,0.99634]#                   % 14N
A[2][1,:] = [200011,0.00366]#                   % 15N
A[3][0,:] = [99492,0.997628]#                   % 16O
A[3][1,:] = [199913,0.000372]#                  % 17O
A[3][2,:] = [299916,0.002000]#                  % 18O
A[4][0,:] = [97207,0.95018]#                    % 32S
A[4][1,:] = [197146,0.00750]#                   % 33S
A[4][2,:] = [296787,0.04215]#                   % 34S
A[4][2,:] = [496708,0.00017]#                   % 36S
A[5][0,:] = [100000,1.00000]#                   % for shifting mass so that Mmi is
#                                               % near left limit of window

Mmi=N.array([N.round(100783*R), N.round(100000*R),\
             N.round(100307*R), N.round(99492*R), N.round(97207*R), 0])*M#  % (Virtual) monoisotopic mass in new units
Mmi = Mmi.sum()
#% mass shift so Mmi is in left limit of window:
print "Mmi",Mmi

FOLDED=N.floor(Mmi/(WINDOW_SIZE-1))+1#  % folded FOLDED times (always one folding due to shift below)

#% shift distribution to 1 Da from lower window limit:
M[MAX_ELEMENTS-1]=N.ceil(((WINDOW_SIZE-1)-N.mod(Mmi,WINDOW_SIZE-1)+N.round(100000*R))*RESOLUTION)
MASS_REMOVED=N.array([0,11,13,15,31,-1])*M#';  % correction for 'virtual' elements and mass shift
#MASS_REMOVED=N.array([1,12,14,16,32,0])*M#';  % correction for 'virtual' elements and mass shift
MASS_REMOVED = MASS_REMOVED.sum()

ptA=N.ones(WINDOW_SIZE);
t_fft=0
t_mult=0

for i in xrange(MAX_ELEMENTS):

    tA=N.zeros(WINDOW_SIZE)
    for j in xrange(MAX_ISOTOPES):
        if A[i][j,0] != 0:
            #removed +1 after R)+1 --we're using python which counts from 0
            tA[N.round(A[i][j,0]*R)]=A[i][j,1]#;  % put isotopic distribution in tA

    print 'Calculate FFT...'
    t0 = time.clock()
    tA=F.fft(tA) # FFT along elements isotopic distribution  O(nlogn)
    t_fft = time.clock()-t0
    print 'Multiply vectors...'
    t0 = time.clock()
    tA=tA**M[i]#  % O(n)
    #################
    ptA = ptA*tA#  % O(n)#this is where it is messing UP
    #################
    t1 = time.clock()
    t_mult=t1-t0


print 'Time for FFT: %4.2f s'%t_fft
print 'Time for multiplications: %4.2f s'%t_mult

print 'Calculate IFFT...'
t0=time.clock()
ptA=F.ifft(ptA).real#;  % O(nlogn)

print 'Time for IFFT: %4.2f s'%(time.clock()-t0)

print 'Plotting...'
t0=time.clock()


start = (FOLDED*(WINDOW_SIZE-1)+1)*RESOLUTION+MASS_REMOVED,(FOLDED+1)*(WINDOW_SIZE-1)*RESOLUTION+MASS_REMOVED
stop = WINDOW_SIZE - 1

MA=N.linspace((FOLDED*(WINDOW_SIZE-1)+1)*RESOLUTION+MASS_REMOVED,(FOLDED+1)*(WINDOW_SIZE-1)*RESOLUTION+MASS_REMOVED, WINDOW_SIZE-1)

ind=N.where(ptA>CUTOFF)[0]

x = MA[ind]
y = ptA[ind]

if numCharges > 0:
    if N.sign(numCharges) == -1:
        #add electrons when a negative ion
        x += N.abs(numCharges)*massE
    else:
        #subtract electrons when a positive ion
        x -= N.abs(numCharges)*massE

    x /= N.abs(numCharges)

#scale Intensity Values
yMax = y.max()
y /=yMax
y *= 100

#P.plot(ptA)
P.vlines(x,0,y, label = 'Isotope Pattern')
P.vlines(x[0], 0, y[0], color = 'r', linestyle = 'dotted', lw = 2, label = 'Monoisotopic Mass')
maxYInd = y.argmax()
P.vlines(x[maxYInd], 0, y[maxYInd], color = 'b', linestyle = 'dotted', lw = 2, label = 'Maximum Mass')

'Time for plotting: %4.2f s'%(time.clock() - t0)
#for i,pnt in enumerate(x):
#    print pnt, y[i]

P.show()

