# GloMu: Gesture Recognition Glove

Real-time hand gesture recognition using ESP32 with machine learning powered classification.

## What is GloMu?

GloMu is an intelligent glove system that recognizes hand gestures in real-time using sensor fusion and machine learning. It combines an ESP32 microcontroller with an IMU sensor (MPU6050) and finger flex sensors to detect hand movements and classify them into predefined gestures. The system provides auditory feedback via text-to-speech and can be extended for various applications like sign language recognition, device control, or gesture-based interfaces.

## Key Features

- **Real-time Gesture Recognition**: MPU6050-based motion capture with 4 potentiometer finger flex sensors
- **Machine Learning Classification**: Random Forest model trained on gesture training data
- **Flexible Training**: Record both static and dynamic gesture patterns
- **Immediate Feedback**: Audio feedback through text-to-speech output
- **Data Logging**: Comprehensive CSV logging for analysis and model improvement
- **Cross-platform**: Python backend works on Windows, macOS, and Linux

## Quick Start

### Hardware Requirements

- ESP32 DevKit V1 board
- MPU6050 (6-axis IMU sensor with accelerometer and gyroscope)
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

#### 2. Flash ESP32 Firmware

```bash
# Navigate to project directory
cd path/to/ESP32

# Build and upload with PlatformIO
platformio run --target upload
```

#### 3. Hardware Wiring

Connect sensors to ESP32:
- **I2C (MPU6050)**: GPIO 21 (SDA), GPIO 22 (SCL)
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
