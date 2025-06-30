@echo off
title ChatGPT Web Automation Server
color 0A

echo.
echo ========================================
echo    ChatGPT Web Automation Server
echo ========================================
echo.
echo Starting web server...
echo Open your browser and go to:
echo http://localhost:3700
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python start_web_server.py

pause
