IoT Vital Signs & Temperature Monitoring System

This project involves designing an IoT system using a Raspberry Pi and ESP to monitor vital signs such as heart rate, oxygen levels, and temperature. It includes real-time data transmission, visualization, and emergency image capture capabilities.

Features

- Vital Signs & Temperature Monitoring: Monitors heart rate, oxygen percentage, and temperature.
- Emergency & Manual Image Capture: Automatically captures images during emergencies (e.g., abnormal heart rate or oxygen levels) or manually via the Node-RED interface.
- MQTT Communication: Transmits sensor data and images using MQTT (via HiveMQ) for real-time monitoring.
- Node-RED Visualization: Displays real-time data on a Node-RED dashboard, including emergency and manually triggered images in base64 format.

System Components

- Raspberry Pi: Central hub for data collection and processing.
- ESP: Connected to sensors for transmitting data to the Raspberry Pi.
- Max302102 Heart Rate & Oxygen Sensor: Monitors heart rate and oxygen percentage.
- DHT11 Temperature Sensor: Tracks body or environmental temperature.
- PiCamera: Captures images during emergencies and manual triggers.
- MQTT Broker (HiveMQ): Facilitates communication between the Raspberry Pi and Node-RED.
- Node-RED: Visualizes real-time sensor data and captured images.

How It Works

1. Data Collection: The Raspberry Pi collects heart rate, oxygen levels, and temperature data from the ESP-connected sensors.
2. Emergency & Manual Image Capture: A PiCamera captures images when abnormal readings occur or when manually triggered via the Node-RED dashboard.
3. Data Transmission: Sensor data and images are transmitted via MQTT to HiveMQ, which forwards the data to Node-RED.
4. Visualization: Node-RED provides real-time visualization, displaying sensor data and captured images in base64 format. Users can also manually trigger image capture from the dashboard.

Installation

1. Clone the repository:
    ```
    git clone https://github.com/laylo11/IoT-Health-Monitoring-System-with-Emergency-Alerts.git
    cd IoT-Health-Monitoring-System-with-Emergency-Alerts
    ```
2. Install the required dependencies:
    ```
    sudo apt-get install node-red
    pip install paho-mqtt
    ```
3. Configure the Raspberry Pi to connect to the HiveMQ MQTT broker and set up Node-RED for real-time data visualization.

Future Improvements

- Integration with cloud storage for long-term data logging.
- Adding more health-related sensors for comprehensive monitoring.
- Enhancing the alert system with SMS or email notifications during emergencies.

