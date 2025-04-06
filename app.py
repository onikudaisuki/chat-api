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
