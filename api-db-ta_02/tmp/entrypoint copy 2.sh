#!/bin/bash

# Update alembic.ini with database connection details
sed -i "s/sqlalchemy.url = .*/sqlalchemy.url = postgresql:\/\/av:password@timescale:5432\/av/" /usr/src/app/alembic.ini

# Create migrations directory
mkdir -p /app/migrations

# Initialize alembic
alembic init /usr/src/app/alembic

# Generate initial migration for models.py
alembic revision --autogenerate -m "Initial migration for models.py"

# Apply the migration
alembic upgrade head

# Start the server
python -c "from . import models"

