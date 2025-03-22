@echo off
setlocal enabledelayedexpansion

:: Define camera ID for testing
set CAMERA_ID=1001

:: Check if the service is running
echo.
echo ===== Checking service health =====
curl http://localhost:8000/healthz

:: Fetch all traffic data
echo.
echo ===== Fetching all traffic data =====
curl -X GET http://localhost:8000/get_all_data

:: Fetch camera data for a specific sensor
echo.
echo ===== Fetching camera data for %CAMERA_ID% =====
curl -X GET "http://localhost:8000/get_camera_data_by_sensor?camera_id=%CAMERA_ID%"

:: Fetch traffic data for a specific sensor
echo.
echo ===== Fetching traffic data for %CAMERA_ID% =====
curl -X GET "http://localhost:8000/get_traffic_data_by_sensor?camera_id=%CAMERA_ID%"

:: Send a traffic update manually
echo.
echo ===== Sending a manual traffic update =====
curl -X POST "http://localhost:8000/save_traffic_flow" -H "Content-Type: application/json" -d "{\"camera_id\": \"%CAMERA_ID%\", \"traffic_flow\": 50}"

:: Send data to the predictive analysis service
echo.
echo ===== Sending data to predictive analysis service =====
curl -X POST "http://localhost:8000/predictive/analyze" -H "Content-Type: application/json" -d "{\"camera_id\": \"%CAMERA_ID%\", \"traffic_flow\": 50}"

echo.
echo ===== All tests completed! =====
pause
