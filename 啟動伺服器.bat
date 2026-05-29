@echo off
chcp 65001 >nul 2>&1
title 黃曆通勝
echo.
echo   ╔══════════════════════════════════════╗
echo   ║        黃 曆 通 勝                    ║
echo   ╚══════════════════════════════════════╝
echo.
echo   啟動中...
start http://localhost:8080
echo   瀏覽器已開啟
echo   按 Ctrl+C 停止伺服器
echo.
cd /d "%~dp0"
python -m http.server 8080
pause
