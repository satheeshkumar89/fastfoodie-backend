#!/bin/bash

# FastFoodie Backend - Quick Start Script

echo "=================================="
echo "FastFoodie Backend - Quick Start"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your actual credentials!"
    echo ""
fi

# Ask if user wants to run migrations
read -p "Do you want to run database migrations? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running migrations..."
    python migrate.py
fi

echo ""
echo "=================================="
echo "Starting FastAPI server..."
echo "=================================="
echo ""
echo "API will be available at:"
echo "  - http://localhost:8000"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
