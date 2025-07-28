#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Wait for the server to be up
# echo "Waiting for Ollama to be ready..."
# until curl -s http://localhost:11434 > /dev/null; do
#   sleep 1
# done

sleep 5

echo "Pulling required models..."
ollama pull nomic-embed-text:latest
ollama pull llama3.2:1b

# Keep the container running
wait
