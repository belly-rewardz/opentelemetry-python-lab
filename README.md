# OpenTelemetry Python Lab

A FastAPI application with Celery workers using RabbitMQ for task queuing.

## Features

- **FastAPI Server** with three endpoints:

  - `GET /` - Returns "Hello World"
  - `GET /long-process` - Simulates a long-running process (5 seconds)
  - `POST /worker` - Sends a number to Celery worker via RabbitMQ

- **Celery Worker** that processes numbers from RabbitMQ and prints "hello {number}"

## Prerequisites

- Python 3.11+ (currently using Python 3.12)
- Docker and Docker Compose
- Virtual environment (already configured)

## Setup Instructions

### 1. Start Infrastructure Services

Start RabbitMQ and Redis using Docker Compose:

```bash
docker-compose up -d
```

This will start:

- RabbitMQ on port 5672 (Management UI on port 15672)
- Redis on port 6379

### 2. Install Dependencies

Dependencies are already installed in the virtual environment, but if needed:

```bash
pip install -r requirements.txt
```

### 3. Start the Celery Worker

In one terminal, start the Celery worker:

```bash
celery -A worker worker --loglevel=info
```

### 4. Start the FastAPI Server

In another terminal, start the FastAPI server:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:

```bash
python app.py
```

## API Endpoints

### GET /

Returns a simple "Hello World" message.

**Example:**

```bash
curl http://localhost:8000/
```

**Response:**

```json
{
  "message": "Hello World"
}
```

### GET /long-process

Simulates a long-running process that takes 5 seconds to complete.

**Example:**

```bash
curl http://localhost:8000/long-process
```

**Response:**

```json
{
  "message": "Long process completed after 5 seconds"
}
```

### POST /worker

Sends a number to the Celery worker via RabbitMQ. The worker will print "hello {number}".

**Example:**

```bash
curl -X POST http://localhost:8000/worker \
  -H "Content-Type: application/json" \
  -d '{"number": 42}'
```

**Response:**

```json
{
  "message": "Task sent to worker with number: 42",
  "task_id": "12345678-1234-1234-1234-123456789012"
}
```

## Monitoring

- **RabbitMQ Management UI**: http://localhost:15672 (guest/guest)
- **FastAPI Docs**: http://localhost:8000/docs
- **FastAPI ReDoc**: http://localhost:8000/redoc

## Project Structure

```
.
├── app.py              # FastAPI application
├── worker.py           # Celery worker
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker services (RabbitMQ, Redis)
└── README.md          # This file
```

## Stopping Services

To stop all services:

```bash
# Stop FastAPI and Celery worker (Ctrl+C in their terminals)
# Stop Docker services
docker-compose down
```

## Troubleshooting

1. **Connection refused errors**: Make sure RabbitMQ and Redis are running via Docker Compose
2. **Port conflicts**: Check if ports 5672, 6379, 8000, or 15672 are already in use
3. **Worker not receiving tasks**: Ensure the Celery worker is running and connected to RabbitMQ
