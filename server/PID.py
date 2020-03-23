#! /usr/bin/python
# File name   : car_dir.py
# Description : By controlling Servo,thecamera can move Up and down,left and right and the Ultrasonic wave can move to left and right.
# Website     : www.gewbot.com
# Author      : William
# Date        : 2018/08/22
import time


class PID:
    def __init__(self):
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        self.Initialize()

    def SetKp(self,invar):
        self.Kp = invar

    def SetKi(self,invar):
        self.Ki = invar

    def SetKd(self,invar):
        self.Kd = invar

    def SetPrevError(self,preverror):
        self.prev_error = preverror

    def Initialize(self):
        self.currtime = time.time()
        self.prevtime = self.currtime

        self.prev_error = 0

        self.Cp = 0
        self.Ci = 0
        self.Cd = 0

    def GenOut(self,error):
        self.currtime = time.time()
        dt = self.currtime - self.prevtime
        de = error - self.prev_error

        self.Cp = self.Kp*error
        self.Ci += error*dt

        self.Cd = 0
        if dt > 0:
            self.Cd = de/dt

        self.prevtime = self.currtime
        self.prev_error = error

        return self.Cp + (self.Ki*self.Ci) + (self.Kd*self.Cd)
'''
pid = PID()
pid.SetKp(Kp)
pid.SetKd(Kd)
pid.SetKi(Ki)

fb = 0
outv = 0

PID_loop = True

while PID_loop:
    error = Sp - fb

    outv = pid.GenOut(error)
    AnalogOut(outv)

    time.sleep(0.05)

    fb = AnalogIn(fb_input)
    pass
'''