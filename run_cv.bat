@ECHO off
ECHO Activating virtual environment...
CALL venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)
CD cv
ECHO Running CV service...
python main.py  REM Run the CV service
PAUSE
