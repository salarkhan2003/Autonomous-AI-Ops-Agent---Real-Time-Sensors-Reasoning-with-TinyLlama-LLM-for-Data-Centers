from fastapi import FastAPI
from src.database import get_recent_data

from src.llm_agent import get_llm_action

app = FastAPI()

@app.get("/data")
async def get_data():
    return get_recent_data()

@app.post("/ask")
async def ask(query: dict):
    prompt = query["query"]
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    })
    return {"action": response.json()["response"]}