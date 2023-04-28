#!/bin/bash

# Update alembic.ini with database connection details
sed -i "s/sqlalchemy.url = .*/sqlalchemy.url = postgresql:\/\/av:password@timescale:5432\/av/" /usr/src/app/alembic.ini

# Create migrations directory
#mkdir -p /app/migrations

# Initialize alembic
alembic init /usr/src/app/alembic

# Check if each table exists in the database
python -c "
from . import models
from sqlalchemy import MetaData
from .database import engine

metadata = MetaData(bind=engine)
metadata.reflect()

for name in models.Base.metadata.tables:
    if not metadata.tables.get(name):
        print(f'Creating table {name}')
        models.Base.metadata.tables[name].create(bind=engine)
"

# Create migration for api_keys table if not exists
alembic revision --autogenerate -m "Initial create"

# Apply any pending migrations
alembic upgrade head

# Start the server
#python /usr/src/app/main.py
