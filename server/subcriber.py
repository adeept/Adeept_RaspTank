import paho.mqtt.client as mqtt
import time


def on_message(client,userdata,message):
    print("Received message : ",str(message.payload.decode('utf-8')))

mqttBroker = "192.168.0.109"
client = mqtt.Client("Robot")
client.connect(mqttBroker)

client.loop_start()

client.subscribe("commande")
client.on_message = on_message

time.sleep(30)
client.loop_stop()