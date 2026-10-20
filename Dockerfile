FROM python:3.12-slim

# Install ffmpeg and curl for audio extraction and health check verification
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render exposes PORT dynamically (usually 10000)
ENV PORT=10000
EXPOSE 8000 10000

# Shell form expands $PORT variable passed by Render
CMD sh -c "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"
