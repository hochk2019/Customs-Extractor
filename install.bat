@echo off
SETLOCAL EnableDelayedExpansion
chcp 65001 >nul
cls

echo.
echo ===============================================================================
echo           CUSTOMS EXTRACTOR - CAI DAT TU DONG
echo ===============================================================================
echo.
echo Script nay se tu dong cai dat Python va cac thu vien can thiet.
echo Vui long doi trong vai phut...
echo.
echo ===============================================================================
echo.

REM ============================================================================
REM BUOC 1: Kiem tra Python
REM ============================================================================
echo [Buoc 1/4] Kiem tra Python...
echo.

python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python da duoc cai dat!
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo     Phien ban: !PYTHON_VER!
    echo.
    goto INSTALL_PACKAGES
) else (
    echo [!] Python chua duoc cai dat tren may nay.
    echo.
    echo -------------------------------------------------------------------------------
    echo  DE CAI DAT PYTHON:
    echo -------------------------------------------------------------------------------
    echo  1. Mo trinh duyet web
    echo  2. Truy cap: https://www.python.org/downloads/
    echo  3. Tai "Python 3.11" hoac moi hon (file .exe)
    echo  4. Chay file da tai
    echo  5. QUAN TRONG: Tick vao o "Add Python to PATH"
    echo  6. Nhan "Install Now"
    echo  7. Sau khi cai xong, chay lai file install.bat nay
    echo -------------------------------------------------------------------------------
    echo.
    echo Nhan phim bat ky de mo trang download Python...
    pause >nul
    
    REM Mo browser den trang download Python
    start https://www.python.org/downloads/
    
    echo.
    echo Da mo trang download. Sau khi cai Python xong, chay lai file nay.
    echo.
    pause
    exit /b 1
)

:INSTALL_PACKAGES
REM ============================================================================
REM BUOC 2: Nang cap pip
REM ============================================================================
echo [Buoc 2/4] Nang cap pip...
echo.
python -m pip install --upgrade pip --quiet --disable-pip-version-check
if %ERRORLEVEL% EQU 0 (
    echo [OK] Pip da duoc nang cap
) else (
    echo [!] Khong the nang cap pip, nhung van tiep tuc...
)
echo.

REM ============================================================================
REM BUOC 3: Cai dat cac thu vien
REM ============================================================================
echo [Buoc 3/4] Cai dat cac thu vien can thiet...
echo.
echo     - customtkinter (giao dien GUI)
echo     - openpyxl (doc/ghi Excel)
echo     - pillow (xu ly hinh anh)
echo     - tkinterdnd2 (keo tha file)
echo.
echo Dang cai dat... Vui long doi...
echo.

python -m pip install customtkinter openpyxl pillow tkinterdnd2 --quiet --disable-pip-version-check
if %ERRORLEVEL% EQU 0 (
    echo [OK] Tat ca cac thu vien da duoc cai dat thanh cong!
) else (
    echo [X] Co loi khi cai dat. Vui long kiem tra ket noi Internet.
    echo.
    pause
    exit /b 1
)
echo.

REM ============================================================================
REM BUOC 4: Kiem tra cai dat
REM ============================================================================
echo [Buoc 4/4] Kiem tra cai dat...
echo.

python -c "import customtkinter" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] customtkinter
) else (
    echo [X] customtkinter - THAT BAI
    set HAS_ERROR=1
)

python -c "import openpyxl" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] openpyxl
) else (
    echo [X] openpyxl - THAT BAI
    set HAS_ERROR=1
)

python -c "import PIL" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] pillow
) else (
    echo [X] pillow - THAT BAI
    set HAS_ERROR=1
)

python -c "import tkinterdnd2" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] tkinterdnd2
) else (
    echo [X] tkinterdnd2 - THAT BAI
    set HAS_ERROR=1
)

echo.

if defined HAS_ERROR (
    echo ===============================================================================
    echo                        CO LOI XAY RA!
    echo ===============================================================================
    echo.
    echo Mot so thu vien khong duoc cai dat thanh cong.
    echo Vui long kiem tra ket noi Internet va thu lai.
    echo.
    pause
    exit /b 1
)

REM ============================================================================
REM HOAN THANH
REM ============================================================================
echo ===============================================================================
echo                    CAI DAT HOAN THANH!
echo ===============================================================================
echo.
echo Ban da cai dat thanh cong ung dung Customs Extractor!
echo.
echo DE CHAY UNG DUNG:
echo   - Double-click file "run_app.bat"
echo   - Hoac chay lenh: python customs_extractor_gui.py
echo.
echo ===============================================================================
echo.
echo Nhan phim bat ky de dong cua so nay...
pause >nul

exit /b 0
