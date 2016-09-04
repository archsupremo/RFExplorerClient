from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import *

import pyqtgraph as pg
import time
import paramiko
import utiles

class GeneratorFeq(QtGui.QMainWindow):
    def __init__(self, ip_generator, username_generator, password_generator, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.feqs_numbers = []

        self.resize(400,600)
        self.setWindowTitle('Configuracion')

        self.area = DockArea()
        self.setCentralWidget(self.area)

        self.config = Dock("Conf", size=(200,600))
        self.feqs = Dock("Frecuencias", size=(200,600))
        self.area.addDock(self.config, 'left')
        self.area.addDock(self.feqs, 'left')

        label_feq = QtGui.QLabel('Frecuencia (mHZ)')
        self.config.addWidget(label_feq)
        self.spin_feq = pg.SpinBox(value=0, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_feq)

        label_signal = QtGui.QLabel('Signal (0-3)')
        self.config.addWidget(label_signal)
        self.spin_signal = pg.SpinBox(value=0, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_signal)

        label_time = QtGui.QLabel('Tiempo (ms)')
        self.config.addWidget(label_time)
        self.spin_time = pg.SpinBox(value=500, dec=True, minStep=1, step=1)
        self.config.addWidget(self.spin_time)

        self.atenuacion_yn = QtGui.QCheckBox(self)
        self.atenuacion_yn.setText("Desea atenuacion? (Y/N)")
        self.config.addWidget(self.atenuacion_yn)
        #self.atenuacion_yn.stateChanged.connect(atenuacion_change)

        self.a_feq = QtGui.QPushButton('Anadir frecuencia')
        self.a_feq.clicked.connect(self.anadir_frecuencia)
        self.config.addWidget(self.a_feq)

        self.emision = QtGui.QPushButton('Iniciar Emision')
        self.emision.clicked.connect(self.emision_feqs)
        self.config.addWidget(self.emision)

    def anadir_frecuencia(self):
        self.feqs_numbers += [self.spin_feq.value()]
        text = QtGui.QLineEdit('PPPQQQ')
        text.setEnabled(False)
        self.feqs.addWidget(text)

    def emision_feqs(self):
        self.a_feq.setEnabled(False)
        self.spin_feq.setEnabled(False)
        self.spin_signal.setEnabled(False)
        self.spin_time.setEnabled(False)
        self.atenuacion_yn.setEnabled(False)

        print self.feqs_numbers

    def cambiar_ip(self, ip):
        self.ip = ip

    def cambiar_username(self, username):
        self.username = username

    def cambiar_password(self, password):
        self.password = password
