#!/usr/bin/python3
# File name   : motor.py
# Description : Control Motors 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import os
import sys

def search(path,name):
    for root, dirs, files in os.walk(path):
        if name in dirs or name in files:
            flag = 1
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1

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

path_get = str(search('//home/pi/','server.py'))
path_get=path_get[:-15]

if path_get != -1:
	while 1:
		command_select = input('Do you want to autostart the sound version or the Test version(without OpenCV)?\nInput "1" to select sound version.\nInput "2" to select Test version(without OpenCV).')
		if command_select == '1' or command_select == '2':
			break
		else:
			continue
else:
	print('Cannot find the programe for this robot, you need to setup the programe first.')


if command_select == '1':
	try:
		try:
			os.system('sudo rm -rf //home/pi/.config/autostart')
		except:
			pass
		os.system('sudo mkdir //home/pi/.config/autostart')
		os.system('sudo touch //home/pi/.config/autostart/car.desktop')
		with open("//home/pi/.config/autostart/car.desktop",'w') as file_to_write:
			file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 %sserver.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true"%path_get)
		print('The sound version will start when boot')
	except:
		pass
elif command_select == '2':
	try:
		try:
			os.system('sudo rm -rf //home/pi/.config/autostart')
		except:
			pass
		os.system('sudo mkdir //home/pi/.config/autostart')
		os.system('sudo touch //home/pi/.config/autostart/car.desktop')
		with open("//home/pi/.config/autostart/car.desktop",'w') as file_to_write:
			file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 %sserverTest.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true"%path_get)
		print('The Test version(without OpenCV) will start when boot')
	except:
		pass

#path_get=str(path_get)
#print(path_get[:-15])