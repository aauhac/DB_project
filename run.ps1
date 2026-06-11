# Run this in PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
Push-Location $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" -m uv run flet run "$PSScriptRoot\app.py"
Pop-Location
