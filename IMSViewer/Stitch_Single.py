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

    mz_range = 100 #mz range of each section
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

    #plot(window)
    #show()

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
##        plot(section_x, section, colorlist[color])
##        plot(section_x, window*50000, 'b')

    i=6
    index_start = step_size*i-over_length
    index_end = step_size*(i+1)+over_length
    #print index_end-index_start
    #print index_start
    #print step_size*i
    #print index_end
    #print step_size*(i+1)

    #print ""
    section = y[index_start:index_end]

    section=section*window
    section_x = x[index_start:index_end]
    if i % len(colorlist) is 0:
        color = 0
    else:
        color+=1

    filtered_section = transform_segment(section)

    comparison_plot(section_x, section, filtered_section)
    #plot(section_x, section, colorlist[color])
    #plot(section_x, window*50000, 'b')
    #plot(section_x, filtered_section, 'r')



    #show()


def transform_segment(interp_chunk):
    fft_output=FFT.fft_spectrum(interp_chunk)
    '''peak results = dict{"peak_location", "peak_intensity", "peak_width"
                            "smoothed_data", "smoothed_deriv", "second_deriv"}'''
    peak_results = FP.Find_Peaks(fft_output.get('fft_mag'))
#    filtered_fft=remove_peaks(fft_output.get('fft_result'), peak_results.get('peak_location'), peak_results.get('peak_width'))
#    filtered_spectrum = fftpack.ifft(filtered_fft)
    #return fft_output.get('fft_mag')
    #return filtered_fft
    #return filtered_spectrum
    return peak_results

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


def remove_peaks(raw_fft, peak_location, peak_width):
    '''The following routine extract and replaces the peak locations in
    the raw_fft (which includes complex #s) with random values
    REMEMBER raw_fft CONTAINS COMPLEX NUMBERS'''
    filtered_fft = raw_fft.copy()
    for i in range(len(peak_location)):
        centroid=int(peak_location[i])#need to convert to integer for future indexing
        sigma = peak_width[i]/2.35482
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

        random_fill_real = N.random.normal(loc = N.average(real_stats_array), scale = N.max(real_stats_array),size=len(real_array_pk))
        random_fill_imag = N.random.normal(loc = N.average(imag_stats_array), scale = N.max(imag_stats_array),size=len(imag_array_pk))
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].real = random_fill_real
        filtered_fft[(centroid-HW/5):(centroid+HW/5)].imag = random_fill_imag

    for j in range(len(peak_location)):
        centroid=int(len(raw_fft.real)-peak_location[j])#need to convert to integer for future indexing
        sigma = peak_width[j]/2.35482
        HW = int(N.round(10*sigma))#FW Baseline is (4*sigma) but we're going to use a wider range
                            #for the stats
        if HW > centroid:
            continue
            #HW = centroid - 1
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
