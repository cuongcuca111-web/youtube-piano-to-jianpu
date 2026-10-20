@echo off
title JianpuPiano AI - YouTube to Jianpu Converter
echo ========================================================
echo   JianpuPiano AI - Khoi dong May Chu Web
echo   Dia chi: http://127.0.0.1:8000
echo ========================================================
cd /d "%~dp0"
start http://127.0.0.1:8000
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
