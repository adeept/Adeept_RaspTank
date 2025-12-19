#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/02/23
from gpiozero import DistanceSensor
from time import sleep
Tr = 23
Ec = 24


sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2) # Maximum detection distance 2m.

def checkdist():
    return (sensor.distance) *100 # Unit: cm

if __name__ == '__main__':
    while True:
        distance = checkdist()*100
        print("%.2f cm" %distance)
        sleep(0.05)
