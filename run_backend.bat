@ECHO OFF
TITLE CONTROLLER
CALL venv\scripts\activate
CD backend
uvicorn controller:app --reload