@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale Python 3.11 ou superior.
  pause
  exit /b 1
)
echo.
echo O portal sera aberto em http://localhost:8765/
echo Para encerrar o servidor, pressione CTRL+C nesta janela.
start "" "http://localhost:8765/"
python -m http.server 8765 --bind 127.0.0.1 --directory web
