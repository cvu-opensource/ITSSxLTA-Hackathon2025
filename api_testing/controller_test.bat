@echo off
setlocal enabledelayedexpansion
set BACKEND_URL=http://localhost:8000
set CAMERA_ID=1001
set AREA="Sentosa"

echo Testing Controller Service API health and availability!!

@REM echo.
@REM echo ===== Checking service health =====
@REM echo.

@REM curl http://localhost:8000/healthz
@REM echo.

@REM echo.
@REM echo ===== Test controller calls =====

@REM echo.
@REM echo 1. get_all_data
@REM curl -X GET "%BACKEND_URL%/get_all_data"
@REM echo.

@REM echo.
@REM echo 2. Test get_camera_data_by_sensor for %CAMERA%
@REM curl -X GET "%BACKEND_URL%/get_camera_data_by_sensor?camera_id=%CAMERA_ID%"
@REM echo.

@REM echo.
@REM echo 3. Test get_traffic_data_by_sensor for %CAMERA_ID%
@REM curl -X GET "%BACKEND_URL%/get_traffic_data_by_sensor?camera_id=%CAMERA_ID%"
@REM echo.

@REM echo.
@REM echo 4. Test get_live_traffic_updates
@REM curl -X GET "%BACKEND_URL%/get_live_traffic_updates"
@REM echo.

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
