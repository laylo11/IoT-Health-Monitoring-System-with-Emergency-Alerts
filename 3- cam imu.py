import paho.mqtt.client as mqtt
from time import sleep
import datetime
import os
import ssl
import subprocess  # Used to run shell commands

# Directory to save captured images
save_dir = "/home/qwe/captured_images"
os.makedirs(save_dir, exist_ok=True)

def capture_image(reason):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"{save_dir}/emergency_{reason}_{timestamp}.jpg"
    
    # Capture image using libcamera-still command
    command = [
        "libcamera-still", 
        "--output", image_path, 
        "--timeout", "2000"  # Adjust timeout as needed
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


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        client.subscribe("temperature")
        client.subscribe("heart_rate")
        client.subscribe("imu")
        print("Subscribed to topics")
    else:
        print(f"Connection failed with result code {rc}")
        if rc == 5:
            print("Connection refused - not authorized. Check your username, password, and TLS settings.")

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = float(msg.payload.decode())  
        print(f"Received message on topic {topic}: {payload}")
    
        # Emergency heart rate condition
        if topic == "heart_rate":
            if payload < 60 or payload > 100:  
                print("Abnormal heart rate detected!")
                capture_image("heart_rate")
        
        # Emergency IMU condition (Z-acceleration)
        if topic == "imu":
            z_acceleration = payload
            if abs(z_acceleration) < 5 or abs(z_acceleration) > 15:
                print("Abnormal IMU reading detected (possible fall)!")
                capture_image("imu_fall")
    
    except ValueError:
        print(f"Invalid payload received on topic {topic}: {msg.payload.decode()}")

# MQTT client setup
client = mqtt.Client(client_id="pi_camera")

# Add username and password
client.username_pw_set("alaaa", "Alaa1234")

client.on_connect = on_connect
client.on_message = on_message

# Enable SSL/TLS
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Consider using ssl.CERT_REQUIRED if you have a CA cert
client.tls_insecure_set(True)

# Add broker address and port
client.connect("2d9dbae8a4de4724b57ae55215e07a89.s1.eu.hivemq.cloud", 8883, 60)

# Start the MQTT loop
client.loop_forever()
