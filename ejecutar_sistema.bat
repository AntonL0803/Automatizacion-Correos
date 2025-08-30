@echo off
echo ============================================
echo    SISTEMA DE CORREOS TAVOLO CASA
echo ============================================
echo.
echo Selecciona una opcion:
echo.
echo 1. Configuracion inicial del sistema
echo 2. Enviar correo de prueba
echo 3. Enviar correos masivos
echo 4. Salir
echo.
set /p choice="Ingresa tu opcion (1-4): "

if "%choice%"=="1" (
    echo.
    echo Iniciando configuracion inicial...
    python setup.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Iniciando envio de correo de prueba...
    python test_email.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo Iniciando envio masivo...
    python email_sender.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo Saliendo del sistema...
    exit
) else (
    echo.
    echo Opcion invalida. Intentalo de nuevo.
    pause
    goto :eof
)

echo.
echo ¿Quieres ejecutar otra opcion?
set /p again="(s/n): "
if /i "%again%"=="s" (
    cls
    "%~f0"
)
