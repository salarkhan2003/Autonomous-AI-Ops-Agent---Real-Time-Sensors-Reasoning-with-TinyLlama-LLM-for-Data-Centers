def digital_twin(temp, load, fan_speed):
    # Simplified model: temp = base_temp + load_effect - cooling_effect
    new_temp = temp + (load * 0.1) - (fan_speed * 0.05)
    return max(20, min(40, new_temp))  # Constrain 20-40°C

def simulate_scenario(data):
    load = 80  # Simulated % CPU load
    fan_speed = 50  # Simulated fan speed
    predicted_temp = digital_twin(data["temp"], load, fan_speed)
    return {"predicted_temp": predicted_temp, "load": load, "fan_speed": fan_speed}