# 黃曆通勝 - 本地伺服器啟動腳本
# 執行後自動開啟瀏覽器

Write-Host ""
Write-Host "  ╔══════════════════════════════════════╗" -ForegroundColor Red
Write-Host "  ║        黃 曆 通 勝                    ║" -ForegroundColor Red
Write-Host "  ╚══════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""
Write-Host "  啟動中..." -ForegroundColor Yellow

$port = 8080
$url = "http://localhost:$port"

Start-Process $url

Write-Host "  瀏覽器已開啟: $url" -ForegroundColor Green
Write-Host "  按 Ctrl+C 停止伺服器" -ForegroundColor Gray
Write-Host ""

Set-Location $PSScriptRoot
python -m http.server $port
