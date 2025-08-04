```python
# Project: Autonomous Drone Navigation System (Sensor Calibration)
#
# What it does:
# This script calibrates the HC-SR04 ultrasonic sensor and USB webcam on a Raspberry Pi 4. It measures distances to a wall and ArUco marker sizes to ensure accurate navigation data.
#
# How we built it:
# 1. Hardware:
#    - Used Raspberry Pi 4, USB webcam (640x480), HC-SR04 (TRIG: GPIO 23, ECHO: GPIO 24).
#    - Set up in a 3x3m room with a 10cm ArUco marker.
# 2. Software:
#    - Installed Python 3.9, opencv-python, RPi.GPIO.
#    - Ran in the same room as Drone_Navigate.py.
# 3. Process:
#    - Measured distances (0.3m, 0.5m, 1m) to a wall for ultrasonic calibration.
#    - Detected marker size at 0.5m for webcam calibration.
#    - Saved average values to calibration.json.
# 4. Usage:
#    - Run: `python Calibrate_Sensors.py`.
#    - Follow prompts to place marker and measure distances.
#    - Use values in config.yaml if needed.
# 5. Notes:
#    - Calibration is from real indoor tests.
#    - Recalibrate if room lighting or sensor changes.

import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import json

# Initialize ultrasonic sensor
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.00001)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    while GPIO.input(ECHO) == 0 and time.time() - start_time < 0.1:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1 and time.time() - start_time < 0.1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 / 100
    return distance

def get_marker_size():
    ret, frame = cap.read()
    if not ret:
        return None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    if ids is not None and len(ids) > 0:
        marker_size = np.mean(np.abs(corners[0][0][1] - corners[0][0][0]))
        return marker_size
    return None

def calibrate():
    print("Starting calibration...")
    
    # Calibrate ultrasonic sensor
    distances = []
    for target in [0.3, 0.5, 1.0]:
        print(f"Place sensor {target}m from wall, press Enter...")
        input()
        samples = []
        for _ in range(10):
            dist = get_distance()
            if dist is not None:
                samples.append(dist)
            time.sleep(0.1)
        avg_dist = np.mean(samples) if samples else None
        distances.append({'target': target, 'measured': avg_dist})
    
    # Calibrate webcam
    print("Place 10cm ArUco marker 0.5m away, press Enter...")
    input()
    marker_sizes = []
    for _ in range(10):
        size = get_marker_size()
        if size is not None:
            marker_sizes.append(size)
        time.sleep(0.1)
    avg_marker_size = np.mean(marker_sizes) if marker_sizes else None
    
    # Save calibration
    calibration = {
        'ultrasonic': distances,
        'marker_size': {'distance': 0.5, 'size': avg_marker_size}
    }
    with open('calibration.json', 'w') as f:
        json.dump(calibration, f, indent=4)
    
    print("Calibration done. Saved to calibration.json")
    print(calibration)

if __name__ == "__main__":
    try:
        calibrate()
    finally:
        cap.release()
        GPIO.cleanup()
```