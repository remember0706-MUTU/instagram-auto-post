@echo off
chcp 65001 > nul
echo 인스타그램 자동 포스팅 스케줄러 시작...
echo 게시 시간: 매일 09:00, 19:00
echo 종료하려면 Ctrl+C를 누르세요.
echo.
cd /d "%~dp0"
python -X utf8 main.py
pause
