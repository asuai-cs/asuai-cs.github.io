```python
"""
Project: Gesture-Controlled Robotic Arm (Sensor Calibration Script)

Summary:
This script calibrates the flex sensors and MPU6050 IMU on the gesture glove to ensure accurate gesture recognition. It runs on the Raspberry Pi, reading serial data from the Arduino (Gesture_Glove.ino) and computing minimum/maximum values for flex sensors and offsets for IMU data. Calibration data is saved to a JSON file for use in Gesture_Control.py.

Implementation Details:
1. Hardware Setup:
   - Same setup as Gesture_Control.py (Arduino Nano, flex sensors, MPU6050, Raspberry Pi).
   - Ensured glove is worn comfortably for calibration.

2. Software Setup:
   - Installed Python libraries: pyserial, numpy, json.
   - Ran this script on the Raspberry Pi after uploading Gesture_Glove.ino to Arduino.

3. Calibration Process:
   - Prompted user to perform straight and fully bent finger positions to capture flex sensor ranges.
   - Recorded IMU data in a neutral position to compute offsets.
   - Saved calibration data to 'calibration.json'.

4. Testing:
   - Tested calibration by verifying mapped flex angles (0-90 degrees) and IMU offsets.
   - Used calibration data in Gesture_Control.py for accurate gesture mapping.

5. Usage:
   - Run this script before deploying Gesture_Control.py.
   - Update Gesture_Glove.ino with calibration values if hardcoding is preferred.

Note: Run this script in a controlled environment with consistent glove positioning. Recalibrate if glove fit changes.
"""

import serial
import json
import numpy as np
import time

# Serial port setup
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def collect_samples(n_samples=100):
    """Collect n_samples of sensor data"""
    flex_data = [[] for _ in range(4)]
    accel_data = {'x': [], 'y': [], 'z': []}
    
    for _ in range(n_samples):
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            for i in range(4):
                flex_data[i].append(data[f'flex{i+1}'])
            accel_data['x'].append(data['accel_x'])
            accel_data['y'].append(data['accel_y'])
            accel_data['z'].append(data['accel_z'])
            time.sleep(0.01)
        except json.JSONDecodeError:
            continue
    
    return flex_data, accel_data

def calibrate():
    print("Calibration started...")
    
    # Collect data for straight fingers
    print("Keep fingers straight for 5 seconds...")
    time.sleep(2)
    flex_straight, _ = collect_samples(100)
    
    # Collect data for bent fingers
    print("Fully bend fingers for 5 seconds...")
    time.sleep(2)
    flex_bent, accel_neutral = collect_samples(100)
    
    # Compute calibration values
    calibration = {
        'flex_min': [float(np.mean(f)) for f in flex_straight],
        'flex_max': [float(np.mean(f)) for f in flex_bent],
        'accel_offset': {
            'x': float(np.mean(accel_neutral['x'])),
            'y': float(np.mean(accel_neutral['y'])),
            'z': float(np.mean(accel_neutral['z']))
        }
    }
    
    # Save to JSON
    with open('calibration.json', 'w') as f:
        json.dump(calibration, f, indent=4)
    
    print("Calibration completed. Data saved to calibration.json")
    print(calibration)

if __name__ == "__main__":
    calibrate()
```