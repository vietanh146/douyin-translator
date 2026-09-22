@echo off
title Douyin Translator

cd /d "%~dp0"

call ".venv\Scripts\activate.bat"

if errorlevel 1 (
    echo.
    echo [ERROR] Khong the activate .venv
    echo.
    pause
    exit /b
)

:MENU

cls

echo.
echo ============================================================
echo                    DOUYIN TRANSLATOR
echo ============================================================
echo.
echo     1. Dich video moi
echo     2. Render lai subtitle
echo     3. Thoat
echo.
echo ------------------------------------------------------------
set /p CHOICE="    Lua chon: "

if "%CHOICE%"=="1" goto TRANSLATE
if "%CHOICE%"=="2" goto RENDER
if "%CHOICE%"=="3" goto EXIT

echo.
echo [!] Lua chon khong hop le.
pause
goto MENU


:TRANSLATE

cls

echo.
echo ============================================================
echo                     DICH VIDEO MOI
echo ============================================================
echo.
echo Keo video vao cua so nay, sau do nhan ENTER.
echo.
echo Vi du:
echo D:\Videos\douyin.mp4
echo.

set "VIDEO="

set /p VIDEO="Video: "

if "%VIDEO%"=="" (
    echo.
    echo [!] Chua nhap video.
    pause
    goto MENU
)

python main.py %VIDEO%

echo.
echo ============================================================
echo                  DA HOAN THANH
echo ============================================================
echo.

pause
goto MENU


:RENDER

cls

echo.
echo ============================================================
echo                    RENDER LAI SUBTITLE
echo ============================================================
echo.
echo Keo VIDEO GOC vao cua so nay, sau do nhan ENTER.
echo.
echo Luu y:
echo - Khong chay lai OCR
echo - Khong chay lai Gemini
echo - Su dung subtitle da sua trong output/drawtext
echo.

set "VIDEO="

set /p VIDEO="Video: "

if "%VIDEO%"=="" (
    echo.
    echo [!] Chua nhap video.
    pause
    goto MENU
)

python main.py %VIDEO% --render

echo.
echo ============================================================
echo                  DA RENDER XONG
echo ============================================================
echo.

pause
goto MENU


:EXIT

cls

echo.
echo Cam on Vanh da su dung Douyin Translator :v
echo.

timeout /t 2 >nul

exit /b