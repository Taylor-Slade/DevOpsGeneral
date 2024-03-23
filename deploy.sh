#!/bin/bash

echo "Building and running containers in detached mode..."
docker-compose up --build -d

# Wait for a few seconds to ensure that the application has started
sleep 2

echo "Making a test request..."
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/users/)

if [ "$STATUS_CODE" -eq 200 ]; then
    echo "Test request successful! Status code: $STATUS_CODE"
else
    echo "Test request failed. Status code: $STATUS_CODE"
fi

echo "Window closing in 5 seconds"
echo "connect to UI at localhost:5000/users/"
sleep 5

# To stop the containers later, you can use the following command:
# docker-compose down
