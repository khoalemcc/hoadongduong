Set-StrictMode -Version Latest
# Allow script execution for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# ---------- Backend ----------
$backendPath = Join-Path $PSScriptRoot "backend2"
Write-Host "Starting backend..." -ForegroundColor Cyan
Start-Process -FilePath "powershell" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command \"cd $backendPath; .\\.venv\\Scripts\\Activate.ps1; pip install -r requirements.txt --quiet; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000\"" -NoNewWindow -PassThru | Out-Null

# ---------- Frontend ----------
$frontendPath = Join-Path $PSScriptRoot "frontend"
Write-Host "Starting frontend..." -ForegroundColor Cyan
Start-Process -FilePath "powershell" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command \"cd $frontendPath; npm ci --silent; npm run dev\"" -NoNewWindow -PassThru | Out-Null

Write-Host "Both services launched. Check the new terminal windows for logs." -ForegroundColor Green
