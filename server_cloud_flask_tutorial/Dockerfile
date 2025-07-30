# Use an official Python 3.10 image
FROM python:3.10-slim

# Set working directory
WORKDIR /usr/src/app

# Copy dependency files first (better layer caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8080 (Cloud Run will set PORT anyway)
EXPOSE 8080

# Run the app with Python (not flask CLI)
CMD ["python", "main.py"]