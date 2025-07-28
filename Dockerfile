FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Ollama CLI
RUN curl -L https://ollama.com/download/ollama-cli-linux -o /usr/local/bin/ollama && \
    chmod +x /usr/local/bin/ollama

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports for Streamlit and Ollama
EXPOSE 8501 11434

# Run the entrypoint script
CMD ["/entrypoint.sh"]
