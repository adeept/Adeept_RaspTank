import paho.mqtt.client as mqtt
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Telecommande")
client.connect(mqttBroker)

while True:
    commande = input('Give me the direction and turn : ')
    client.publish("commande",commande)
    print("Just published " + str(commande) + " to the Robot")
    time.sleep(1)