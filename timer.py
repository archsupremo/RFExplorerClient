from PyQt4.QtCore import QThread
import pyqtgraph as pg
import time
import paramiko

class Timer(QThread):

    def __init__(self, function_update, time, ip, username, password):
        QThread.__init__(self)
        self.function_update = function_update
        self.time = time

        self.ip = ip
        self.username = username
        self.password = password

        self.client_ssh = paramiko.SSHClient()
        self.client_ssh.load_system_host_keys()
        self.client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client_ssh.connect(self.ip, username=self.username, password=self.password)

        self.parar = False

    def __del__(self):
        self.wait()

    def run(self):
        while not self.parar:
            self.function_update(self.client_ssh)
            time.sleep(self.time / 1000)

    def iniciar_lectura(self):
        self.parar = False
        self.client_ssh.connect(self.ip, username=self.username, password=self.password)
        self.start()

    def parar_lectura(self):
        self.parar = True
        self.client_ssh.close()

    def cambiar_refresco(self, time):
        self.time = time

    def cambiar_ip(self, ip):
        self.ip = ip

    def cambiar_username(self, username):
        self.username = username

    def cambiar_password(self, password):
        self.password = password
