#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Product     : GWR
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/07/24
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

MOTOR_M1_IN1 =  15      #Define the positive pole of M1
MOTOR_M1_IN2 =  14      #Define the negative pole of M1
MOTOR_M2_IN1 =  12      #Define the positive pole of M2
MOTOR_M2_IN2 =  13      #Define the negative pole of M2

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 0
left_backward = 1

right_forward = 0
right_backward= 1

pwn_A = 0
pwm_B = 0
FREQ = 50



def map(x,in_min,in_max,out_min,out_max):
  return (x - in_min)/(in_max - in_min) *(out_max - out_min) +out_min

def setup():#Motor initialization
    global motor1,motor2,motor3,motor4,pwm_motor,pwm_motor
    i2c = busio.I2C(SCL, SDA)
    pwm_motor = PCA9685(i2c, address=0x40) #default 0x40

    pwm_motor.frequency = FREQ

    motor1 = motor.DCMotor(pwm_motor.channels[MOTOR_M1_IN1],pwm_motor.channels[MOTOR_M1_IN2] )
    motor1.decay_mode = (motor.SLOW_DECAY)
    motor2 = motor.DCMotor(pwm_motor.channels[MOTOR_M2_IN1],pwm_motor.channels[MOTOR_M2_IN2] )
    motor2.decay_mode = (motor.SLOW_DECAY)



def motorStop():#Motor stops
    global motor1,motor2
    motor1.throttle = 0
    motor2.throttle = 0


def Motor(channel,direction,motor_speed):
    # channel,1~4:M1~M4
  if motor_speed > 100:
    motor_speed = 100
  elif motor_speed < 0:
    motor_speed = 0

  speed = map(motor_speed, 0, 100, 0, 1.0)

  pwm_motor.frequency = FREQ
  # Prevent the servo from affecting the frequency of the motor
  if direction == 1:
    speed = -speed
  if channel == 1:
    motor1.throttle = speed
  elif channel == 2:
    motor2.throttle = speed




def motor_left(status, direction, speed):#Motor 2 positive and negative rotation
	if status == 0: # stop
		motorStop()
	else:
		if direction == Dir_backward:
			Motor(1, Dir_forward, speed)
			Motor(2, Dir_backward, speed)
		elif direction == Dir_forward:
			Motor(1, Dir_backward, speed)
			Motor(2, Dir_forward, speed)

def motor_right(status, direction, speed):#Motor 1 positive and negative rotation
	if status == 0: # stop
		motorStop()
	else:
		if direction == Dir_backward:
			Motor(1, Dir_backward, speed)
			Motor(2, Dir_forward, speed)
		elif direction == Dir_forward:
			Motor(1, Dir_forward, speed)
			Motor(2, Dir_backward, speed)


def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1  
	#speed = 100
	if direction == 'forward':
		if turn == 'right':
			motor_left(0, left_forward, int(speed*radius))
			motor_right(1, right_backward, speed)
		elif turn == 'left':
			motor_left(1, left_backward, speed)
			motor_right(0, right_forward, int(speed*radius))
		else:
			motor_left(1, left_backward, speed)
			motor_right(1, right_backward, speed)
	elif direction == 'backward':			
		if turn == 'right':
			motor_left(0, left_backward, int(speed*radius))
			motor_right(1, right_forward, speed)
		elif turn == 'left':
			motor_left(1, left_forward, speed)
			motor_right(0, right_backward, int(speed*radius))
		else:
			motor_left(1, left_forward, speed)
			motor_right(1, right_forward, speed)
	elif direction == 'no':
		if turn == 'right':
			motor_left(1, left_backward, speed)
			motor_right(1, right_forward, speed)
		elif turn == 'left':
			motor_left(1, left_forward, speed)
			motor_right(1, right_backward, speed)
		else:
			motorStop()
	else:
		pass




def destroy():
    motorStop()
    pwm_motor.deinit()

if __name__ == '__main__':
	try:
		speed_set = 60
		setup()
		move(speed_set, 'forward', 'no', 0.8)
		time.sleep(1.3)
		motorStop()
		destroy()
	except KeyboardInterrupt:
		destroy()

