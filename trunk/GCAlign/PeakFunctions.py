#!/usr/bin/env python
#import wx
import os

from SG_Filter import savitzky_golay
from scipy import optimize
import numpy as N
import pylab as P
from matplotlib.widgets import SpanSelector, Button
import CARSMath as CM

from baseline2 import SplitNSmooth

#######################
'''Function to locate the positive peaks in a noisy x-y data
    % set.  Detects peaks by looking for downward zero-crossings
    % in the first derivative that exceed SlopeThreshold.
    % Returns list (P) containing peak number and
    % position, height, and width of each peak. SlopeThreshold,
    % AmpThreshold, and smoothwidth control sensitivity
    % Higher values will neglect smaller features. Peakgroup
    % is the number of points around the "top part" of the peak.
    % T. C. O'Haver, 1995.  Version 2  Last revised Oct 27, 2006

    Revised for Python by Brian H. Clowers, October 15, 2007'''

def crudeNoiseEstimate(datArray, sigmaThresh=3):
    '''
    Accepts a numpy array and zeros the values below the user defined threshold
    '''
    mean = datArray.mean()
    std = datArray.std()
    thresh = mean+std*5
    #first pass selection to minimize contribution of large peaks
    #only takes values below the thresh
    #should use clip
    noiseArray = N.select([datArray<thresh],[datArray],default = mean)


    mean2 = noiseArray.mean()
    std2 = noiseArray.std()
    thresh2 = mean2+std2*sigmaThresh

    return thresh2


def findPeaks(data_array, peakWidth, minSNR = 3, slopeThresh = None, ampThresh = None,\
              smthKern = None, fitWidth = None,  peakWin = None):
    '''
    peakWidth = Average number of points in half-width of peaks (CHANGE TO FIT YOUR SIGNAL)
    minSNR = minimum SNR for a peak to be considered, noise is defined by function crudeNoiseEstimate
    slopeThresh = threshold of the first derivative from which a peak should be detected
    ampThresh = absolute value for the threshold cutoff
    smthKern = width to use for Savitzky-Golay smoothing of derivative
    '''
    data_array = data_array.astype(N.float32)
    if slopeThresh == None:
        SlopeThreshold=1/(peakWidth**3)
    else:
        SlopeThreshold = slopeThresh
    y_stdev = N.std(data_array)
    y_len = len(data_array)
    if ampThresh == None:
        gblThreshold=crudeNoiseEstimate(data_array, minSNR)#, sigmaThresh)y_stdev*2+N.mean(data_array)# first estimation of noise
        AmpThreshold, minNoise = SplitNSmooth(data_array, len(data_array)/10, minSNR)
    else:
        gblThreshold=crudeNoiseEstimate(data_array, minSNR)#, sigmaThresh)y_stdev*2+N.mean(data_array)# first estimation of noise
        AmpThreshold,minNoise = SplitNSmooth(data_array, len(data_array)/10, minSNR)
#        AmpThreshold = ampThresh
#    print 'Threshold', AmpThreshold
    if smthKern == None:
        smthKern = 15#=peakWidth/2 #SmoothWidth should be roughly equal to 1/2 the peak width (in points)
    else:
        smthKern = smthKern

    if fitWidth == None:
        FitWidth=peakWidth/2 #FitWidth should be roughly equal to 1/2 the peak widths(in points)
    else:
        FitWidth = fitWidth

    if peakWin == None:
        peakWindow = 0.025
    else:
        peakWindow = peakWin
    if FitWidth < 3:
        FitWidth=3

    PeakNumber=0

    peakgroup=round(FitWidth)
    smoothed_data=savitzky_golay(data_array, kernel = smthKern, order = 4)
    #d=savitzky_golay(first_derivative(smoothed_data), kernel = 11, order = 4)
    d = derivative(smoothed_data)
    smthAmpThresh = savitzky_golay(N.clip(AmpThreshold, 0, AmpThreshold.max()), kernel = smthKern, order = 4)
    smthAmpThresh = N.clip(smthAmpThresh,0,smthAmpThresh.max())
    #the gblThreshold2 is a rough estimate of the baseline estimate of the noise
    #it allows the lower abundance peaks to be identified with a greater degree of reliability.
    gblThreshold2=crudeNoiseEstimate(smthAmpThresh, minSNR/5)
