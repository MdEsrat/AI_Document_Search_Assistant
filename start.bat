@echo off
echo ================================================
echo   AI Document Search Assistant - Quick Start
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your OPENAI_API_KEY
    echo.
    pause
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if MongoDB is running
echo Checking MongoDB connection...
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000); client.server_info(); print('✓ MongoDB is running')" 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  WARNING: MongoDB is not running!
    echo Please start MongoDB before running the application.
    echo.
    pause
)

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start the application, run: python app/main.py
echo Then open http://localhost:8000 in your browser
echo.
echo Press any key to start the application now...
pause >nul

REM Start the application
python app/main.py
