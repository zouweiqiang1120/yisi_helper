# 股票监控定时任务设置脚本
# 在PowerShell中运行: powershell -ExecutionPolicy Bypass -File setup_task.ps1

$action = New-ScheduledTaskAction -Execute "C:\Python312\python.exe" -Argument "C:\Users\Administrator\.openclaw\workspace\auto_monitor.py"

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Days 365)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings

Register-ScheduledTask -TaskName "StockMonitor_佳缘科技" -InputObject $task -Force

Write-Host "定时任务已创建！"
Write-Host "任务名称: StockMonitor_佳缘科技"
Write-Host "运行频率: 每30分钟"
Write-Host "监控股票: 佳缘科技(301117)、招标股份(301136)"
Write-Host ""
Write-Host "查看日志文件: auto_monitor_YYYYMMDD.log"
Write-Host ""
Write-Host "如需删除任务，运行: Unregister-ScheduledTask -TaskName 'StockMonitor_佳缘科技' -Confirm:$false"
