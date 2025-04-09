#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e


./wait-for-it.sh db:3306 -- echo "DB is up"

echo "Running database migrations..."
flask db upgrade

echo "Seeding test data..."
python seed.py

echo "Starting the app with Gunicorn..."
gunicorn wsgi:app --workers=4 --bind=0.0.0.0:8000
