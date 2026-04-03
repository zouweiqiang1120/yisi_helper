# 易思培训助手 - 自动打包脚本
# 使用方法：右键点击此文件 → 使用 PowerShell 运行

# 设置变量
$ProjectName = "yisi_helper"
$WorkspacePath = "C:\Users\Administrator\.openclaw\workspace"
$ProjectPath = Join-Path $WorkspacePath $ProjectName
$ZipFileName = "$ProjectName.zip"
$OutputPath = Join-Path $WorkspacePath $ZipFileName

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  易思培训助手 - 自动打包工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查项目文件夹是否存在
if (-not (Test-Path $ProjectPath)) {
    Write-Host "错误：找不到项目文件夹 $ProjectPath" -ForegroundColor Red
    Write-Host "请确认工作目录是否正确" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "✓ 找到项目文件夹" -ForegroundColor Green
Write-Host "  位置: $ProjectPath" -ForegroundColor Gray
Write-Host ""

# 如果已存在zip文件，先删除
if (Test-Path $OutputPath) {
    Write-Host "发现旧的压缩包，正在删除..." -ForegroundColor Yellow
    Remove-Item $OutputPath -Force
}

# 压缩文件夹
Write-Host "正在压缩项目文件..." -ForegroundColor Cyan
Write-Host "  这可能需要几分钟，请耐心等待..." -ForegroundColor Gray

try {
    Compress-Archive -Path $ProjectPath -DestinationPath $OutputPath -CompressionLevel Optimal
    Write-Host "✓ 压缩完成！" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ 压缩失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 获取文件信息
$ZipFile = Get-Item $OutputPath
$FileSize = $ZipFile.Length
$FileSizeMB = [math]::Round($FileSize / 1MB, 2)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "文件信息：" -ForegroundColor Yellow
Write-Host "  文件名: $ZipFileName" -ForegroundColor White
Write-Host "  位置: $OutputPath" -ForegroundColor White
Write-Host "  大小: $FileSizeMB MB" -ForegroundColor White
Write-Host ""

# 打开文件夹
Write-Host "正在打开文件夹..." -ForegroundColor Cyan
Start-Process explorer.exe -ArgumentList "/select,$OutputPath"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  下一步操作：" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. 上传文件到网盘" -ForegroundColor Yellow
Write-Host "   推荐: 百度网盘、阿里云盘、奶牛快传" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 或直接使用 FlutLab 构建" -ForegroundColor Yellow
Write-Host "   访问: https://flutlab.io" -ForegroundColor Gray
Write-Host "   上传此zip文件即可构建APK" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# 询问是否复制路径到剪贴板
$CopyPath = Read-Host "是否复制文件路径到剪贴板? (Y/N)"
if ($CopyPath -eq "Y" -or $CopyPath -eq "y") {
    $OutputPath | Set-Clipboard
    Write-Host "✓ 路径已复制到剪贴板" -ForegroundColor Green
}

Write-Host ""
Read-Host "按回车键退出"
