import sounddevice as sd
import numpy as np
import time
import serial
import random

PORT = 'COM6'  # Replace with your NUCLEO's port
BAUD = 115200  # Replace with your NUCLEO's baud rate

THRESHOLD = 35 # Adjust this threshold based on your microphone sensitivity
COOLDOWN = 0.1  # Cooldown time in seconds to prevent multiple triggers from a single clap


try : 
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print(f"Connected to {PORT} at {BAUD} baud.")
except Exception as e:
    print(f"Failed to connect to {PORT} at {BAUD} baud. Error: {e}")
    exit()

print("Listening for claps...(Stop the program with Ctrl+C)")
last_beat_time = time.time() 

def send_payload(r, g, b, duration):
    """
    STM32'ye 6 baytlık özel veri paketimizi gönderir.
    Format: [START(0xFF), R(0-255), G(0-255), B(0-255), TIME(0-255), STOP(0xFE)]
    """
    # Verileri 1 byte (0-255) sınırları içinde tutmayı garantile
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    duration = max(0, min(255, int(duration)))
    
    # Bayt dizisini (Bytearray) oluştur ve UART'tan fırlat
    paket = bytearray([0xFF, r, g, b, duration, 0xFE])
    ser.write(paket)

    
def ses_yakalayicisi(indata, frames, time_info, status):
    global last_beat_time
    if status:
        pass

    audio_data = indata[:, 0]
    rms = np.sqrt(np.mean(audio_data**2)) * 100000  

    if rms > THRESHOLD and (time.time() - last_beat_time) > COOLDOWN:
        print(f"BASS DROP! ⚡ RMS: {int(rms)}")
        
        # Karışık rastgele sayılar yerine, keskin ve profesyonel sahne renkleri paleti
        renk_paleti = [
            (255, 0, 0),     # Sadece Kırmızı
            (0, 255, 0),     # Sadece Yeşil
            (0, 0, 255),     # Sadece Mavi
            (255, 0, 255),   # Mor (Kırmızı + Mavi)
            (0, 255, 255),   # Turkuaz (Yeşil + Mavi)
            (255, 255, 0)    # Sarı (Kırmızı + Yeşil)
        ]
        
        # Bu paletten o anki ritim için rastgele tek bir renk seç
        kirmizi, yesil, mavi = random.choice(renk_paleti)
        
        sure = 70 # Işıkların biraz daha belirgin olması için süreyi 50ms yaptık
        
        send_payload(kirmizi, yesil, mavi, sure)
        
        last_beat_time = time.time()

try : 
    with sd.InputStream(channels=1, callback=ses_yakalayicisi, samplerate=44100):
        while True:
            time.sleep(0.1)  # Keep the main thread alive

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    ser.close()