# PowerShell script to load environment variables from .env file
# Usage: .\load_env.ps1

$envFile = Join-Path $PSScriptRoot ".env"

if (-Not (Test-Path $envFile)) {
    Write-Host "Error: .env file not found" -ForegroundColor Red
    exit 1
}

Write-Host "Loading environment variables from .env..." -ForegroundColor Cyan

Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') {
        return
    }
    
    if ($_ -match '^([^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        
        if ($value) {
            [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
            Write-Host "  OK $key" -ForegroundColor Green
        }
    }
}

Write-Host "Environment variables loaded!" -ForegroundColor Green
