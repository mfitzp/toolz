from pylab import *
from File_Dialog import File_Dialog

def run_IMS():
    display_IMS(get_IMS_ascii(File_Dialog()))
            
def get_IMS_ascii(filename):
    IMS_spectrum=load(filename,skiprows=1)
    return IMS_spectrum

def display_IMS(IMS_array):
    drift_time=IMS_array[:,0]/1e6
    intensity=IMS_array[:,1]
    figure(num=1, figsize=(9,7), frameon=True)
    plot(drift_time, intensity)
    font = {'fontname'   : 'Arial',
        'color'      : 'b',
        'fontweight' : 'bold',
        'fontsize'   : 10}
    
    xlabel('Drift Time (ms)',font)
    ylabel('Intensity',font)
    grid(True,linewidth=0.5,color='g')
    show()


