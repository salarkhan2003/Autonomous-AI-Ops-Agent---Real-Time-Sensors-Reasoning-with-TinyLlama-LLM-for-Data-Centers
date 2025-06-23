import requests

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "deepseek-r1:1.5b", "prompt": "Test", "stream": False},
        timeout=10
    )
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
