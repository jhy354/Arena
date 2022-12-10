:: Build Project by Pyinstaller
:: Windows

@echo off

pyinstaller --icon=logo.ico -w main.py

md .\dist\main\assets
xcopy .\assets .\dist\main\assets /e /Y

cd dist
cd main

del /f /s /q libcrypto-1_1.dll
del /f /s /q ucrtbase.dll
del /f /s /q unicodedata.pyd
del /f /s /q libssl-1_1.dll
del /f /s /q libwebp-7.dll
del /f /s /q libFLAC-8.dll
del /f /s /q libtiff-5.dll
del /f /s /q libmpg123-0.dll
del /f /s /q _decimal.pyd
del /f /s /q _hashlib.pyd
del /f /s /q _ssl.pyd
del /f /s /q api-ms-win-core-console-l1-1-0.dll
del /f /s /q api-ms-win-core-datetime-l1-1-0.dll
del /f /s /q api-ms-win-core-debug-l1-1-0.dll
del /f /s /q api-ms-win-core-errorhandling-l1-1-0.dll
del /f /s /q api-ms-win-core-file-l1-1-0.dll
del /f /s /q api-ms-win-core-file-l1-2-0.dll
del /f /s /q api-ms-win-core-file-l2-1-0.dll
del /f /s /q api-ms-win-core-handle-l1-1-0.dll
del /f /s /q api-ms-win-core-heap-l1-1-0.dll
del /f /s /q api-ms-win-core-interlocked-l1-1-0.dll
del /f /s /q api-ms-win-core-localization-l1-2-0.dll
del /f /s /q api-ms-win-core-libraryloader-l1-1-0.dll
del /f /s /q api-ms-win-core-memory-l1-1-0.dll
del /f /s /q api-ms-win-core-namedpipe-l1-1-0.dll
del /f /s /q api-ms-win-core-processenvironment-l1-1-0.dll
del /f /s /q api-ms-win-core-processthreads-l1-1-0.dll
del /f /s /q api-ms-win-core-processthreads-l1-1-1.dll
del /f /s /q api-ms-win-core-profile-l1-1-0.dll
del /f /s /q api-ms-win-core-rtlsupport-l1-1-0.dll
del /f /s /q api-ms-win-core-string-l1-1-0.dll
del /f /s /q api-ms-win-core-synch-l1-1-0.dll
del /f /s /q api-ms-win-core-synch-l1-2-0.dll
del /f /s /q api-ms-win-core-sysinfo-l1-1-0.dll
del /f /s /q api-ms-win-core-timezone-l1-1-0.dll
del /f /s /q api-ms-win-core-util-l1-1-0.dll
del /f /s /q api-ms-win-crt-convert-l1-1-0.dll
del /f /s /q api-ms-win-crt-conio-l1-1-0.dll
del /f /s /q api-ms-win-crt-environment-l1-1-0.dll
del /f /s /q api-ms-win-crt-filesystem-l1-1-0.dll
del /f /s /q api-ms-win-crt-heap-l1-1-0.dll
del /f /s /q api-ms-win-crt-locale-l1-1-0.dll
del /f /s /q api-ms-win-crt-math-l1-1-0.dll
del /f /s /q api-ms-win-crt-process-l1-1-0.dll
del /f /s /q api-ms-win-crt-runtime-l1-1-0.dll
del /f /s /q api-ms-win-crt-stdio-l1-1-0.dll
del /f /s /q api-ms-win-crt-string-l1-1-0.dll
del /f /s /q api-ms-win-crt-time-l1-1-0.dll
del /f /s /q api-ms-win-crt-utility-l1-1-0.dll

echo ---------------------------------------------
echo Build Arena.exe Successfully
echo ./dist/main/Arena.exe
echo ---------------------------------------------

rename main.exe Arena.exe
cd ..
rename main Arena

pause
