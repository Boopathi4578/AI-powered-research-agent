@echo off
REM Script to run the Streamlit frontend for AI-Powered Research Agent

echo ================================================
echo AI-Powered Research Agent - Streamlit Frontend
echo ================================================
echo.

REM Check if python virtual environment exists, create if not
if not exist "venv" (
    echo Warning: Python virtual environment not found.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo.

REM Check if streamlit is installed
streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Streamlit is not installed.
    echo Installing Streamlit...
    pip install streamlit>=1.28.0
    echo.
)

REM Check for required environment variables
if "%BEDROCK_MODEL_ID%"=="" (
    echo Warning: BEDROCK_MODEL_ID is not set
    echo Please set the following environment variables:
    echo.
    echo   set BEDROCK_MODEL_ID=your-model-id
    echo   set AWS_REGION=us-east-1
    echo   set AWS_ACCESS_KEY_ID=your-access-key
    echo   set AWS_SECRET_ACCESS_KEY=your-secret-key
    echo.
    echo Or create a .env file with these variables.
    echo.
)

REM Check if .env file exists
if exist .env (
    echo Found .env file
    echo.
)

echo Starting Streamlit app...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run streamlit
streamlit run streamlit_app.py

