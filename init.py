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
import sys
import utiles
from timer import Timer

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

# Se crea la grafica, se le da un nombre y se crea las labels abajo e izquierda y derecha
grafica_plot = pg.PlotWidget(title="RFExplorer")
grafica_plot.setLabel('left', 'Signal (dBm)')
grafica_plot.setLabel('bottom', 'Frecuencia (mHZ)')
grafica_plot.setLabel('right', 'Signal (dBm)')

#config.hide()
#if config.isVisible() is not True:
#    config.show()

# Se establecen maximos y minimos para la grafica, tanto en rango se medicion como para mostrar
utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

# Elemento de la clase Plot, que es la curva de la grafica
curva = grafica_plot.plot()

# cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
grafica_plot.addItem(vLine, ignoreBounds=True)

vb = grafica_plot.plotItem.vb
def mouseMoved(evt):
    global grafica_plot, curva, vb, min_feq, max_feq, vLine
    utiles.mouseMoved(evt, grafica_plot, curva, vb, min_feq, max_feq, vLine)

proxy = pg.SignalProxy(grafica_plot.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

# Se anade la grafica al panel y se muestra.
grafica.addWidget(grafica_plot)

# Pantalla de configuracion
def feq_minima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top
    min_feq = str(sb.value())
    utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

def feq_maxima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top
    max_feq = str(sb.value())
    utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

def signal_minima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top
    max_top = str(-sb.value())
    utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

def signal_maxima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top
    min_top = str(-sb.value())
    utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)


# Creacion de los botones de configuracion en el Dock config
spins = [
    ("Frecuencia Minima (mHZ)", pg.SpinBox(value=float(min_feq), dec=True, minStep=1, step=1), feq_minima_changed),
    ("Frecuencia Maxima (mHZ)", pg.SpinBox(value=float(max_feq), dec=True, minStep=1, step=1), feq_maxima_changed),
    ("Signal Minima (dBm)", pg.SpinBox(value=-float(max_top), dec=True, minStep=1, step=1), signal_minima_changed),
    ("Signal Maxima (dBm)", pg.SpinBox(value=-float(min_top), dec=True, minStep=1, step=1), signal_maxima_changed)
]

for text, spin, function_changed in spins:
    label = QtGui.QLabel(text)
    config.addWidget(label)
    config.addWidget(spin)
    spin.sigValueChanged.connect(function_changed)

start = QtGui.QPushButton('Empezar Lectura')
stop = QtGui.QPushButton('Parar Lectura')
config.addWidget(start)
config.addWidget(stop)

# Funcion que actualiza los datos cada X tiempo.
def update():
    global lectura, curva, grafica_plot, name_device, min_feq, max_feq, min_top, max_top
    x = []
    y = []
    dats_rfexplorer = ["./rfexplorer", name_device, min_feq, max_feq, min_top, max_top]

    p1 = subprocess.Popen(dats_rfexplorer, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    str, err = p1.communicate()
    if str:
        resultados = str.split("\r\n")

        for i, res in enumerate(resultados):
            if res != '':
                frequency_signal = res.split("\t")
                x += [int(float(frequency_signal[0]))/1000]
                y += [float(frequency_signal[1])]
        curva.setData(x=x, y=y);


# Timer donde se indica que funcion se va a repetir cada X tiempo para actualizar la grafica
t = Timer(update, 50)
t.start()

start.clicked.connect(t.iniciar_lectura)
stop.clicked.connect(t.parar_lectura)

w.show();
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
