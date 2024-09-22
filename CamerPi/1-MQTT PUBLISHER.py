#pip install paho-mqtt

import paho.mqtt.client as mqtt
import ssl

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("temperature")
    client.subscribe("heart_rate")
    client.subscribe("imu")
    print("Subscribed to topics")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id="pi_camera")

# add username and password
client.username_pw_set("alaaa", "Alaa1234")

client.on_connect = on_connect
client.on_message = on_message

# enable SSL/TLS
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

# add broker URL, Port 8883 for SSL
client.connect("http://2d9dbae8a4de4724b57ae55215e07a89.s1.eu.hivemq.cloud", 8883, 60)

client.loop_forever()
