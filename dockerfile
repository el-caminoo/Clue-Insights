# Use a lightweight official Python image
FROM python:3.14-rc-alpine3.21

RUN apk add --no-cache bash

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

COPY ./start.sh .
COPY ./wait-for-it.sh .

RUN chmod +x *.sh

CMD ["./start.sh"]
