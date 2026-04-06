# 易思培训助手 - 构建指南

## ⚠️ 重要提示

当前环境中未安装Flutter，无法直接构建APK。

请在你的电脑上按照以下步骤操作：

## 📋 环境要求

### 1. 安装Flutter

**Windows:**
```powershell
# 下载Flutter SDK
# https://docs.flutter.dev/get-started/install/windows

# 解压到 C:\flutter

# 添加环境变量
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\flutter\bin", "User")
```

**macOS:**
```bash
brew install flutter
```

**Linux:**
```bash
sudo snap install flutter --classic
```

### 2. 安装Android Studio

1. 下载: https://developer.android.com/studio
2. 安装Android SDK
3. 配置Android模拟器（可选）

### 3. 验证环境

```bash
flutter doctor
```

确保所有项都是 ✅

## 🚀 构建步骤

### 1. 获取项目

将 `yisi_helper` 文件夹复制到你的电脑

### 2. 安装依赖

```bash
cd yisi_helper
flutter pub get
```

### 3. 构建APK

**开发版（快速测试）:**
```bash
flutter run
```

**发布版（推荐使用）:**
```bash
flutter build apk --release
```

APK文件将生成在:
```
build/app/outputs/flutter-apk/app-release.apk
```

### 4. 安装到手机

```bash
# 通过USB连接手机后
flutter install

# 或手动复制APK到手机安装
```

## 📱 安装后配置

### 1. 开启无障碍服务
1. 打开 **设置** → **无障碍**
2. 找到 **易思培训助手**
3. 开启服务
4. 确认弹出的权限请求

### 2. 开启悬浮窗权限
1. 打开 **设置** → **应用管理** → **易思培训助手**
2. 点击 **权限**
3. 开启 **悬浮窗** 权限

### 3. 使用
1. 打开 **易思培训助手** APP
2. 等待题库加载完成（显示"题库加载完成"）
3. 打开 **易思培训** APP开始考试
4. 悬浮窗会自动显示答案

## 🔧 常见问题

### flutter命令找不到
```bash
# 检查环境变量
echo $env:Path  # Windows
echo $PATH      # Mac/Linux

# 确保包含Flutter的bin目录
```

### 构建失败
```bash
# 清理后重新构建
flutter clean
flutter pub get
flutter build apk --release
```

### 依赖下载慢
```bash
# 使用国内镜像
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
flutter pub get
```

## 📦 项目文件清单

确保以下文件都存在：

```
yisi_helper/
├── lib/
│   ├── main.dart
│   ├── data/
│   │   ├── question_bank.dart
│   │   └── all_questions.dart
│   ├── database/
│   │   └── database_helper.dart
│   ├── screens/
│   │   └── home_screen.dart
│   └── services/
│       ├── advanced_matcher.dart
│       └── question_importer.dart
├── android/
│   └── app/src/main/
│       ├── AndroidManifest.xml
│       └── kotlin/com/example/yisi_helper/
│           ├── YisiAccessibilityService.kt
│           └── FloatingWindowService.kt
└── pubspec.yaml
```

## ✅ 构建前检查清单

- [ ] Flutter已安装 (`flutter --version`)
- [ ] Android SDK已配置 (`flutter doctor`)
- [ ] 项目文件完整
- [ ] 依赖已安装 (`flutter pub get`)

## 🎯 构建成功后

你会得到 `app-release.apk`，可以：
1. 直接安装到手机测试
2. 分享给他人使用
3. 发布到应用商店

## 📞 需要帮助?

如果构建过程中遇到问题：
1. 检查 `flutter doctor` 输出
2. 查看错误日志
3. 确保网络连接正常（需要下载依赖）

---

**项目已准备就绪，只需安装Flutter环境即可构建！**
