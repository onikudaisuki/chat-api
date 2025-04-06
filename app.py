from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
import requests  # ← 追加

# 環境変数からAPIキー読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_TABLE = "messages"

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Chatリクエスト用モデル（modelフィールドを追加）
class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"  # デフォルトモデルを指定

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # ChatGPTから応答を取得
        response = openai.ChatCompletion.create(
            model=req.model,
            messages=[
                {"role": "user", "content": req.message}
            ]
        )
        reply = response.choices[0].message.content.strip()

        # 🔽 Supabaseにチャットログを保存
        headers = {
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
            "Content-Type": "application/json"
        }

        data = [
            {"role": "user", "message": req.message, "model": req.model},
            {"role": "bot", "message": reply, "model": req.model}
        ]

        supabase_url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"

        res = requests.post(
            supabase_url,
            json=data,
            headers=headers
        )

        if res.status_code >= 400:
            print("Supabase insert failed:", res.text)

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
