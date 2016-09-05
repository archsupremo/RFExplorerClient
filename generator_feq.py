from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *
from timer import Timer
from Tkinter import *

import pyqtgraph as pg
import time
import paramiko
import utiles

class GeneratorFeq(QtGui.QMainWindow):

    root = Tk()

    def __init__(self, ip_generator, username_generator, password_generator, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ip_generator = ip_generator
        self.username_generator = username_generator
        self.password_generator = password_generator

        self.feqs_numbers = []
        self.texts_color = []
        self.name_device = "/dev/ttyUSB0"
        self.contador = IntVar()
        self.contador.set(5)
        #print self.contador.get()
        self.rows = 0

        self.resize(800,600)
        self.setWindowTitle('Configuracion')

        self.area = DockArea()
        self.setCentralWidget(self.area)

        self.config = Dock("Conf", size=(400,600))
        self.feqs = Dock("Frecuencias", size=(400,600))
        self.area.addDock(self.config, 'left')
        self.area.addDock(self.feqs, 'left')

        label_feq = QtGui.QLabel('Frecuencia (HZ)')
        self.config.addWidget(label_feq)
        self.spin_feq = pg.SpinBox(value=0, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_feq)

        label_signal = QtGui.QLabel('Signal (0-3)')
        self.config.addWidget(label_signal)
        self.spin_signal = pg.SpinBox(value=0, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_signal)

        label_time = QtGui.QLabel('Tiempo (s)')
        self.config.addWidget(label_time)
        self.spin_time = pg.SpinBox(value=1, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_time)

        self.atenuacion_yn = QtGui.QCheckBox(self)
        self.atenuacion_yn.setText("Desea atenuacion? (Y/N)")
        self.config.addWidget(self.atenuacion_yn)

        self.a_feq = QtGui.QPushButton('Anadir frecuencia')
        self.a_feq.clicked.connect(self.anadir_frecuencia)
        self.config.addWidget(self.a_feq)

        self.iniciar_emision = QtGui.QPushButton('Iniciar Emision')
        self.iniciar_emision.clicked.connect(self.iniciar_emision_feqs)
        self.config.addWidget(self.iniciar_emision)

        self.parar_emision = QtGui.QPushButton('Parar Emision')
        self.parar_emision.clicked.connect(self.parar_emision_feqs)
        self.config.addWidget(self.parar_emision)

    def anadir_frecuencia(self):
        self.feqs_numbers += [[int(self.spin_feq.value()), self.definir_atenuacion(), int(self.spin_signal.value())]]

        text_color = QtGui.QLineEdit()
        text_color.setEnabled(False)
        self.feqs.addWidget(text_color, self.rows, 1)
        self.texts_color += [text_color]

        text_feq = QtGui.QLineEdit("Feq: " + str(int(self.spin_feq.value())))
        text_feq.setEnabled(False)
        self.feqs.addWidget(text_feq, self.rows, 2)

        text_atenuacion = QtGui.QLineEdit("Atn: " + str(self.definir_atenuacion()))
        text_atenuacion.setEnabled(False)
        self.feqs.addWidget(text_atenuacion, self.rows, 3)

        text_signal = QtGui.QLineEdit("dBm: " + str(int(self.spin_signal.value())))
        text_signal.setEnabled(False)
        self.feqs.addWidget(text_signal, self.rows, 4)

        self.rows += 1

    def generate(self, client_ssh):
        if self.contador > len(self.feqs_numbers)-1:
            self.contador = 0

        frecuencia = self.feqs_numbers[self.contador][0]
        atenuacion = self.feqs_numbers[self.contador][1]
        signal = self.feqs_numbers[self.contador][2]
        cadena_command = "Desktop/RFExplorer_Command/RFExplorerCommand %s " % (self.name_device)
        cadena_command += '"C3-F:%d,%d,%d"' % (frecuencia, atenuacion, signal)

        #for text_color in self.texts_color:
            #text_color.setStyleSheet("background-color: red;")
        #self.texts_color[self.contador].setStyleSheet("background-color: green;")
        self.contador += 1

        print cadena_command
        client_ssh.exec_command(cadena_command)

    def iniciar_emision_feqs(self):
        self.cambiar_enabled(False)
        self.timer = Timer(self.ip_generator,
                           self.username_generator,
                           self.password_generator,
                           self.generate,
                           self.spin_time.value() * 1000)
        self.timer.start()

    def parar_emision_feqs(self):
        self.cambiar_enabled(True)
        self.timer.parar_timer()

    def definir_atenuacion(self):
        if self.atenuacion_yn.isChecked():
            return 1
        return 0

    def cambiar_enabled(self, cond):
        self.a_feq.setEnabled(cond)
        self.spin_feq.setEnabled(cond)
        self.spin_signal.setEnabled(cond)
        self.spin_time.setEnabled(cond)
        self.atenuacion_yn.setEnabled(cond)

    def cambiar_ip(self, ip):
        self.ip = ip

    def cambiar_username(self, username):
        self.username = username

    def cambiar_password(self, password):
        self.password = password
