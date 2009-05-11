#!/usr/bin/env python
import os

import numpy as N
from scipy import fftpack
from pylab import *

import Find_Peaks as FP
import Interpolate_Spectrum_w_FFT as FFT
import Filter_Noise as FN
import CARSMath as CM
import Savitsky_Golay_Filter as SG

colorlist = ['b','g','r','c','m','y','k']

def stitch_mz_spectrum(spectrum):
    '''spectrum is the interpolated spectrum containing two columns, x and y'''
    x=interp_list[0]
    y=interp_list[1]

    filtered_data = y.copy()

    range = N.max(x)
    mz_range = 250 #mz range of each section
    num_steps = int(range/mz_range)
    total_length = len(x)
    step_size = int(total_length/num_steps)
    over_length_percentage = 10
    over_length = N.floor(step_size*(over_length_percentage/100.0)) #% of the segment size on each end

    print "m/z range: ", range
    print 'Array Length: ', total_length
    print 'For segments of %(range)s m/z, there are %(steps)s steps, each with %(seg_length)s points' % \
    {'range': str(mz_range), 'steps': str(num_steps), 'seg_length': str(step_size)}

    color=0

    window = chunk_window(step_size, over_length_percentage)

##    fig = figure(figsize=(10,8), facecolor='#FFFFFF')
##    ax = fig.add_subplot(111, axisbg='#FFFFFF')
##    ax.set_title('Mass Spectrum')
##
##    for i in xrange(1,num_steps-1):
##        index_start = step_size*i-over_length
##        index_end = step_size*(i+1)+over_length
##        #print index_end-index_start
##        #print index_start
##        #print step_size*i
##        #print index_end
##        #print step_size*(i+1)
##
##        #print ""
##        section = y[index_start:index_end]
##
##        section=section*window
##        section_x = x[index_start:index_end]
##        if i % len(colorlist) is 0:
##            color = 0
##        else:
##            color+=1
##
##        filtered_section = transform_segment(section)
##        filtered_data[index_start:index_end] = filtered_section
##        ax.plot(section_x, section, 'r:')
##        ax.plot(section_x, window*50000, 'b')
##        ax.plot(section_x, filtered_section, colorlist[color])
##
##    show()
    #comparison_plot(x, y, filtered_data)

    fig = figure(figsize=(10,8), facecolor='#FFFFFF')
    ax = fig.add_subplot(211, axisbg='#FFFFFF')
    ax2 = fig.add_subplot(212, axisbg='#FFFFFF')
    for i in xrange(1,4):
        #i=2
        index_start = step_size*i-over_length
        index_end = step_size*(i+1)+over_length
        section = y[index_start:index_end]

        section=section*window
        section_x = x[index_start:index_end]
        if i % len(colorlist) is 0:
            color = 0
        else:
            color+=1

        #filtered_section = transform_segment(section)
        fft_output=FFT.fft_spectrum(section)
        test = (fft_output.get('fft_result')).copy()
        filtered = transform_segment(section)






        #filtered_spectrum = fftpack.ifft(fft_output.get('fft_result'))
        ax2.plot(section_x, filtered[0], 'b')
        ax2.plot(section_x, section, 'r:')

    ax.plot(test, 'r:')
    ax.plot(filtered[1].get('fft_result'), 'g')
    show()

def transform_segment(interp_chunk):
    fft_output=FFT.fft_spectrum(interp_chunk)

    fft_filtered = remove_peaks_by_harmonic(fft_output)
    num_filters = 2
    for i in range(num_filters):
        fft_filtered = remove_peaks_by_harmonic(fft_filtered)

    filtered_spectrum = fftpack.ifft(fft_filtered.get('fft_result'))
    return filtered_spectrum, fft_filtered


