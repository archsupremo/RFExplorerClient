from PyQt4.QtCore import QThread
import pyqtgraph as pg
import time

class Timer(QThread):

    def __init__(self, function_update, time):
        QThread.__init__(self)
        self.function_update = function_update
        self.time = time
        self.parar = False

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            if not self.parar:
                self.function_update()
                time.sleep(self.time / 1000)

    def iniciar_lectura(self):
        self.parar = False

    def parar_lectura(self):
        self.parar = True

    def cambiar_refresco(self, time):
        self.time = time
