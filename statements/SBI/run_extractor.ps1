# SBI Transaction Extractor - PowerShell Script
# This script runs the SBI transaction extractor with organized output

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "   SBI Transaction Extractor - Easy Run" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Set the Python executable path
$pythonExe = Join-Path $scriptDir ".venv\Scripts\python.exe"

# Check if Python environment exists
if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: Python environment not found!" -ForegroundColor Red
    Write-Host "Please make sure the .venv directory exists in $scriptDir" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if statements folder exists
$statementsDir = Join-Path $scriptDir "statements"
if (Test-Path $statementsDir) {
    Write-Host "Found statements folder with PDF files" -ForegroundColor Green
} else {
    Write-Host "WARNING: 'statements' folder not found" -ForegroundColor Yellow
    Write-Host "Will search for PDF files in current directory" -ForegroundColor Yellow
}

# Run the extractor
Write-Host "Running SBI Transaction Extractor..." -ForegroundColor Yellow
Write-Host ""

$extractorScript = Join-Path $scriptDir "sbi_extractor.py"

# Execute the Python script
& $pythonExe $extractorScript $args

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "Process completed. Check the output folder." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
