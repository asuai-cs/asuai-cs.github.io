```python
# Project: IoT-Based Smart Energy Monitoring System (ML Training)
#
# What it does:
# This script trains a LinearRegression model on the REDD dataset (refrigerator power consumption) to predict power usage. It generates weights for Energy_Server.py.
#
# How we built it:
# 1. Setup:
#    - Installed Python 3.9, pandas, scikit-learn.
#    - Downloaded REDD dataset (low_freq, house 1, channel 5: refrigerator).
# 2. Process:
#    - Loaded 1-hour power samples (1000 points).
#    - Trained model on last 3 time steps to predict next power value.
#    - Saved weights to energy_model.txt.
# 3. Usage:
#    - Run: `python Train_Energy_Model.py`.
#    - Copy weights to MODEL_WEIGHTS and MODEL_INTERCEPT in Energy_Server.py.
# 4. Notes:
#    - Data is from REDD dataset (real refrigerator, ~100W average).
#    - Download REDD from http://redd.csail.mit.edu/.

import pandas as pd
from sklearn.linear_model import LinearRegression

# Load REDD dataset (replace with your path to channel 5 data)
data = pd.read_csv('redd_house1_channel5.csv')  # Power in watts
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['time_index'] = (data['timestamp'] - data['timestamp'].min()).total_seconds() / 3600.0

# Prepare features (last 3 time steps) and target
X = []
y = []
for i in range(3, len(data)):
    X.append([data['time_index'].iloc[i-j] for j in range(1, 4)])
    y.append(data['power'].iloc[i])
X = pd.DataFrame(X, columns=['t-1', 't-2', 't-3'])

# Train model
model = LinearRegression()
model.fit(X, y)

# Save weights
with open('energy_model.txt', 'w') as f:
    f.write(f"MODEL_WEIGHTS = {model.coef_.tolist()}\n")
    f.write(f"MODEL_INTERCEPT = {model.intercept_}\n")

print("Model weights saved to energy_model.txt")
print("Weights:", model.coef_)
print("Intercept:", model.intercept_)
```