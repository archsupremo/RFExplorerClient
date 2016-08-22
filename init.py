import subprocess

p1 = subprocess.Popen(["./rfexplorer", "/dev/ttyUSB0", "0400000", "0500000", "050", "120"], stdout=subprocess.PIPE)

print(p1.communicate()[0])
