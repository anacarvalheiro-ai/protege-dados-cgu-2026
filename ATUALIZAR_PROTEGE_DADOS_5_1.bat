@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Atualizador Protege.Dados 5.1
echo.
echo ========================================================
echo   ATUALIZADOR PROFISSIONAL - PROTEGE.DADOS 5.1
echo ========================================================
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale Python 3.11 ou superior.
  pause
  exit /b 1
)
python "%~dp0atualizar_protege_dados_5_1.py"
if errorlevel 1 (
  echo.
  echo A ATUALIZACAO FOI INTERROMPIDA. LEIA A MENSAGEM ACIMA.
  pause
  exit /b 1
)
echo.
pause
exit /b 0
