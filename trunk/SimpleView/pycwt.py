# Continuous wavelet transfrom via Fourier transform
# Collection of routines for wavelet transform via FFT algorithm


#-- Some naming and other conventions --
# use f instead of omega wherever rational/possible
# *_ft means Fourier transform

#-- Some references --
# [1] Mallat, S.  A wavelet tour of signal processing
# [2] Addison, Paul S. The illustrated wavelet transform handbook

import numpy
from numpy.fft import fft, ifft, fftfreq


from scipy.special import gamma
import supportFunc as SF


pi = numpy.pi

class DOG:
    """Derivative of Gaussian, general form"""
    # Incomplete, as the general form of the mother wavelet
    # would require symbolic differentiation.
    # Should be enough for the CWT computation, though

    def __init__(self, m = 1.):
        self.order = m
        self.fc = (m+.5)**.5 / (2*pi)

    def psi_ft(self, f):
        c = 1j**self.order / numpy.sqrt(gamma(self.order + .5)) #normalization
        w = 2*pi*f
        return c * w**self.order * numpy.exp(-.5*w**2)

class Mexican_hat:
    def __init__(self, sigma = 1.0):
        self.sigma = sigma
        self.fc = .5 * 2.5**.5 / pi
    def psi_ft(self, f):
        """Fourier transform of the Mexican hat wavelet"""
        c = numpy.sqrt(8./3.) * pi**.25 * self.sigma**2.5
        wsq = (2. * pi * f)**2.
        return -c * wsq * numpy.exp(-.5 * wsq * self.sigma**2.)
    def psi(self, tau):
        """Mexian hat wavelet as described in [1]"""
        xsq = (tau / self.sigma)**2.
        c = 2 * pi**-.25 / numpy.sqrt(3 * self.sigma) # normalization constant from [1]
        return c * (1 - xsq) * numpy.exp(-.5 * xsq)
    def set_f0(self, f0):
        pass

class Morlet:
    def __init__(self, f0 = 1.5):
        self.set_f0(f0)
    def psi_ft(self, f):
        """Fourier transform of the approximate Morlet wavelet
            f0 should be more than 0.8 for this function to be correct."""
        return (pi**-.25) * (2.**.5) * numpy.exp(-.5 * (2. * pi * (f - self.fc))**2.)
    def set_f0(self, f0):
        self.f0 = f0
        self.fc = f0


class Shannon:
	def __init__(self, f0 = 1.5):
		self.set_f0(f0)
	def psi_ft(self, f):
		"""Fourier transform of the approximate Shannon wavelet"""
		#return (pi**-.25) * (2.**.5) * numpy.exp(-.5 * (2. * pi * (f - self.fc))**2.)
		return 2*numpy.sinc(2*f)-numpy.sinc(f)
	def set_f0(self, f0):
		self.f0 = f0
		self.fc = f0

def _getWavelet_(waveString):
    if type(waveString) != str:
        return None

    if waveString is 'MexHat':
        return Mexican_hat()
    elif waveString is 'DOG':
        return DOG()
    elif waveString is 'Morlet':
        return Morlet()
    elif waveString is 'Shannon':
        return Shannon()
    else:
        return None

def cwt_a(signal, scales, sampling_scale = 1.0, wavelet='MexHat'):
    """ Continuous wavelet transform via fft. Scales version.  """
    signal_ft = fft(signal)                     # FFT of the signal
    W = numpy.zeros((len(scales), len(signal)),'complex') # create the matrix beforehand
    ftfreqs = fftfreq(len(signal), sampling_scale)       # FFT frequencies
    wvLet = _getWavelet_(wavelet)
    if wvLet != None:
		# Now fill in the matrix
		for n,s in enumerate(scales):
			#print "Scale, Freq: ", s, s*ftfreqs
			psi_ft_bar = numpy.conjugate(wvLet.psi_ft(s * ftfreqs))
			W[n,:] = ifft(signal_ft * psi_ft_bar)*(s**.5)
			#W[n,:] = (signal_ft * psi_ft_bar)*(s**.5)
		return W


def cwt_f(signal, freqs, Fs=1.0, wavelet = 'Morlet'):
    """Continuous wavelet transform -- frequencies version"""
    wvLet = _getWavelet_(wavelet)
    if wvLet != None:
	    scales = wvLet.fc/freqs
	    dt = 1./Fs
	    return cwt_a(signal, scales, dt, wavelet)


if __name__ == "__main__":
	from pylab import *
	#fs = 65.0
	#t = numpy.arange(0,16,(1/fs))
	#signal = numpy.sin(2*pi*1.2*t)+numpy.cos(2*pi*3.7*t)

	dat = load('Tryptone.csv', delimiter = ',')
	signal = dat[:,1]
	xSignal = dat[:,0]
	xArray, yArray = SF.interpolate_spectrum_XY(xSignal, signal)
	print len(yArray)
	signal = signal[20000:65000]
	xSignal = dat[:,0][20000:65000]
	xDiff = xArray[1]-xArray[0]
	print "Diff X: ", xDiff, xArray[-1]-xArray[-2]
	print "Diff Multiplier: ", 8*xDiff, 16*xDiff
	#tOnes = numpy.zeros_like(t)
	#tOnes+=1
	scales = [1,2,4,8,16,32]
	scales2 = [32,44,55,66]
	scales3 = N.arange(2,64,6)
	#cwt = cwt_a(yArray, scales, sampling_scale = 1.0, wavelet='MexHat')
	#print cwt.shape
	ax1 = subplot(311)
	ax2 = subplot(312, sharex = ax1)
	ax3 = subplot(313, sharex = ax1)

	cwt1 = cwt_a(yArray, scales, sampling_scale = 1.0, wavelet='DOG')
	#cwt1 = cwt_a(signal, scales2, sampling_scale = 1.0, wavelet='MexHat')
	#cwt1 = cwt_a(signal, scales2, sampling_scale = 1.0, wavelet='Shannon')
	#cwt1 = cwt_a(signal, scales2, sampling_scale = 1.0, wavelet='Morlet')

	#ax3.imshow(cwt1.real, aspect = 'auto')
	#ax3.plot(cwt1.real[-1])
	for i in xrange(cwt1.shape[0]):
		ax3.plot(cwt1.real[i], label = '%s'%scales[i])
	ax3.legend()


	ax1.plot(yArray)
	ax2.imshow(cwt1.real, aspect = 'auto', cmap = cm.jet)

	#mh = Mexican_hat()
	#ans = mh.psi(signal)
	#ans = mh.psi_ft(tOnes)
	#plot(signal)
	#print ans

	show()

