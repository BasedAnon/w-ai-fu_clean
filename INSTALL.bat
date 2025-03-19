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

REM Install PyAudio automatically by downloading the appropriate wheel file
echo Installing PyAudio...
mkdir install\temp 2>nul

REM Detect Python version and architecture to determine correct wheel file
%PYTHON_COMMAND% -c "import sys; open('install/temp/pyver.txt', 'w').write('{}{}{}'.format(sys.version_info.major, sys.version_info.minor, '64' if sys.maxsize > 2**32 else '32'))"

set /p PYVERSION=<install\temp\pyver.txt
echo Detected Python version: %PYVERSION%

REM Define wheel URLs for different Python versions (3.9 only for now)
set PYAUDIO_WHEEL_URL=
if "%PYVERSION%"=="3964" (
    set PYAUDIO_WHEEL_URL=https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win_amd64.whl
    echo Matched Python 3.9 64-bit
)
if "%PYVERSION%"=="3932" (
    set PYAUDIO_WHEEL_URL=https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win32.whl
    echo Matched Python 3.9 32-bit
)

REM Download and install PyAudio wheel if a URL was found
if not "%PYAUDIO_WHEEL_URL%"=="" (
    echo Downloading PyAudio wheel from %PYAUDIO_WHEEL_URL%...
    powershell -Command "Invoke-WebRequest -Uri '%PYAUDIO_WHEEL_URL%' -OutFile 'install\temp\pyaudio.whl'"
    
    if exist "install\temp\pyaudio.whl" (
        echo Installing PyAudio wheel...
        %PYTHON_COMMAND% -m pip install install\temp\pyaudio.whl
        
        if %ERRORLEVEL% EQU 0 (
            echo PyAudio installed successfully.
        ) else (
            echo PyAudio installation failed. Voice input will be disabled.
            echo You may need to install Microsoft Visual C++ Build Tools.
        )
    ) else (
        echo Failed to download PyAudio wheel. Voice input will be disabled.
    )
) else (
    echo Could not determine PyAudio wheel URL for your Python version.
    echo Voice input will be disabled.
)

REM Clean up
rmdir /s /q install\temp 2>nul

echo Creating shortcut ...
cscript /nologo install/create_shortcut.vbs

echo Done.
pause
