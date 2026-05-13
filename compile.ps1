# PowerShell script to compile main.tex and log errors
$ErrorActionPreference = "Continue"

$inputFile = "main.tex"
$logFile = "latest_compilation_log.txt"

Write-Host "`n[1/3] Deep cleaning environment..." -ForegroundColor Cyan
$extensions = @("*.pdf", "*.aux", "*.log", "*.toc", "*.out", "*.synctex.gz")
foreach ($ext in $extensions) {
    if (Test-Path $ext) { try { Remove-Item $ext -Force } catch { } }
}

Write-Host "[2/3] Compiling $inputFile using XeLaTeX (3 Clean Passes)..." -ForegroundColor Cyan

$tempLog = New-TemporaryFile

# Triple pass for maximum stability in TOC and cross-references
for ($i = 1; $i -le 3; $i++) {
    Write-Host "  -> Pass $i..." -ForegroundColor Gray
    xelatex -interaction=nonstopmode $inputFile 2>&1 | Tee-Object -FilePath $tempLog.FullName -Append
}

# Copy temp log to our persistent log file
try {
    Copy-Item -Path $tempLog.FullName -Destination $logFile -Force
} catch {
    Write-Host "Warning: Could not update $logFile." -ForegroundColor Yellow
}
Remove-Item $tempLog.FullName -Force

$pdfGenerated = Test-Path "main.pdf"
if ($pdfGenerated) {
    Write-Host "`n[3/3] Success! Clean main.pdf generated." -ForegroundColor Green
} else {
    Write-Host "`n[3/3] Critical Failure! Check $logFile." -ForegroundColor Red
}
