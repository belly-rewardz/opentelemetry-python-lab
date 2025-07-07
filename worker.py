from celery import Celery
import time

# Configure Celery with RabbitMQ
celery_app = Celery(
    "worker",
    broker="pyamqp://guest@localhost//",  # RabbitMQ broker URL
    backend="redis://localhost:6379/0"   # Redis for result backend (optional)
)


@celery_app.task(name="worker.process_number")
def process_number(number: int):
    """Process the number received from RabbitMQ"""
    print(f"hello {number}")

    # Simulate some work
    # time.sleep(2)

    return f"Processed number: {number}"


if __name__ == "__main__":
    # Start the Celery worker
    celery_app.start()
