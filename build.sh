#!/usr/bin/env bash
# Build script for Render deployment
# This script runs during the build phase on Render

set -o errexit  # Exit on error

echo "Building application..."

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed successfully!"
