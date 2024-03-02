# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .


# Expose ports for both Python and Node.js APIs
EXPOSE 5000

# Command to run both APIs (You need to adapt this according to your specific setup)
CMD ["python", "main.py"]

