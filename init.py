#!/usr/bin/python

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *
from pyqtgraph.Point import Point
from array import array

import subprocess
import time
import math
import numpy as np
import pyqtgraph as pg
import serial
import utiles

name_device = "/dev/ttyUSB0"
min_feq = "0412000"
max_feq = "0472000"
min_top = "050"
max_top = "120"

app = QtGui.QApplication([])
w = QtGui.QMainWindow()
area = DockArea()
w.setCentralWidget(area)
w.setGeometry(0, 0, 1750, 850)
#w.showMaximized()

# Se crean las areas (Docks)
grafica = Dock("Grafica RFExplorer", size=(1250, 850))
config = Dock("Configuracion", size=(500, 850), closable=True)
area.addDock(grafica, 'left')
area.addDock(config, 'right')

# Creacion de los botones de configuracion en el Dock config

# Se crea la grafica, se le da un nombre y se crea las labels abajo e izquierda y derecha
grafica_plot = pg.PlotWidget(title="RFExplorer")
grafica_plot.setLabel('left', 'Signal (dBm)')
grafica_plot.setLabel('bottom', 'Frecuencia (mHZ)')
grafica_plot.setLabel('right', 'Signal (dBm)')

#config.hide()
#if config.isVisible() is not True:
#    config.show()

# Se establecen maximos y minimos para la grafica, tanto en rango se medicion como para mostrar
grafica_plot.setRange(xRange=[float(min_feq), float(max_feq)], yRange=[-float(max_top), -float(min_top)])
#grafica_plot.setLimits(xMin=float(min_feq), xMax=float(max_feq), yMin=-float(max_top), yMax=-float(min_top))

# Elemento de la clase Plot, que es la curva de la grafica
curva = grafica_plot.plot()

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
grafica_plot.addItem(vLine, ignoreBounds=True)
#hLine = pg.InfiniteLine(angle=0, movable=False)
#grafica_plot.addItem(hLine, ignoreBounds=True)

vb = grafica_plot.plotItem.vb
def mouseMoved(evt):
    global grafica_plot, curva, vb, min_feq, max_feq, vLine
    utiles.mouseMoved(evt, grafica_plot, curva, vb, min_feq, max_feq, vLine)

proxy = pg.SignalProxy(grafica_plot.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

# Se anade la grafica al panel y se muestra.
grafica.addWidget(grafica_plot)
w.show();

# Funcion que actualiza los datos cada X tiempo.
def update():
    #utiles.update()
    global curva, grafica_plot
    x = []
    y = []

    p1 = subprocess.Popen(["./rfexplorer", name_device, min_feq, max_feq, min_top, max_top], stdout=subprocess.PIPE)
    str = p1.communicate()[0]
    resultados = str.split("\r\n")

    for i, res in enumerate(resultados):
        if res != '':
            frequency_signal = res.split("\t")
            x += [int(float(frequency_signal[0]))/1000]
            y += [float(frequency_signal[1])]
    curva.setData(x=x, y=y);

# Timer donde se indica que funcion se va a repetir cada X tiempo para actualizar la grafica
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
    str = p1.communicate()[0]
    resultados = str.split("\r\n")

    for i, res in enumerate(resultados):
        if res != '':
            frequency_signal = res.split("\t")
            print "%d => {F => %s, S => %s}" % (i, frequency_signal[0], frequency_signal[1])

    #print(p1.communicate()[0])
    time.sleep(1)
"""
