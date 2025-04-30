# Travelio - Travel Itinerary Planning Assistant

Travelio is an AI-powered travel planning application that helps users create custom travel itineraries. The system consists of a backend MCP (Model-Control-Presentation) server, a database for storing travel information, and client interfaces.

## Prerequisites

- Python 3.13+
- PostgreSQL database
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/var-code-5/travelio-mcp.git
cd travelio
```

### 2. Set up environment variables

Copy the example environment file and update it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` to include:
- `DATABASE_URL` - PostgreSQL connection string
- `GEMINI_API_KEY` - Google Gemini API key for AI capabilities
- `MCP_SERVER_URL` - URL for the MCP server (default: http://localhost:8000)

### 3. Set up Python environment with uv

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using uv
uv pip install -e .
```

## Database Setup

### Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE travel_mcp;

# Exit psql
\q
```

### Initialize and migrate the database

```bash
# Test database connection
python scripts/test_db.py

# Run database migrations
python scripts/migrations.py init
python scripts/migrations.py upgrade head

# Seed the database with initial data
./seed_db.sh
```

## Running the Application

### Start the MCP Server

```bash
# Start the server
python main.py

# The server will be available at http://localhost:8000
```

### Connect the Chatbot Client

```bash
# Run the chatbot CLI interface
python travelio_chatbot.py
```

## Project Structure

- `app/` - Core application code
  - `api/` - API definitions and routes
  - `client/` - Client implementations
  - `core/` - Core functionality and config
  - `db/` - Database models and session management
  - `mcp/` - MCP server implementation
  - `services/` - Business logic services
- `scripts/` - Utility scripts for DB operations
- `tests/` - Test suite
- `alembic/` - Database migration scripts

## Development

### Run tests

```bash
pytest
```

### Create new migrations

After changing database models:

```bash
python scripts/migrations.py migrate -m "Description of changes"
python scripts/migrations.py upgrade head
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `GEMINI_API_KEY` - Google Gemini API for AI capabilities
- `MCP_SERVER_URL` - URL for the MCP server
- `GROQ_API_KEY` - (Optional) Groq API key
- `OPENAI_API_KEY` - (Optional) OpenAI API key
