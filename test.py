import serial
import time

PORT = 'COM6'  # Kendi portunuz
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print("Donanım Testi Başlıyor... Bütün ışıkların (Beyaz) yanması lazım!")
except:
    print("Porta bağlanılamadı. Kodu durdurup tekrar deneyin.")
    exit()

while True:
    # 255, 255, 255 (Tam Parlaklık R, G, B), Süre: 250ms
    paket = bytearray([0xFF, 255, 255, 255, 250, 0xFE]) 
    ser.write(paket)
    print("Paket gönderildi: BEYAZ FLAŞ (250ms)")
    time.sleep(1) # Saniyede 1 kere gönder