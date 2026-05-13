$i=0
Get-Content encryption_chapters/chapter2_debug.tex | ForEach-Object {
    $i++
    if ($i -ge 351 -and $i -le 500) {
        if ($_ -match '^%') {
            $_.Substring(1)
        } else {
            $_
        }
    } else {
        $_
    }
} | Set-Content encryption_chapters/chapter2_debug.temp.tex
Move-Item -Force encryption_chapters/chapter2_debug.temp.tex encryption_chapters/chapter2_debug.tex
