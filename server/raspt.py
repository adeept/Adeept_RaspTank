
import time
import paho.mqtt.client as mqtt
import uuid 
import RPi.GPIO as GPIO
import InfraLib


line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
IR_RECEIVER = 15


flag_zone = False

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    GPIO.setup(IR_RECEIVER, GPIO.IN)
    #motor.setup()


def tracking(channel):
    global flag_zone
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    print('LF3: %d   LF2: %d   LF1: %d\n'%(status_right,status_middle,status_left))
    topic = "tanks/" + str(tank_id) + "/flag"
    print(topic)
    if status_middle:
      if not flag_zone:
        client.publish(topic,"ENTER_FLAG_AREA")
        flag_zone = True
    else:
      if flag_zone:
        client.publish(topic,"EXIT_FLAG_AREA")
        flag_zone = False


# Set up MQTT client
broker_address = "192.168.1.5"  # Replace with your MQTT broker address
port = 1883
topic = "init"  

tank_id =  uuid.getnode()         
print( "mac addr: ",tank_id)    
solo_topic = "tanks/"+ str(tank_id)+"/init"                                

client = mqtt.Client("robot")

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)
        
def on_message(client, userdata, msg):
    movement = msg.payload.decode("utf-8")
    print(f"Received init info: {movement}")


"""# Set callback functions
client.on_connect = on_connect
client.on_message = on_message"""





""" # Motor control functions
def move_forward():
    # Code to move the tank forward
    pass

def move_backward():
    # Code to move the tank backward
    pass

def turn_left():
    # Code to turn the tank left
    pass

def turn_right():
    # Code to turn the tank right
    pass

def stop_movement():
    # Code to stop all tank movements
    pass """

# Keep the program running
try:
    setup()
    GPIO.add_event_detect(line_pin_middle, GPIO.BOTH, callback=tracking)
    shot_topic = "tanks/"+str(tank_id)+"shots"
    GPIO.add_event_detect(IR_RECEIVER, GPIO.FALLING, callback=lambda x: print(InfraLib.getSignal(IR_RECEIVER, client)), bouncetime=100)

    # Connect to the broker
    client.connect(broker_address, port, 60)
    client.subscribe(solo_topic)
    client.on_message = on_message
    # Start the MQTT loop
    client.publish(topic,"INIT "+str(tank_id))
    time.sleep(40)

    # enter flag area
    flag_topic = "tanks/" + str(tank_id) + "/flag"
    client.subscribe(flag_topic)
    #GPI0.add_event_detect((client,flag_topic)


    client.subscribe(shot_topic)


except KeyboardInterrupt:
    client.disconnect()
