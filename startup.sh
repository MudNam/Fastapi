#!/bin/bash

# Update system and install dependencies
apt-get update
apt-get install -y python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

# Create model cache directory
mkdir -p model_cache

# Initialize model using model_loader
python3 -c "
from model_loader import model
print('Model initialized successfully')
"

# Start FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8080 