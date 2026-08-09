import sounddevice as sd
import numpy as np
import time
import serial
import random

PORT = 'COM6'  # Replace with your NUCLEO's port
BAUD = 115200  # Replace with your NUCLEO's baud rate

THRESHOLD = 5 # Adjust this threshold based on your microphone sensitivity
COOLDOWN = 0.1  # Cooldown time in seconds to prevent multiple triggers from a single clap


try : 
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print(f"Connected to {PORT} at {BAUD} baud.")
except Exception as e:
    print(f"Failed to connect to {PORT} at {BAUD} baud. Error: {e}")
    exit()

print("Listening for claps...(Stop the program with Ctrl+C)")
last_beat_time = time.time() 


def ses_yakalayicisi(indata, frames, time_info, status):
    global last_beat_time
    if status:
        pass

    audio_data = indata [:, 0]  # Assuming mono input, take the first channel
    rms = np.sqrt(np.mean(audio_data**2))*8000  # Calculate RMS value
    if rms > THRESHOLD and (time.time() - last_beat_time) > COOLDOWN:
            print(f"Clap detected! RMS: {rms}")

            komut = str(random.randint(1, 4)).encode()  # Random command between 1 and 4
            ser.write(komut)  # Send the command to the NUCLEO,

            last_beat_time = time.time()  # Update the last beat time

try : 
    with sd.InputStream(channels=1, callback=ses_yakalayicisi, samplerate=44100):
        while True:
            time.sleep(0.1)  # Keep the main thread alive

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    ser.close()