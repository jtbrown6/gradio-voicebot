# Use the official Python image as the base image
FROM --platform=linux/amd64 python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application runs
EXPOSE 8000

# Run the application
CMD ["python3", "spanishtutor.py"]
