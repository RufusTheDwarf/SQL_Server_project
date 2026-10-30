@echo off
setlocal
title Mission SQL Cinema - Installation
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
set "SETUP_EXIT_CODE=%ERRORLEVEL%"
if not "%SETUP_EXIT_CODE%"=="0" (
    echo.
    echo L'installation a echoue. Lis le message ci-dessus.
) else (
    echo.
    echo Note le PID affiche pour pouvoir arreter Flask plus tard.
    echo Le serveur continue de tourner apres la fermeture de cette fenetre.
)
pause
exit /b %SETUP_EXIT_CODE%
