@echo off
setlocal
title Mission SQL Cinema - Installation
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
set "SETUP_EXIT_CODE=%ERRORLEVEL%"
if not "%SETUP_EXIT_CODE%"=="0" (
    echo.
    echo L'installation a echoue. Lis le message ci-dessus.
    pause
)
exit /b %SETUP_EXIT_CODE%
