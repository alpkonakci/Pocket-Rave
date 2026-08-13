import sounddevice as sd
import numpy as np
import time
import serial

PORT = 'COM6'  # Change to your specific port
BAUD = 115200

# Continuous Mode Audio Calibration Settings
# IMPORTANT: Adjust these based on the printed "Current RMS" values!
NOISE_GATE = 15  # Sounds below this level are ignored (Cuts background noise)
MAX_RMS = 120   # Maximum audio intensity required for 100% brightness

try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print(f"Connected to {PORT} at {BAUD} baud.")
except Exception as e:
    print(f"Connection error: {e}")
    exit()

print("Continuous mode activated... Smooth lighting based on audio started. (Press Ctrl+C to stop)")

last_send_time = 0
# Send max 30 packets per second (30 FPS) to prevent UART DMA flooding
FPS_LIMIT = 1.0 / 30.0  

def audio_callback(indata, frames, time_info, status):
    global last_send_time
    if status:
        pass

    audio_data = indata[:, 0]
    rms = np.sqrt(np.mean(audio_data**2)) * 100000  

    current_time = time.time()
    
    # -------------------------------------------------------------
    # DIAGNOSTIC TOOL: Watch your terminal to see the music volume
    print(f"Current RMS: {int(rms)}") 
    # -------------------------------------------------------------

    if (current_time - last_send_time) >= FPS_LIMIT:
        
        if rms < NOISE_GATE:
            # If the song is paused or too quiet, turn off the lights immediately
            payload = bytearray([0xFF, 0, 0, 0, 0, 0xFE])
            ser.write(payload)
        else:
            # Map the audio intensity proportionally to the 0-255 range
            intensity = int(((rms - NOISE_GATE) / (MAX_RMS - NOISE_GATE)) * 255)
            
            # Clamp the values strictly between 0 and 255
            intensity = max(0, min(255, intensity))
            
            # Visual Theme: Cyberpunk (Purple - Pink fluctuations)
            red = intensity
            green = int(intensity * 0.8)  # 60% of red
            blue = int(intensity * 0.8)   # 80% of red

            # The 4th byte (duration) is sent as 0 because continuous mode does not use osDelay
            payload = bytearray([0xFF, red, green, blue, 0, 0xFE])
            ser.write(payload)
        
        last_send_time = current_time

try:
    with sd.InputStream(channels=1, callback=audio_callback, samplerate=44100):
        while True:
            time.sleep(0.1)

except KeyboardInterrupt:
    # Turn off the lights safely when the program is manually terminated
    ser.write(bytearray([0xFF, 0, 0, 0, 0, 0xFE]))
    print("\nProgram terminated and lights turned off.")
finally:
    ser.close()