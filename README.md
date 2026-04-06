# 易思培训助手 - 使用说明

## 项目结构

```
yisi_helper/
├── lib/
│   ├── main.dart                 # 应用入口
│   ├── screens/
│   │   └── home_screen.dart      # 主界面
│   ├── services/
│   │   └── question_matcher.dart # 题目匹配服务
│   └── database/
│       └── database_helper.dart  # SQLite数据库
├── android/
│   └── app/src/main/kotlin/com/example/yisi_helper/
│       ├── YisiAccessibilityService.kt  # 无障碍服务
│       ├── FloatingWindowService.kt     # 悬浮窗服务
│       └── res/
│           ├── layout/floating_window.xml
│           ├── drawable/floating_bg.xml
│           └── xml/accessibility_service_config.xml
├── tools/
│   └── parse_questions.py        # 题库解析脚本
└── pubspec.yaml
```

## 功能说明

### 1. 无障碍服务
- 监听"易思培训"APP的屏幕内容变化
- 自动提取题目文本
- 通过模糊匹配算法查找题库中的对应题目

### 2. 悬浮窗显示
- 在考试界面上方显示半透明悬浮窗
- 显示识别到的题目和对应答案
- 支持拖动位置

### 3. 题库匹配
- 使用最长公共子序列(LCS)算法计算文本相似度
- 相似度超过阈值(默认0.6)即认为是同一道题
- 支持SQLite数据库存储和检索

## 安装步骤

### 1. 环境准备
```bash
# 安装Flutter
# https://flutter.dev/docs/get-started/install

# 检查环境
flutter doctor
```

### 2. 导入项目
```bash
cd yisi_helper
flutter pub get
```

### 3. 导入题库
将提供的题库文本保存为 `tools/questions.txt`，然后运行：
```bash
cd tools
python parse_questions.py
```

将生成的 `questions.json` 放入 `assets/` 目录

### 4. 构建APK
```bash
flutter build apk --release
```

## 使用方法

### 1. 安装APK
将生成的APK安装到Android手机

### 2. 开启权限
- **无障碍服务**：设置 → 无障碍 → 易思培训助手 → 开启
- **悬浮窗权限**：设置 → 应用管理 → 易思培训助手 → 权限 → 悬浮窗 → 允许

### 3. 使用
1. 打开"易思培训助手"APP
2. 点击"显示悬浮窗"按钮
3. 打开"易思培训"APP开始考试
4. 悬浮窗会自动显示当前题目的答案

## 注意事项

1. **无障碍服务**：必须开启才能读取屏幕内容
2. **悬浮窗权限**：必须开启才能显示答案
3. **题库更新**：如需更新题库，重新运行解析脚本并替换JSON文件
4. **匹配精度**：相似度阈值可在 `question_matcher.dart` 中调整

## 技术细节

### 题目匹配算法
使用最长公共子序列(LCS)算法计算两字符串的相似度：
```
相似度 = (2 × LCS长度) / (字符串1长度 + 字符串2长度)
```

### 无障碍服务配置
- 监听事件：窗口内容变化、视图点击、视图聚焦
- 目标包名：`com.yisi.training`（需根据实际APP包名修改）

## 免责声明

本工具仅供学习研究使用，请遵守相关考试规定和法律法规。

## 更新日志

### v1.0.0
- 基础功能实现
- 无障碍服务读取屏幕
- 悬浮窗显示答案
- SQLite题库存储
