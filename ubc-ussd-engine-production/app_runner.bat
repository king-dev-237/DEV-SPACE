@echo off
setlocal enabledelayedexpansion

set PORT=8080
set LOG_FILE=app.log

echo Starting the application on port %PORT%...
start /b uvicorn main:app --reload --port %PORT% >> %LOG_FILE% 2>&1
for /f "tokens=2 delims=," %%A in ('wmic process call create "uvicorn main:app --reload --port %PORT%"') do set APP_PID=%%A

echo Application started. Logs are being written to %LOG_FILE%.

REM Wait for the application to start
timeout /t 1 /nobreak

REM Check if the application is running by checking the log file
if exist %LOG_FILE% (
    echo Application is running successfully.
) else (
    echo Failed to start the application. Check %LOG_FILE% for details.
)

endlocal
