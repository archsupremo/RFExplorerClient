#!/usr/bin/python

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *
from pyqtgraph.Point import Point

import subprocess
import time
import math
import numpy as np
import pyqtgraph as pg
import serial

name_device = "/dev/ttyUSB0"
min_feq = "0400000"
max_feq = "0420000"
min_top = "050"
max_top = "120"


win = pg.GraphicsWindow()
win.setWindowTitle('RFExplorer')
win.setGeometry(0, 0, 1750, 850)
#win.showMaximized()
win.addLabel("RFExplorer", colspan=2)
win.nextRow()

plot = win.addPlot()
plot.setLabel('left', 'Signal (dBm)')
plot.setLabel('bottom', 'Frecuencia (mHZ)')
plot.setLabel('right', '')
curva = plot.plot()

plot.setRange(xRange=[float(min_feq), float(max_feq)], yRange=[-float(max_top), -float(min_top)])
plot.setLimits(xMin=float(min_feq), xMax=float(max_feq), yMin=-float(max_top), yMax=-float(min_top))
datosx = [410000, 412000, 414000, 416000, 418000]
datosy = [-60, -70, -80, -90, -100]

def update():
    global curva, datosx, datosy
    curva.setData(datosx, datosy)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

"""
while True:
    subprocess.Popen(["clear"])
    print("--------------------------")
    print("Informacion del rfexplorer")
    print("--------------------------")
    p1 = subprocess.Popen(["./rfexplorer", name_device, min_feq, max_feq, min_top, max_top], stdout=subprocess.PIPE)
    print(p1.communicate()[0])

    time.sleep(1)
"""
