@ECHO OFF
TITLE CONTROLLER
ECHO Activating virtual environment...
CALL venv\scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)
CD backend
uvicorn controller:app --reload