# 易思培训助手 - 上传到奶牛快传
# 使用方法：右键点击此文件 → 使用 PowerShell 运行

$ZipFile = "C:\Users\Administrator\.openclaw\workspace\yisi_helper.zip"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  上传到奶牛快传 (cowtransfer.com)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查文件
if (-not (Test-Path $ZipFile)) {
    Write-Host "错误：找不到文件 $ZipFile" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "准备上传的文件：" -ForegroundColor Yellow
Write-Host "  $ZipFile" -ForegroundColor White
Write-Host ""

# 打开奶牛快传
Write-Host "正在打开奶牛快传网站..." -ForegroundColor Cyan
Write-Host "请按以下步骤操作：" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 在浏览器中点击 '添加文件'" -ForegroundColor White
Write-Host "2. 选择文件：$ZipFile" -ForegroundColor White
Write-Host "3. 等待上传完成" -ForegroundColor White
Write-Host "4. 复制分享链接" -ForegroundColor White
Write-Host "5. 把链接发给我" -ForegroundColor White
Write-Host ""

Start-Process "https://cowtransfer.com"

Write-Host "========================================" -ForegroundColor Green
Write-Host "  浏览器已打开！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 同时打开文件夹
Start-Process explorer.exe -ArgumentList "/select,$ZipFile"

Read-Host "按回车键退出"
