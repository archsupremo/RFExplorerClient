#!/usr/bin/python

#import numpy as np
#import serial
#import paramiko

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *
from pyqtgraph.Point import Point
from array import array

import subprocess
import time
import math
import pyqtgraph as pg
import sys
import utiles

from timer import Timer
from generator import Generator
from generator_feq import GeneratorFeq

# ip_analyzer = "5.40.205.100"
ip_analyzer = "172.36.0.204"
username_analyzer = "pi"
password_analyzer = "pi"
name_device_analyzer = "/dev/ttyUSB1"
#-----------------------------
min_feq = "0400000"
max_feq = "0500000"
min_top = "050"
max_top = "120"

#-------------------------------------------------------------------------------

# ip_generator= "5.40.205.100"
ip_generator = "172.36.0.204"
username_generator = "pi"
password_generator = "pi"
name_device_generator = "/dev/ttyUSB0"
#-----------------------------
feq_generator = "0450000"
signal_generator = 0
step_generator = 1
feq_step_generator = 100
limite_feq = False
atenuacion_generator = False

#-------------------------------------------------------------------------------

array_config_analyzer = utiles.leer_config("config_analyzer.txt")
array_config_generator = utiles.leer_config("config_generator.txt")
utiles.extract(locals(), array_config_analyzer)
utiles.extract(locals(), array_config_generator)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Ventana Principal.
app = QtGui.QApplication([])
w = QtGui.QMainWindow()
area = DockArea()
w.setCentralWidget(area)

# Se crean las areas (Docks)
grafica = Dock("Grafica RFExplorer", size=(1250, 850))
config_analyzer = Dock("Configuracion Analizer", size=(300, 850), closable=True)
config_generator = Dock("Configuracion Generator", size=(200, 850), closable=True)
area.addDock(grafica, 'left')
area.addDock(config_analyzer, 'right')
area.addDock(config_generator, 'right')

# Se crea la grafica, se le da un nombre y se crea las labels abajo e izquierda y derecha.
grafica_plot = pg.PlotWidget(title="RFExplorer")
grafica_plot.setLabel('left', 'Signal (dBm)')
grafica_plot.setLabel('bottom', 'Frecuencia (mHZ)')
grafica_plot.setLabel('right', 'Signal (dBm)')

# Se establecen maximos y minimos para la grafica, tanto en rango se medicion como para mostrar.
utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

# Elemento de la clase Plot, que es la curva de la grafica.
curva = pg.PlotCurveItem()
grafica_plot.addItem(curva)

# Se anade la grafica al panel y se muestra.
grafica.addWidget(grafica_plot)

# cross hair.
vLine = pg.InfiniteLine(angle=90, movable=False)
grafica_plot.addItem(vLine, ignoreBounds=True)

vb = grafica_plot.plotItem.vb
def mouseMoved(evt):
    global grafica_plot, curva, vb, min_feq, max_feq, vLine
    utiles.mouseMoved(evt, grafica_plot, curva, vb, min_feq, max_feq, vLine)
proxy = pg.SignalProxy(grafica_plot.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

#-------------------------------------------------------------------------------
# Pantalla de configuracion.
#-----------------------------
# Analyzer.
#-----------------------------
def device_changed_analyzer():
    global name_device_analyzer
    name_device_analyzer = str(texts_analyzer[0][1].text())

def ip_changed_analyzer():
    global ip_analyzer, t
    validacion = utiles.validacion(str(texts_analyzer[1][1].text()),
                                   "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                                   "La ip no puede ser correcta.")

    if validacion:
        ip_analyzer = str(texts_analyzer[1][1].text())
        t.cambiar_ip(ip_analyzer)

    texts_analyzer[1][1].setText(ip_analyzer)

def user_changed_analyzer():
    global username_analyzer, t
    username_analyzer = str(texts_analyzer[2][1].text())
    t.cambiar_username(username_analyzer)

def pass_changed_analyzer():
    global password_analyzer, t
    password_analyzer = str(texts_analyzer[3][1].text())
    t.cambiar_password(password_analyzer)

def feq_minima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top

    validacion = utiles.validacion(str(int(sb.value())),
                                   "^[1-9]+|[0-9]{2,}$",
                                   "La frecuencia minima debe ser mayor que cero.")
    if validacion:
        min_feq = int(sb.value())
        utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)
    sb.setValue(min_feq)

def feq_maxima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top

    validacion = utiles.validacion(str(int(sb.value())),
                                   "^[1-9]+|[0-9]{2,}$",
                                   "La frecuencia maxima debe ser mayor que cero.")
    if validacion:
        max_feq = int(sb.value())
        utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)
    sb.setValue(max_feq)

