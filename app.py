from fastapi import FastAPI

app = FastAPI()

# 👋 トップページ（そのまま）
@app.get("/")
def read_root():
    return {"message": "Hello, Eric! 👋"}

# 🧠 追加：aboutページ
@app.get("/about")
def about():
    return {"message": "This is Eric's API 🚀"}
