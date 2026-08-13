# Sound-Reactive RTOS LED Controller 🎵⚡

This project is an industrial-grade, real-time sound-reactive LED controller built on the STM32F4 microcontroller. It uses **FreeRTOS** for task management, **DMA** for zero-overhead UART communication, and a **Custom 6-Byte Payload Protocol** to bridge Python-based digital signal processing (DSP) with embedded hardware.

**Author:** Ömer Alp Konakçı

## 🚀 Key Engineering Features
* **Real-Time OS (FreeRTOS):** Hardware control is decoupled from blocking delays. The system operates asynchronously, ensuring high stability and responsive PWM generation.
* **DMA UART Reception:** The STM32 receives high-frequency audio data packets via Direct Memory Access (DMA), entirely bypassing the CPU until a full 6-byte packet is securely buffered.
* **Universal C Firmware:** The microcontroller runs a single, smart firmware that automatically determines the operating mode (Continuous or Strobe) on the fly based on the parsed payload parameters, requiring no firmware flashes to switch modes.
* **Python DSP Engine:** Real-time audio RMS calculation and linear mapping using `sounddevice` and `numpy`.

## 📦 The 6-Byte Custom Protocol
Communication between the PC and STM32 is handled via a lightweight, custom bytearray protocol running at 115200 baud:
`[START (0xFF)]` `[RED (0-255)]` `[GREEN (0-255)]` `[BLUE (0-255)]` `[DURATION (ms)]` `[STOP (0xFE)]`

## 🛠️ Operating Modes (Dual-Python Architecture)

### 1. Continuous Mode (`rave_continuous.py`)
* **Concept:** Smooth, ambient audio visualization.
* **Logic:** Analyzes audio at 30 FPS, linearly mapping the RMS volume strictly to a 0-999 PWM range.
* **Theme:** Pre-configured with a Cyberpunk (Neon Purple/Pink) ratio, but mathematically adjustable. The hardware never blocks; it dynamically updates brightness as long as the duration byte is `0`.

### 2. Strobe / Rave Mode (`rave.py`)
* **Concept:** High-energy, peak-detection flashes.
* **Logic:** Uses a dynamic noise gate to detect sharp bass drops. Upon detection, it blasts a randomized, full-intensity color for a short duration (e.g., 50ms) and returns to pitch black.

## ⚙️ Hardware Stack
* **MCU:** STM32F4 Series (Nucleo)
* **Actuators:** RGB LEDs mapped to discrete Hardware Timers (TIM3, TIM4, TIM12) with Internal Clocks enabled.
* **Communication:** USB over UART (USART3).

## 🚀 How to Run
1. Flash the `main.c` firmware to the STM32 board via STM32CubeIDE.
2. Calibrate `NOISE_GATE` and `MAX_RMS` inside the Python scripts according to your specific microphone hardware.
3. Run `python rave_continuous.py` for ambient lighting, or `python rave.py` for a club-style strobe effect.