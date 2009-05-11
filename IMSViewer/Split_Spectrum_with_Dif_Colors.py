#!/usr/bin/env python
import os

import numpy as N
from scipy import fftpack
from pylab import *

import Find_Peaks as FP
import Interpolate_Spectrum_w_FFT as FFT

colorlist = ['b','g','r','c','m','y','k'] 

def stitch_mz_spectrum(spectrum):
    '''spectrum is the interpolated spectrum containing two columns, x and y'''
    x=interp_list[0]
    y=interp_list[1]
        
    range = N.max(x)
    print "m/z range: ", range
    seg_range = 50 #mz range of each section
    num_steps = int(range/seg_range)
    print num_steps
    length = len(x)
    step_size = int(length/num_steps)
    stitch = y.copy()
    #stitch_x = x.copy()
    
    step = 0
    index_start = step*step_size
       
    step = 1
    print "Step :", step
    index_end = step_size*step
    section = y[index_start:index_end]
    
    color=0
    
    for i in xrange(seg_range):
        index_start = i*step_size
        index_end = (i+1)*step_size
        section = y[index_start:index_end]
        section_x = x[index_start:index_end]
        if i % len(colorlist) is 0:
            color = 0
        else:
            color+=1
        plot(section_x, section, colorlist[color])
        #print color
        #stitch[index_start:index_end] = section
    show()
    
    #print "Length", len(section)
    #fft_output=FFT.fft_spectrum(section)
    #peak_results = FP.Find_Peaks(fft_output.get('fft_mag'))
    #filtered_fft=remove_peaks(fft_output.get('fft_result'), peak_results.get('peak_location'), peak_results.get('peak_width'))    
    #filtered_section = fftpack.ifft(filtered_fft)
    
    #stitch[index_start:index_end] = filtered_section
    
    #index_start = step_size*step
        
    #return stitch
    #plot(y)
    #plot(stitch)
    #plot(section)
    #plot (filtered_section)
    #plot(fft_output.get('fft_result'))
    #plot(filtered_fft)
    #show()

    
    

def comparison_plot(interp_list, filtered_spectrum):
    
    fig = figure(figsize=(10,8), facecolor='#FFFFFF')
    ax = fig.add_subplot(111, axisbg='#FFFFFF')
    x=interp_list[0]
    y=interp_list[1]
    print len(x)
    ax.plot(x,y, 'b:')
    ax.plot(x, filtered_spectrum, 'r')
    ax.set_title('Fourier Filtering')
    ax.legend(('Raw Spectrum','Filtered Spectrum'))    
    show()

    
    
if __name__ == '__main__':
    data_array=FFT.get_ascii_data('C:\\Documents and Settings\\d3p483\\Desktop\\IMS-TOF Noise Project\\Noisy_IMS_XY.csv')
    interp_list=FFT.interpolate_spectrum(data_array)
    stitch_mz_spectrum(interp_list)
    #stitch = stitch_mz_spectrum(interp_list)
    #comparison_plot(interp_list, stitch)      
