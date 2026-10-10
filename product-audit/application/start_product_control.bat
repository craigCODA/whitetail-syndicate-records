@echo off
cd /d "%~dp0"
start "Whitetail Product Control Server" cmd /k "py -m http.server 4173"
timeout /t 2 /nobreak >nul
start "" "http://localhost:4173"
