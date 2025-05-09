FROM python:3.11-slim

# Set environment variables
ENV MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
ENV MODEL_CACHE_DIR="/app/model_cache"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p ${MODEL_CACHE_DIR} /app/credentials

# Copy application code
COPY . .

# Download and cache model during build
RUN python -c "from model_loader import ModelLoader; loader = ModelLoader(); loader.get_model('${MODEL_NAME}')"

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 