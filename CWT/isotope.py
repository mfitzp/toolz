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
'''
import numpy as N
import numpy.fft.fftpack as F
import time
import pylab as P


def next2pow(x):
    return 2**int(N.ceil(N.log(float(x))/N.log(2.0)))


MAX_ELEMENTS=5+1  # add 1 due to mass correction 'element'
MAX_ISOTOPES=4    # maxiumum # of isotopes for one element
CUTOFF=1e-8       # relative intensity cutoff for plotting

WINDOW_SIZE = 1000
#WINDOW_SIZE=input('Window size (in Da) ---> ');

#RESOLUTION=input('Resolution (in Da) ----> ');  % mass unit used in vectors
RESOLUTION = 0.5
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

M=N.array([378,254,65,75,6,0]) #% empiric formula, e.g. bovine insulin

# isotopic abundances stored in matrix A (one row for each element)
A=N.zeros((MAX_ELEMENTS,MAX_ISOTOPES,2));

A[0][0,:] = [100783,0.9998443]#                 % 1H
A[0][1,:] = [201410,0.0001557]#                 % 2H
A[1][0,:] = [100000,0.98889]#                   % 12C
A[1][1,:] = [200336,0.01111]#                   % 13C
A[2][0,:] = [100307,0.99634]#                   % 14N
A[2][1,:] = [200011,0.00366]#                   % 15N
A[3][0,:] = [99492,0.997628]#                  % 16O
A[3][1,:] = [199913,0.000372]#                  % 17O
A[3][2,:] = [299916,0.002000]#                  % 18O
A[4][0,:] = [97207,0.95018]#                   % 32S
A[4][1,:] = [197146,0.00750]#                   % 33S
A[4][2,:] = [296787,0.04215]#                   % 34S
A[4][2,:] = [496708,0.00017]#                   % 36S
A[5][0,:] = [100000,1.00000]#                   % for shifting mass so that Mmi is
#                                             % near left limit of window

Mmi=N.array([N.round(100783*R), N.round(100000*R),\
             N.round(100307*R), N.round(99492*R), N.round(97207*R), 0])*M#  % (Virtual) monoisotopic mass in new units
Mmi = Mmi.sum()
#% mass shift so Mmi is in left limit of window:
print "Mmi",Mmi
print "Window", WINDOW_SIZE
FOLDED=N.floor(Mmi/(WINDOW_SIZE-1))+1#  % folded FOLDED times (always one folding due to shift below)

#% shift distribution to 1 Da from lower window limit:
M[MAX_ELEMENTS-1]=N.ceil(((WINDOW_SIZE-1)-N.mod(Mmi,WINDOW_SIZE-1)+N.round(100000*R))*RESOLUTION)
MASS_REMOVED=N.array([0,11,13,15,31,-1])*M#';  % correction for 'virtual' elements and mass shift
MASS_REMOVED = MASS_REMOVED.sum()

ptA=N.ones(WINDOW_SIZE);
t_fft=0
t_mult=0

for i in xrange(MAX_ELEMENTS):

    tA=N.zeros(WINDOW_SIZE)
    for j in xrange(MAX_ISOTOPES):
        if A[i][j,0] != 0:
            #removed +1 after R)+1
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
#print type(start), start
#print '\n'
#print stop
MA=N.linspace((FOLDED*(WINDOW_SIZE-1)+1)*RESOLUTION+MASS_REMOVED,(FOLDED+1)*(WINDOW_SIZE-1)*RESOLUTION+MASS_REMOVED, WINDOW_SIZE-1)
#MA = N.arange()
#axis([MA(1) MA(WINDOW_SIZE-1) 0 1]);

ind=N.where(ptA>CUTOFF)[0]
#P=[MA[ind],ptA(ind)];
x = MA[ind]
y = ptA[ind]

#H=bar(P(:,1),P(:,2),0);
P.bar(x,y)
#P.plot(ptA)
#set(H,'FaceColor','k');
#grid
#zoom on;

'Time for plotting: %4.2f s'%(time.clock() - t0)
P.show()

