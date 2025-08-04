```python
# Project: FPGA-Based Real-Time Audio Signal Processor (Test Vector Generator)
#
# What it does:
# This script generates I2S test vectors from a real 48 kHz WAV file (male voice saying "hello world"). It extracts 16 samples and converts them to 16-bit VHDL array format.
#
# How we built it:
# 1. Setup:
#    - Installed Python 3.9, scipy, numpy.
#    - Used a public-domain WAV file (48 kHz, mono, 16-bit PCM).
# 2. Process:
#    - Loaded WAV file and extracted first 16 samples.
#    - Scaled to 16-bit signed integers.
#    - Formatted as VHDL array for Audio_Processor_tb.vhd.
# 3. Usage:
#    - Run: `python Generate_Audio_Test.py`.
#    - Copy output to TEST_SAMPLES in Audio_Processor_tb.vhd.
# 4. Notes:
#    - WAV file is from a real speech clip (available at freesound.org).
#    - Samples are raw PCM, matching WM8731 I2S format.

import scipy.io.wavfile as wavfile
import numpy as np

# Load WAV file (replace with your 48 kHz mono WAV file path)
sample_rate, audio = wavfile.read('speech_hello_world.wav')
assert sample_rate == 48000, "WAV must be 48 kHz"

# Extract first 16 samples (mono)
samples = audio[:16].astype(np.int16)

# Convert to VHDL hex format
vhdl_samples = [f'x"{sample:04X}"' for sample in samples]
vhdl_array = f"constant TEST_SAMPLES : sample_array := (\n    {', '.join(vhdl_samples)}\n);"

# Save to file
with open('audio_test_vectors.txt', 'w') as f:
    f.write(vhdl_array)

print("Test vectors saved to audio_test_vectors.txt")
print("Copy to TEST_SAMPLES in Audio_Processor_tb.vhd")
```