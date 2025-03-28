@echo off
setlocal enabledelayedexpansion
set BACKEND_URL=http://localhost:8000
set CAMERA_ID=1001
set AREA="Sentosa"

echo Testing Controller Service API health and availability!!

echo.
echo ===== Checking service health =====
echo.

curl http://localhost:8000/healthz
echo.

echo.
echo ===== Test controller calls =====

echo.
echo 1. get_all_data
curl -X GET "%BACKEND_URL%/get_all_data"
echo.

echo.
echo 2. Test get_camera_data_by_sensor for %CAMERA%
curl -X GET "%BACKEND_URL%/get_camera_data_by_sensor?camera_id=%CAMERA_ID%"
echo.

echo.
echo 3. Test get_traffic_data_by_sensor for %CAMERA_ID%
curl -X GET "%BACKEND_URL%/get_traffic_data_by_sensor?camera_id=%CAMERA_ID%"
echo.

echo.
echo 4. Test get_live_traffic_updates
curl -X GET "%BACKEND_URL%/get_live_traffic_updates"
echo.

echo.
echo ===== Test recommendations =====

echo.
echo 1. Test get_recommendations
curl -X POST "%BACKEND_URL%/get_recommendations?area=%AREA%"
echo.

echo.
echo ===== All tests completed! =====
echo.
pause
