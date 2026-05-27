FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV HERMES_HOME=/app/data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl git nodejs npm ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Install hermes
RUN pip install --no-cache-dir hermes-agent

# Create data directory
RUN mkdir -p /app/data

# Copy our config
COPY railway/config.yaml /app/data/config.yaml
COPY railway/SOUL.md /app/data/SOUL.md

WORKDIR /app

# Run hermes gateway (Discord bot mode)
CMD ["hermes", "gateway", "run"]
