@echo off
chcp 65001 > nul
echo 테스트 포스팅 실행 중...
cd /d "%~dp0"
python -X utf8 main.py test
pause