def remove_peaks_by_harmonic(fft_dictionary):
    '''returns the same dictionary after it has been filtered'''
    fft_magnitude = fft_dictionary.get('fft_mag')
    max_peak_params = fitmax2gaussian(fft_magnitude.real)
    max_loc = int(round(max_peak_params[1]))#most abundant peak
    max_peak_width = int(round(max_peak_params[2]))

    harmonic_loc_x = N.arange(0,15)
    harmonic_loc_y = N.arange(0,15)

    for i in range(len(harmonic_loc_x)):
        harmonic_loc_x[i] = i * max_loc
        if harmonic_loc_x[i] < len(fft_magnitude.real):
            harmonic_loc_y[i] = fft_magnitude.real[harmonic_loc_x[i]]
        else:
            break

    harmonic_loc_x = harmonic_loc_x[0:i]
    harmonic_loc_y = harmonic_loc_y[0:i]

    for peak in harmonic_loc_x:
        '''we can set this to zero because the mag is only used for peak picking'''
        fft_magnitude.real[(peak-max_peak_width):(peak+max_peak_width)] = 0


    '''The following routine extract and replaces the peak locations in
    the raw_fft (which includes complex #s) with random values
    REMEMBER raw_fft CONTAINS COMPLEX NUMBERS'''
    filtered_fft = fft_dictionary.get('fft_result').copy()
    raw_fft = fft_dictionary.get('fft_result')
    for j in range(len(harmonic_loc_x)):
        centroid=int(harmonic_loc_x[j])#need to convert to integer for future indexing
        sigma = max_peak_params[2]/2.35482
        HW = int(N.round(5*sigma))#FW Baseline is (4*sigma) but we're going to use a wider range
                            #for the stats
        if HW > centroid:
            continue

        real_array = raw_fft[(centroid-HW):(centroid+HW)].real
        imag_array = raw_fft[(centroid-HW):(centroid+HW)].imag
        real_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].real
        imag_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].imag

        real_stats_array = real_array[(0):(HW-HW/5)]
        imag_stats_array = imag_array[(0):(HW-HW/5)]

        random_fill_real = N.random.normal(loc = N.average(real_stats_array), scale = N.max(real_stats_array)/2,size=len(real_array_pk))
        random_fill_imag = N.random.normal(loc = N.average(imag_stats_array), scale = N.max(imag_stats_array)/2,size=len(imag_array_pk))
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].real = random_fill_real
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].imag = random_fill_imag
    '''I know this is lazy but that's how I'm feeling right now'''
    for n in range(len(harmonic_loc_x)):
        centroid=int(len(raw_fft.real)-harmonic_loc_x[n])#need to convert to integer for future indexing
        sigma = max_peak_params[2]/2.35482
        HW = int(N.round(10*sigma))#FW Baseline is (4*sigma) but we're going to use a wider range
                            #for the stats
        if HW > centroid:
            continue

        real_array = raw_fft[(centroid-HW):(centroid+HW)].real
        imag_array = raw_fft[(centroid-HW):(centroid+HW)].imag
        real_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].real
        imag_array_pk = raw_fft[(centroid-HW/5):(centroid+HW/5)].imag

        real_stats_array = real_array[(0):(HW-HW/5)]
        imag_stats_array = imag_array[(0):(HW-HW/5)]

        random_fill_real = N.random.normal(loc = N.average(real_stats_array), scale = N.max(real_stats_array)/2,size=len(real_array_pk))
        random_fill_imag = N.random.normal(loc = N.average(imag_stats_array), scale = N.max(imag_stats_array)/2,size=len(imag_array_pk))
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].real = random_fill_real
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].imag = random_fill_imag


    ########################################################
    fft_dictionary['fft_mag']=fft_magnitude
    fft_dictionary['fft_result']=filtered_fft

    return fft_dictionary


def fitmax2gaussian(spectral_array):
    start_point = int(round(len(spectral_array)*0.25))
    '''this ignores the first 2% because we don't want the primary in the fft
    magnitude spectrum to register'''
    subset = spectral_array[start_point:]
    spectral_max = N.max(spectral_array[start_point:])
    spectral_max_loc = N.argmax(subset)
    shift = spectral_max_loc + start_point
    #print spectral_max
    #print spectral_max_loc
    #print start_point
    #print shift
    '''It is assumed that the peak width at the base
    for the noise frequencies is approximately 10 points and is smaller than
    the shift!!!! This is key'''
    fwhb = 3

    fit_x = N.arange(shift - fwhb, shift + fwhb)
    fit_y = spectral_array[shift - fwhb: shift + fwhb]
    smoothed_data=SG.savitzky_golay(fit_y, kernel = 5, order = 2)
    peak_params = CM.fit_gaussian(fit_x, smoothed_data)

    return peak_params

def derivative(y_data):
    '''calculates the 1st derivative'''

    y = (y_data[1:]-y_data[:-1])

    dy = y/2 #((x_data[1:]-x_data[:-1])/2)

    return dy



def chunk_window(segmentsize, percent_extension):
    '''used to generate the windowing that will be applied to each spectral chunk
    segmentsize is the size of the chunk before extension by the value of the second
    variable.  This variable, percent extension, is the % by which
    the chunk will be extended on both ends'''
    #print segmentsize
    extension_length = N.floor(segmentsize*(percent_extension/100.0))
    #print extension_length
    total_length=segmentsize+2*extension_length
    slope = 1.0/(extension_length)
    window_func=N.ones(total_length)
    for i in xrange(int(extension_length)):
        window_func[i]=slope*i
        window_func[i+segmentsize+extension_length]=((slope*i)*-1)+1

    #print "Window Length: ", total_length
    return window_func



def comparison_plot(x_interp_spectrum, y_interp_spectrum, filtered_spectrum):

    fig = figure(figsize=(10,8), facecolor='#FFFFFF')
    ax = fig.add_subplot(211, axisbg='#FFFFFF')
    x=x_interp_spectrum
    y=y_interp_spectrum
    ax.plot(x,y, 'b')
    #ax.plot(x, interp_spectrum, 'r')
    ax.set_title('Mass Spectrum')

    ax2 = fig.add_subplot(212, axisbg='#FFFFFF')
    ax2.plot(x, filtered_spectrum, 'r')
    ax2.set_title('Filtered Data')

    show()


if __name__ == '__main__':
    data_array=FFT.get_ascii_data('C:\\Documents and Settings\\d3p483\\Desktop\\IMS-TOF Noise Project\\Noisy_IMS_XY.csv')
    interp_list=FFT.interpolate_spectrum(data_array)
    stitch_mz_spectrum(interp_list)
    #stitch = stitch_mz_spectrum(interp_list)
    #comparison_plot(interp_list, stitch)
