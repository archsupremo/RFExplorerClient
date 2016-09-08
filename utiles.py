#!/usr/bin/python

from logging.handlers import TimedRotatingFileHandler
from time import gmtime, strftime
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *
from Tkinter import *

import sys
import re
import tkMessageBox

def validacion(valor, regex, string_output):
    patron = re.compile(regex)

    if patron.search(valor) == None:
        print valor
        window = Tk()
        window.wm_withdraw()

        window.geometry("1x1+200+200")#remember its .geometry("WidthxHeight(+or-)X(+or-)Y")
        window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))

        tkMessageBox.showerror(title="Error!!!",message=string_output,parent=window)

        return False
    print valor
    return True

def extract(locales, array_config):
    for var,res in array_config.iteritems():
        locales[var] = res

def leer_config(name_config):
    config = {}
    f = open(name_config, "r")
    for linea in f.readlines():
        if linea[0] == '#' or not linea or linea == "\r\n": continue

        line = linea.split('=')
        string_res = line[1].replace("\r\n", "").strip()

        if string_res == 'True':
            string_res = True
        elif string_res == 'False':
            string_res = False

        string_res = string_res
        config[line[0].strip()] = string_res
    return config

def escribir_config_analyzer(name_device, ip, username, password, min_feq, max_feq, min_top, max_top):
    f = open("config_analyzer.txt", "w")
    f.write("name_device_analyzer=%s\r\n" % (name_device))
    f.write("ip_analyzer=%s\r\n" % (ip))
    f.write("username_analyzer=%s\r\n" % (username))
    f.write("password_analyzer=%s\r\n" % (password))
    f.write("min_feq=%s\r\n" % (min_feq))
    f.write("max_feq=%s\r\n" % (max_feq))
    f.write("min_top=%s\r\n" % (min_top))
    f.write("max_top=%s\r\n" % (max_top))
    f.close()

def escribir_config_generator(name_device, ip, username, password, feq_generator,
                     signal_generator, step_generator, feq_step_generator,
                     limite_feq, atenuacion_generator):
    f = open("config_generator.txt", "w")
    f.write("name_device_generator=%s\r\n" % (name_device))
    f.write("ip_generator=%s\r\n" % (ip))
    f.write("username_generator=%s\r\n" % (username))
    f.write("password_generator=%s\r\n" % (password))
    f.write("feq_generator=%s\r\n" % (feq_generator))
    f.write("signal_generator=%s\r\n" % (signal_generator))
    f.write("step_generator=%s\r\n" % (step_generator))
    f.write("feq_step_generator=%s\r\n" % (feq_step_generator))
    f.write("limite_feq=%s\r\n" % (limite_feq))
    f.write("atenuacion_generator=%s\r\n" % (atenuacion_generator))
    f.close()

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

        if function_changed is not None:
            spin.sigValueChanged.connect(function_changed)

def crear_log(filename_log, ex):
    """
    instant_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f = open(filename_log, "a")
    f.write("%s: %s \r\n\r\n" % (instant_time, str(ex)))
    f.close()
    """

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
