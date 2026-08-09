# Pocket Rave: Real-Time Audio-Reactive LED Controller 🎵⚡

This project bridges the gap between high-level audio signal processing and low-level embedded hardware control. It transforms an STM32 microcontroller into a real-time, audio-reactive lighting controller by analyzing ambient music beats (bass drops) and triggering synchronized LED strobe effects via asynchronous USB UART communication.

## 🧠 System Architecture

The architecture relies on a "Brain + Spinal Cord" methodology:
* **The Brain (PC/Python):** Continuously listens to ambient audio, calculates the RMS (Root Mean Square) to measure audio intensity, and detects beats using a predefined dynamic threshold.
* **The Spinal Cord (STM32 MCU):** Waits for commands via UART. Utilizing Direct Memory Access (DMA), it receives data without interrupting the main CPU execution. A non-blocking State Machine immediately translates these triggers into hardware PWM signals to drive the LEDs.

## ✨ Key Features
* **Real-Time DSP (Digital Signal Processing):** Captures microphone input at a 44.1kHz sample rate using the `sounddevice` library for zero-latency audio capture.
* **Non-Blocking Firmware:** Replaces amateur `delay()` functions with hardware Timers and a state-machine logic on the STM32 for robust execution.
* **DMA-Powered UART:** Serial data reception is handled entirely by the DMA controller, ensuring 0% packet loss and keeping the main loop strictly for logic execution.
* **Customizable Sensitivities:** Easily adjustable thresholds and cooldown algorithms in the Python script to match any room acoustics or speaker volume.

## 🛠️ Hardware Requirements
* STM32 Nucleo-144 Board (e.g., STM32F439ZI)
* LEDs (Green, Blue, Red) and appropriate resistors
* Jumper wires & Breadboard
* PC with a built-in or external microphone

## 💻 Software & Dependencies
**Embedded Firmware:**
* STM32CubeIDE
* HAL Library

**Python PC Client:**
* Python 3.x
* `pip install sounddevice numpy pyserial`

## 🚀 How to Run the Project

### Part 1: Microcontroller Setup
1. Open the `STM32_Firmware` folder in STM32CubeIDE.
2. Build the project and flash it to your STM32 board.
3. Ensure the LEDs are connected to the designated Timer PWM pins (Check `.ioc` file for exact pinout).

### Part 2: PC Setup
1. Connect the STM32 board via USB. 
2. Open Device Manager to find your ST-Link Virtual COM Port (e.g., `COM6`).
3. Open `rave.py` and update the `PORT` variable with your COM port.
4. Run the Python script. 
5. Play your favorite bass-heavy track and watch the LEDs sync to the beat!

## 🛣️ Roadmap (V2.0 Coming Soon)
* [ ] **FreeRTOS Integration:** Migrating from a bare-metal `while(1)` loop to a task-based RTOS architecture.
* [ ] **Custom Payload Protocol:** Implementing a robust packet structure `[START][R][G][B][TIME][STOP]` instead of single-character triggers.
* [ ] **FFT Audio Analysis:** Separating audio into frequency bands (Bass, Mid, Treble) to trigger specific colors for different instruments.

---
*Developed by Ömer Alp Konakçı*