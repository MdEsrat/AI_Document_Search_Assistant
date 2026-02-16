#!/bin/bash

echo "================================================"
echo "  AI Document Search Assistant - Quick Start"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your OPENAI_API_KEY"
    echo ""
    read -p "Press enter to continue..."
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if MongoDB is running
echo "Checking MongoDB connection..."
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000); client.server_info(); print('✓ MongoDB is running')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  WARNING: MongoDB is not running!"
    echo "Please start MongoDB before running the application."
    echo ""
    read -p "Press enter to continue..."
fi

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "To start the application, run: python app/main.py"
echo "Then open http://localhost:8000 in your browser"
echo ""
read -p "Press enter to start the application now..."

# Start the application
python app/main.py
