import paho.mqtt.client as mqtt
import time

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    print(f"Received message: " , str(message.payload.decode()) , "on topic {message.topic}")



client.username_pw_set("Patients_monitoring_system", "P2553")

# Create an MQTT client instance
client = mqtt.Client("Patients monitoring system")  # the client ID

# Assign the on_message callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect("2d9dbae8a4de4724b57ae55215e07a89.s1.eu.hivemq.cloud", 8883, 60) 

# Subscribe to a topic
client.subscribe("test/topic") # Replace with your topic

# Start the loop to process received messages
client.loop_forever()

