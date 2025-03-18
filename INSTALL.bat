@echo off
title Installing w-AI-fu v2

echo Installing nodejs dependencies ...
call npm ci --no-audit
call npm fund

echo Installing python dependencies ...
REM Ensure Python 3.9 is used instead of the latest version
python -V
pip -V

REM Try using Python Launcher if available (py command)
SET PYTHON_COMMAND=python
WHERE py >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo Python launcher (py) found, trying to use Python 3.9...
    py -3.9 -V >nul 2>nul
    IF %ERRORLEVEL% EQU 0 (
        SET PYTHON_COMMAND=py -3.9
        echo Python 3.9 found via Python launcher!
        goto install_deps
    )
)

REM Check specific Python 3.9 installations
FOR %%p IN (
    "C:\Python39\python.exe"
    "C:\Program Files\Python39\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe"
) DO (
    IF EXIST %%p (
        SET PYTHON_COMMAND=%%p
        echo Found Python 3.9 at: %%p
        goto install_deps
    )
)

echo WARNING: Python 3.9 not found!
echo This application requires Python 3.9. Please install Python 3.9 from https://www.python.org/downloads/release/python-3913/
echo After installing Python 3.9, run this script again.
echo.
echo Attempting to continue with default Python version, but this may cause errors...

:install_deps
echo Using Python command: %PYTHON_COMMAND%
%PYTHON_COMMAND% -m pip install -r requirements.txt

echo Creating shortcut ...
cscript /nologo install/create_shortcut.vbs

echo Done.
pause
