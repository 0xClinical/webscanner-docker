# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Set environment variable
ENV FLASK_APP=app.py

# Expose the port the app runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
