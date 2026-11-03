@echo off
rem Opens the Nookery Mods installer window. Needs Python 3.9 or newer (python.org or the Microsoft Store).
cd /d "%~dp0"
where py >nul 2>nul && (py -3 install_mods.py %* & goto :end)
where python >nul 2>nul && (python install_mods.py %* & goto :end)
echo Python 3 was not found. Install it from https://www.python.org/downloads/ and run this again.
pause
:end
