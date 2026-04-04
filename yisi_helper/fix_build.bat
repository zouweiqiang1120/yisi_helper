@echo off
chcp 65001 >nul
echo === 开始修复 Android 构建问题 ===
echo.

:: 检查是否在正确的目录
if not exist "android\build.gradle" (
    echo 错误：请在 yisi_helper 项目根目录运行此脚本
    pause
    exit /b 1
)

echo [1/3] 修复 android\build.gradle...
(
echo allprojects {
echo     repositories {
echo         google^^^(^^^)
echo         mavenCentral^^^(^^^)
echo     }
echo }
echo.
echo rootProject.buildDir = '../build'
echo subprojects {
echo     project.buildDir = "${rootProject.buildDir}/${project.name}"
echo }
echo subprojects {
echo     project.evaluationDependsOn^^^(':app'^^^)
echo }
echo.
echo tasks.register^^^("clean", Delete^^^) {
echo     delete rootProject.buildDir
echo }
) > android\build.gradle
echo ✓ android\build.gradle 已修复
echo.

echo [2/3] 修复 .github\workflows\build.yml...
if not exist ".github\workflows" mkdir ".github\workflows"
(
echo name: Build APK
echo.
echo on:
echo   push:
echo     branches: [ main, master ]
echo   workflow_dispatch:
echo.
echo jobs:
echo   build:
echo     runs-on: ubuntu-latest
echo     steps:
echo     - uses: actions/checkout@v4
echo     
echo     - uses: actions/setup-java@v4
echo       with:
echo         distribution: 'temurin'
echo         java-version: '17'
echo     
echo     - uses: subosito/flutter-action@v2
echo       with:
echo         flutter-version: '3.16.0'
echo         channel: 'stable'
echo     
echo     - name: Extract and fix permissions
echo       run: ^|
echo         # Extract zip
echo         unzip -q yisi_helper.zip ^|^| true
echo         
echo         # Find the actual project directory
echo         if [ -d "yisi_helper/yisi_helper" ]; then
echo           echo "Found nested directory, using yisi_helper/yisi_helper"
echo           PROJECT_DIR="yisi_helper/yisi_helper"
echo         elif [ -d "yisi_helper" ] ^&^& [ -f "yisi_helper/pubspec.yaml" ]; then
echo           echo "Found yisi_helper directory"
echo           PROJECT_DIR="yisi_helper"
echo         else
echo           echo "ERROR: Cannot find project"
echo           ls -la
echo           exit 1
echo         fi
echo         
echo         echo "Project directory: $PROJECT_DIR"
echo         
echo         # Fix permissions for Android build
echo         sudo chown -R $(whoami) "$PROJECT_DIR"
echo         sudo chmod -R 755 "$PROJECT_DIR"
echo         
echo         echo "Permissions fixed"
echo     
echo     - name: Setup Flutter and Build
echo       run: ^|
echo         # Determine project directory again
echo         if [ -d "yisi_helper/yisi_helper" ]; then
echo           PROJECT_DIR="yisi_helper/yisi_helper"
echo         else
echo           PROJECT_DIR="yisi_helper"
echo         fi
echo         
echo         cd "$PROJECT_DIR"
echo         
echo         # Create local.properties with Flutter SDK path
echo         echo "flutter.sdk=$FLUTTER_ROOT" ^> android/local.properties
echo         
echo         # Clean and get dependencies
echo         flutter clean
echo         flutter pub get
echo         
echo         # Build APK
echo         flutter build apk --release
echo     
echo     - uses: actions/upload-artifact@v4
echo       with:
echo         name: yisi-helper-apk
echo         path: yisi_helper/yisi_helper/build/app/outputs/flutter-apk/app-release.apk
) > .github\workflows\build.yml
echo ✓ .github\workflows\build.yml 已修复
echo.

echo [3/3] 清理构建缓存...
if exist "build" rmdir /s /q "build" 2>nul
echo ✓ 清理完成
echo.

echo === 修复完成！===
echo.
echo 接下来请执行：
echo   1. git add android/build.gradle .github/workflows/build.yml
echo   2. git commit -m "修复 Android 构建问题"
echo   3. git push
echo.
echo 然后到 GitHub 上重新运行 Actions 工作流
echo.
pause
