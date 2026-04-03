# Self-Improving Agent 定时任务设置
# 在PowerShell中运行: powershell -ExecutionPolicy Bypass -File setup_agent_task.ps1

$action = New-ScheduledTaskAction -Execute "C:\Python312\python.exe" -Argument "C:\Users\Administrator\.openclaw\workspace\self_improving_agent.py"

# 每30分钟运行一次
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Days 365)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings

Register-ScheduledTask -TaskName "SelfImprovingAgent_StockMonitor" -InputObject $task -Force

Write-Host ""
Write-Host "=============================================="
Write-Host " Self-Improving Agent 定时任务已创建！"
Write-Host "=============================================="
Write-Host ""
Write-Host "任务名称: SelfImprovingAgent_StockMonitor"
Write-Host "运行频率: 每30分钟"
Write-Host "监控股票: 佳缘科技(301117)、招标股份(301136)"
Write-Host ""
Write-Host "功能:"
Write-Host "  - 自动获取股票数据"
Write-Host "  - 智能分析资金流向"
Write-Host "  - 自动生成报告"
Write-Host "  - 自我学习优化策略"
Write-Host ""
Write-Host "输出文件:"
Write-Host "  - agent_report_YYYYMMDD_HHMMSS.html"
Write-Host "  - StockMonitorAgent_log.txt"
Write-Host "  - StockMonitorAgent_memory.json"
Write-Host ""
Write-Host "查看任务: Get-ScheduledTask -TaskName 'SelfImprovingAgent*'"
Write-Host "删除任务: Unregister-ScheduledTask -TaskName 'SelfImprovingAgent_StockMonitor' -Confirm:`$false"
Write-Host "=============================================="
