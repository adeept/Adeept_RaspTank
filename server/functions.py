#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Functions
# Author	  : William
# Date		: 2020/03/17
import time
import RPi.GPIO as GPIO
import threading
from mpu6050 import mpu6050
import Adafruit_PCA9685
import os
import json
import ultra
import Kalman_filter
import move

move.setup()

kalman_filter_X =  Kalman_filter.Kalman_filter(0.01,0.1)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# MPU_connection = 1
# try:
#     sensor = mpu6050(0x68)
#     print('mpu6050 connected, PT MODE ON')
# except:
#     MPU_connection = 0
#     print('mpu6050 disconnected, ARM MODE ON')

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

def num_import_int(initial):        #Call this function to import data from '.txt' file
    global r
    with open(thisPath+"/RPIservo.py") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

pwm0_direction = 1
pwm0_init = num_import_int('init_pwm0 = ')
pwm0_max  = 520
pwm0_min  = 100
pwm0_pos  = pwm0_init

pwm1_direction = 1
pwm1_init = num_import_int('init_pwm1 = ')
pwm1_max  = 520
pwm1_min  = 100
pwm1_pos  = pwm1_init

pwm2_direction = 1
pwm2_init = num_import_int('init_pwm2 = ')
pwm2_max  = 520
pwm2_min  = 100
pwm2_pos  = pwm2_init

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

def pwmGenOut(angleInput):
	return int(round(23/9*angleInput))


def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(line_pin_right,GPIO.IN)
	GPIO.setup(line_pin_middle,GPIO.IN)
	GPIO.setup(line_pin_left,GPIO.IN)


