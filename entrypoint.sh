#!/bin/bash
set -e

echo '⏳ Waiting for Qdrant to be ready...'
until curl -s http://qdrant:6333/collections > /dev/null; do
    sleep 2
done

echo '✅ Qdrant is ready.'

echo '📂 Listing data_loader directory:'
ls -al data_loader

echo '🚀 Running load_data.py...'
if python3 data_loader/load_data.py; then
    echo "✅ Data loaded successfully."
else
    echo "❌ Failed to load data."
    exit 1
fi

echo '🚀 Starting Streamlit app...'
exec streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true --server.enableCORS=false
