#!/bin/bash
# 本地修复脚本 - 在 yisi_helper 项目根目录运行

echo "=== 开始修复 Android 构建问题 ==="

# 1. 修复 android/build.gradle
echo "[1/3] 修复 android/build.gradle..."
cat > android/build.gradle << 'EOF'
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.buildDir = '../build'
subprojects {
    project.buildDir = "${rootProject.buildDir}/${project.name}"
}
subprojects {
    project.evaluationDependsOn(':app')
}

tasks.register("clean", Delete) {
    delete rootProject.buildDir
}
EOF
echo "✓ android/build.gradle 已修复"

# 2. 修复 GitHub Actions 工作流
echo "[2/3] 修复 .github/workflows/build.yml..."
mkdir -p .github/workflows
cat > .github/workflows/build.yml << 'EOF'
name: Build APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
        channel: 'stable'
    
    - name: Extract and fix permissions
      run: |
        # Extract zip
        unzip -q yisi_helper.zip || true
        
        # Find the actual project directory
        if [ -d "yisi_helper/yisi_helper" ]; then
          echo "Found nested directory, using yisi_helper/yisi_helper"
          PROJECT_DIR="yisi_helper/yisi_helper"
        elif [ -d "yisi_helper" ] && [ -f "yisi_helper/pubspec.yaml" ]; then
          echo "Found yisi_helper directory"
          PROJECT_DIR="yisi_helper"
        else
          echo "ERROR: Cannot find project"
          ls -la
          exit 1
        fi
        
        echo "Project directory: $PROJECT_DIR"
        
        # Fix permissions for Android build
        sudo chown -R $(whoami) "$PROJECT_DIR"
        sudo chmod -R 755 "$PROJECT_DIR"
        
        echo "Permissions fixed"
    
    - name: Setup Flutter and Build
      run: |
        # Determine project directory again
        if [ -d "yisi_helper/yisi_helper" ]; then
          PROJECT_DIR="yisi_helper/yisi_helper"
        else
          PROJECT_DIR="yisi_helper"
        fi
        
        cd "$PROJECT_DIR"
        
        # Create local.properties with Flutter SDK path
        echo "flutter.sdk=$FLUTTER_ROOT" > android/local.properties
        
        # Clean and get dependencies
        flutter clean
        flutter pub get
        
        # Build APK
        flutter build apk --release
    
    - uses: actions/upload-artifact@v4
      with:
        name: yisi-helper-apk
        path: yisi_helper/yisi_helper/build/app/outputs/flutter-apk/app-release.apk
EOF
echo "✓ .github/workflows/build.yml 已修复"

# 3. 清理并准备提交
echo "[3/3] 准备提交..."
flutter clean 2>/dev/null || true
echo "✓ 清理完成"

echo ""
echo "=== 修复完成！==="
echo ""
echo "接下来请执行："
echo "  1. git add android/build.gradle .github/workflows/build.yml"
echo "  2. git commit -m '修复 Android 构建问题'"
echo "  3. git push"
echo ""
echo "然后到 GitHub 上重新运行 Actions 工作流"