#    second_d = derivative(d)

    n=round(peakgroup/2)
    vectorlength=len(data_array)
    peak=1

    p=N.arange(0,3,1)#peak parameters
    peak_loc=[]
    peak_intensity=[]
    peak_width=[]
    peak_area = []


    for j in xrange(len(d)-1): #d is the smoothed first derivative
        if N.sign(d[j]) > N.sign (d[j+1]): # Detects zero-crossing
            #print j
            if d[j]-d[j+1] > SlopeThreshold*data_array[j]: # if slope of derivative is larger than SlopeThreshold
                #setting up SNR screening which looks before and after the peak to get an idea of the local noise
                if (j - peakWidth) < 0:
                    index_start_prev = 0#index start before peak
                    index_end_prev = j - peakWidth#index end before peak
                    local_max_prev = 0
                elif (j - peakWidth - peakWindow*y_len) < 0:#if the peak location is close to the beginning
                    index_start_prev = 0#index start before peak
                    index_end_prev = j + peakWidth#index end before peak #not sure if this is right changed to + sign 03/10/08 bhc
                    #print index_start_prev
                    #print index_end_prev
                    local_max_prev = N.max(data_array[index_start_prev:index_end_prev])
                else:
                    index_start_prev = j - peakWidth - peakWindow*y_len
                    index_end_prev = j - peakWidth
                    local_max_prev = N.max(data_array[index_start_prev:index_end_prev])

                if (j + peakWidth) > y_len:
                    index_start_after = 0#index start before peak
                    index_end_after = j + peakWidth#index end before peak
                    local_max_after = 0
                elif (j + peakWidth + peakWindow*y_len) > y_len:#if the peak location is close to the beginning
                    index_start_after = 0#index start before peak
                    index_end_after = j + peakWidth#index end before peak
                    local_max_after = N.max(data_array[index_start_prev:index_end_prev])
                else:
                    index_start_after = j + peakWidth + peakWindow*y_len
                    index_end_after = j + peakWidth
                    local_max_after = N.max(data_array[index_start_prev:index_end_prev])

                if local_max_prev == 0:
                    local_max_prev = local_max_after
                elif local_max_after == 0:
                    local_max_after = local_max_prev

                local_max = (local_max_prev + local_max_after)/2

                #if data_array[j] > AmpThreshold[j]:#3*local_max: # if height of peak is larger than AmpThreshold
                if data_array[j] > gblThreshold2:#3*local_max: # if height of peak is larger than AmpThreshold
#                    print j, data_array[j], AmpThreshold[j]
                    xx=[]
                    yy=[]
                    noise_range=[]
                    for k in range(int(peakgroup)): # Create sub-group of points near peak
                        groupindex=j+k-n+1
                        if groupindex<1:
                            groupindex=1
                        if groupindex >= vectorlength:
                            groupindex = vectorlength-1
                        xx.append(groupindex)
#                        print len(data_array), groupindex
                        yy.append(data_array[groupindex])

                    #print local_max
                    p = CM.fit_gaussian(xx, yy)
                    #noise_range = data_array[]
                    #if p[0] <= y_stdev:
                    #    print "low SNR...skipping"
                    #    continue

#                    if p[0]>53185522652:
#                        plot(data_array)
#                        show()
#                        print 'too big'

                    peak_intensity.append(p[0])
                    peak_loc.append(abs(p[1]))
                    peak_width.append(p[2])
                    peak_area.append(N.trapz(yy, xx))

                    ##print "Peak Intensity: ", p[0]
                    ##print "Peak Location:", p[1]
                    ##print "Width: ", p[2]
                    ##print ""
