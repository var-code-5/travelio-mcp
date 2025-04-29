#!/bin/bash

echo "Setting up environment..."

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Warning: Not running in a virtual environment."
    echo "It's recommended to create and activate a virtual environment first."
    echo "You can do this with:"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate"
    echo ""
    echo "Continuing anyway in 3 seconds..."
    sleep 3
fi

# Install required packages using uv
echo "Installing required packages with uv..."
uv pip install sqlalchemy[asyncio] asyncpg pydantic pydantic-settings

# # Check for .env file and create if not exists
# if [ ! -f .env ]; then
#     echo "Creating .env file with default database settings..."
#     echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/travel_mcp" > .env
#     echo "Note: You may need to edit the .env file with your actual database credentials."
# fi

echo "Making scripts executable..."
chmod +x scripts/seed_data.py
chmod +x scripts/test_db.py

# Test database connection first
echo "Testing database connection..."
uv run scripts/test_db.py

# Always proceed with seeding (the test script will exit with 0 even if it fails)
echo "Starting database seeding..."
uv run scripts/seed_data.py

echo "Done! Check above for any errors."
