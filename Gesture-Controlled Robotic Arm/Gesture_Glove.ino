```cpp
/*
 * Project: Gesture-Controlled Robotic Arm (Arduino Firmware)
 *
 * Summary:
 * This project implements a gesture-controlled robotic arm using a wearable sensor glove and a 6-DOF robotic arm. This Arduino firmware runs on an Arduino Nano, reading data from four flex sensors (for finger movements) and an MPU6050 IMU (for hand orientation). The sensor data is processed and sent to a Raspberry Pi via serial communication in JSON format. The Raspberry Pi maps gestures to arm movements using inverse kinematics. The system demonstrates skills in robotics, embedded systems, sensor fusion, and control systems, with applications in human-machine interaction.
 *
 * Implementation Details:
 * 1. Hardware Setup:
 *    - Components: Arduino Nano, 4x flex sensors (e.g., 2.2-inch), MPU6050 IMU, 6-DOF robotic arm, Raspberry Pi 4, 5V power supply.
 *    - Connected flex sensors to analog pins A0-A3 with voltage divider circuits (10kΩ resistors).
 *    - Connected MPU6050 to I2C pins (SDA: A4, SCL: A5, VCC: 3.3V, GND: GND).
 *    - Linked Arduino to Raspberry Pi via USB serial (TX/RX or USB cable).
 *    - Powered Arduino via USB or external 5V supply.
 *
 * 2. Software Setup:
 *    - Installed Arduino IDE (2.3.2 or later).
 *    - Installed libraries: Wire, Adafruit_MPU6050, ArduinoJson.
 *    - Configured serial baud rate to 115200 for communication with Raspberry Pi.
 *    - Uploaded this code to the Arduino Nano.
 *
 * 3. Sensor Configuration:
 *    - Calibrated flex sensors to map resistance changes to finger bend angles (0-90 degrees).
 *    - Initialized MPU6050 for accelerometer and gyroscope data (2g, 250dps ranges).
 *    - Set sampling rate to 10 Hz to balance responsiveness and stability.
 *
 * 4. Data Processing:
 *    - Read flex sensor voltages and mapped to bend angles.
 *    - Read IMU acceleration and angular velocity for hand orientation.
 *    - Formatted data as JSON (e.g., {"flex1": angle, ..., "accel_x": value, ...}).
 *    - Sent JSON data over serial to Raspberry Pi.
 *
 * 5. Testing and Calibration:
 *    - Tested flex sensor readings via Serial Monitor, ensuring consistent angle mapping.
 *    - Verified IMU data accuracy using a test sketch to monitor orientation.
 *    - Calibrated sensors using a separate Python script (optional) for precise gesture recognition.
 *    - Confirmed serial communication with Raspberry Pi using a terminal (e.g., minicom).
 *
 * 6. Deployment and Optimization:
 *    - Integrated the glove with the robotic arm system, ensuring secure wiring.
 *    - Tested gesture-to-arm mapping in a controlled environment (e.g., pick-and-place tasks).
 *    - Optimized sensor sampling rate and serial communication for low latency.
 *    - Documented the setup in a GitHub repository with a demo video.
 *
 * Note: This code handles glove sensor data collection. The Raspberry Pi processes gestures and controls the arm (see Gesture_Control.py). Ensure proper calibration and secure wiring for reliable operation.
 */

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>

Adafruit_MPU6050 mpu;

// Flex sensor pins
const int FLEX_PINS[] = {A0, A1, A2, A3};
const int NUM_FLEX = 4;

// Real calibration values (from Calibrate_Sensors.py)
const float FLEX_MIN[] = {512.0, 510.0, 508.0, 515.0}; // Straight fingers
const float FLEX_MAX[] = {800.0, 795.0, 810.0, 805.0}; // Bent fingers


void setup() {
  Serial.begin(115200);
  
  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) { delay(10); }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  
  Serial.println("MPU6050 initialized");
}

void loop() {
  // Read flex sensors
  float flex_angles[NUM_FLEX];
  for (int i = 0; i < NUM_FLEX; i++) {
    int raw = analogRead(FLEX_PINS[i]);
    // Map ADC values to angles (0-90 degrees)
    flex_angles[i] = map(raw, FLEX_MIN[i], FLEX_MAX[i], 0, 90);
    flex_angles[i] = constrain(flex_angles[i], 0, 90);
  }
  
  // Read IMU data
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  
  // Create JSON object
  StaticJsonDocument<200> doc;
  doc["flex1"] = flex_angles[0];
  doc["flex2"] = flex_angles[1];
  doc["flex3"] = flex_angles[2];
  doc["flex4"] = flex_angles[3];
  doc["accel_x"] = a.acceleration.x;
  doc["accel_y"] = a.acceleration.y;
  doc["accel_z"] = a.acceleration.z;
  doc["gyro_x"] = g.gyro.x;
  doc["gyro_y"] = g.gyro.y;
  doc["gyro_z"] = g.gyro.z;
  
  // Serialize and send over serial
  String output;
  serializeJson(doc, output);
  Serial.println(output);
  
  delay(100); // 10 Hz sampling
}
```