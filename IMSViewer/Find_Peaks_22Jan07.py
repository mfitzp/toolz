#!/usr/bin/env python
import os
import wx

import Find_Peaks as FP
import Interpolate_Spectrum_w_FFT as FFT
import numpy as N
from scipy import fftpack
from pylab import *


def Filter_Raw_Spectrum():
    #data_array=FFT.get_ascii_data(FP.File_Dialog())#setup for csv
    data_array=FFT.get_ascii_data('/home/clowers/Desktop/IMS-TOF Noise Project/Noisy_IMS_XY.csv')
    #interp_list contains (x_new, y_new)
    interp_list=FFT.interpolate_spectrum(data_array)
    
    #fft_ouput is a dictionary with 'fft_result', 'fft_mag', and 'freq_array'    
    fft_output=FFT.fft_spectrum(interp_list[1])
    
    '''peak results = dict{"peak_location", "peak_intensity", "peak_width"
                            "smoothed_data", "smoothed_deriv", "second_deriv"}'''
    peak_results = FP.Find_Peaks(fft_output.get('fft_mag'))
    
    filtered_fft=remove_peaks(fft_output.get('fft_result'), peak_results.get('peak_location'), peak_results.get('peak_width'))    
    filtered_spectrum = fftpack.ifft(filtered_fft)
    summary_plot(interp_list, fft_output, peak_results, filtered_spectrum)

def remove_peaks(raw_fft, peak_location, peak_width):
    '''The following routine extract and replaces the peak locations in 
    the raw_fft (which includes complex #s) with random values
    REMEMBER raw_fft CONTAINS COMPLEX NUMBERS'''
    filtered_fft = raw_fft.copy()
    for i in range(len(peak_location)):
        #print i    
        centroid=int(peak_location[i])#need to convert to integer for future indexing 
        sigma = peak_width[i]/2.35482    
        HW = int(N.round(10*sigma))#FW Baseline is (4*sigma) but we're going to use a wider range
        #print centroid, HW
                            #for the stats 
        real_array = raw_fft[(centroid-HW):(centroid+HW)].real
        imag_array = raw_fft[(centroid-HW):(centroid+HW)].imag
        real_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].real
        imag_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].imag
        
        real_stats_array = real_array[(0):(HW-HW/5)]
        imag_stats_array = imag_array[(0):(HW-HW/5)]
                
        random_fill_real = N.random.normal(loc = N.average(real_stats_array), scale = N.max(real_stats_array),size=len(real_array_pk))
        random_fill_imag = N.random.normal(loc = N.average(imag_stats_array), scale = N.max(imag_stats_array),size=len(imag_array_pk))
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].real = random_fill_real
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].imag = random_fill_imag   
    
    for j in range(len(peak_location)):
        centroid=int(len(raw_fft.real)-peak_location[j])#need to convert to integer for future indexing 
        sigma = peak_width[j]/2.35482    
        HW = int(N.round(10*sigma))#FW Baseline is (4*sigma) but we're going to use a wider range
                            #for the stats 
        real_array = raw_fft[(centroid-HW):(centroid+HW)].real
        imag_array = raw_fft[(centroid-HW):(centroid+HW)].imag
        real_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].real
        imag_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].imag
        
        real_stats_array = real_array[(0):(HW-HW/5)]
        imag_stats_array = imag_array[(0):(HW-HW/5)]
        
        random_fill_real = N.random.normal(loc = N.average(real_stats_array), scale = N.max(real_stats_array),size=len(real_array_pk))
        random_fill_imag = N.random.normal(loc = N.average(imag_stats_array), scale = N.max(imag_stats_array),size=len(imag_array_pk))
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].real = random_fill_real
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].imag = random_fill_imag 
        
    #plot(raw_fft)
    #plot(filtered_fft)
    #show()
        
    return filtered_fft   
##    x_range = N.arange(0, HW*2)
##    #the range below is to make the dimensions fit. An added 1 is necessary.
##    x_pk_range = N.arange(int(HW*2*0.4)+1,int(HW*2*0.6))    
##    
##    
##    filtered_real = real_array.copy()
##    filtered_imag = imag_array.copy()
##    
##    filtered_real[int(HW*2*0.4)+1:int(HW*2*0.6)] = random_fill_real
##    filtered_imag[int(HW*2*0.4)+1:int(HW*2*0.6)] = random_fill_imag
##    
##    plot(x_range, real_array)
##    plot(x_range, imag_array)
##    plot(x_pk_range, real_array_pk, 'go')
##    plot(x_pk_range, imag_array_pk, 'ro')
##    #plot(x_pk_range, random_fill_imag, 'bx')
##    #plot(x_pk_range, random_fill_real, 'kx')
##    plot(x_range, filtered_real, 'k:')
##    plot(x_range, filtered_imag, 'g:')
##    
##    show()
    
def summary_plot(interp_list, fft_result_dict, peak_result_dict, filtered_spectrum):
    
    fig = figure(figsize=(10,8), facecolor='#FFFFFF')
    ax = fig.add_subplot(311, axisbg='#FFFFFF')
    x=interp_list[0]
    y=interp_list[1]
    ax.plot(x,y, 'b')
    ax.plot(x, filtered_spectrum, 'r')
    ax.set_title('Mass Spectrum')
    
    ax2 = fig.add_subplot(312, axisbg='#FFFFFF')
    ax2.plot(fft_result_dict.get('fft_mag'), 'r')
    ax2.plot(peak_result_dict.get('smoothed_data'), 'b')
    ax2.plot(peak_result_dict.get('peak_location'), peak_result_dict.get('peak_intensity'), 'go')
    ax2.set_title('FFT (magnitude)')
    
    ax3 = fig.add_subplot(313, axisbg='#FFFFFF', sharex=ax2)
    #ax3.plot(x,y, 'b')
    #ax3.plot(fft_result_dict.get('fft_result'), 'k')
    zero_array=N.array(range(0, len(peak_result_dict.get('peak_location'))))
    zero_array*=0
    ax3.plot(peak_result_dict.get('smoothed_deriv'), 'k')
    ax3.plot(-10*(peak_result_dict.get('second_deriv')), 'r')
    ax3.plot(peak_result_dict.get('peak_location'), zero_array , 'go')
    
    show()
    


if __name__ == '__main__':
    Filter_Raw_Spectrum()

    
    

