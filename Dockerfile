# PACLI Dockerfile
# This Dockerfile sets up the backend CLI only.
# Docker support is **not** added for the frontend calendar or email automation.
# To use the calendar frontend and schedule emails, run those scripts locally as described in the README.
# You can schedule and interact with the assistant and email scripts using Windows Task Scheduler or manual commands.

# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and source code
COPY requirements.txt ./
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (can be overridden)
ENV PYTHONUNBUFFERED=1

# Default command to run PACLI
CMD ["python", "main.py"]
