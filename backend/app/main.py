from fastapi import FastAPI
from .api.routes_generate import router as generate_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI script generation tool is running"}

@app.get("/health")
def health():
    return {"status": "all ok"}

app.include_router(generate_router, prefix="/api")