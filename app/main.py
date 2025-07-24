import uvicorn
import logging
from fastapi import FastAPI

from app.endpoints import device

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("api.log"), logging.StreamHandler()],
)

app = FastAPI()

app.include_router(device.router)
# app.include_router(report.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
