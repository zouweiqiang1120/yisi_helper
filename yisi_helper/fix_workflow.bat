@echo off
chcp 65001 >nul
echo ==========================================
echo   GitHub Workflow 修复工具
echo ==========================================
echo.
echo 这个脚本会帮你创建正确的 workflow 文件
echo.

:: 创建 workflow 目录
if not exist ".github\workflows" (
    mkdir ".github\workflows"
    echo [1/3] 创建 .github\workflows 目录
) else (
    echo [1/3] workflow 目录已存在
)

echo.
echo [2/3] 创建 build.yml 文件...

echo name: Build APK> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo on:>> .github\workflows\build.yml
echo   push:>> .github\workflows\build.yml
echo     branches: [ main, master ]>> .github\workflows\build.yml
echo   pull_request:>> .github\workflows\build.yml
echo     branches: [ main, master ]>> .github\workflows\build.yml
echo   workflow_dispatch:>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo jobs:>> .github\workflows\build.yml
echo   build:>> .github\workflows\build.yml
echo     runs-on: ubuntu-latest>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo     steps:>> .github\workflows\build.yml
echo     - name: Checkout code>> .github\workflows\build.yml
echo       uses: actions/checkout@v4>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo     - name: Extract project>> .github\workflows\build.yml
echo       run: ^|>> .github\workflows\build.yml
echo         if [ -f "yisi_helper.zip" ]; then>> .github\workflows\build.yml
echo           echo "Extracting yisi_helper.zip...">> .github\workflows\build.yml
echo           unzip -q yisi_helper.zip ^|^| true>> .github\workflows\build.yml
echo           if [ -d "yisi_helper/yisi_helper" ]; then>> .github\workflows\build.yml
echo             mv yisi_helper/yisi_helper/* yisi_helper/>> .github\workflows\build.yml
echo             rmdir yisi_helper/yisi_helper>> .github\workflows\build.yml
echo           fi>> .github\workflows\build.yml
echo           echo "PROJECT_DIR=yisi_helper" ^>^> $GITHUB_ENV>> .github\workflows\build.yml
echo         elif [ -f "pubspec.yaml" ]; then>> .github\workflows\build.yml
echo           echo "PROJECT_DIR=." ^>^> $GITHUB_ENV>> .github\workflows\build.yml
echo         else>> .github\workflows\build.yml
echo           echo "No project found">> .github\workflows\build.yml
echo           exit 1>> .github\workflows\build.yml
echo         fi>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo     - name: Setup Java>> .github\workflows\build.yml
echo       uses: actions/setup-java@v4>> .github\workflows\build.yml
echo       with:>> .github\workflows\build.yml
echo         distribution: 'temurin'>> .github\workflows\build.yml
echo         java-version: '17'>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo     - name: Setup Flutter>> .github\workflows\build.yml
echo       uses: subosito/flutter-action@v2>> .github\workflows\build.yml
echo       with:>> .github\workflows\build.yml
echo         flutter-version: '3.16.0'>> .github\workflows\build.yml
echo         channel: 'stable'>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo     - name: Build APK>> .github\workflows\build.yml
echo       run: ^|>> .github\workflows\build.yml
echo         cd ${{ env.PROJECT_DIR }}>> .github\workflows\build.yml
echo         flutter pub get>> .github\workflows\build.yml
echo         flutter build apk --release>> .github\workflows\build.yml
echo.>> .github\workflows\build.yml
echo     - name: Upload APK>> .github\workflows\build.yml
echo       uses: actions/upload-artifact@v4>> .github\workflows\build.yml
echo       with:>> .github\workflows\build.yml
echo         name: yisi-helper-apk>> .github\workflows\build.yml
echo         path: ${{ env.PROJECT_DIR }}/build/app/outputs/flutter-apk/app-release.apk>> .github\workflows\build.yml
echo         retention-days: 30>> .github\workflows\build.yml

echo.
echo [3/3] 文件创建完成！
echo.
echo ==========================================
echo   下一步操作：
echo ==========================================
echo.
echo 1. 打开 GitHub Desktop 或 Git 命令行
echo 2. 提交这个 workflow 文件到仓库
echo 3. 推送到 GitHub
echo 4. 在 GitHub 上触发构建
echo.
pause
