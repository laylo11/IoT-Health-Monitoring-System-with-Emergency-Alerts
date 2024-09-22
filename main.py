import random
import winsound
import time

# from max30102 import MAX30102



# Define the heart rate range and emergency value
MIN_HEART_RATE = 60
MAX_HEART_RATE = 100
EMERGENCY_MIN = 180
EMERGENCY_MAX = 200

# Initialize the MAX30102 sensor
sensor = MAX30102()

def play_emergency_sound():
    # Play a sound (frequency in Hz, duration in milliseconds)
    winsound.Beep(1000, 1000)  # 1000 Hz for 1 second

def check_heart_rate():
    # Read the heart rate from the sensor
    heart_rate = sensor.get_heart_rate()
    
    print(f"Heart Rate: {heart_rate} BPM")
    
    # Check if the heart rate is in the emergency range
    if EMERGENCY_MIN <= heart_rate <= EMERGENCY_MAX:
        print("Emergency! Heart rate is too high!")
        play_emergency_sound()
    elif heart_rate < MIN_HEART_RATE or heart_rate > MAX_HEART_RATE:
        print("Heart rate is out of normal range!")
    else:
        print("Heart rate is normal.")

# Main loop for testing
if __name__ == "_main_":
    while True:
        check_heart_rate()
        time.sleep(2)  # Wait for 2 seconds before next reading