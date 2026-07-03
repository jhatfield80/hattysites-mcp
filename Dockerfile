# Hatty.ai MCP Server - Dockerfile
FROM python:3.11-slim

LABEL maintainer="Hatty.ai <hello@hatty.ai>"
LABEL description="Hatty.ai MCP Server for mcp.hattysites.com"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY server/ ./server/
COPY agents/ ./agents/
COPY skills/ ./skills/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create directories for runtime data
RUN mkdir -p credentials logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose MCP server port
EXPOSE 8000

# Default command runs the MCP server
# Use docker-compose to also run the orchestrator
CMD ["python", "server/main.py"]
