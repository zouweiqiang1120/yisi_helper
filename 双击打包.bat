@echo off
chcp 65001 >nul
title 易思培训助手 - 自动打包工具
echo.
echo ========================================
echo   易思培训助手 - 自动打包工具
echo ========================================
echo.

set "PROJECT_NAME=yisi_helper"
set "WORKSPACE_PATH=C:\Users\Administrator\.openclaw\workspace"
set "PROJECT_PATH=%WORKSPACE_PATH%\%PROJECT_NAME%"
set "ZIP_FILE=%WORKSPACE_PATH%\%PROJECT_NAME%.zip"

echo 正在检查项目文件夹...
if not exist "%PROJECT_PATH%" (
    echo 错误：找不到项目文件夹 %PROJECT_PATH%
    echo 请确认工作目录是否正确
    pause
    exit /b 1
)

echo [OK] 找到项目文件夹
echo   位置: %PROJECT_PATH%
echo.

if exist "%ZIP_FILE%" (
    echo 发现旧的压缩包，正在删除...
    del /f /q "%ZIP_FILE%"
)

echo 正在压缩项目文件...
echo   这可能需要几分钟，请耐心等待...
echo.

powershell -Command "Compress-Archive -Path '%PROJECT_PATH%' -DestinationPath '%ZIP_FILE%' -CompressionLevel Optimal"

if errorlevel 1 (
    echo [错误] 压缩失败！
    pause
    exit /b 1
)

echo [OK] 压缩完成！
echo.

for %%I in ("%ZIP_FILE%") do (
    set "FILE_SIZE=%%~zI"
)

echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 文件信息：
echo   文件名: %PROJECT_NAME%.zip
echo   位置: %ZIP_FILE%
echo   大小: %FILE_SIZE% 字节
echo.

:: 打开文件夹并选中文件
start explorer.exe /select,"%ZIP_FILE%"

echo ========================================
echo   下一步操作：
echo ========================================
echo.
echo 1. 上传文件到网盘
echo    推荐: 百度网盘、阿里云盘、奶牛快传
echo.
echo 2. 或直接使用 FlutLab 构建
echo    访问: https://flutlab.io
echo    上传此zip文件即可构建APK
echo.
echo ========================================
echo.

pause
