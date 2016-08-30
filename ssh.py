import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect("5.40.205.100", username="pi", password="pi")
stdin, stdout, stderr = client.exec_command('Desktop/RFExplorerClient/rfexplorer /dev/ttyUSB0 0400000 0500000 050 120')

for line in stdout:
    print line.strip('\r\n')

client.close()

"""
import pxssh
import getpass

try:
    s = pxssh.pxssh()
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    s.login (hostname, username, password)

    s.sendline ('uptime')
    s.prompt()
    print s.before

    s.sendline ('uname -a')
    s.prompt()
    print s.before

    s.logout()
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)
"""
