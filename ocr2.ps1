Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName System.Runtime.WindowsRuntime
Add-Type -AssemblyName Windows.Storage
Add-Type -AssemblyName Windows.Graphics.Imaging
Add-Type -AssemblyName Windows.Media.Ocr

$null = [Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType=WindowsRuntime]

function Get-OcrText {
    param([string]$imagePath, [string]$lang = 'zh-CN')
    $null = [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
    $null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
    $null = [Windows.Graphics.Imaging.BitmapFactory, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
    $null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
    $null = [System.IO.FileStream, System.IO, ContentType=System]
    
    try {
        $langObj = [Globalization.CultureInfo]::GetCultureInfo($lang)
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($langObj)
        if ($null -eq $engine) {
            $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
            Write-Host "Using user profile language"
        }
        
        $bytes = [System.IO.File]::ReadAllBytes($imagePath)
        $ms = New-Object System.IO.MemoryStream(,$bytes)
        
        $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($ms.AsRandomAccessStream())
        $task = $decoder
        $task.Wait(5000)
        $dec = $task.Result
        
        $bmp = [Windows.Graphics.Imaging.SoftwareBitmap]::ConvertAsync($dec.GetPixelDataAsync().GetResults(), 'Bgra8', 'Premultiplied')
        $task2 = $bmp
        $task2.Wait(5000)
        $sb = $task2.Result
        
        $result = $engine.RecognizeAsync($sb).GetAwaiter().GetResult()
        return $result.Text
    } catch {
        return "Error: $($_.Exception.Message)"
    }
}

$text1 = Get-OcrText 'C:\Users\admin\.qclaw\workspace\img_top.jpg' 'zh-CN'
Write-Host "=== TOP HALF ==="
Write-Host $text1
Write-Host "=== BOTTOM HALF ==="
$text2 = Get-OcrText 'C:\Users\admin\.qclaw\workspace\img_bottom.jpg' 'zh-CN'
Write-Host $text2