#                elif data_array[j] > gblThreshold2:#used to screen very low noise peaks.
##                    print j, data_array[j], AmpThreshold[j]
#                    xx=[]
#                    yy=[]
#                    noise_range=[]
#                    for k in range(int(peakgroup)): # Create sub-group of points near peak
#                        groupindex=j+k-n+1
#                        if groupindex<1:
#                            groupindex=1
#                        if groupindex >= vectorlength:
#                            groupindex = vectorlength-1
#                        xx.append(groupindex)
#                        yy.append(data_array[groupindex])
#
#                    p = CM.fit_gaussian(xx, yy)
#                    peak_intensity.append(p[0])
#                    peak_loc.append(abs(p[1]))
#                    peak_width.append(p[2])
#                    peak_area.append(N.trapz(yy, xx))


    file_info={}
    file_info['peak_location'] = N.array(peak_loc)
    file_info['peak_intensity'] = N.array(peak_intensity)
    file_info['peak_width'] = N.array(peak_width)
    file_info['peak_area'] = N.array(peak_area)
#    file_info['smoothed_data'] = N.array(smoothed_data)
#    file_info['smoothed_deriv'] = d
#    file_info['second_deriv'] = second_d

    return file_info

###################

def get_ascii_data(filename):
    data_spectrum=P.load(filename, skiprows = 0, delimiter = ',' )##remember to change this depending on file format
    print "File Loaded: ", filename
    return data_spectrum

###################

def derivative(y_data):
    '''calculates the 1st derivative'''

    y = (y_data[1:]-y_data[:-1])

    dy = y/2 #((x_data[1:]-x_data[:-1])/2)

    return dy

############################
def plot_results(raw_data_x, raw_data_y, peak_result_dict):

    fig = P.figure(figsize=(8,6))
    ax = fig.add_subplot(111, axisbg='#FFFFFF')
    x=raw_data_x
    y=raw_data_y
    ax.plot(x,y, 'b')
#    sdata = peak_result_dict['smoothed_data']

#    ax.plot(x, peak_result_dict.get('smoothed_data'), 'r')
    ax.plot(peak_result_dict.get('peak_location'), peak_result_dict.get('peak_intensity'), 'go')
    noise,minNoise = SplitNSmooth(y, len(y)/10, 10)
    print len(y)
    smthNoise = savitzky_golay(N.clip(noise,0,noise.max()), kernel = 15, order = 4)
    smthNoiseZero = N.clip(smthNoise, 0, smthNoise.max())
    gblThreshold2=crudeNoiseEstimate(smthNoiseZero, 10/5)
#    smthAmpThresh = savitzky_golay(N.clip(AmpThreshold, 0, AmpThreshold.max()), kernel = smthKern, order = 4)
    ax.plot(smthNoise, '-g', alpha = 0.5)
#    ax.plot(smthNoiseZero, '-k', alpha = 0.5)
    ax.plot(noise, '-r', alpha = 0.5)
    ax.hlines(crudeNoiseEstimate(y, 10), 0, len(y))
    ax.hlines(gblThreshold2, 0, len(y), 'b')

#    ax.set_title('Widget')
#
#    ax2 = fig.add_subplot(212, axisbg='#FFFFFF', sharex=ax)
#    line2, = ax2.plot(peak_result_dict.get('smoothed_deriv'))

    P.show()




if __name__ == '__main__':
#    data_array = get_ascii_data(File_Dialog())
    data_array = get_ascii_data('chrom1D.csv')
#    data_array = data_array[0:500]
#    P.plot(data_array)
    x = N.arange(len(data_array))
    y = data_array
#    P.plot(x,y)
    peak_info=findPeaks(data_array, 10, minSNR = 10)
    plot_results(x, y, peak_info)
#    P.show()



