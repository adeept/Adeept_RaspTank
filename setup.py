#!/usr/bin/python3
# coding=utf-8
# File name   : setup.py
# Author      : Devin

import os
import time
import subprocess

username = os.popen("echo ${SUDO_USER:-$(who -m | awk '{ print $1 }')}").readline().strip() # pi
user_home = os.popen('getent passwd %s | cut -d: -f 6'%username).readline().strip()         # home
 
curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

print(thisPath)

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


def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result

def check_rpi_model():
    _, result = run_command("cat /proc/device-tree/model |awk '{print $3}'")
    result = result.strip()
    if result == '3':
        return int(3)
    elif result == '4':
        return int(4)
    else:
        return None

def check_raspbain_version():
    _, result = run_command("cat /etc/debian_version|awk -F. '{print $1}'")
    return int(result.strip())

def check_python_version():
    import sys
    major = int(sys.version_info.major)
    minor = int(sys.version_info.minor)
    micro = int(sys.version_info.micro)
    return major, minor, micro

def check_os_bit():
    '''
    # import platform
    # machine_type = platform.machine() 
    latest bullseye uses a 64-bit kernel
    This method is no longer applicable, the latest raspbian will uses 64-bit kernel 
    (kernel 6.1.x) by default, "uname -m" shows "aarch64", 
    but the system is still 32-bit.
    '''
    _ , os_bit = run_command("getconf LONG_BIT")
    return int(os_bit)

def check_systemctl_service(service_name):
    return subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True, text=True
        ).stdout.strip() == "active"


commands_apt = [
"sudo apt-get update",
"sudo apt-get install python3-gpiozero python3-pigpio",
"sudo apt-get install -y python3-pyqt5 python3-opengl",
"sudo apt-get install -y python3-picamera2",
"sudo apt-get install -y python3-opencv",
"sudo apt-get install -y opencv-data",
"sudo apt-get install -y python3-pyaudio"
]
mark_apt = 0
for x in range(3):
    for command in commands_apt:
        if os.system(command) != 0:
            print("Error running installation step apt")
            mark_apt = 1
    if mark_apt == 0:
        break

commands_pip_1 = [
"sudo pip3 install adafruit-circuitpython-motor",
"sudo pip3 install adafruit-circuitpython-pca9685",
"sudo pip3 install flask",
"sudo pip3 install flask_cors",
"sudo pip3 install numpy",
"sudo pip3 install pyzmq",
"sudo pip3 install imutils zmq pybase64 psutil",
"sudo pip3 install websockets==13.0",
"sudo pip3 install rpi_ws281x",
"sudo pip3 install adafruit-circuitpython-ads7830",
"sudo pip3 install adafruit-pca9685"
]
commands_pip_2 = [
"sudo pip3 install adafruit-circuitpython-motor --break-system-packages",
"sudo pip3 install adafruit-circuitpython-pca9685 --break-system-packages",
"sudo pip3 install flask --break-system-packages",
"sudo pip3 install flask_cors --break-system-packages",
"sudo pip3 install numpy --break-system-packages",
"sudo pip3 install pyzmq --break-system-packages",
"sudo pip3 install imutils zmq pybase64 psutil --break-system-packages",
"sudo pip3 install websockets==13.0 --break-system-packages",
"sudo pip3 install rpi_ws281x --break-system-packages",
"sudo pip3 install adafruit-circuitpython-ads7830 --break-system-packages",
"sudo pip3 install adafruit-pca9685 --break-system-packages"
]
mark_pip = 0
OS_version = check_raspbain_version()
if OS_version <= 11:
    for x in range(3):
        for command in commands_pip_1:
            if os.system(command) != 0:
                print("Error running installation step pip")
                mark_pip = 1
        if mark_pip == 0:
            break
else:
    for x in range(3):
        for command in commands_pip_2:
            if os.system(command) != 0:
                print("Error running installation step pip")
                mark_pip = 1
        if mark_pip == 0:
            break


wifi_service_name="wifi-hotspot-manager.service"
if not check_systemctl_service(wifi_service_name):
    # wifi and hotspot switch script
    os.system(f"sudo cp {thisPath}/wifi_hotspot_manager.sh /home/pi")
    os.system("sudo chmod +x /home/pi/wifi_hotspot_manager.sh")


    wifi_service_content="""[Unit]
Description=WiFi and Hotspot Manager Service
After=network.target NetworkManager.service
Wants=NetworkManager.service

[Service]
Type=oneshot
ExecStart=/home/pi/wifi_hotspot_manager.sh  
User=root
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""
    # system-level services must be placed in this directory
    wifi_service_file_path = "/etc/systemd/system/" + wifi_service_name 

    try:
        # Write to the service file (requires root privileges)
        with open(wifi_service_file_path, "w") as f:
            f.write(wifi_service_content)
        print(f"Service file created: {wifi_service_file_path}")

        # Set file permissions
        os.chmod(wifi_service_file_path, 0o644)

        # Reload systemd configuration, enable and start the service
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", wifi_service_name], check=True)

        print(f"Service {wifi_service_name} has been enabled and started")
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


robot_service_name="Adeept_Robot.service"
if not check_systemctl_service(robot_service_name):
    # auto start script
    try:
        os.system("sudo touch /"+ user_home +"/startup.sh")
        with open("/"+ user_home +"/startup.sh",'w') as file_to_write:
            #you can choose how to control the robot
            file_to_write.write("#!/bin/sh\nsleep 5\nsudo python3 " + thisPath + "/server/webServer.py")
    except:
        pass
    os.system("sudo chmod 777 /"+ user_home +"/startup.sh")

    #config systemctl service
    # Define the content of the systemd service file
    robot_service_content=f"""[Unit]
Description=Auto-start robot control script
After={wifi_service_name} 

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi
ExecStart=/home/pi/startup.sh  
Restart=no

[Install]
WantedBy=multi-user.target
"""

    # Path for the service file (system-level services must be placed in this directory)
    robot_service_file_path = "/etc/systemd/system/" + robot_service_name 

    try:
        # Write to the service file (requires root privileges)
        with open(robot_service_file_path, "w") as f:
            f.write(robot_service_content)
        print(f"Service file created: {robot_service_file_path}")

        # Set file permissions
        os.chmod(robot_service_file_path, 0o644)

        # Reload systemd configuration, enable and start the service
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", robot_service_name], check=True)

        print(f"Service {robot_service_name} has been enabled and started")
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


print('The program in Raspberry Pi has been installed, disconnected and restarted. \nYou can now power off the Raspberry Pi to install the camera and driver board (Robot HAT). \nAfter turning on again, the Raspberry Pi will automatically run the program to set the servos port signal to turn the servos to the middle position, which is convenient for mechanical assembly.')
print('restarting...')
os.system("sudo reboot")
