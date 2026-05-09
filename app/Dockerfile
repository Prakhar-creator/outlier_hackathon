FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update \
    && apt-get install -y git unzip \
    && rm -rf /var/lib/apt/lists/*

# Create directories expected by validation.sh
RUN mkdir -p /app /eval_assets

# Set working directory
WORKDIR /app

# Copy validation helper scripts ONLY
COPY run.sh parsing.py validation.sh ./

# Make scripts executable
RUN chmod +x run.sh validation.sh

# Keep container alive for docker exec steps
CMD ["tail", "-f", "/dev/null"]