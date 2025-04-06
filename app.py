from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os

app = FastAPI()

# ✅ CORS設定は FastAPI() の後に！
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発中はこれでOK！
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, Eric! 👋"}

@app.get("/about")
def about():
    return {"message": "This is Eric's API 🚀"}

class GreetRequest(BaseModel):
    name: str

@app.post("/greet")
def greet(data: GreetRequest):
    return {"message": f"Hello, {data.name}! 🚀"}

@app.get("/hello")
def say_hello(name: str = "Guest"):
    return {"message": f"Hello, {name}! 🎉"}

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
