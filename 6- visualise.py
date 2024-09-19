import paho.mqtt.client as mqtt
from time import sleep
import datetime
import os
import ssl
import subprocess  # Used to run shell commands
import base64  # For converting images to Base64

# Directory to save captured images
save_dir = "/home/qwe/captured_images"
os.makedirs(save_dir, exist_ok=True)

# Function to capture image and send it as Base64 over MQTT
def capture_and_send_image(client, reason):
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
        
        # Convert image to Base64
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Publish the image as Base64 to MQTT
        client.publish("image/frame", image_base64)
        print(f"Image sent to 'image/frame' topic on MQTT")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture image: {e}")

# Callback function for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        client.subscribe("take_shot")
        client.subscribe("temperature")
        client.subscribe("heart_rate")
        client.subscribe("spo2")
        client.subscribe("imu")
        print("Subscribed to topics")
    else:
        print(f"Connection failed with result code {rc}")
        if rc == 5:
            print("Connection refused - not authorized. Check your username, password, and TLS settings.")

# Callback function when a message is received
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()  # Decode the message payload
    print(f"Received message on topic {topic}: {payload}")
    
    # Handle manual camera shot request
    if topic == "take_shot" and payload == "1":
        print("Manual camera shot requested!")
        capture_and_send_image(client, "manual_shot")
    
    # Handle heart rate emergency condition
    if topic == "heart_rate":
        try:
            heart_rate = float(payload)
            if heart_rate < 60 or heart_rate > 100:  
                print("Abnormal heart rate detected!")
                capture_and_send_image(client, "heart_rate")
        except ValueError:
            print(f"Invalid heart rate payload: {payload}")
    
    # Handle SpO2 emergency condition
    if topic == "spo2":
        try:
            spo2 = float(payload)
            if spo2 < 95:
                print("Abnormal SpO2 level detected!")
                capture_and_send_image(client, "spo2")
        except ValueError:
            print(f"Invalid SpO2 payload: {payload}")
    
    # Handle IMU (Z-acceleration) emergency condition
    if topic == "imu":
        try:
            z_acceleration = float(payload)
            if abs(z_acceleration) < 5 or abs(z_acceleration) > 15:
                print("Abnormal IMU reading detected (possible fall)!")
                capture_and_send_image(client, "imu_fall")
        except ValueError:
            print(f"Invalid IMU payload: {payload}")

# MQTT client setup
client = mqtt.Client(client_id="pi_camera")

# Add username and password
client.username_pw_set("alaaa", "Alaa1234")

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Enable SSL/TLS
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Consider using ssl.CERT_REQUIRED if you have a CA cert
client.tls_insecure_set(True)

# Connect to the HiveMQ broker
client.connect("2d9dbae8a4de4724b57ae55215e07a89.s1.eu.hivemq.cloud", 8883, 60)

# Start the MQTT loop
client.loop_forever()

