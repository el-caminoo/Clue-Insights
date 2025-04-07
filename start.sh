#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running database migrations..."
flask db upgrade

echo "Seeding test data..."
python seed.py

echo "Starting the app with Gunicorn..."
exec gunicorn app.wsgi:app --workers=4 --bind=0.0.0.0:8000
