@echo off
title Fully OwO Dashboard — Fully Development
color 0A
cls

echo.
echo  =====================================================
echo   >>  Fully OwO Dashboard  ^|  Fully Development
echo  =====================================================
echo.

:: Check if venv exists, create if not
if not exist "venv\Scripts\python.exe" (
    echo  [..] venv not found - creating with Python 3.11...
    py -3.11 -m venv venv
    if not exist "venv\Scripts\python.exe" (
        echo  [!!] Failed! Make sure Python 3.11 is installed.
        echo  [!!] Download: https://www.python.org/downloads/release/python-3119/
        pause
        exit /b 1
    )
    echo  [OK] venv created with Python 3.11
    echo  [..] Installing requirements...
    venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
    echo  [OK] Requirements installed
) else (
    echo  [OK] venv already exists
)

set PYTHON=venv\Scripts\python.exe

:: Install Flask if missing
echo  [..] Checking Flask...
%PYTHON% -c "import flask" 2>nul
if errorlevel 1 (
    echo  [..] Installing Flask...
    %PYTHON% -m pip install flask --quiet
)
echo  [OK] Flask ready

:: Open browser after 2 second delay
start "" cmd /c "timeout /t 2 >nul && start http://localhost:5000"

:: Start the server
echo.
echo  =====================================================
echo   Dashboard: http://localhost:5000
echo   Close this window to stop the server
echo  =====================================================
echo.

%PYTHON% server.py

echo.
echo  [!] Server stopped.
pause
