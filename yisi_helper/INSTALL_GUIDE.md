# 易思培训助手 - 下载安装指南

## 📱 方案一：我帮你构建APK（推荐）

### 步骤：

1. **你提供以下信息：**
   - 你的邮箱（用于接收APK文件）
   - 或网盘链接（百度网盘、阿里云盘等）

2. **我构建APK：**
   - 在安装了Flutter的环境中构建
   - 生成 `app-release.apk` 文件

3. **发送给你：**
   - 通过邮件发送
   - 或上传到网盘分享

4. **你安装到手机：**
   - 下载APK文件
   - 点击安装
   - 开启权限使用

---

## 📱 方案二：你自己构建（需要电脑）

### 需要准备：

1. **一台电脑**（Windows/Mac/Linux）
2. **网络连接**（下载依赖需要）
3. **约30分钟时间**

### 详细步骤：

#### 1. 安装Flutter

**Windows:**
```powershell
# 1. 下载Flutter SDK
# 访问: https://docs.flutter.dev/get-started/install/windows

# 2. 解压到 C:\flutter

# 3. 添加环境变量
[Environment]::SetEnvironmentVariable(
    "Path", 
    $env:Path + ";C:\flutter\bin", 
    "User"
)

# 4. 重启命令行，验证安装
flutter doctor
```

**Mac:**
```bash
# 使用Homebrew安装
brew install flutter

# 验证安装
flutter doctor
```

**Linux:**
```bash
# 使用Snap安装
sudo snap install flutter --classic

# 验证安装
flutter doctor
```

#### 2. 安装Android Studio

1. 下载：https://developer.android.com/studio
2. 安装并启动
3. 安装Android SDK（默认会安装）
4. 创建虚拟设备（可选，用于测试）

#### 3. 获取项目代码

**方式A：复制项目文件夹**
- 将我给你的 `yisi_helper` 文件夹复制到电脑

**方式B：Git克隆（如果有Git仓库）**
```bash
git clone [仓库地址]
cd yisi_helper
```

#### 4. 构建APK

```bash
# 进入项目目录
cd yisi_helper

# 安装依赖（约5-10分钟）
flutter pub get

# 构建APK（约5-10分钟）
flutter build apk --release
```

构建完成后，APK文件位置：
```
yisi_helper/build/app/outputs/flutter-apk/app-release.apk
```

#### 5. 传输到手机

**方式A：USB数据线**
```bash
# 连接手机后
flutter install

# 或手动复制APK到手机
```

**方式B：微信/QQ文件传输**
- 将APK发送到手机
- 在手机上点击安装

**方式C：网盘**
- 上传到百度网盘/阿里云盘
- 手机下载安装

---

## 📱 方案三：使用在线构建服务

### 推荐平台：

#### 1. Codemagic (https://codemagic.io)
- 免费Flutter构建服务
- 连接GitHub自动构建
- 直接下载APK

**步骤：**
1. 注册Codemagic账号
2. 上传项目到GitHub
3. 连接GitHub仓库
4. 点击构建
5. 下载APK

#### 2. GitHub Actions
- 免费自动化构建
- 需要GitHub账号

**步骤：**
1. 创建GitHub仓库
2. 上传项目代码
3. 配置GitHub Actions工作流
4. 推送到GitHub自动构建
5. 下载构建产物

---

## 📱 方案四：找朋友帮忙

如果你有朋友：
- 会Flutter开发
- 或从事Android开发
- 或有相关经验

可以请他们帮忙：
1. 把 `yisi_helper` 文件夹发给他们
2. 让他们执行构建命令
3. 把生成的APK发给你

---

## 🔧 安装APK到手机

### 步骤：

1. **开启允许安装未知来源应用**
   - 设置 → 安全 → 未知来源应用
   - 允许浏览器/文件管理器安装

2. **传输APK到手机**
   - USB数据线
   - 微信/QQ文件传输
   - 网盘下载
   - 蓝牙传输

3. **安装APK**
   - 找到APK文件
   - 点击安装
   - 等待安装完成

4. **开启权限**
   - 设置 → 无障碍 → 易思培训助手 → 开启
   - 设置 → 应用管理 → 易思培训助手 → 权限 → 悬浮窗 → 允许

5. **使用**
   - 打开易思培训APP
   - 悬浮窗自动显示答案

---

## ⚠️ 常见问题

### 安装时提示"安装包损坏"
- 重新下载APK
- 确保下载完整
- 检查文件大小（应该>10MB）

### 安装时提示"未知来源"
- 开启"允许安装未知来源应用"
- 不同手机设置位置不同

### 无法开启无障碍权限
- 部分手机需要关闭"悬浮球"等辅助功能
- 或重启手机后再试

### 悬浮窗不显示
- 检查悬浮窗权限是否开启
- 检查无障碍服务是否运行
- 重启APP试试

---

## 💡 推荐方案

| 方案 | 难度 | 时间 | 适合人群 |
|------|------|------|----------|
| 我帮你构建 | ⭐ 简单 | 10分钟 | 所有人 |
| 自己构建 | ⭐⭐⭐ 复杂 | 30分钟 | 有技术基础 |
| 在线构建 | ⭐⭐ 中等 | 20分钟 | 有GitHub账号 |
| 找朋友 | ⭐ 简单 | 不定 | 有朋友帮忙 |

**强烈推荐：方案一（我帮你构建）**
- 最简单快捷
- 无需技术基础
- 10分钟即可使用

---

## 📧 选择方案一？

请告诉我：
1. 你的邮箱地址
2. 或你常用的网盘（百度/阿里）

我会尽快构建APK并发送给你！

---

**需要我帮你构建APK吗？** 📱
