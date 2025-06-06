#!/bin/bash

# Start the container
docker run -d \
  --name test-app-container \
  -p 8000:8000 \
  ${container-image}

# Wait for container to start
sleep 5

# Check container logs
echo "Container logs:"
docker logs test-app-container 