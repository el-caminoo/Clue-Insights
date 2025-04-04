# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 5000

# Define environment variable to avoid buffering logs
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "app.py"]
