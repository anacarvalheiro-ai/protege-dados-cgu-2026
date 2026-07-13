@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Publicar Protege.Dados 5.1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Publicar_No_GitHub_5_1.ps1"
if errorlevel 1 (
  echo.
  echo A PUBLICACAO FOI INTERROMPIDA.
  pause
  exit /b 1
)
