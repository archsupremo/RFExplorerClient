#!/usr/bin/python

from logging.handlers import TimedRotatingFileHandler
from time import gmtime, strftime
from pyqtgraph.Qt import QtGui, QtCore
import sys

def texts(config, texts):
    for text, spin, function_changed, modo_echo in texts:
        label = QtGui.QLabel(text)
        config.addWidget(label)
        config.addWidget(spin)
        spin.setEchoMode(modo_echo)

        if function_changed is not None:
            spin.editingFinished.connect(function_changed)

def spins(config, spins):
    for text, spin, function_changed in spins:
        label = QtGui.QLabel(text)
        config.addWidget(label)
        config.addWidget(spin)
        spin.sigValueChanged.connect(function_changed)

def crear_log(filename_log, ex):
    instant_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f = open(filename_log, "a")
    f.write("%s: %s \r\n\r\n" % (instant_time, str(ex)))
    f.close()

def limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top):
    grafica_plot.setRange(xRange=[float(min_feq), float(max_feq)], yRange=[-float(max_top), -float(min_top)])
    grafica_plot.setLimits(xMin=float(min_feq), xMax=float(max_feq), yMin=-float(max_top), yMax=-float(min_top))

def obtener_datos_x(index, datosx):
    for i in range(len(datosx)):
        if datosx[i] > index:
            return i-1

def mouseMoved(evt, grafica_plot, curva, vb, min_feq, max_feq, vLine):
    pos = evt[0]
    if grafica_plot.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > float(min_feq) and index < float(max_feq):
            x,y = curva.getData()
            try:
                res =  y[obtener_datos_x(index, x)]
                grafica_plot.setLabel('top', "<span style='font-size: 12pt'>x=%0.1f, <span style='color: red'>y=%0.1f</span>" % (mousePoint.x(), res))
            except Exception as ex:
                crear_log("log.log", ex)
        vLine.setPos(mousePoint.x())

# Para generar un histograma. No olvidar.
"""
for i, res in enumerate(resultados):
    if res != '':
        frequency_signal = res.split("\t")

        datos = [frequency_signal[0]]

        multiplicador = 120 - int(float(frequency_signal[1])) * -1
        vals = np.hstack([datos] * multiplicador)

        y, x = np.histogram(vals, bins=np.linspace(float(min_feq), float(max_feq), 150))

        grafica_plot.plot(x, y - 120, stepMode=True, fillLevel=0, brush=(0, 0, 0, 0))
"""

# Para leer en local, no olvidar
"""
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
"""
