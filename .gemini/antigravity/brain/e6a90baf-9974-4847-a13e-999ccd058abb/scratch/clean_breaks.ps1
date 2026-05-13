Get-ChildItem encryption_chapters/*.tex | ForEach-Object {
    $content = Get-Content $_.FullName
    $content = $content -replace '\\hfill\\break', ''
    $content | Set-Content $_.FullName
}
