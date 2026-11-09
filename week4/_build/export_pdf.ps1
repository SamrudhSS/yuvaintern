param(
    [string]$Docx = "$PSScriptRoot\..\Agribusiness_Predictive_Modelling_Framework_Week4.docx",
    [string]$Pdf  = "$PSScriptRoot\..\Agribusiness_Predictive_Modelling_Framework_Week4_preview.pdf"
)
$ErrorActionPreference = "Stop"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500
$docxPath = (Resolve-Path $Docx).Path
$pdfPath  = [System.IO.Path]::GetFullPath($Pdf)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($docxPath, $false, $true)
    $doc.Fields.Update() | Out-Null
    foreach ($s in $doc.Sections) {
        foreach ($h in $s.Headers) { $h.Range.Fields.Update() | Out-Null }
        foreach ($f in $s.Footers) { $f.Range.Fields.Update() | Out-Null }
    }
    $doc.Repaginate()
    $pages = $doc.ComputeStatistics(2)
    $words = $doc.ComputeStatistics(0)
    $doc.ExportAsFixedFormat($pdfPath, 17)
    Write-Output "pages=$pages words=$words pdf=$pdfPath"
    $doc.Close($false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}

