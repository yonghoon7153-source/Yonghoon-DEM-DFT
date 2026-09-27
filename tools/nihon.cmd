@echo off
setlocal EnableExtensions
rem nihon.cmd - run nihon inside WSL from PowerShell / cmd / Windows Terminal.
rem Put this file somewhere on the Windows PATH; it runs a login shell so ~/.local/bin is on PATH.
rem   nihon          start the dev server and open the browser
rem   nihon doctor   check the environment
rem Set NIHON_WSL_DISTRO to pick a distribution when you have more than one.

where wsl.exe >nul 2>&1
if errorlevel 1 (
  echo [nihon] WSL is not installed. Open PowerShell as administrator and run: wsl --install
  exit /b 1
)
set "NIHON_ARGS=%*"
if defined NIHON_WSL_DISTRO (
  wsl.exe -d "%NIHON_WSL_DISTRO%" -- bash -lc "nihon %NIHON_ARGS%"
) else (
  wsl.exe -- bash -lc "nihon %NIHON_ARGS%"
)
exit /b %errorlevel%
