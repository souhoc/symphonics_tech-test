import uvicorn
from fastapi import FastAPI
from app.endpoints import device, report

app = FastAPI()

app.include_router(device.rooter)
app.include_router(report.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")

