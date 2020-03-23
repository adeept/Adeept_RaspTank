#!/usr/bin/env/python
# File name   : switch.py
# Production  : HAT
# Website     : www.gewbot.com
# Author      : William
# Date        : 2018/08/22

import RPi.GPIO as GPIO

def switchSetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

def switch(port, status):
    if port == 1:
        if status == 1:
            GPIO.output(5, GPIO.HIGH)
        elif status == 0:
            GPIO.output(5,GPIO.LOW)
        else:
            pass
    elif port == 2:
        if status == 1:
            GPIO.output(6, GPIO.HIGH)
        elif status == 0:
            GPIO.output(6,GPIO.LOW)
        else:
            pass
    elif port == 3:
        if status == 1:
            GPIO.output(13, GPIO.HIGH)
        elif status == 0:
            GPIO.output(13,GPIO.LOW)
        else:
            pass
    else:
        print('Wrong Command: Example--switch(3, 1)->to switch on port3')

def set_all_switch_off():
    switch(1,0)
    switch(2,0)
    switch(3,0)
