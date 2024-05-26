@echo off
rem Define the path to the Python script
set PYTHON_SCRIPT=.\compile\compilecmd.py

rem Call the Python script with the forwarded arguments
py "%PYTHON_SCRIPT%" %*
