Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName System.Drawing

$img = [System.Drawing.Image]::FromFile('C:\Users\admin\.qclaw\workspace\img_top.jpg')
$ms = New-Object System.IO.MemoryStream
$img.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
$bytes = $ms.ToArray()
$base64 = [Convert]::ToBase64String($bytes)
$prefix = 'data:image/png;base64,'
Write-Host $prefix
[Console]::Out.Write($prefix)
$ms2 = New-Object System.IO.MemoryStream
$writer = New-Object System.IO.StreamWriter($ms2)
$writer.Write($base64)
$writer.Flush()
$bytes2 = $ms2.ToArray()
$base64_short = [Text.Encoding]::ASCII.GetString($bytes2)
Write-Host ('BASE64_LENGTH:' + $base64_short.Length)
$img.Dispose()
$ms.Dispose()
$ms2.Dispose()

# Save to file for web display
$base64 | Out-File -FilePath 'C:\Users\admin\.qclaw\workspace\img_top_b64.txt' -Encoding ascii
$ms_img = New-Object System.IO.MemoryStream
$img2 = [System.Drawing.Image]::FromFile('C:\Users\admin\.qclaw\workspace\img_bottom.jpg')
$img2.Save($ms_img, [System.Drawing.Imaging.ImageFormat]::Png)
$bytes3 = $ms_img.ToArray()
[IO.File]::WriteAllBytes('C:\Users\admin\.qclaw\workspace\img_bottom_b64.txt', [Text.Encoding]::ASCII.GetBytes([Convert]::ToBase64String($bytes3)))
$img2.Dispose()
$ms_img.Dispose()
Write-Host 'Done'
