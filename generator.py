from PyQt4.QtCore import QThread
import pyqtgraph as pg
import time
import paramiko

class Generator(QThread):

    def __init__(self, ip, username, password, function_generator, function_parar):
        QThread.__init__(self)
        self.function_generator = function_generator
        self.function_parar = function_parar
        self.ip = ip
        self.username = username
        self.password = password

        self.client_ssh = paramiko.SSHClient()
        self.client_ssh.load_system_host_keys()
        self.client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __del__(self):
        self.wait()

    def run(self):
        self.client_ssh.connect(self.ip, username=self.username, password=self.password)
        self.function_generator(self.client_ssh)
        self.client_ssh.close()

    def iniciar_emision(self):
        self.start()

    def parar_emision(self):
        self.client_ssh.connect(self.ip, username=self.username, password=self.password)
        self.function_parar(self.client_ssh)
        self.client_ssh.close()

    def cambiar_ip(self, ip):
        self.ip = ip

    def cambiar_username(self, username):
        self.username = username

    def cambiar_password(self, password):
        self.password = password
