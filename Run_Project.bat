@echo off
setlocal enabledelayedexpansion
title Telecom Customer Churn Prediction - Launcher
color 0A

REM ============================================================
REM  Telecom Customer Churn Prediction - One-Click Launcher
REM  Automates: dependency check, venv, install, DB, model,
REM             server start and browser launch.
REM ============================================================

cd /d "%~dp0"

set "PYTHON_CMD="
set "VENV_DIR=.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "PORT=5000"
set "URL=http://127.0.0.1:%PORT%/"

echo.
echo ======================================================
echo    Telecom Customer Churn Prediction
echo    Starting setup and launch...
echo ======================================================
echo.

REM ---------- 1. Locate Python ----------
echo [1/6] Checking for Python...
for %%P in (python py) do (
    where %%P >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=%%P"
        goto :found_python
    )
)
echo [!] ERROR: Python not found. Please install Python 3.10+ and add it to PATH.
pause
exit /b 1
:found_python
for /f "delims=" %%V in ('%PYTHON_CMD% --version 2^>^&1') do set "PY_VERSION=%%V"
echo     Found %PY_VERSION%
echo.

REM ---------- 2. Create Virtual Environment if missing ----------
echo [2/6] Checking virtual environment...
if not exist "%VENV_PYTHON%" (
    echo     Creating virtual environment...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [!] ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo     Virtual environment already exists.
)
echo.

REM ---------- 3. Install / Verify Dependencies ----------
echo [3/6] Checking dependencies...
"%VENV_PYTHON%" -c "import flask, numpy, pandas, sklearn, xgboost, lightgbm, catboost" >nul 2>&1
if errorlevel 1 (
    echo     Installing dependencies from requirements.txt...
    "%VENV_PYTHON%" -m pip install --upgrade pip >nul 2>&1
    "%VENV_PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [!] ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
    echo     Dependencies installed successfully.
) else (
    echo     Dependencies already installed.
)
echo.

REM ---------- 4. Ensure .env exists ----------
echo [4/6] Checking environment configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy /y ".env.example" ".env" >nul
        echo     Created .env from .env.example.
    ) else (
        echo     No .env.example found, generating .env with a random key...
        for /f "delims=" %%K in ('"%VENV_PYTHON%" -c "import secrets; print(secrets.token_hex(32))"') do set "RANDOM_KEY=%%K"
        (
            echo SECRET_KEY=!RANDOM_KEY!
            echo FLASK_DEBUG=False
            echo PORT=5000
        )> ".env"
    )
) else (
    echo     .env already present.
)
echo.

REM ---------- 5. Ensure Database exists ----------
echo [5/6] Checking database...
if not exist "users.db" (
    if exist "database_setup.py" (
        echo     Initializing database and default users...
        "%VENV_PYTHON%" database_setup.py
        if errorlevel 1 (
            echo     [WARN] database_setup.py failed; will rely on app auto-init.
        )
    )
)
echo.

REM ---------- 6. Check Model & Start Server ----------
echo [6/6] Starting the Flask server...
if not exist "churn_prediction_model.pkl" (
    echo [!] WARNING: Model file 'churn_prediction_model.pkl' not found.
    echo     The app will start but predictions will be unavailable.
    echo     Please run the Jupyter notebook to regenerate the model.
    echo.
)

REM ---------- 6b. Check if server is already running ----------
netstat -ano | findstr ":5000 " | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo     Port 5000 is already in use - the app may already be running.
    echo     Opening web browser to the existing instance.
    start "" "%URL%"
    echo.
    echo You can close this window.
    pause
    exit /b 0
)

echo.
echo Starting server at %URL%
echo Keep this window open. Press CTRL+C to stop the server.
echo.
echo Opening web browser...
start "" "%URL%"

REM Start the Flask development/server.
"%VENV_PYTHON%" app.py

echo.
echo Server stopped.
pause
exit /b 0
