FROM python:3.12-alpine

WORKDIR /app

# Install git and other dependencies
RUN apk add --no-cache git

# Copy application files
COPY metrics_cli.py .
COPY complexity.py .
COPY analyzer.py .
COPY report.py .
COPY charts.py .

# Install Python dependencies
RUN pip install --no-cache-dir matplotlib

# Make the script executable
RUN chmod +x metrics_cli.py

# Default command
CMD ["python", "metrics_cli.py", "--help"]
