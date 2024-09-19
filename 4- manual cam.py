#sudo apt update
#sudo apt install mosquitto mosquitto-clients
#check first: sudo ss -tuln | grep 1883
#sudo nano /etc/mosquitto/mosquitto.conf
# add: listener 1883
#and : #listener 8883
#cafile /path/to/ca.crt
#certfile /path/to/server.crt
#keyfile /path/to/server.key
#allow_anonymous true
#sudo systemctl restart mosquitto


import paho.mqtt.client as mqtt
from time import sleep
import datetime
import os
import ssl
import subprocess  # Used to run shell commands

# Directory to save captured images
save_dir = "/home/qwe/captured_images"
os.makedirs(save_dir, exist_ok=True)

# Function to capture image using libcamera-still
def capture_image(reason):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"{save_dir}/manual_shot_{timestamp}.jpg"
    
    # Command to capture image using libcamera-still
    command = [
        "libcamera-still", 
        "--output", image_path, 
        "--timeout", "2000"  # Timeout set to 2000 ms
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Image captured and saved at {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture image: {e}")

# Callback function for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ broker successfully.")
        client.subscribe("take_shot")  # Subscribe to the 'take_shot' topic
    else:
        print(f"Connection failed with result code {rc}")

# Callback function when a message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()  # Decode the message payload
    print(f"Received message on topic {topic}: {payload}")
    
    # Trigger manual shot if payload is "1"
    if topic == "take_shot" and payload == "1":
        print("Manual camera shot requested!")
        capture_image("manual_shot")

# MQTT client setup
client = mqtt.Client(client_id="pi_camera")

# Add username and password for HiveMQ broker
client.username_pw_set("alaaa", "Alaa1234")

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Enable SSL/TLS for secure connection
client.tls_set(cert_reqs=ssl.CERT_NONE)  # You can use ssl.CERT_REQUIRED with a valid CA cert if needed
client.tls_insecure_set(True)

# Connect to HiveMQ broker (update with your broker URL and port)
client.connect("2d9dbae8a4de4724b57ae55215e07a89.s1.eu.hivemq.cloud", 8883, 60)

# Start the MQTT loop to continuously listen for messages
client.loop_forever()
