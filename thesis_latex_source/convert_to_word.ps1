[CmdletBinding()]
param(
    [switch]$Open
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetScript = Join-Path (Split-Path -Parent $scriptDir) "scripts\convert_to_word.ps1"

if ($Open) {
    & powershell.exe -ExecutionPolicy Bypass -File $targetScript -Open
} else {
    & powershell.exe -ExecutionPolicy Bypass -File $targetScript
}