class Functions(threading.Thread):
	def __init__(self, *args, **kwargs):
		self.functionMode = 'none'
		self.steadyGoal = 0

		self.scanNum = 3
		self.scanList = [0,0,0]
		self.scanPos = 1
		self.scanDir = 1
		self.rangeKeep = 0.7
		self.scanRange = 100
		self.scanServo = 1
		self.turnServo = 0
		self.turnWiggle = 200

		setup()

		super(Functions, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()
		self.__flag.clear()

	def radarScan(self):
		global pwm0_pos
		scan_speed = 3
		result = []

		if pwm0_direction:
			pwm0_pos = pwm0_max
			pwm.set_pwm(1, 0, pwm0_pos)
			time.sleep(0.8)

			while pwm0_pos>pwm0_min:
				pwm0_pos-=scan_speed
				pwm.set_pwm(1, 0, pwm0_pos)
				dist = ultra.checkdist()
				if dist > 20:
					continue
				theta = 180 - (pwm0_pos-100)/2.55 # +30 deviation
				result.append([dist, theta])
		else:
			pwm0_pos = pwm0_min
			pwm.set_pwm(1, 0, pwm0_pos)
			time.sleep(0.8)

			while pwm0_pos<pwm0_max:
				pwm0_pos+=scan_speed
				pwm.set_pwm(1, 0, pwm0_pos)
				dist = ultra.checkdist()
				if dist > 20:
					continue
				theta = (pwm0_pos-100)/2.55
				result.append([dist, theta])
		pwm.set_pwm(1, 0, pwm0_init)
		return result


	def pause(self):
		self.functionMode = 'none'
		move.move(80, 'no', 'no', 0.5)
		self.__flag.clear()


	def resume(self):
		self.__flag.set()


	def automatic(self):
		self.functionMode = 'Automatic'
		self.resume()


	def trackLine(self):
		self.functionMode = 'trackLine'
		self.resume()


	def steady(self,goalPos):
		self.functionMode = 'Steady'
		self.steadyGoal = goalPos
		self.resume()


	def trackLineProcessing(self):
		status_right = GPIO.input(line_pin_right)
		status_middle = GPIO.input(line_pin_middle)
		status_left = GPIO.input(line_pin_left)
		#print('R%d   M%d   L%d'%(status_right,status_middle,status_left))
		if status_middle == 1:
			move.move(100, 'forward', 'no', 1)
		elif status_left == 1:
			move.move(100, 'no', 'right', 1)
		elif status_right == 1:
			move.move(100, 'no', 'left', 1)
		else:
			move.move(100, 'backward', 'no', 1)

		time.sleep(0.1)


	def automaticProcessing(self):
		print('automaticProcessing')
		if self.rangeKeep/3 > ultra.checkdist():
			 move.move(100, 'backward', 'no', 0.5)
		elif self.rangeKeep > ultra.checkdist():
			move.move(100, 'no', 'left', 0.5)
		else:
			move.move(100, 'forward', 'no', 0.5)
		time.sleep(0.1)
		if self.functionMode == 'none':
			move.move(80, 'no', 'no', 0.5)

		# pwm.set_pwm(2, 0, pwm2_init)
		# if self.scanPos == 1:
		# 	pwm.set_pwm(self.scanServo, 0, pwm1_init-self.scanRange)
		# 	time.sleep(0.3)
		# 	self.scanList[0] = ultra.checkdist()
		# elif self.scanPos == 2:
		# 	pwm.set_pwm(self.scanServo, 0, pwm1_init)
		# 	time.sleep(0.3)
		# 	self.scanList[1] = ultra.checkdist()
		# elif self.scanPos == 3:
		# 	pwm.set_pwm(self.scanServo, 0, pwm1_init+self.scanRange)
		# 	time.sleep(0.3)
		# 	self.scanList[2] = ultra.checkdist()

		# self.scanPos = self.scanPos + self.scanDir

		# if self.scanPos > self.scanNum or self.scanPos < 1:
		# 	if self.scanDir == 1:self.scanDir = -1
		# 	elif self.scanDir == -1:self.scanDir = 1
		# 	self.scanPos = self.scanPos + self.scanDir*2
		# print(self.scanList)

		# if min(self.scanList) < self.rangeKeep:
		# 	if self.scanList.index(min(self.scanList)) == 0:
		# 		pwm.set_pwm(self.turnServo, 0, pwm0_init+int(self.turnWiggle/3.5))
		# 	elif self.scanList.index(min(self.scanList)) == 1:
		# 		if self.scanList[0] < self.scanList[2]:
		# 			pwm.set_pwm(self.turnServo, 0, pwm0_init+self.turnWiggle)
		# 		else:
		# 			pwm.set_pwm(self.turnServo, 0, pwm0_init-self.turnWiggle)
		# 	elif self.scanList.index(min(self.scanList)) == 2:
		# 		pwm.set_pwm(self.turnServo, 0, pwm0_init-int(self.turnWiggle/3.5))
		# 	if max(self.scanList) < self.rangeKeep or min(self.scanList) < self.rangeKeep/3:
		# 		move.move(80, 'backward', 'no', 0.5)
		# else:
		# 	#move along
		# 	move.move(80, 'forward', 'no', 0.5)
		# 	pass


	def steadyProcessing(self):
		print('steadyProcessing')
		xGet = sensor.get_accel_data()
		xGet = xGet['x']
		xOut = kalman_filter_X.kalman(xGet)
		pwm.set_pwm(2, 0, self.steadyGoal+pwmGenOut(xOut*9))
		# pwm.set_pwm(2, 0, self.steadyGoal+pwmGenOut(xGet*10))
		time.sleep(0.05)


	def functionGoing(self):
		if self.functionMode == 'none':
			self.pause()
		elif self.functionMode == 'Automatic':
			self.automaticProcessing()
		elif self.functionMode == 'Steady':
			self.steadyProcessing()
		elif self.functionMode == 'trackLine':
			self.trackLineProcessing()


	def run(self):
		while 1:
			self.__flag.wait()
			self.functionGoing()
			pass


if __name__ == '__main__':
	pass
	# fuc=Functions()
	# fuc.radarScan()
	# fuc.start()
	# fuc.automatic()
	# # fuc.steady(300)
	# time.sleep(30)
	# fuc.pause()
	# time.sleep(1)
	# move.move(80, 'no', 'no', 0.5)
