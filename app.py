import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery import Celery
from typing import Dict

# Create FastAPI app
app = FastAPI(title="OpenTelemetry Python Lab", version="1.0.0")

# Configure Celery with RabbitMQ
celery_app = Celery(
    "worker",
    broker="pyamqp://guest@localhost//",  # RabbitMQ broker URL
    backend="redis://localhost:6379/0"   # Redis for result backend (optional)
)

# Pydantic model for worker endpoint


class NumberRequest(BaseModel):
    number: int


@app.get("/")
async def hello_world() -> Dict[str, str]:
    """Simple hello world endpoint"""
    return {"message": "Hello World"}


@app.get("/long-process")
async def long_process() -> Dict[str, str]:
    """Simulate a long-running process"""
    # Simulate long process with async sleep
    await asyncio.sleep(5)  # 5 seconds delay
    return {"message": "Long process completed after 5 seconds"}


@app.post("/worker")
async def send_to_worker(request: NumberRequest) -> Dict[str, str]:
    """Send number to Celery worker via RabbitMQ"""
    try:
        # Send task to Celery worker
        task = celery_app.send_task(
            "worker.process_number", args=[request.number])

        return {
            "message": f"Task sent to worker with number: {request.number}",
            "task_id": task.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send task to worker: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
