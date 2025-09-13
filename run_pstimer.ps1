# PSTimer launcher for virtual environment with Tcl/Tk fix
# Activates virtual environment and sets Tcl/Tk environment variables

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

Write-Host "Setting Tcl/Tk environment variables..." -ForegroundColor Green
$env:TCL_LIBRARY = "C:/msys64/ucrt64/lib/tcl8.6"
$env:TK_LIBRARY = "C:/msys64/ucrt64/lib/tk8.6"

Write-Host "Testing Tkinter..." -ForegroundColor Green
try {
    & python -c "import tkinter as tk; print('Tkinter test passed'); tk.Tk().destroy()"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Launching PSTimer with virtual environment..." -ForegroundColor Green
        & python main.py
    } else {
        throw "Tkinter test failed"
    }
} catch {
    Write-Host "Tkinter test failed, trying with system Python..." -ForegroundColor Yellow
    deactivate
    & python main.py
}
