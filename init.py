#!/usr/bin/python

import subprocess
import time

name_device = "/dev/ttyUSB0"
min_feq = "0400000"
max_feq = "0420000"
min_top = "050"
max_top = "120"

while True:
    subprocess.Popen(["clear"])
    print("--------------------------")
    print("Informacion del rfexplorer")
    print("--------------------------")
    p1 = subprocess.Popen(["./rfexplorer", name_device, min_feq, max_feq, min_top, max_top], stdout=subprocess.PIPE)
    print(p1.communicate()[0])

    time.sleep(1)
