#!/usr/bin/python3
# File name   : motor.py
# Description : Control Motors 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import os
import time

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

for x in range(1,4):
	if os.system("sudo apt-get update") == 0:
		break

os.system("sudo apt-get purge -y wolfram-engine")
os.system("sudo apt-get purge -y libreoffice*")
os.system("sudo apt-get -y clean")
os.system("sudo apt-get -y autoremove")

for x in range(1,4):
	if os.system("sudo apt-get -y upgrade") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y i2c-tools") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install adafruit-pca9685") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install rpi_ws281x") == 0:
		break

try:
	replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
except:
	print('try again')

for x in range(1,4):
	if os.system("sudo pip3 install -U pip") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install numpy") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install opencv-contrib-python") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libhdf5-dev") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libhdf5-serial-dev") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y build-essential pkg-config") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libgtk2.0-dev libatlas-base-dev gfortran") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libqtgui4 python3-pyqt5 libqt4-test") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install imutils zmq pybase64 psutil") == 0:   ####
		break

for x in range(1,4):
	if os.system("git clone https://github.com/oblique/create_ap") == 0:
		break

try:
	os.system("sudo cd //home/pi/adeept_rasptank/create_ap && sudo make install")
except:
	pass

for x in range(1,4):
	if os.system("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq") == 0:
		break

try:
	os.system('sudo mkdir //home/pi/.config/autostart')
	os.system('sudo touch //home/pi/.config/autostart/car.desktop')
	with open("//home/pi/.config/autostart/car.desktop",'w') as file_to_write:
		file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 //home/pi/adeept_rasptank/server/server.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true")
except:
	pass

os.system("sudo cp -f //home/pi/adeept_rasptank/server/config.txt //home/pi/config.txt")

print('restarting')

os.system("sudo reboot")
