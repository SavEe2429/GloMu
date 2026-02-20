# GloMu: Gesture Recognition Glove

## Link
Google Sheet : https://docs.google.com/spreadsheets/d/1AK52Po2PopiThQfetodwSPBXLgG8P6sq/edit?gid=2104163647#gid=2104163647
Canva : https://www.canva.com/design/DAHBloOVODk/kTl6ioJri6zoe9AX_2IMqg/edit?utm_content=DAHBloOVODk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

Real-time hand gesture recognition using ESP32 with machine learning powered classification.

## What is GloMu?

GloMu is an intelligent glove system that recognizes hand gestures in real-time using sensor fusion and machine learning. It combines an ESP32 microcontroller with a GY-521 IMU breakout module (containing MPU6050 chip) and finger flex sensors to detect hand movements and classify them into predefined gestures. The system provides auditory feedback via text-to-speech and can be extended for various applications like sign language recognition, device control, or gesture-based interfaces.

## Background & Motivation

### Problem Statement

Individuals with hearing and speech disabilities face significant communication barriers in daily life. While sign language is a vital communication tool, many people in the general population lack proficiency in understanding it. This creates communication gaps and reduces opportunities for accessibility to services and social interaction.

### Solution: GloMu

GloMu (Gesture Recognition Glove) was developed to bridge this communication gap by translating hand sign language gestures into text and speech output in real-time. The system leverages Real-Time Embedded Systems technology and Machine Learning to achieve this goal.

### Technical Approach

The system architecture combines three key components:

- **Potentiometer Sensors** (4x) - Measure finger flexion angles for capturing hand gesture shapes
- **GY-521 IMU Module** (6-axis accelerometer and gyroscope) - Detect hand motion and movement patterns
- **ESP32 Microcontroller** - Process sensor data in real-time using FreeRTOS for concurrent tasks
- **Random Forest ML Model** - Classify gestures based on extracted features from sensor data

### Course Alignment

This project aligns with **Real-Time Embedded Systems (CPE-414)** concepts through:
- Real-time task scheduling using FreeRTOS
- Multi-tasking sensor data collection and processing
- Time-critical gesture recognition pipeline
- Hardware abstraction and interrupt-driven I/O

## Key Features

- **Real-time Gesture Recognition**: GY-521 (MPU6050) 6-axis motion capture with 4 potentiometer finger flex sensors
- **Machine Learning Classification**: Random Forest model trained on gesture training data
- **Flexible Training**: Record both static and dynamic gesture patterns
- **Immediate Feedback**: Audio feedback through text-to-speech output
- **Data Logging**: Comprehensive CSV logging for analysis and model improvement
- **Cross-platform**: Python backend works on Windows, macOS, and Linux

## Quick Start

### Hardware Requirements

- ESP32 DevKit V1 board
- GY-521 Module (MPU6050 6-axis IMU breakout board with accelerometer and gyroscope)
- 4x Flex/Potentiometer sensors (for finger detection)
- USB cable for serial communication

### Software Prerequisites

- Python 3.10+
- PlatformIO IDE (for ESP32 firmware)
- pip and virtual environment

### Installation

#### 1. Clone and Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install pyttsx3 pyserial
```

#### 1.1 Install All Python Dependencies

Install all required Python packages for both backend and ML components:

```bash
# Core dependencies for backend and ML
pip install numpy pandas scikit-learn joblib pyttsx3 pyserial matplotlib

# Or using requirements file approach (create requirements.txt)
# numpy>=1.21.0
# pandas>=1.3.0
# scikit-learn>=1.0.0
# joblib>=1.1.0
# pyttsx3>=2.90
# pyserial>=3.5
# matplotlib>=3.5.0
```

**Key Libraries:**
- **numpy** - Numerical computing and array operations
- **pandas** - Data manipulation and CSV handling
- **scikit-learn** - Machine learning tools (Random Forest model)
- **joblib** - Model serialization and deserialization
- **pyttsx3** - Text-to-speech for audio feedback
- **pyserial** - Serial communication with ESP32
- **matplotlib** - Data visualization (for analysis and plotting)

#### 2. Flash ESP32 Firmware

```bash
# Navigate to project directory
cd path/to/ESP32

