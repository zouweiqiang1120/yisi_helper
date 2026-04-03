# GitHub Actions 自动构建详细教程

## 📋 准备工作

### 1. 注册GitHub账号

1. 访问：https://github.com
2. 点击 **"Sign up"**
3. 填写信息：
   - 邮箱：你的邮箱
   - 密码：设置密码
   - 用户名：设置用户名
4. 验证邮箱
5. 完成注册

---

## 🚀 步骤一：创建GitHub仓库

### 1. 登录GitHub
- 访问 https://github.com
- 点击 **"Sign in"** 登录

### 2. 创建新仓库
1. 点击右上角 **"+"** → **"New repository"**
2. 填写仓库信息：
   - **Repository name**: `yisi_helper`
   - **Description**: `易思培训助手 - LLDPE考试辅助APP`
   - **Public** （选中公开）
   - **Add a README file** （勾选）
3. 点击 **"Create repository"**

---

## 📁 步骤二：上传项目文件

### 方法A：网页上传（推荐，最简单）

1. 进入刚创建的仓库页面
2. 点击 **"Add file"** → **"Upload files"**
3. 点击 **"choose your files"**
4. 选择你的 `yisi_helper.zip` 文件
5. 等待上传完成
6. 点击 **"Commit changes"**

### 方法B：解压后上传（如果zip上传失败）

如果zip文件太大，可以分批上传关键文件：

**必须上传的文件：**
```
lib/
├── main.dart
├── data/
│   ├── question_bank.dart
│   └── all_questions.dart
├── database/
│   └── database_helper.dart
├── screens/
│   └── home_screen.dart
└── services/
    └── ultra_fast_matcher.dart

android/app/src/main/
├── AndroidManifest.xml
└── kotlin/com/example/yisi_helper/
    ├── MainActivity.kt
    ├── YisiAccessibilityService.kt
    └── FloatingWindowService.kt

pubspec.yaml
```

**操作步骤：**
1. 点击 **"Add file"** → **"Create new file"**
2. 创建文件夹结构（输入 `lib/main.dart`）
3. 复制粘贴代码内容
4. 点击 **"Commit new file"**
5. 重复创建其他文件

---

## ⚙️ 步骤三：配置GitHub Actions

### 1. 创建工作流文件

1. 在仓库页面，点击 **"Actions"** 标签
2. 点击 **"set up a workflow yourself"**
3. 复制粘贴以下配置：

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
        channel: 'stable'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Build APK
      run: flutter build apk --release
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: release-apk
        path: build/app/outputs/flutter-apk/app-release.apk
```

4. 点击 **"Start commit"** → **"Commit new file"**

### 2. 触发构建

**方式A：自动触发**
- 上传代码后会自动开始构建

**方式B：手动触发**
1. 点击 **"Actions"** 标签
2. 点击 **"Build APK"**
3. 点击 **"Run workflow"** → **"Run workflow"**

---

## ⏳ 步骤四：等待构建完成

### 构建时间
- 首次构建：约 10-15 分钟
- 后续构建：约 5-10 分钟

### 查看进度
1. 点击 **"Actions"** 标签
2. 点击正在运行的工作流
3. 查看实时日志

### 构建成功标志
看到绿色 ✅ **"Build APK"** 表示成功

---

## 📥 步骤五：下载APK

### 1. 进入构建详情
1. 点击 **"Actions"** 标签
2. 点击最新的成功构建（绿色✅）
3. 页面下方找到 **"Artifacts"**

### 2. 下载APK
1. 找到 **"release-apk"**
2. 点击下载
3. 得到 `app-release.apk` 文件

### 3. 安装到手机
1. 传输APK到手机（微信/QQ/数据线）
2. 点击安装
3. 开启权限使用

---

## ❓ 常见问题

### Q1: 构建失败？
**解决：**
- 检查 `pubspec.yaml` 是否正确上传
- 检查依赖版本
- 查看错误日志，根据提示修改

### Q2: 找不到Artifacts？
**解决：**
- 确保构建成功（绿色✅）
- 页面往下滚动找到Artifacts
- 或点击页面右侧的Artifacts

### Q3: 下载的APK安装失败？
**解决：**
- 开启"允许安装未知来源应用"
- 重新下载试试

### Q4: 如何更新代码？
**解决：**
- 修改文件后重新上传
- 自动触发新构建
- 下载新的APK

---

## 💡 提示

1. **构建是免费的**，但有额度限制（每月2000分钟）
2. **公开仓库免费**，私有仓库有额度限制
3. **首次构建较慢**，需要下载依赖
4. **可以多次构建**，不限制次数

---

## 🎯 成功标志

当你看到：
```
✅ Build APK
📦 release-apk (15 MB)
```

恭喜你！可以下载APK并安装到手机了！

---

## 📞 需要帮助？

如果在任何步骤遇到问题，告诉我：
- 具体步骤
- 错误信息
- 截图（如果有）

我可以帮你解决！

---

**开始操作吧！有问题随时问我！** 🚀
