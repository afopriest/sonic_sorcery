

import pyaudio
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import os
import time
from Xlib import X, display
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 14100
CHUNK = 1024
MAX_PLOT_SIZE = CHUNK * 50

# setup audio recording
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

win = pg.GraphicsWindow()
win.setWindowTitle("Microphone Audio Data")

# create a plot for the time domain data
data_plot = win.addPlot(title="Audio Signal Vs Time")
data_plot.setXRange(0 ,MAX_PLOT_SIZE)
data_plot.showGrid(True, True)
data_plot.addLegend()
time_curve = data_plot.plot(pen=(24,215,248), name = "Time Domain Audio")

# create a plot for the frequency domain data
win.nextRow()
fft_plot = win.addPlot(title="Power Vs Frequency Domain") 
fft_plot.addLegend()
fft_curve = fft_plot.plot(pen='y', name = "Power Spectrum")

fft_plot.showGrid(True, True)
total_data = []
frames=[]
i=0

def update():
    global stream, total_data, max_hold,i
    
    # read data
    raw_data = stream.read(CHUNK)
    
    # convert raw bytes into integers
    data_sample = np.fromstring(raw_data, dtype=np.int16)
    total_data = np.concatenate([total_data, data_sample ])
    
    # remove old data
    if len(total_data) > MAX_PLOT_SIZE:
        total_data = total_data[CHUNK:]
    time_curve.setData(total_data)
    
    # calculate the FFT
    fft_data = data_sample * np.hanning(len(data_sample))
    power_spectrum =  20*np.log10(np.abs(np.fft.rfft(fft_data))/len(fft_data)) + 50
    #power_spectrum = 20*(np.abs(np.fft.rfft(fft_data))/len(fft_data)) 
    #frames=power_spectrum[485:497]
 
    
    
    releFreqWindow=11
    leftband=1
    rightband=1
    maxratio=.7
    ratio1=power_spectrum[491-leftband]/power_spectrum[491]
    while leftband<releFreqWindow and ratio1 > maxratio :
        leftband=leftband+1
        ratio1=power_spectrum[491-leftband]/power_spectrum[491]
    if leftband>6 :
        print "left"
        print leftband
        '''os.system("amixer -D pulse sset Master 5%-")'''
        d = display.Display() #Display reference for Xlib manipulation
        s = d.screen()
        root = s.root
        #root.warp_pointer(1000,1000)
        #d.sync()

        button = 1
        Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
        d.sync()
        '''print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"'''
        button = 1
        Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
        d.sync()
        button=4
        Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
        d.sync()
        '''print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"'''
        button = 4
        Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
        d.sync()
        
        
        


    
    
    maxratio=.7
    ratio2=power_spectrum[491+rightband]/power_spectrum[491]
    while rightband<releFreqWindow and ratio2 > maxratio :
        rightband=rightband+1
        ratio2=power_spectrum[491+rightband]/power_spectrum[491]
    if rightband>6:
        print "right"
        print rightband
        os.system("amixer -D pulse sset Master 5%+")
        d = display.Display() #Display reference for Xlib manipulation
        s = d.screen()
        root = s.root
        #root.warp_pointer(1000,1000)
        #d.sync()

        button = 1
        Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
        d.sync()
        
        button = 1
        Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
        d.sync()
        button=5
        Xlib.ext.xtest.fake_input(d,X.ButtonPress, button)
        d.sync()
        button = 5
        Xlib.ext.xtest.fake_input(d,X.ButtonRelease, button)
        d.sync()


    print 
    #a=power_spectrum[480]+60
    #b=power_spectrum[491]+60
    #@c=power_spectrum[501]+60
    #print 
    #print 
    #print 
    #print 
    #c=power_spectrum[497]
    
    #if a>   .9*b:
        
    #    print "left"
    #    print a,b
    #    print a/b
    
    #print a/b
    #print  c/b
    #print  power_spectrum[490:492]
    fft_curve.setData(power_spectrum)
    fft_plot.enableAutoRange('xy', False)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt Event
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
