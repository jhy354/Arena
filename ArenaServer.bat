@echo off
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do python server.py --address %%i
pause