# Build and upload with PlatformIO
platformio run --target upload
```

#### 2.1 ESP32 Library Dependencies

The following libraries are automatically installed via `platformio.ini`:

- **MPU6050_light** (v1.1.0) - Lightweight I2C driver for MPU6050 sensor

These are defined in `platformio.ini` and automatically downloaded during the build process. No manual installation needed.

#### 3. Hardware Wiring

Connect sensors to ESP32:
- **I2C (GY-521 Module)**: GPIO 21 (SDA), GPIO 22 (SCL)
- **Potentiometers**: GPIO 34, 35, 32, 33 (analog inputs for fingers)
- **Serial**: USB connection (CH340/CP2102 adapter)

## Usage

### Running the Backend

```bash
cd backend
python main.py
```

The interface provides two modes:

#### Mode 1: Live Execution (w)
Recognizes gestures in real-time and provides audio feedback.

```
เลือกโหมด (w: ใช้งานจริง , d: เก็บข้อมูล) : w
```

#### Mode 2: Data Collection (d)

Record new gesture training data:

```
เลือกโหมด (w: ใช้งานจริง , d: เก็บข้อมูล) : d
เลือกโหมด (r: เก็บข้อมูลท่าเคลื่อนไหว, s: เก็บข้อมูลท่านิ่ง, q: ออก): r
ชื่อท่า : wave
ID ของท่า : 1
```

- **r**: Record dynamic gesture (moving hand)
- **s**: Record static gesture (fixed hand position)

### Training the Model

Navigate to the ML folder:

```bash
cd ML
python main.py
```

This loads the trained Random Forest model (`models/gesture_model.joblib`) and uses feature extraction from sensor data for real-time classification.

## Project Structure

```
ESP32/
├── src/                          # ESP32 firmware (C++)
│   └── main.cpp                  # FreeRTOS-based sensor collection
├── backend/                       # Python serial interface
│   ├── main.py                   # User control interface
│   ├── Local_Serial.py           # Serial communication handler
│   ├── tts.py                    # Text-to-speech module
│   ├── dynamic_record_gesture.csv # Training data (dynamic)
│   └── static_gesture_data.csv   # Training data (static)
├── ML/                           # Machine learning pipeline
│   ├── main.py                   # Feature extraction & prediction
│   ├── random_forest.ipynb       # Model training notebook
│   ├── data/                     # Raw sensor data
│   └── models/
│       └── gesture_model.joblib  # Trained Random Forest model
├── platformio.ini                # PlatformIO configuration
└── README.md
```

## Sensor Data Format

The system captures 13 values per sensor reading:

| Column  | Description           |
|---------|----------------------|
| ax      | X-axis acceleration  |
| ay      | Y-axis acceleration  |
| az      | Z-axis acceleration  |
| gx      | X-axis gyroscope     |
| gy      | Y-axis gyroscope     |
| gz      | Z-axis gyroscope     |
| p0-p3   | Finger flex sensors  |

## Feature Extraction

For each 10-signal window, the ML pipeline extracts:
- **Statistical features**: Mean, std, max, min, range, RMS
- **Derived features**: Acceleration magnitude, Gyroscope magnitude

This produces a feature vector that feeds into the Random Forest classifier.

## Getting Help

- **Serial Connection Issues**: Check USB driver installation (CH340/CP2102)
- **Model Accuracy**: Record more diverse gesture examples in the data collection mode
- **Installation**: Verify Python version 3.10+ and virtual environment activation

For detailed ML implementation, see [ML/README.md](ML/README.md)

## Contributing

To contribute improvements:

1. Collect additional gesture training data
2. Experiment with model architectures in [ML/random_forest.ipynb](ML/random_forest.ipynb)
3. Test cross-platform compatibility (Windows/macOS/Linux)
4. Submit improvements with training data and model updates

## Project Maintainer

Created and maintained as an open-source gesture recognition research project.

## License

See LICENSE file for details.

---

**Note**: The project includes Thai language prompts for native user interface. Modify strings in [backend/main.py](backend/main.py) and [backend/Local_Serial.py](backend/Local_Serial.py) for other languages.
