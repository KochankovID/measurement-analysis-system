#!/bin/bash

# Start server
echo "Starting server"
uvicorn app.main:app --host 0.0.0.0 --port 8001