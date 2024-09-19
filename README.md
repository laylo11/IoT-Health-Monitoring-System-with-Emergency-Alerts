IoT Vital Signs & Temperature Monitoring System

This project involves designing an IoT system using a Raspberry Pi and ESP to monitor vital signs such as heart rate, oxygen percentage, and temperature. It also includes real-time data transmission and visualization. The system can capture images during emergencies or manually through the Node-RED interface.

Features

Vital Signs & Temperature Monitoring: Monitors heart rate, oxygen percentage, and temperature.
Emergency & Manual Image Capture: Automatically captures images using a PiCamera during emergencies (e.g., abnormal heart rate, oxygen levels) or manually through the Node-RED interface.
MQTT Communication: Transmits sensor data and images using MQTT (via HiveMQ) for real-time monitoring.
Node-RED Visualization: Provides real-time data visualization on a Node-RED dashboard, including manually triggered and emergency images in base64 format.
System Components

Raspberry Pi: Central hub for data collection and processing.
ESP: Connected to sensors for transmitting data to the Raspberry Pi.
Heart Rate & Oxygen Sensor: Monitors heart rate and oxygen percentage.
Temperature Sensor: Tracks body or environmental temperature.
PiCamera: Captures images during emergencies and manual triggers.
MQTT Broker (HiveMQ): Facilitates data communication between the Raspberry Pi and Node-RED.
Node-RED: Visualizes real-time sensor data and captured images.
How It Works

Data Collection: The Raspberry Pi collects data from the sensors connected to the ESP, including heart rate, oxygen percentage, and temperature readings.
Emergency & Manual Image Capture: The system captures images using a PiCamera in case of abnormal readings or manually via the Node-RED dashboard.
Data Transmission: Sensor data and captured images are sent via MQTT to the HiveMQ broker, which forwards the information to Node-RED.
Visualization: Node-RED provides real-time visualization, showing sensor data and images in base64 format. Users can trigger photo capture manually from the dashboard.
Installation

Clone the repository:
git clone https://github.com/laylo11/IoT-Health-Monitoring-System-with-Emergency-Alerts.git
cd IoT-Health-Monitoring-System-with-Emergency-Alerts
Install the required dependencies:
sudo apt-get install node-red
pip install paho-mqtt
Configure the Raspberry Pi to connect to the HiveMQ MQTT broker and set up Node-RED for real-time data visualization.
Future Improvements

Integration with cloud storage for long-term data logging.
Adding more health-related sensors for comprehensive monitoring.
Enhancing the alert system with SMS or email notifications during emergencies.
