#!/usr/bin/env python
#import wx
import os

from SG_Filter import savitzky_golay
from scipy import optimize
import numpy as N
from pylab import *
from matplotlib.widgets import SpanSelector, Button
import CARSMath as CM

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


def findPeaks(data_array, peakWidth):

    #y_data = data_array[:,1]
    y_data = data_array

    WidthPoints=peakWidth  ##Average number of points in half-width of peaks (CHANGE TO FIT YOUR SIGNAL)
    SlopeThreshold=1/(WidthPoints**3)
    y_stdev = N.std(y_data)
    y_len = len(y_data)
    AmpThreshold=crudeNoiseEstimate(y_data, 3)#, sigmaThresh)y_stdev*2+N.mean(y_data)# first estimation of noise
#    print 'Threshold', AmpThreshold
    SmoothWidth=WidthPoints/2; #changed to * instead of / for gaussian fit ## SmoothWidth should be roughly equal to 1/2 the peak width (in points)
    FitWidth=WidthPoints/2; #changed to * ## FitWidth should be roughly equal to 1/2 the peak widths(in points)
    if FitWidth < 3:
        FitWidth=3

    PeakNumber=0

    smoothwidth=round(SmoothWidth)
    peakgroup=round(FitWidth)
    smoothed_data=savitzky_golay(y_data, kernel = 15, order = 4)
    #d=savitzky_golay(first_derivative(smoothed_data), kernel = 11, order = 4)
    d = derivative(smoothed_data)
    second_d = derivative(d)

    n=round(peakgroup/2)
    vectorlength=len(y_data)
    peak=1
    AmpTest=AmpThreshold

    p=N.arange(0,3,1)#peak parameters
    peak_loc=[]
    peak_intensity=[]
    peak_width=[]


    for j in range(len(d)-1): #d is the smoothed first derivative
        if sign(d[j]) > sign (d[j+1]): # Detects zero-crossing
            #print j
            if d[j]-d[j+1] > SlopeThreshold*y_data[j]: # if slope of derivative is larger than SlopeThreshold
                #setting up SNR screening which looks before and after the peak to get an idea of the local noise
                if (j - WidthPoints) < 0:
                    index_start_prev = 0#index start before peak
                    index_end_prev = j - WidthPoints#index end before peak
                    local_max_prev = 0
                elif (j - WidthPoints - 0.025*y_len) < 0:#if the peak location is close to the beginning
                    index_start_prev = 0#index start before peak
                    index_end_prev = j + WidthPoints#index end before peak #not sure if this is right changed to + sign 03/10/08 bhc
                    #print index_start_prev
                    #print index_end_prev
                    local_max_prev = N.max(y_data[index_start_prev:index_end_prev])
                else:
                    index_start_prev = j - WidthPoints - 0.025*y_len
                    index_end_prev = j - WidthPoints
                    local_max_prev = N.max(y_data[index_start_prev:index_end_prev])

                if (j + WidthPoints) > y_len:
                    index_start_after = 0#index start before peak
                    index_end_after = j + WidthPoints#index end before peak
                    local_max_after = 0
                elif (j + WidthPoints + 0.025*y_len) > y_len:#if the peak location is close to the beginning
                    index_start_after = 0#index start before peak
                    index_end_after = j + WidthPoints#index end before peak
                    local_max_after = N.max(y_data[index_start_prev:index_end_prev])
                else:
                    index_start_after = j + WidthPoints + 0.025*y_len
                    index_end_after = j + WidthPoints
                    local_max_after = N.max(y_data[index_start_prev:index_end_prev])

                if local_max_prev == 0:
                    local_max_prev = local_max_after
                elif local_max_after == 0:
                    local_max_after = local_max_prev

                local_max = (local_max_prev + local_max_after)/2

                if y_data[j] > AmpThreshold:#3*local_max: # if height of peak is larger than AmpThreshold
                    #print j
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
#                        print len(y_data), groupindex
                        yy.append(y_data[groupindex])

                    #print local_max
                    p = CM.fit_gaussian(xx, yy)
                    #noise_range = y_data[]
                    #if p[0] <= y_stdev:
                    #    print "low SNR...skipping"
                    #    continue

                    peak_intensity.append(p[0])
                    peak_loc.append(abs(p[1]))
                    peak_width.append(p[2])

                    ##print "Peak Intensity: ", p[0]
                    ##print "Peak Location:", p[1]
                    ##print "Width: ", p[2]
                    ##print ""

    file_info={}
    file_info['peak_location'] = peak_loc
    file_info['peak_intensity'] = peak_intensity
    file_info['peak_width'] = peak_width
    file_info['smoothed_data'] = smoothed_data
    file_info['smoothed_deriv'] = d
    file_info['second_deriv'] = second_d

    return file_info

###################

def get_ascii_data(filename):
    data_spectrum=load(filename, skiprows = 0, delimiter = ',' )##remember to change this depending on file format
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

    fig = figure(figsize=(8,6))
    ax = fig.add_subplot(211, axisbg='#FFFFFF')
    x=raw_data_x
    y=raw_data_y
    ax.plot(x,y, 'b')
    ax.plot(x, peak_result_dict.get('smoothed_data'), 'r')
    ax.plot(peak_result_dict.get('peak_location'), peak_result_dict.get('peak_intensity'), 'go')

    ax.set_title('Widget')

    ax2 = fig.add_subplot(212, axisbg='#FFFFFF', sharex=ax)
    line2, = ax2.plot(peak_result_dict.get('smoothed_deriv'))

    show()




if __name__ == '__main__':
    data_array = get_ascii_data(File_Dialog())
    #data_array = get_ascii_data('/home/clowers/Desktop/IMS-TOF Noise Project/Noisy_IMS_XY.csv')
    peak_info=Find_Peaks(data_array[:,1])
    plot_results(data_array[:,0], data_array[:,1], peak_info)



