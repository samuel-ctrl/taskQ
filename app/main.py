from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import backTask

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse("test")

# url pattern declaration:
app.include_router(backTask.router)