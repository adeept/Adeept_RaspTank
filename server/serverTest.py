#!/usr/bin/env/python
# File name   : server.py
# Production  : RaspTank
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/08/22

import socket
import time
import threading
import move
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
pwm.set_all_pwm(0,300)
from rpi_ws281x import *
import argparse
import os
import ultra
#import psutil
import servo
import LED
import findline

step_set = 1
speed_set = 100
rad = 0.6

direction_command = 'no'
turn_command = 'no'
#pwm = Adafruit_PCA9685.PCA9685()
#pwm.set_pwm_freq(50)
pos_input = 1
catch_input = 1
cir_input = 6

ultrasonicMode = 0
FindLineMode = 0
FindColorMode = 0


def findline_thread():       #Line tracking mode
    while 1:
        while FindLineMode:
            findline.run()
        time.sleep(0.2)

def get_cpu_tempfunc():
    """ Return CPU temperature """
    result = 0
    mypath = "/sys/class/thermal/thermal_zone0/temp"
    with open(mypath, 'r') as mytmpfile:
        for line in mytmpfile:
            result = line

    result = float(result)/1000
    result = round(result, 1)
    return str(result)


def get_gpu_tempfunc():
    """ Return GPU temperature as a character string"""
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return res.replace("temp=", "")


def get_cpu_use():
    """ Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return str(cpu_cent)


def get_ram_info():
    """ Return RAM usage using psutil """
    ram_cent = psutil.virtual_memory()[2]
    return str(ram_cent)


def get_swap_info():
    """ Return swap memory  usage using psutil """
    swap_cent = psutil.swap_memory()[3]
    return str(swap_cent)


def info_get():
    global cpu_t,cpu_u,gpu_t,ram_info
    while 1:
        cpu_t = get_cpu_tempfunc()
        cpu_u = get_cpu_use()
        ram_info = get_ram_info()
        time.sleep(3)


def info_send_client():
    SERVER_IP = addr[0]
    SERVER_PORT = 2256   #Define port serial 
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)
    Info_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
    Info_Socket.connect(SERVER_ADDR)
    print(SERVER_ADDR)
    while 1:
        try:
            Info_Socket.send((get_cpu_tempfunc()+' '+get_cpu_use()+' '+get_ram_info()).encode())
            time.sleep(1)
        except:
            pass


def ultra_send_client():
    ultra_IP = addr[0]
    ultra_PORT = 2257   #Define port serial 
    ultra_ADDR = (ultra_IP, ultra_PORT)
    ultra_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
    ultra_Socket.connect(ultra_ADDR)
    print(ultra_ADDR)
    while 1:
        while ultrasonicMode:
            try:
                ultra_Socket.send(str(round(ultra.checkdist(),2)).encode())
                time.sleep(0.5)
                continue
            except:
                pass
        time.sleep(0.5)


def  ap_thread():
    os.system("sudo create_ap wlan0 eth0 AdeeptCar 12345678")


def run():
    global direction_command, turn_command, pos_input, catch_input, cir_input, ultrasonicMode, FindLineMode, FindColorMode
    move.setup()
    findline.setup()

    info_threading=threading.Thread(target=info_send_client)    #Define a thread for FPV and OpenCV
    info_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    info_threading.start()                                     #Thread starts

    ultra_threading=threading.Thread(target=ultra_send_client)    #Define a thread for FPV and OpenCV
    ultra_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    ultra_threading.start()                                     #Thread starts

    findline_threading=threading.Thread(target=findline_thread)    #Define a thread for FPV and OpenCV
    findline_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    findline_threading.start()                                     #Thread starts
    #move.stand()

    ws_R = 0
    ws_G = 0
    ws_B = 0

    Y_pitch = 0
    Y_pitch_MAX = 200
    Y_pitch_MIN = -200

    while True: 
        data = ''
        data = str(tcpCliSock.recv(BUFSIZ).decode())
        if not data:
            continue
        elif 'forward' == data:
            direction_command = 'forward'
            move.move(speed_set, direction_command, turn_command, rad)
        elif 'backward' == data:
            direction_command = 'backward'
            move.move(speed_set, direction_command, turn_command, rad)
        elif 'DS' in data:
            direction_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'left' == data:
            turn_command = 'left'
            move.move(speed_set, direction_command, turn_command, rad)
        elif 'right' == data:
            turn_command = 'right'
            move.move(speed_set, direction_command, turn_command, rad)
        elif 'TS' in data:
            turn_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'out' == data:
            if pos_input < 17:
                pos_input+=1
            servo.hand_pos(pos_input)
        elif 'in' == data:
            if pos_input > 1:
                pos_input-=1
            servo.hand_pos(pos_input)

        elif 'headup' == data:
            servo.camera_ang('lookup',0)
        elif 'headdown' == data:
            servo.camera_ang('lookdown',0)
        elif 'headhome' == data:
            servo.camera_ang('home',0)
            servo.hand('in')
            servo.cir_pos(6)
            pos_input = 1
            catch_input = 1
            cir_input = 6
            servo.catch(catch_input)
            time.sleep(0.5)
            servo.clean_all()

        elif 'c_left' == data:
            if cir_input < 12:
                cir_input+=1
            servo.cir_pos(cir_input)
        elif 'c_right' == data:
            if cir_input > 1:
                cir_input-=1
            servo.cir_pos(cir_input)

        elif 'catch' == data:
            if catch_input < 13:
                catch_input+=1
            servo.catch(catch_input)
        elif 'loose' == data:
            if catch_input > 1:
                catch_input-=1
            servo.catch(catch_input)

        elif 'wsR' in data:
            try:
                set_R=data.split()
                ws_R = int(set_R[1])
                LED.colorWipe(Color(ws_R,ws_G,ws_B))
            except:
                pass
        elif 'wsG' in data:
            try:
                set_G=data.split()
                ws_G = int(set_G[1])
                LED.colorWipe(Color(ws_R,ws_G,ws_B))
            except:
                pass
        elif 'wsB' in data:
            try:
                set_B=data.split()
                ws_B = int(set_B[1])
                LED.colorWipe(Color(ws_R,ws_G,ws_B))
            except:
                pass

        elif 'FindColor' in data:
            FindColorMode = 0
            tcpCliSock.send(('FunEnd').encode())

        elif 'WatchDog' in data:
            tcpCliSock.send(('FunEnd').encode())

        elif 'steady' in data:
            ultrasonicMode = 1
            tcpCliSock.send(('steady').encode())

        elif 'FindLine' in data:
            FindLineMode = 1
            tcpCliSock.send(('FindLine').encode())

        elif 'funEnd' in data:
            ultrasonicMode = 0
            FindLineMode   = 0
            FindColorMode  = 0
            tcpCliSock.send(('FunEnd').encode())
            move.motorStop()

        else:
            pass


if __name__ == '__main__':

    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    try:
        LED  = LED.LED()
        LED.colorWipe(Color(255,16,0))
    except:
        print('Use "sudo pip3 install rpi_ws281x" to install WS_281x package')
        pass

    while  1:
        try:
            s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check=s.getsockname()[0]
            s.close()
            print(ipaddr_check)
        except:
            ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
            ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
            ap_threading.start()                                  #Thread starts

            LED.colorWipe(Color(0,16,50))
            time.sleep(1)
            LED.colorWipe(Color(0,16,100))
            time.sleep(1)
            LED.colorWipe(Color(0,16,150))
            time.sleep(1)
            LED.colorWipe(Color(0,16,200))
            time.sleep(1)
            LED.colorWipe(Color(0,16,255))
            time.sleep(1)
            LED.colorWipe(Color(35,255,35))

        try:
            tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            tcpSerSock.bind(ADDR)
            tcpSerSock.listen(5)                      #Start server,waiting for client
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('...connected from :', addr)
            break
        except:
            LED.colorWipe(Color(0,0,0))

        try:
            LED.colorWipe(Color(0,80,255))
        except:
            pass

    try:
        run()
    except:
        servo.clean_all()
        move.destroy()
        LED.colorWipe(Color(0,0,0))
