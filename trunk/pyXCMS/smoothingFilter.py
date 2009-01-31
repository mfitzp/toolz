#!/usr/bin/env python
#import wx
import os

from pylab import *
import numpy as N

#######################

def File_Dialog():
# setup the GUI main loop
    app = wx.PySimpleApp()
    filename = wx.FileSelector(message='Select Data File', default_path=os.getcwd(), parent=None)
    return filename

###################

def get_ascii_data(filename):
    data_spectrum=load(filename,skiprows=0)##remember to change this depending on file format
    return data_spectrum

###################

def savitzky_golay(data, kernel = 11, order = 4):
    """
        applies a Savitzky-Golay filter
        input parameters:
        - data => data as a 1D numpy array
        - kernel => a positive integer > 2*order giving the kernel size
        - order => order of the polynomal
        returns smoothed data as a numpy array

        invoke like:
        smoothed = savitzky_golay(<rough>, [kernel = value], [order = value]
    """
    try:
            kernel = abs(int(kernel))
            order = abs(int(order))
    except ValueError, msg:
        raise ValueError("kernel and order have to be of type int (floats will be converted).")
    if kernel % 2 != 1 or kernel < 1:
        raise TypeError("kernel size must be a positive odd number, was: %d" % kernel)
    if kernel < order + 2:
        raise TypeError("kernel is to small for the polynomals\nshould be > order + 2")

    # a second order polynomal has 3 coefficients
    order_range = range(order+1)
    half_window = (kernel -1) // 2
    b = N.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    # since we don't want the derivative, else choose [1] or [2], respectively
    m = N.linalg.pinv(b).A[0]
    window_size = len(m)
    half_window = (window_size-1) // 2

    # precompute the offset values for better performance
    offsets = range(-half_window, half_window+1)
    offset_data = zip(offsets, m)

    smooth_data = list()

    # temporary data, with padded zeros (since we want the same length after smoothing)
    #data = numpy.concatenate((numpy.zeros(half_window), data, numpy.zeros(half_window)))
    # temporary data, with padded first/last values (since we want the same length after smoothing)
    firstval=data[0]
    lastval=data[len(data)-1]
    data = N.concatenate((N.zeros(half_window)+firstval, data, N.zeros(half_window)+lastval))

    for i in range(half_window, len(data) - half_window):
            value = 0.0
            for offset, weight in offset_data:
                value += weight * data[i + offset]
            smooth_data.append(value)
    return N.array(smooth_data)

##################

def first_derivative(y_data):
    """\
    calculates the derivative
    """

    y = (y_data[1:]-y_data[:-1])

    dy = y/2#((x_data[1:]-x_data[:-1])/2)

    return dy


##################

def plot_smoothed(data_array):
    y_data = data_array[:,2]
    x_data = data_array[:,0]
    smth_y_data = savitzky_golay(y_data, kernel = 11, order = 4)
    #intensity=IMS_array[:,1]
    figure(num=1, figsize=(9,7), frameon=True)
    plot(y_data, 'ro')
    plot(y_data)
    plot(smth_y_data)
    #plot(first_derivative(x_data, smth_y_data))
    plot(first_derivative(savitzky_golay(smth_y_data, kernel = 11, order = 4)))

    font = {'fontname'   : 'Arial',
        'color'      : 'black',
        'fontweight' : 'bold',
        'fontsize'   : 10}

    xlabel('x',font)
    ylabel('Intensity',font)
    grid(True,linewidth=0.5,color='g')
    show()





if __name__ == '__main__':
    data_array = get_ascii_data(File_Dialog())
    plot_smoothed(data_array)


