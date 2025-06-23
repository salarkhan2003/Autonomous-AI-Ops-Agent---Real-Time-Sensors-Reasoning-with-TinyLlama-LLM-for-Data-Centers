# AI-Powered Energy Optimization Agent for Data Centers

## Overview
A BTech EEE final-year project to optimize data center energy using TinyML and DeepSeek-R1:1.5B LLM. Monitors temperature, voltage, current, and airflow; detects anomalies; and makes autonomous decisions (e.g., adjust cooling, shift load). Features predictive maintenance, multi-agent coordination, and a digital twin.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Install Ollama and run DeepSeek: `ollama run deepseek-r1:1.5b`
3. Install Mosquitto: `sudo apt install mosquitto mosquitto-clients`
4. Run API: `uvicorn src.api:app --host 0.0.0.0 --port 8000`
5. Run dashboard: `python src/dashboard.py`
6. Run main script: `python main.py`

## Features
- TinyML for anomaly detection (overheating, current spikes).
- DeepSeek LLM for autonomous decisions.
- Multi-agent coordination via MQTT.
- Digital twin for scenario simulation.
- Flask dashboard with real-time metrics and chat interface.

## Next Steps
- Weeks 9–12: Integrate Raspberry Pi and sensors (DHT22, INA219, BMP280).
- Deploy in KL University lab and measure energy savings.

## Setup
1. Install Mosquitto: Download from mosquitto.org and add to PATH.
2. Install dependencies: `pip install -r requirements.txt`
3. Run Ollama: `ollama run deepseek-r1:1.5b`
4. Run Mosquitto: `mosquitto`
5. Train model: `python src\anomaly_detector.py`
6. Run main: `python main.py`
7. Run API: `uvicorn src.api:app --host 0.0.0.0 --port 8000`
8. Run dashboard: `python src\dashboard.py`

## Author
Salar, BTech EEE, KL University