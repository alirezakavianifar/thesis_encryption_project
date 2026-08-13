<#
.SYNOPSIS
    Convert main.tex into a styled Microsoft Word (.docx) document.

.DESCRIPTION
    Runs the custom python conversion pipeline inside thesis_latex_source/word-build/:
        1. make_reference.py -> reference.docx (B Lotus, RTL layout, 1.5 line height)
        2. build.py          -> preprocess main.tex, fix XePersian math, run pandoc -> _intermediate.docx
        3. postprocess.py    -> apply RTL w:bidi tags, format table/captions -> thesis.docx & main_updated.docx

.EXAMPLE
    .\convert_to_word.ps1
#>

[CmdletBinding()]
param(
    [switch]$Open
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($scriptDir)) {
    $scriptDir = Get-Location
}
$engineDir = $scriptDir

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    $msg" -ForegroundColor Green }

# Tool checks
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    throw "python is required but was not found on PATH."
}
if (-not (Get-Command "pandoc" -ErrorAction SilentlyContinue)) {
    throw "pandoc is required but was not found on PATH. Install from https://pandoc.org"
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONWARNINGS = "ignore"

function Invoke-Py($script) {
    Write-Step "python $script"
    & python (Join-Path $engineDir $script)
    if ($LASTEXITCODE -ne 0) { throw "$script failed with exit code $LASTEXITCODE." }
}

Push-Location $engineDir
try {
    Invoke-Py "make_reference.py"
    Invoke-Py "build.py"
    Invoke-Py "postprocess.py"
} finally {
    Pop-Location
}

$repoRoot = Split-Path -Parent $scriptDir
$docx = Join-Path $repoRoot "thesis_latex_source\word-build\thesis.docx"
$rootDocx = Join-Path $repoRoot "main_updated.docx"

Write-Step "Done."
if (Test-Path $docx) { Write-Ok "Word output: $docx" }
if (Test-Path $rootDocx) { Write-Ok "Root output: $rootDocx" }

if ($Open -and (Test-Path $docx)) {
    Invoke-Item $docx
}
