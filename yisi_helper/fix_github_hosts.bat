@echo off
chcp 65001 >nul
echo ==========================================
echo   GitHub Hosts 自动修复工具
echo ==========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 需要管理员权限！
    echo.
    echo 请右键点击此文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo [1/4] 正在备份原始 hosts 文件...
copy C:\Windows\System32\drivers\etc\hosts C:\Windows\System32\drivers\etc\hosts.backup.%date:~0,4%%date:~5,2%%date:~8,2% >nul 2>&1
echo       备份完成！
echo.

echo [2/4] 正在添加 GitHub 解析记录...
echo. >> C:\Windows\System32\drivers\etc\hosts
echo # === GitHub Hosts Start === >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.4 github.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.4 gist.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.4 api.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.4 raw.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 140.82.114.4 githubusercontent.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.108.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.109.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.110.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.111.153 assets-cdn.github.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.108.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.109.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.110.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo 185.199.111.154 github.githubassets.com >> C:\Windows\System32\drivers\etc\hosts
echo # === GitHub Hosts End === >> C:\Windows\System32\drivers\etc\hosts
echo       添加完成！
echo.

echo [3/4] 正在刷新 DNS 缓存...
ipconfig /flushdns >nul 2>&1
echo       DNS 缓存已刷新！
echo.

echo [4/4] 正在测试连接...
ping -n 1 -w 3000 github.com >nul 2>&1
if %errorLevel% equ 0 (
    echo       GitHub 连接测试成功！
) else (
    echo       连接测试失败，但 hosts 已修改
    echo       可能需要重启浏览器或电脑
)
echo.

echo ==========================================
echo   修复完成！
echo ==========================================
echo.
echo 现在请尝试访问：https://github.com
echo.
echo 如果仍无法访问：
echo   1. 重启浏览器
echo   2. 重启电脑
echo   3. 尝试使用手机热点
echo.
pause
