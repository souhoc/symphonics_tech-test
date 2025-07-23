import uvicorn

from fastapi import FastAPI

from .routes import devices, report

app = FastAPI()

# Include routes
app.include_router(devices.router, tags=["devices"])
app.include_router(report.router, tags=["devices"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
