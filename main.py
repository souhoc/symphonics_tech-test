import uvicorn

from fastapi import FastAPI

app = FastAPI()

# Include routes

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
