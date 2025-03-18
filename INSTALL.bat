@echo off
title Installing w-AI-fu v2

echo Installing nodejs dependencies ...
call npm ci --no-audit
call npm fund

echo Installing python dependencies ...
REM Ensure Python 3.9 is used instead of the latest version
python -V
pip -V

REM Set specific Python 3.9 path
set PYTHON_PATH=python3.9
if exist "C:\Python39\python.exe" (
    set PYTHON_PATH=C:\Python39\python.exe
) else if exist "C:\Program Files\Python39\python.exe" (
    set PYTHON_PATH=C:\Program Files\Python39\python.exe
) else if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python39\python.exe
)

echo Using Python path: %PYTHON_PATH%
%PYTHON_PATH% -m pip install -r requirements.txt

echo Creating shortcut ...
cscript /nologo install/create_shortcut.vbs

echo Done.
pause
