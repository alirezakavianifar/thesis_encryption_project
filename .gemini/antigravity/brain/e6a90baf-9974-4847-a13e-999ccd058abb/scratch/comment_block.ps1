$i=0
Get-Content encryption_chapters/chapter2.tex | ForEach-Object {
    $i++
    if ($i -ge 210 -and $i -le 500) {
        '%' + $_
    } else {
        $_
    }
} | Set-Content encryption_chapters/chapter2.tex
