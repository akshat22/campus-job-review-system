#!/bin/bash

# Stop and remove any existing container
echo "Stopping existing container..."
docker stop ncsu_app || true
docker rm ncsu_app || true

# Build the Docker image
echo "Building Docker image..."
docker build -t ncsu-campus-jobs-review-system .

# Run the Docker container
echo "Running Docker container..."
docker run -d -p 3000:5000 --name ncsu_app ncsu-campus-jobs-review-system

echo "Initializing the database..."
docker exec -it ncsu_app flask db init || true
docker exec -it ncsu_app flask db migrate -m "Initial migration." || true
docker exec -it ncsu_app flask db upgrade || true

echo "Deployment complete! Access the app at http://localhost:3000"