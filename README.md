# Face Recognition and Room Access System

A modular Embedded Vision and Edge AI project for face recognition-based room access control using Raspberry Pi and Computer Vision technologies.

---

## Overview

This project aims to build a complete room access control system that can:

- Capture images from a camera
- Detect human faces
- Recognize authorized users
- Make access decisions
- Log access events
- Store unknown face snapshots
- Simulate or control physical access hardware

The project follows a clean and modular software architecture and is developed incrementally from simulation to real embedded hardware deployment.

---

## Project Goals

- Learn Computer Vision fundamentals
- Learn Embedded AI workflows
- Learn Raspberry Pi development
- Learn software architecture and modular design
- Build a portfolio-ready GitHub project
- Create a foundation for future AI and Medical Imaging projects

---

## Technology Stack

### Core Technologies

- Python
- OpenCV
- InsightFace
- ONNX Runtime
- NumPy

### Development Environment

- Git
- GitHub
- Visual Studio Code

### Hardware (Planned)

- Raspberry Pi 4
- Raspberry Pi Camera Module
- SD Card
- Green / Red LEDs
- Temperature Sensor
- GPIO

---

## Architecture

Current architecture:

```text
room_access
├── access_control
├── app
├── camera
├── config
├── dashboard
├── hardware
├── recognition
└── storage
```

Each module has a single responsibility and can be extended independently.

---

## Development Roadmap

### Phase 0
Project setup and architecture

### Phase 1
Development environment and simulation setup

### Phase 2
Image acquisition

### Phase 3
Face detection

### Phase 4
Face recognition

### Phase 5
Access control logic

### Phase 6
Logging and storage

### Phase 7
Dashboard

### Phase 8
Raspberry Pi integration

### Phase 9
GPIO integration

---
## Current Status

The project currently includes the following implemented features:

- Real-time face recognition
- Live dashboard overlay
- Authorized user enrollment
- Automatic embedding generation
- Event logging to CSV
- Event image capture
- Camera factory and registry
- Hardware factory and registry
- Mock LED controller
- Mock temperature sensor
- Centralized configuration system
- Raspberry Pi ready architecture

---

## Running the Project

### Run the live access control system

```bash
python main.py live
```

### Enroll a new authorized user

```bash
python main.py enroll <user_name>
```

Example:

```bash
python main.py enroll abbas
```

### Rebuild embeddings for all authorized users

```bash
python main.py enroll-all
```

---

## Configuration

Project configuration is stored in:

```text
config/settings.json
```

Current configurable components include:

- Recognition threshold
- Camera backend
- Display resolution
- Recognition interval
- Hardware backend
- Enrollment capture count

---

## Runtime Data

The following folders are generated automatically during execution:

```text
data/events/
data/logs/
data/embeddings/
```

These files are excluded from Git where appropriate.

---

## Future Work

- Raspberry Pi Camera integration
- Real Raspberry Pi GPIO integration
- Physical temperature sensor integration
- Final production UI
- Documentation improvements
- UML diagrams
- Version 1.0 release
