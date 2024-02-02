import time
import RPi.GPIO as GPIO


line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    #motor.setup()


def run(client,topic):
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    print('LF3: %d   LF2: %d   LF1: %d\n'%(status_right,status_middle,status_left))
    flag = 0
    if (status_right == 1 or status_middle == 1 or status_left == 1) and flag == 0:
      client.publish(topic,"ENTER_FLAG_AREA")
      flag = 1
    else:
      client.publish(topic,"EXIT_FLAG_AREA")
      flag = 0
    time.sleep(0.2)

def tracking(client,topic):
  setup()
  run(client,topic)

if __name__ == '__main__':
    try:
      setup()
      while True:
        run()
    except KeyboardInterrupt:
      pass


