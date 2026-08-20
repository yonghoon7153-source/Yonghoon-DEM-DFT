@echo off
setlocal EnableExtensions
rem ---------------------------------------------------------------------------
rem bml.cmd — run bml inside WSL from PowerShell, cmd, or Windows Terminal.
rem
rem Put this file (or a copy) somewhere on the Windows PATH and you can type
rem `bml` without entering WSL first.  It runs a *login* shell so ~/.bashrc and
rem ~/.profile are read, which is where ~/.local/bin joins PATH.
rem
rem   bml            start the workbench, then open the browser
rem   bml dev        hot reload
rem   bml stop       stop it
rem   bml doctor     check the environment
rem
rem Set BML_WSL_DISTRO to pick a distribution when you have more than one:
rem   setx BML_WSL_DISTRO Ubuntu
rem ---------------------------------------------------------------------------

where wsl.exe >nul 2>&1
if errorlevel 1 (
  echo [bml] WSL이 설치되어 있지 않습니다.  PowerShell을 관리자로 열고: wsl --install
  exit /b 1
)

set "BML_ARGS=%*"

if defined BML_WSL_DISTRO (
  wsl.exe -d "%BML_WSL_DISTRO%" -- bash -lc "bml %BML_ARGS%"
) else (
  wsl.exe -- bash -lc "bml %BML_ARGS%"
)
exit /b %errorlevel%
