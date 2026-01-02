from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.get("/quote")
def quote(theme: str):
    prompt = f"Give one short inspirational quote about {theme}."

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 40}
    }

    r = requests.post(API_URL, headers=headers, json=payload)

    if r.status_code != 200:
        return {"quote": "Error generating quote"}

    return {"quote": r.json()[0]["generated_text"]}
