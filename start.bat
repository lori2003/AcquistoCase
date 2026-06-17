@echo off
REM ============================================================
REM  AcquistoCase - avvio con un solo doppio clic (Windows)
REM  Avvia il backend FastAPI e il frontend Next.js in due
REM  finestre separate, poi apre il browser sull'app.
REM
REM  Prerequisiti (da installare una sola volta):
REM    - Python 3.11+   ->  https://www.python.org/downloads/
REM    - Node.js 20+    ->  https://nodejs.org/
REM  La prima esecuzione installa le dipendenze (puo' essere lenta).
REM ============================================================

setlocal
cd /d "%~dp0"

echo.
echo === AcquistoCase ===
echo Cartella progetto: %CD%
echo.

REM ---------- Controllo prerequisiti ----------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERRORE] Python non trovato nel PATH. Installa Python 3.11+ da https://www.python.org/downloads/
    echo          Durante l'installazione spunta "Add Python to PATH".
    pause
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo [ERRORE] Node.js/npm non trovato nel PATH. Installa Node.js 20+ da https://nodejs.org/
    pause
    exit /b 1
)

REM ---------- Setup backend ----------
echo [1/4] Preparazione backend...
if not exist "backend\.venv" (
    echo     Creo l'ambiente virtuale Python...
    python -m venv "backend\.venv"
    echo     Installo le dipendenze backend...
    call "backend\.venv\Scripts\python.exe" -m pip install --upgrade pip
    call "backend\.venv\Scripts\python.exe" -m pip install -e "backend"
) else (
    echo     Ambiente virtuale gia' presente.
)

REM ---------- Setup frontend ----------
echo [2/4] Preparazione frontend...
if not exist "frontend\node_modules" (
    echo     Installo le dipendenze frontend ^(npm install^)...
    pushd "frontend"
    call npm install
    popd
) else (
    echo     Dipendenze frontend gia' presenti.
)

REM ---------- Avvio backend ----------
echo [3/4] Avvio backend su http://localhost:8000 ...
start "AcquistoCase - Backend" /D "%CD%\backend" cmd /k ".venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM ---------- Avvio frontend ----------
echo [4/4] Avvio frontend su http://localhost:3000 ...
start "AcquistoCase - Frontend" /D "%CD%\frontend" cmd /k "set NEXT_PUBLIC_API_URL=http://localhost:8000&& npm run dev"

REM ---------- Apri il browser ----------
echo.
echo Attendo l'avvio dei server...
timeout /t 8 /nobreak >nul
start "" http://localhost:3000

echo.
echo === Tutto avviato! ===
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000  (health: /api/health)
echo.
echo Per fermare l'app chiudi le due finestre "Backend" e "Frontend".
echo.
endlocal
