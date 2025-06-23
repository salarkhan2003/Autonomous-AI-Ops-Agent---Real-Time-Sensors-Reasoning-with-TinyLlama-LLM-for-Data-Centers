import random
import time
import json
from .mqtt_client import publish_data

def simulate_sensor_data(rack_id=1):
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "rack_id": rack_id,
        "temp": round(random.uniform(20, 40), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "voltage": round(random.uniform(3.3, 5.0), 2),
        "current": round(random.uniform(100, 1000), 2),
        "pressure": round(random.uniform(900, 1100), 2)
    }