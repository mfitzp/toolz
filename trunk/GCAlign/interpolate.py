#!/usr/bin/env python
#import wx
import os

from pylab import *
import numpy as N
from scipy.interpolate import interp1d
from scipy import fftpack
from smoothingFilter import savitzky_golay


##############################

def File_Dialog():
# setup the GUI main loop
    app = wx.PySimpleApp()
    filename = wx.FileSelector(message='Select Data File', default_path=os.getcwd(), parent=None)
    return filename

###################

def get_ascii_data(filename):
    data_spectrum=load(filename, skiprows=0, delimiter = ',' )##remember to change this depending on file format
    print "File Loaded: ", filename
    return data_spectrum

###################

def interpolate_spectrum(data_array): #data array contains two columns. x & y, respectively
    x=data_array[:,0]
    y=data_array[:,1]
    f=interp1d(x,y)
    x_new = N.arange(x.min(), x.max(), ((x.max()-x.min())/(2*len(x))))
    y_new=f(x_new)
    return (x_new, y_new)

###################
def fft_spectrum(evenly_spaced_y_data):#idealy this is the y_new from the previous function
    #smoothed_data=savitzky_golay(evenly_spaced_y_data, kernel = 11, order = 4)
    fft_result=fftpack.fft(evenly_spaced_y_data)

    n = len(evenly_spaced_y_data)
    nUniquePts = ceil((n+1)/2.0)
    mag = abs(fft_result[0:nUniquePts])
    mag /= float(n)
    # odd nfft excludes Nyquist point
    if n % 2 > 0: # we've got odd number of points fft
        mag[1:len(mag)] = mag[1:len(mag)] * 2
    else:
        mag[1:len(mag) -1] = mag[1:len(mag) - 1] * 2 # we've got even number of points fft

    sampling_Freq=100000#this may  not be correct but is used in the original code
    freqArray = arange(0, nUniquePts, 1.0) * (sampling_Freq / n);

    result_dict={}
    result_dict.__setitem__('fft_result', fft_result)
    result_dict.__setitem__('fft_mag', mag)
    result_dict.__setitem__('freq_array', freqArray/1000)#put in kHz

    return(result_dict)
    #return(savitzky_golay(fft_result, kernel = 11, order = 4))


def plot_fft(interp_list, fft_result_dict):

    fig = figure(figsize=(8,6), facecolor='#FFFFFF')
    ax = fig.add_subplot(221, axisbg='#FFFFFF')
    x=interp_list[0]
    y=interp_list[1]
    ax.plot(x,y, 'b')

    ax2 = fig.add_subplot(223, axisbg='#FFFFFF')

    line2, = ax2.plot(fft_result_dict.get('fft_mag'), 'r')

##    ax3 = fig.add_subplot(222)
##
##    ax3.plot(x,y, 'g')
##
##    ax4 = fig.add_subplot(224, axisbg='#FFFFFF')
##
##    line3, = ax4.plot(fft_result_dict.get('fft_mag'), 'k')

    show()


if __name__ == '__main__':
    data_array = get_ascii_data(File_Dialog())
    interpolated_data=interpolate_spectrum(data_array)
    fft_transform=fft_spectrum(interpolated_data[1])
    plot_fft(interpolated_data, fft_transform)





