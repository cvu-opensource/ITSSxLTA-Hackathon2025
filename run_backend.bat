@ECHO OFF
TITLE CONTROLLER
CALL venv\scripts\activate
CD backend
uvicorn controller_test:app --reload