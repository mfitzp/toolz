from pylab import *
from matplotlib.widgets import Slider, Button



voltage=1400##in volts
volt_range1=voltage*6.5##arbitrary scaling factor
volt_range=arange(0,100,2)

boltzmann_k=1.38065E-23 ## Joules/Kelvin
elementary_charge=1.60217646E-19 ## in Coulombs
temp=26.2 ##in degrees C
temp_kelvin=273.15 + temp
gatepulsewidth=200.0  ## in microseconds
drift_time=25.25 ## in ms
drift_length=88.2 ## in cm

numpoints=500

mobility_value=(drift_length**2)/(voltage*drift_time/1000)
print mobility_value

v_array=[]
resolving_power_array=[]
diffusion_array=[]
gpw_array=[]

n=0

for i in range(1,(numpoints+1)):
    theoretical_drift_time=(drift_length**2)/(i*((volt_range1/numpoints)*mobility_value))
    diffusion_width=theoretical_drift_time*sqrt((16*boltzmann_k*temp_kelvin*math.log(2))/(i*elementary_charge*(volt_range1/numpoints)))
    total_width=sqrt((diffusion_width**2)+((gatepulsewidth/1E6)**2))
    resolving_power=theoretical_drift_time/total_width
    
    v_array.append(i*volt_range1/numpoints)
    resolving_power_array.append(resolving_power)
    diffusion_array.append(theoretical_drift_time/diffusion_width)
    gpw_array.append(theoretical_drift_time/(gatepulsewidth/1E6))



ax = subplot(111)
subplots_adjust(bottom=0.3)

#t = arange(0.0, 1.0, 0.001)
#s = sin(2*pi*volt_range)
rp_plot=plot(v_array, resolving_power_array, 'r', v_array, diffusion_array, 'b:', v_array, gpw_array, 'g--')
#axis([0, 1, -10, 10])

ax.set_ylim((0,argmax(resolving_power_array)))

axcolor = 'lightgoldenrodyellow'
axfreq = axes([0.125, 0.1, 0.775, 0.03], axisbg=axcolor)
axamp  = axes([0.125, 0.15, 0.775, 0.03], axisbg=axcolor)

sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=1)
samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=1)

def update(val):
   amp = samp.val
   freq = sfreq.val
   l.set_ydata(amp*sin(2*pi*freq*voltage_array))
   draw()
sfreq.on_changed(update)
samp.on_changed(update)

resetax = axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset')

def reset(event):
   sfreq.reset()
   samp.reset()
button.on_clicked(reset)


show()

