# Use Python 3.10 as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000
EXPOSE 8501

# Create a startup script
RUN echo '#!/bin/bash\n\
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &\n\
python -m streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]
