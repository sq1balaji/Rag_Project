FROM python:3.12-slim

# Install system dependencies and dos2unix
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . .

# Convert entrypoint.sh to Unix format
RUN dos2unix entrypoint.sh

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entrypoint script (again) and make executable
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

COPY .streamlit /root/.streamlit

# Expose ports for Streamlit and Ollama
EXPOSE 8501 11434

# Run the entrypoint script
CMD ["/entrypoint.sh"]
