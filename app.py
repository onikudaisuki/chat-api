from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Eric! 👋"}

@app.get("/about")
def about():
    return {"message": "This is Eric's API 🚀"}

# 🆕 ここからPOSTの定義！
class GreetRequest(BaseModel):
    name: str

@app.post("/greet")
def greet(data: GreetRequest):
    return {"message": f"Hello, {data.name}! 🚀"}

@app.get("/hello")
def say_hello(name: str = "Guest"):
    return {"message": f"Hello, {name}! 🎉"}

import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": req.message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
