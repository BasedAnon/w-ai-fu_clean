@echo off
title Installing w-AI-fu v2

echo Installing nodejs dependencies ...
call npm ci --no-audit
call npm fund

echo Installing python dependencies ...
REM Try to detect Python 3.9 installation

REM Default to regular python command
set PYTHON_COMMAND=python

REM Try Python 3.9 specifically if installed and in PATH
python -m pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python in PATH
) else (
    echo Python not found in PATH
)

REM Check for common Python 3.9 locations
if exist "C:\Python39\python.exe" (
    set PYTHON_COMMAND=C:\Python39\python.exe
    echo Found Python 3.9 at C:\Python39\python.exe
    goto install_deps
)

if exist "C:\Program Files\Python39\python.exe" (
    set PYTHON_COMMAND="C:\Program Files\Python39\python.exe"
    echo Found Python 3.9 at C:\Program Files\Python39\python.exe
    goto install_deps
)

if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    set PYTHON_COMMAND="%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    echo Found Python 3.9 at %LOCALAPPDATA%\Programs\Python\Python39\python.exe
    goto install_deps
)

echo WARNING: Could not find Python 3.9. Using default Python installation.
echo This application works best with Python 3.9.
echo If you encounter issues, please install Python 3.9 from:
echo https://www.python.org/downloads/release/python-3913/

:install_deps
echo Using Python command: %PYTHON_COMMAND%

REM Install everything except PyAudio first
%PYTHON_COMMAND% -m pip install -r requirements.txt

REM Install PyAudio using pipwin (more reliable on Windows)
echo Installing PyAudio via pipwin (workaround for common installation issues)...
%PYTHON_COMMAND% -m pip install pipwin
%PYTHON_COMMAND% -m pipwin install pyaudio

echo Creating shortcut ...
cscript /nologo install/create_shortcut.vbs

echo Done.
pause
