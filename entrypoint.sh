#!/bin/bash

echo '▶️ Starting Ollama server...' 
ollama serve &

echo '⏳ Waiting for Qdrant to be ready...'
until curl -s http://qdrant:6333/collections > /dev/null; do
    sleep 2
done

echo '✅ Qdrant is ready. Loading initial data into collection...'
python3 data_loader/load_data.py

echo '🚀 Starting Streamlit app...'
exec streamlit run app.py