def signal_minima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top
    max_top = str(-sb.value())
    utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

def signal_maxima_changed(sb):
    global grafica_plot, min_feq, max_feq, min_top, max_top
    min_top = str(-sb.value())
    utiles.limites_grafica(grafica_plot, min_feq, max_feq, min_top, max_top)

#-----------------------------
# Generator.
#-----------------------------
def device_changed_generator():
    global name_device_generator, gq
    name_device_generator = str(texts_generator[0][1].text())
    gq.cambiar_name_device(name_device_generator)

def ip_changed_generator():
    global ip_generator, g, gq
    validacion = utiles.validacion(str(texts_generator[1][1].text()),
                                   "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                                   "La ip no puede ser correcta.")

    if validacion:
        ip_generator = str(texts_generator[1][1].text())
        g.cambiar_ip(ip_generator)
        gq.cambiar_ip(ip_generator)

    texts_generator[1][1].setText(ip_generator)

def user_changed_generator():
    global username_generator, g, gq
    username_generator = str(texts_generator[2][1].text())
    g.cambiar_username(username_generator)
    gq.cambiar_username(username_generator)

def pass_changed_generator():
    global password_generator, g, gq
    password_generator = str(texts_generator[3][1].text())
    g.cambiar_password(password_generator)
    gq.cambiar_password(password_generator)

def atenuacion_change(valor_checkbox):
    global atenuacion_generator
    atenuacion_generator = bool(valor_checkbox)

def have_limit_frecuencia(valor_checkbox):
    global limite_feq, spin_step_generator, spin_feq_step_generator

    limite_feq = False if (valor_checkbox == 0) else True
    spin_step_generator.setEnabled(limite_feq)
    spin_feq_step_generator.setEnabled(limite_feq)

def feq_generator_changed(sb):
    global feq_generator

    validacion = utiles.validacion(str(int(sb.value())),
                                   "^[1-9]+|[0-9]{2,}$",
                                   "La frecuencia debe ser mayor que cero.")

    if validacion: feq_generator = int(sb.value())
    sb.setValue(int(feq_generator))

def step_generator_changed(sb):
    global step_generator

    validacion = utiles.validacion(str(int(sb.value())),
                                   "^[1-9]+|[0-9]{2,}$",
                                   "El valor del step debe ser mayor que uno y numero entero.")

    if validacion: step_generator = int(sb.value())
    sb.setValue(int(step_generator))

def feq_step_generator_changed(sb):
    global feq_step_generator

    validacion = utiles.validacion(str(int(sb.value())),
                                   "^[1-9]+|[0-9]{2,}$",
                                   "El step de la frecuencia debe ser mayor que cero.")

    if validacion: feq_step_generator = int(sb.value())
    sb.setValue(int(feq_step_generator))

def signal_generator_changed(sb):
    global signal_generator

    validacion = utiles.validacion(str(int(sb.value())),
                                       "^[0-3]$",
                                       "El valor que va a tener la signal debe ser entre 0 y 3.")
    signal_generator = int(sb.value()) if validacion else sb.setValue(int(signal_generator))

#-------------------------------------------------------------------------------
# Creacion de los botones de configuracion en el Dock config.
text_name_device_analyzer = QtGui.QLineEdit(name_device_analyzer)
text_name_device_analyzer.setEnabled(False)
texts_analyzer = [
    ("Device:", text_name_device_analyzer, device_changed_analyzer, 0),
    ("IP SSH:", QtGui.QLineEdit(ip_analyzer), ip_changed_analyzer, 0),
    ("USER SSH:", QtGui.QLineEdit(username_analyzer), user_changed_analyzer, 0),
    ("PASS SSH:", QtGui.QLineEdit(password_analyzer), pass_changed_analyzer, 2)
]
text_name_device_generator = QtGui.QLineEdit(name_device_generator)
text_name_device_generator.setEnabled(False)
texts_generator = [
    ("Device:", text_name_device_generator, device_changed_generator, 0),
    ("IP SSH:", QtGui.QLineEdit(ip_generator), ip_changed_generator, 0),
    ("USER SSH:", QtGui.QLineEdit(username_generator), user_changed_generator, 0),
    ("PASS SSH:", QtGui.QLineEdit(password_generator), pass_changed_generator, 2)
]
spins_analyzer = [
    ("Frecuencia Minima (HZ)", pg.SpinBox(value=float(min_feq), dec=True, minStep=1, step=1), feq_minima_changed),
    ("Frecuencia Maxima (HZ)", pg.SpinBox(value=float(max_feq), dec=True, minStep=1, step=1), feq_maxima_changed),
    ("Signal Minima (dBm)", pg.SpinBox(value=-float(max_top), dec=True, minStep=1, step=1), signal_minima_changed),
    ("Signal Maxima (dBm)", pg.SpinBox(value=-float(min_top), dec=True, minStep=1, step=1), signal_maxima_changed)
]

spin_step_generator = pg.SpinBox(value=step_generator, dec=True, minStep=1, step=1)
spin_feq_step_generator = pg.SpinBox(value=feq_step_generator, dec=True, minStep=1, step=1)
spin_step_generator.setEnabled(limite_feq)
spin_feq_step_generator.setEnabled(limite_feq)
spins_generator = [
    ("Frecuencia Inicial (HZ):", pg.SpinBox(value=float(feq_generator), dec=True, minStep=1, step=1), feq_generator_changed),
    ("Valor Step (>1):", spin_step_generator, step_generator_changed),
    ("Freq Step KHZ:", spin_feq_step_generator, feq_step_generator_changed),
    ("Signal [0-3]:", pg.SpinBox(value=signal_generator, dec=True, minStep=1, step=1), signal_generator_changed)
]

# Creacion de los checkbox's para cambiar los dispositivos sobre los que se consulta informacion
change_device_analyzer = QtGui.QCheckBox("Cambiar dispositivo de Analyzer", w)
config_analyzer.addWidget(change_device_analyzer)
change_device_analyzer.stateChanged.connect(lambda value: text_name_device_analyzer.setEnabled(bool(value)))

change_device_generator = QtGui.QCheckBox("Cambiar dispositivo de Generator", w)
config_generator.addWidget(change_device_generator)
change_device_generator.stateChanged.connect(lambda value: text_name_device_generator.setEnabled(bool(value)))

# Creacion de los text box y de los spins de numeros.
utiles.texts(config_analyzer, texts_analyzer)
utiles.texts(config_generator, texts_generator)
utiles.spins(config_analyzer, spins_analyzer)
utiles.spins(config_generator, spins_generator)

# Checkbox's sobre atenuacion y limite de frecuencia en caso de establecerse un limite en la frecuencia.
limit_frecuencia = QtGui.QCheckBox("Rango de Frecuencia (Y/N)", w)
limit_frecuencia.setChecked(limite_feq)
config_generator.addWidget(limit_frecuencia)
limit_frecuencia.stateChanged.connect(have_limit_frecuencia)

atenuacion_yn = QtGui.QCheckBox("Desea atenuacion? (Y/N)", w)
atenuacion_yn.setChecked(atenuacion_generator)
config_generator.addWidget(atenuacion_yn)
atenuacion_yn.stateChanged.connect(atenuacion_change)

# Creacion de los botones de empezar y parar lectura.
start_analyzer = QtGui.QPushButton('Empezar Lectura')
stop_analyzer = QtGui.QPushButton('Parar Lectura')
guardar_config_analyzer = QtGui.QPushButton('Guardar Configuracion')
guardar_config_analyzer.clicked.connect(
    lambda : utiles.escribir_config_analyzer(name_device_analyzer,
                                    ip_analyzer,
                                    username_analyzer,
                                    password_analyzer,
                                    min_feq,
                                    max_feq,
                                    min_top,
                                    max_top)
)
config_analyzer.addWidget(start_analyzer)
config_analyzer.addWidget(stop_analyzer)
config_analyzer.addWidget(guardar_config_analyzer)

#-----------------------------
start_generator = QtGui.QPushButton('Empezar Emision')
stop_generator = QtGui.QPushButton('Parar Emision')
crear_lista_frecuencias = QtGui.QPushButton('Crear Lista de Frecuencias')
guardar_config_generator = QtGui.QPushButton('Guardar Configuracion')
guardar_config_generator.clicked.connect(
    lambda : utiles.escribir_config_generator(name_device_generator,
                                     ip_generator,
                                     username_generator,
                                     password_generator,
                                     feq_generator,
                                     signal_generator,
                                     step_generator,
                                     feq_step_generator,
                                     limite_feq,
                                     atenuacion_generator)
)
config_generator.addWidget(start_generator)
config_generator.addWidget(stop_generator)
config_generator.addWidget(crear_lista_frecuencias)
config_generator.addWidget(guardar_config_generator)

#-------------------------------------------------------------------------------
# Funcion que actualiza los datos cada X tiempo.
def update(client_ssh):
    global curva, grafica_plot, name_device_analyzer, min_feq, max_feq, min_top, max_top
    x = []
    y = []

    stdin, stdout, stderr = client_ssh.exec_command("Desktop/RFExplorerClient/rfexplorer %s %s %s %s %s" % (name_device_analyzer, min_feq, max_feq, min_top, max_top))
    if stdout:
        for line in stdout:
            res = line.strip('\r\n')
            if res != '':
                frequency_signal = res.split("\t")
                x += [int(float(frequency_signal[0]))/1000]
                y += [float(frequency_signal[1])]
                if x and y:
                    curva.setData(x=x, y=y, clear=True)
    elif stderr:
        print stderr

# Funcion para mandar los comandos a signal generator.
def function_generator(client_ssh):
    global name_device_generator, feq_generator, step_generator, feq_step_generator, signal_generator, limite_feq, atenuacion_generator

    atenuacion_generator_number = 1 if (atenuacion_generator) else 0
    cadena_command = "Desktop/RFExplorer_Command/RFExplorerCommand %s " % (name_device_generator)

    if limite_feq:
        cadena_command += '"C3-F:%d,%d,%d,%d,%d,%0.1f"' % (int(feq_generator), atenuacion_generator_number, signal_generator, step_generator, feq_step_generator, 0.1)
    else:
        cadena_command += '"C3-F:%d,%d,%d"' % (int(feq_generator), atenuacion_generator_number, signal_generator)

    print cadena_command
    client_ssh.exec_command(cadena_command)

# Funcion para parar la emision del signal generator
def function_parar(client_ssh):
    global name_device_generator

    cadena_command = "Desktop/RFExplorer_Command/RFExplorerCommand %s %s" % (name_device_generator, 'CP0')

    print cadena_command
    client_ssh.exec_command(cadena_command)

#-------------------------------------------------------------------------------
# Timer donde se indica que funcion se va a repetir cada X tiempo para actualizar la grafica.
t = Timer(ip_analyzer, username_analyzer, password_analyzer, update, 50)
start_analyzer.clicked.connect(t.iniciar_timer)
stop_analyzer.clicked.connect(t.parar_timer)

# Generator donde se realiza la generacion de senal.
g = Generator(ip_generator, username_generator, password_generator, function_generator, function_parar)
start_generator.clicked.connect(g.iniciar_emision)
stop_generator.clicked.connect(g.parar_emision)

# Generator donde se realiza la generacion de distintas senal en varias frecuencias.
gq = GeneratorFeq(ip_generator, username_generator, password_generator, name_device_generator)
crear_lista_frecuencias.clicked.connect(gq.show)

w.showMaximized()
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
