@echo off
title Installing w-AI-fu v2

echo Installing nodejs dependencies ...
call npm ci --no-audit
call npm fund

echo Installing python dependencies ...
REM Find and use Python 3.9 specifically

REM Default to regular python command
set PYTHON_COMMAND=python

REM Check for common Python 3.9 installations
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

REM Check for Python 3.9 via Python Launcher
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3.9 -c "print('Python 3.9 check')" >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_COMMAND=py -3.9
        echo Found Python 3.9 via Python Launcher
        goto install_deps
    )
)

echo WARNING: Could not find Python 3.9 specifically. Using default Python installation.
echo This application works best with Python 3.9. If installation fails, please install Python 3.9.
echo Python 3.9 can be downloaded from: https://www.python.org/downloads/release/python-3913/

:install_deps
echo Using Python command: %PYTHON_COMMAND%

REM Make sure pip is up to date
%PYTHON_COMMAND% -m pip install --upgrade pip

REM Install the required packages
echo Installing core Python packages...
%PYTHON_COMMAND% -m pip install -r requirements.txt

REM Specifically ensure websockets is installed
echo Ensuring websockets package is properly installed...
%PYTHON_COMMAND% -m pip install websockets==10.4 --force-reinstall

REM Install PyAudio using a separate Python script
echo Installing PyAudio...
%PYTHON_COMMAND% install\install_pyaudio.py
if %ERRORLEVEL% NEQ 0 (
    echo PyAudio installation failed. Voice input will be disabled.
    echo You may need to install PyAudio manually.
) else (
    echo Voice input functionality should work correctly.
)

echo Creating shortcut ...
cscript /nologo install/create_shortcut.vbs

echo Done.
pause
