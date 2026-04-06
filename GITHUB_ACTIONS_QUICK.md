# GitHub Actions 构建 - 5步完成

## 第1步：注册GitHub（2分钟）
```
1. 访问 https://github.com
2. 点击 Sign up
3. 用邮箱注册
4. 验证邮箱
```

## 第2步：创建仓库（1分钟）
```
1. 登录GitHub
2. 点击右上角 + → New repository
3. 仓库名：yisi_helper
4. 选择 Public
5. 勾选 Add a README file
6. 点击 Create repository
```

## 第3步：上传代码（3分钟）
```
1. 进入仓库页面
2. 点击 Add file → Upload files
3. 选择 yisi_helper.zip
4. 点击 Commit changes
```

## 第4步：配置自动构建（2分钟）
```
1. 点击 Actions 标签
2. 点击 set up a workflow yourself
3. 粘贴下面的配置：
```

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

```
4. 点击 Start commit → Commit new file
```

## 第5步：下载APK（等待10分钟）
```
1. 点击 Actions 标签
2. 等待构建完成（绿色✅）
3. 点击最新的构建
4. 页面下方找到 Artifacts
5. 点击 release-apk 下载
6. 安装到手机
```

---

## ✅ 完成！

**总时间：约20分钟**
**费用：免费**

---

**详细教程查看：** `GITHUB_ACTIONS_TUTORIAL.md`

**开始吧！** 🚀
