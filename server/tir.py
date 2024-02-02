#emission de tirs : 





import RPi.GPIO as GPIO
import time
import uuid 
import InfraLib 
tankID  =  uuid.getnode()
# Set GPIO mode

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins for IR emitter and receiver
ir_emitter_pin = 11  # Replace with your GPIO pin number
ir_receiver_pin = 15  # Replace with your GPIO pin number

# Set up GPIO pins
GPIO.setup(ir_emitter_pin, GPIO.OUT)
GPIO.setup(ir_receiver_pin, GPIO.IN)

def send_ir_signal():
  InfraLib.IRBlast(uuid.getnode(), "LASER") 

def receive_ir_signal():
            
    while True:
        received = InfraLib.getSignal(ir_receiver_pin)
        print(received)


# Example: Send IR signal
send_ir_signal()

# Example: Receive IR signal
received_signal = receive_ir_signal()
print("Received IR Signal:", received_signal)

# Clean up GPIO
GPIO.cleanup()
