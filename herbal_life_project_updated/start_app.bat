@echo off
echo Herbal Life - Ayurvedic Wellness Platform
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment. Please make sure Python is installed.
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
python -m pip install flask flask-login flask-sqlalchemy flask-wtf email-validator
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

REM Run the application
echo Starting the application...
python run.py
if errorlevel 1 (
    echo Application exited with an error.
    pause
    exit /b 1
)

pause