import time
import os
import socket
from getmac import get_mac_address


eth_mac_raw = get_mac_address()
eth_mac = eth_mac_raw.replace(":","")
print(eth_mac)


f = open("/home/pi/static/ID.js", "w")
f.write("var ID = 'rpi-" + eth_mac + "';")
f.close()

os.system("sudo hostnamectl set-hostname zp-client-" + eth_mac)

