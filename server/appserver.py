#!/usr/bin/env/python
# File name   : appserver.py
# Author      : William
# Date        : 2019/10/24

import socket
import threading
import time

from rpi_ws281x import *
import LED
import move
import servo

LED  = LED.LED()
LED.colorWipe(Color(80,255,0))

step_set = 1
speed_set = 100
rad = 0.6

direction_command = 'no'
turn_command = 'no'
pos_input = 1
catch_input = 1
cir_input = 6

def app_ctrl():
    app_HOST = ''
    app_PORT = 10123
    app_BUFSIZ = 1024
    app_ADDR = (app_HOST, app_PORT)

    AppSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    AppSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    AppSerSock.bind(app_ADDR)

    def setup():
        move.setup()

    def appCommand(data_input):
        global direction_command, turn_command, pos_input, catch_input, cir_input
        if data_input == 'forwardStart\n':
            direction_command = 'forward'
            move.move(speed_set, direction_command, turn_command, rad)

        elif data_input == 'backwardStart\n':
            direction_command = 'backward'
            move.move(speed_set, direction_command, turn_command, rad)

        elif data_input == 'leftStart\n':
            turn_command = 'left'
            move.move(speed_set, direction_command, turn_command, rad)

        elif data_input == 'rightStart\n':
            turn_command = 'right'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'forwardStop' in data_input:
            direction_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'backwardStop' in data_input:
            direction_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'leftStop' in data_input:
            turn_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'rightStop' in data_input:
            turn_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)


        if data_input == 'lookLeftStart\n':
            if cir_input < 12:
                cir_input+=1
            servo.cir_pos(cir_input)

        elif data_input == 'lookRightStart\n': 
            if cir_input > 1:
                cir_input-=1
            servo.cir_pos(cir_input)

        elif data_input == 'downStart\n':
            servo.camera_ang('lookdown',10)

        elif data_input == 'upStart\n':
            servo.camera_ang('lookup',10)

        elif 'lookLeftStop' in data_input:
            pass
        elif 'lookRightStop' in data_input:
            pass
        elif 'downStop' in data_input:
            pass
        elif 'upStop' in data_input:
            pass


        if data_input == 'aStart\n':
            if pos_input < 17:
                pos_input+=1
            servo.hand_pos(pos_input)

        elif data_input == 'bStart\n':
            if pos_input > 1:
                pos_input-=1
            servo.hand_pos(pos_input)

        elif data_input == 'cStart\n':
            if catch_input < 13:
                catch_input+=3
            servo.catch(catch_input)

        elif data_input == 'dStart\n':
            if catch_input > 1:
                catch_input-=3
            servo.catch(catch_input)

        elif 'aStop' in data_input:
            pass
        elif 'bStop' in data_input:
            pass
        elif 'cStop' in data_input:
            pass
        elif 'dStop' in data_input:
            pass

        print(data_input)

    def appconnect():
        global AppCliSock, AppAddr
        AppSerSock.listen(5)
        print('waiting for App connection...')
        AppCliSock, AppAddr = AppSerSock.accept()
        print('...App connected from :', AppAddr)

    appconnect()
    setup()
    app_threading=threading.Thread(target=appconnect)         #Define a thread for FPV and OpenCV
    app_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    app_threading.start()                                     #Thread starts

    while 1:
        data = ''
        data = str(AppCliSock.recv(app_BUFSIZ).decode())
        if not data:
            continue
        appCommand(data)
        pass

AppConntect_threading=threading.Thread(target=app_ctrl)         #Define a thread for FPV and OpenCV
AppConntect_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
AppConntect_threading.start()                                     #Thread starts

if __name__ == '__main__':
    i = 1
    while 1:
        i += 1
        print(i)
        time.sleep(30)
        pass