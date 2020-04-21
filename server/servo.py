#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Motor
# Product     : RaspTank  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/12/27
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

def num_import_int(initial):		#Call this function to import data from '.txt' file
	global r
	with open("//etc/config.txt") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				r=line
	begin=len(list(initial))
	snum=r[begin:]
	n=int(snum)
	return n

print('Loading...')
for i in range(0,16):
	exec('L%d_MAX=num_import_int("L%d_MAX:")'%(i,i))
	exec('L%d_MIN=num_import_int("L%d_MIN:")'%(i,i))
	for n in range(1,11):
		exec('L%d_ST%d=num_import_int("L%d_ST%d:")'%(i,n,i,n))
print('Setting up server...')

org_pos = L11_ST1

def camera_ang(direction, ang):
	global org_pos
	if ang == 0:
		ang=4
	if direction == 'lookdown':
		if org_pos <= L11_MAX:
			org_pos+=ang
		else:
			org_pos = L11_MAX
	elif direction == 'lookup':
		if org_pos >= L11_MIN:
			org_pos-=ang
		else:
			org_pos = L11_MIN
	elif direction == 'home':
		org_pos = L11_MAX
	else:
		pass
	#print(ang)
	pwm.set_pwm(11,0,org_pos)


def hand(command):
	if command == 'in':
		pwm.set_pwm(13, 0, L13_ST3)
		pwm.set_pwm(12, 0, L12_ST4)
		time.sleep(0.5)
		pwm.set_pwm(13, 0, L13_ST2)
		pwm.set_pwm(12, 0, L12_ST2)
	elif command == 'out':
		pwm.set_pwm(12, 0, L12_ST1)
		pwm.set_pwm(13, 0, L13_ST1)


def cir_pos(pos):
	pwm.set_pwm(14, 0, L14_ST2+30*pos)


def catch(pos):
	pwm.set_pwm(15, 0, L15_ST2+10*pos)


def hand_pos(pos):
	if pos <= 4:
		pwm.set_pwm(12, 0, L12_ST1-30*pos)
		pwm.set_pwm(13, 0, L13_ST1-30*pos)
	else:
		pwm.set_pwm(12, 0, (L12_ST1-24*pos))
		pwm.set_pwm(13, 0, L13_ST3-6*(pos-4))

def ahead():
	pwm.set_pwm(11,0,300)


def initPosAll():
	pwm.set_all_pwm(0, 300)


def clean_all():
	pwm.set_pwm(0, 0, 0)
	pwm.set_pwm(1, 0, 0)
	pwm.set_pwm(2, 0, 0)
	pwm.set_pwm(3, 0, 0)
	pwm.set_pwm(4, 0, 0)
	pwm.set_pwm(5, 0, 0)
	pwm.set_pwm(6, 0, 0)
	pwm.set_pwm(7, 0, 0)
	pwm.set_pwm(8, 0, 0)
	pwm.set_pwm(9, 0, 0)
	pwm.set_pwm(10, 0, 0)
	pwm.set_pwm(11, 0, 0)
	pwm.set_pwm(12, 0, 0)
	pwm.set_pwm(13, 0, 0)
	pwm.set_pwm(14, 0, 0)
	pwm.set_pwm(15, 0, 0)


if __name__ == '__main__':
	try:
		pos_input = 0
		OUT = 1
		while 1:
			a=input()
			if OUT == 1:
				if pos_input < 13:
					pos_input+=1
				else:
					print('MAX')
					OUT = 0
			else:
				if pos_input > 1:
					pos_input-=1
				else:
					print('MIN')
					OUT = 1
			catch(pos_input)
			print(pos_input)

			pass
	except KeyboardInterrupt:
		clean_all()

