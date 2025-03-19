@echo off
REM This script ensures that the temp directory for PyAudio installation exists
mkdir "%~dp0\temp" 2>nul
echo Temporary directory created.
