# Define the application build stage
FROM python:3.11-slim-bookworm AS build-stage

# Set work directory and environment variables
WORKDIR /SHSPORTAL
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

# Install & upgrade system dependencies
RUN apt-get update \
    && apt-get -y install netcat-openbsd gcc  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the script executable
RUN ["chmod", "+x", "./run.sh"]

# Command to run the application
CMD ["./run.sh"]
