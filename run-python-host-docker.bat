@echo off
REM Main Docker launcher for Python Django SQLi Lab with Host MySQL
REM This script can be called from the main sqli directory

cd /d "%~dp0python"
call docker-host-lab.bat %*
