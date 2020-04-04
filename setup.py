#!/usr/bin/python3
# File name   : setup.py
# Author      : Adeept
# Date        : 2020/3/14

import os
import time

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

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
    if os.system() == 0:
        break



# for x in range(1,4):
# 	if os.system("sudo apt-get -y upgrade") == 0:
# 		break

commands = [
    "sudo apt-get update",
    "sudo apt-get purge -y wolfram-engine",
    "sudo apt-get purge -y libreoffice*",
    "sudo apt-get -y clean",
    "sudo apt-get -y autoremove",
    "sudo pip3 install -U pip",
    "sudo apt-get install -y python-dev python-pip libfreetype6-dev libjpeg-dev build-essential",
    "sudo apt-get install -y i2c-tools",
    "sudo apt-get install -y python3-smbus",
    "sudo apt-get install -y libjasper-dev",
    "sudo apt-get install -y libatlas-base-dev"
]

for command in commands:
    if os.system(command) != 0:
        print("Error running installation step")


try:
    replace_num("/boot/config.txt", '#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
except:
    print('Error updating boot config to enable i2c. Please try again.')

commands = [
    "sudo apt-get -y install libqtgui4 libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqt4-test",
    "sudo pip3 install -r server/requirements.txt",
    "sudo git clone https://github.com/oblique/create_ap",
    "cd " + thisPath + "/create_ap && sudo make install",
    "cd //home/pi/create_ap && sudo make install",
    "sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq"
]

for command in commands:
    if os.system(command) != 0:
        print("Error running installation step")


try:
    os.system('sudo touch //home/pi/startup.sh')
    with open("//home/pi/startup.sh",'w') as file_to_write:
        #file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/webServer.py")
        file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/server.py")
except:
    pass

os.system('sudo chmod 777 //home/pi/startup.sh')

replace_num('/etc/rc.local','fi','fi\n//home/pi/startup.sh start')

try: #fix conflict with onboard Raspberry Pi audio
    os.system('sudo touch /etc/modprobe.d/snd-blacklist.conf')
    with open("/etc/modprobe.d/snd-blacklist.conf",'w') as file_to_write:
        file_to_write.write("blacklist snd_bcm2835")
except:
    pass

print('The program in Raspberry Pi has been installed, disconnected and restarted. \nYou can now power off the Raspberry Pi to install the camera and driver board (Robot HAT). \nAfter turning on again, the Raspberry Pi will automatically run the program to set the servos port signal to turn the servos to the middle position, which is convenient for mechanical assembly.')
print('restarting...')
os.system("sudo reboot")
