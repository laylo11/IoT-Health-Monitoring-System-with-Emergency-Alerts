#pip install picamera

import paho.mqtt.client as mqtt
from picamera import PiCamera
from time import sleep
import datetime
import os
import ssl

camera = PiCamera()

save_dir = "/home/pi/captured_images"
os.makedirs(save_dir, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("temperature")
    client.subscribe("heart_rate")
    client.subscribe("imu")
    print("Subscribed to topics")

def capture_image(reason):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"{save_dir}/emergency_{reason}_{timestamp}.jpg"
    camera.start_preview()
    sleep(2)  
    camera.capture(image_path)
    camera.stop_preview()
    print(f"Image captured and saved at {image_path}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = float(msg.payload.decode())  
    print(f"Received message on topic {topic}: {payload}")
    
    # Emergency heart rate condition
    if topic == "heart_rate":
        if payload < 60 or payload > 100:  
            print("Abnormal heart rate detected!")
            capture_image("heart_rate")

client = mqtt.Client(client_id="pi_camera")

# Add username and password
client.username_pw_set("Subscribe", "pH2the8w")

client.on_connect = on_connect
client.on_message = on_message

# Enable SSL/TLS
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

# Add broker address and port
client.connect("fbe870248d9e499c9df6d3aa5c1e264b.s1.eu.hivemq.cloud", 8883, 60)

client.loop_forever()
