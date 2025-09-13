@echo off
REM PSTimer launcher for virtual environment with Tcl/Tk fix
REM Activates virtual environment and sets Tcl/Tk environment variables

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Setting Tcl/Tk environment variables...
set TCL_LIBRARY=C:\msys64\ucrt64\lib\tcl8.6
set TK_LIBRARY=C:\msys64\ucrt64\lib\tk8.6

echo Testing Tkinter...
python -c "import tkinter as tk; print('Tkinter test passed'); tk.Tk().destroy()" 2>nul
if %errorlevel% neq 0 (
    echo Tkinter test failed, trying with system Python...
    python main.py
) else (
    echo Launching PSTimer with virtual environment...
    python main.py
)

pause
