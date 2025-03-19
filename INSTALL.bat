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

REM Install PyAudio using a Python script that downloads the wheel
echo Installing PyAudio...
mkdir install\temp 2>nul

REM Create a Python script to detect version and download/install PyAudio
echo import sys, os, urllib.request, subprocess > install\temp\install_pyaudio.py
echo from urllib.error import URLError >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo def main(): >> install\temp\install_pyaudio.py
echo     arch = "64" if sys.maxsize > 2**32 else "32" >> install\temp\install_pyaudio.py
echo     version = f"{sys.version_info.major}{sys.version_info.minor}" >> install\temp\install_pyaudio.py
echo     print(f"Detected Python {version}{arch}") >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     if version != "39": >> install\temp\install_pyaudio.py
echo         print("PyAudio auto-installation only supports Python 3.9") >> install\temp\install_pyaudio.py
echo         return False >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     wheel_url = "" >> install\temp\install_pyaudio.py
echo     if arch == "64": >> install\temp\install_pyaudio.py
echo         wheel_url = "https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win_amd64.whl" >> install\temp\install_pyaudio.py
echo         wheel_filename = "PyAudio-0.2.11-cp39-cp39-win_amd64.whl" >> install\temp\install_pyaudio.py
echo     else: >> install\temp\install_pyaudio.py
echo         wheel_url = "https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win32.whl" >> install\temp\install_pyaudio.py
echo         wheel_filename = "PyAudio-0.2.11-cp39-cp39-win32.whl" >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     wheel_path = os.path.join("install", "temp", wheel_filename) >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     print(f"Downloading PyAudio wheel from {wheel_url}...") >> install\temp\install_pyaudio.py
echo     try: >> install\temp\install_pyaudio.py
echo         urllib.request.urlretrieve(wheel_url, wheel_path) >> install\temp\install_pyaudio.py
echo     except URLError as e: >> install\temp\install_pyaudio.py
echo         print(f"Error downloading wheel: {e}") >> install\temp\install_pyaudio.py
echo         return False >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     if not os.path.exists(wheel_path): >> install\temp\install_pyaudio.py
echo         print("Failed to download wheel file") >> install\temp\install_pyaudio.py
echo         return False >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     filesize = os.path.getsize(wheel_path) >> install\temp\install_pyaudio.py
echo     if filesize < 1000: # File too small, probably an error >> install\temp\install_pyaudio.py
echo         print(f"Downloaded file is too small ({filesize} bytes). Likely not a valid wheel.") >> install\temp\install_pyaudio.py
echo         return False >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     print(f"Installing PyAudio wheel ({filesize} bytes)...") >> install\temp\install_pyaudio.py
echo     result = subprocess.run([sys.executable, "-m", "pip", "install", wheel_path], capture_output=True, text=True) >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo     if result.returncode != 0: >> install\temp\install_pyaudio.py
echo         print(f"Installation failed with code {result.returncode}") >> install\temp\install_pyaudio.py
echo         print(f"Error: {result.stderr}") >> install\temp\install_pyaudio.py
echo         return False >> install\temp\install_pyaudio.py
echo     else: >> install\temp\install_pyaudio.py
echo         print("PyAudio installed successfully.") >> install\temp\install_pyaudio.py
echo         return True >> install\temp\install_pyaudio.py
echo. >> install\temp\install_pyaudio.py
echo if __name__ == "__main__": >> install\temp\install_pyaudio.py
echo     success = main() >> install\temp\install_pyaudio.py
echo     sys.exit(0 if success else 1) >> install\temp\install_pyaudio.py

REM Run the PyAudio installation script
%PYTHON_COMMAND% install\temp\install_pyaudio.py
if %ERRORLEVEL% NEQ 0 (
    echo PyAudio installation failed. Voice input will be disabled.
    echo You may need to install PyAudio manually.
) else (
    echo Voice input functionality should work correctly.
)

REM Clean up
rmdir /s /q install\temp 2>nul

echo Creating shortcut ...
cscript /nologo install/create_shortcut.vbs

echo Done.
pause
