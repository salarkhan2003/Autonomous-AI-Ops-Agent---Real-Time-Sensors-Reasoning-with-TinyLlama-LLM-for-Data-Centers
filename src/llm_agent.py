import requests

def get_llm_action(data, anomaly_type):
    prompt = f"""
    You are an AI agent managing a data center. Sensors report:
    - Rack ID: {data['rack_id']}
    - Temperature: {data['temp']}°C
    - Voltage: {data['voltage']}V
    - Current: {data['current']}mA
    - Pressure: {data['pressure']}hPa
    Anomaly detected: {anomaly_type}.
    Suggest 1-2 specific actions to optimize energy or prevent failure.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:1.5b", "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        action = response.json()["response"]
        return action
    except requests.exceptions.RequestException as e:
        print(f"Ollama error: {e}")
        return "Notify admin: LLM unavailable"

def execute_action(action):
    if "fan speed" in action.lower():
        return {"command": "set_fan_speed", "value": 10}
    elif "shift load" in action.lower():
        return {"command": "shift_load", "value": 0.1}
    return {"command": "notify_admin", "message": action}