# Hugging Face Spaces Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/uploads data/chroma

# Expose port 7860 (required by Hugging Face Spaces)
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV USE_LOCAL_MODELS=True
ENV MONGO_URI=sqlite:///./data/document_search.db

# Run the application on port 7860 (HF Spaces requirement)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
