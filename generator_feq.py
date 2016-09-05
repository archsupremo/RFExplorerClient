from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *

import threading
import pyqtgraph as pg
import time
import paramiko
import utiles

class GeneratorFeq(QtGui.QMainWindow):
    def __init__(self, ip, username, password, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.generate)

        self.ip = ip
        self.username = username
        self.password = password

        self.client_ssh = paramiko.SSHClient()
        self.client_ssh.load_system_host_keys()
        self.client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.feqs_numbers = []
        self.texts_color = []
        self.name_device = "/dev/ttyUSB0"
        self.contador = 0
        self.rows = 0

        self.resize(800,600)
        self.setWindowTitle('Configuracion')

        self.area = DockArea()
        self.setCentralWidget(self.area)

        self.config = Dock("Conf", size=(400,600))
        self.feqs = Dock("Frecuencias", size=(400,600))
        self.area.addDock(self.config, 'left')
        self.area.addDock(self.feqs, 'left')

        self.crear_spin_boxes()
        self.crear_checkbox()
        self.crear_botones()

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

    def generate(self):
        if self.contador > len(self.feqs_numbers)-1:
            self.contador = 0

        frecuencia = self.feqs_numbers[self.contador][0]
        atenuacion = self.feqs_numbers[self.contador][1]
        signal = self.feqs_numbers[self.contador][2]
        cadena_command = "Desktop/RFExplorer_Command/RFExplorerCommand %s " % (self.name_device)
        cadena_command += '"C3-F:%d,%d,%d"' % (frecuencia, atenuacion, signal)

        for text_color in self.texts_color:
            text_color.setStyleSheet("background-color: red;")
        self.texts_color[self.contador].setStyleSheet("background-color: green;")
        self.contador += 1

        print cadena_command
        self.client_ssh.exec_command(cadena_command)

    def iniciar_emision_feqs(self):
        self.cambiar_enabled(False)
        self.client_ssh.connect(self.ip, username=self.username, password=self.password)
        self.timer.start(self.spin_time.value()*1000)

    def parar_emision_feqs(self):
        self.cambiar_enabled(True)
        self.timer.stop()
        self.client_ssh.close()

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

    def crear_spin_boxes(self):
        self.config.addWidget(QtGui.QLabel('Frecuencia (HZ)'))
        self.spin_feq = pg.SpinBox(value=0, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_feq)

        self.config.addWidget(QtGui.QLabel('Signal (0-3)'))
        self.spin_signal = pg.SpinBox(value=0, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_signal)

        self.config.addWidget(QtGui.QLabel('Tiempo (s)'))
        self.spin_time = pg.SpinBox(value=1, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_time)

    def crear_checkbox(self):
        self.atenuacion_yn = QtGui.QCheckBox(self)
        self.atenuacion_yn.setText("Desea atenuacion? (Y/N)")
        self.config.addWidget(self.atenuacion_yn)

    def crear_botones(self):
        self.a_feq = QtGui.QPushButton('Anadir frecuencia')
        self.a_feq.clicked.connect(self.anadir_frecuencia)
        self.config.addWidget(self.a_feq)

        self.iniciar_emision = QtGui.QPushButton('Iniciar Emision')
        self.iniciar_emision.clicked.connect(self.iniciar_emision_feqs)
        self.config.addWidget(self.iniciar_emision)

        self.parar_emision = QtGui.QPushButton('Parar Emision')
        self.parar_emision.clicked.connect(self.parar_emision_feqs)
        self.config.addWidget(self.parar_emision)

    def cambiar_ip(self, ip):
        self.ip = ip

    def cambiar_username(self, username):
        self.username = username

    def cambiar_password(self, password):
        self.password = password
