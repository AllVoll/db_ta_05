#entrypoint.sh

#!/bin/bash

# Update alembic.ini with database connection details
sed -i "s/sqlalchemy.url = .*/sqlalchemy.url = postgresql:\/\/av:password@timescale:5432\/av/" /usr/src/app/alembic.ini

# Create migrations directory
mkdir -p /app/migrations

# Initialize alembic
alembic init /usr/src/app/alembic

# Create migration for api_keys table
alembic revision -m "Create api_keys table"

# Edit the migration file
migration_file=$(ls /usr/src/app/alembic/versions/*_create_api_keys_table.py)
sed -i "s/def upgrade():/def upgrade():\n    # Add migration code here\n    pass/" $migration_file

# Apply the migration
alembic upgrade head


# Start the server
#python /usr/src/app/main.py