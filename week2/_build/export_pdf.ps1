param(
    [string]$Docx = "..\Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2.docx",
    [string]$Pdf  = "..\Agribusiness_Data_Cleaning_Preprocessing_Strategy_Week2_preview.pdf"
)

$ErrorActionPreference = "Stop"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500

$docxPath = (Resolve-Path $Docx).Path
$pdfPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Pdf))

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($docxPath, $false, $true)
    $doc.Fields.Update() | Out-Null
    foreach ($section in $doc.Sections) {
        foreach ($header in $section.Headers) { $header.Range.Fields.Update() | Out-Null }
        foreach ($footer in $section.Footers) { $footer.Range.Fields.Update() | Out-Null }
    }
    $doc.Repaginate()
    $pages = $doc.ComputeStatistics(2)
    $words = $doc.ComputeStatistics(0)
    $doc.ExportAsFixedFormat($pdfPath, 17)
    Write-Output "pages=$pages words=$words pdf=$pdfPath"
    $doc.Close($false)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
