#!/bin/bash

# Start infrastructure services
echo "Starting RabbitMQ and Redis..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

echo "Services are ready!"
echo ""
echo "To start the application:"
echo "1. In one terminal: celery -A worker worker --loglevel=info"
echo "2. In another terminal: uvicorn app:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "API will be available at: http://localhost:8000"
echo "RabbitMQ Management UI: http://localhost:15672 (guest/guest)"
