import 'dart:convert';
import 'package:flutter/material.dart';
import '../database/database_helper.dart';
import '../services/ultra_fast_matcher.dart';
import '../services/question_importer.dart';
import '../data/question_bank.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;
  final UltraFastMatcher _matcher = UltraFastMatcher();
  final QuestionImporter _importer = QuestionImporter.instance;
  
  bool _isLoading = true;
  bool _isImporting = false;
  int _questionCount = 0;
  int _databaseSize = 0;
  String _status = '正在初始化...';
  double _importProgress = 0;

  @override
  void initState() {
    super.initState();
    _initDatabase();
  }

  Future<void> _initDatabase() async {
    try {
      setState(() => _status = '正在检查数据库...');
      
      final needImport = await _importer.needImport();
      
      if (needImport) {
        setState(() => _status = '正在导入题库...');
        await _importQuestions();
      }
      
      final allQuestions = await _dbHelper.getAllQuestionsForMatching();
      _matcher.loadQuestions(allQuestions);
      
      final count = await _dbHelper.getQuestionCount();
      final size = await _dbHelper.getDatabaseSize();
      
      setState(() {
        _questionCount = count;
        _databaseSize = size;
        _isLoading = false;
        _status = '题库加载完成，匹配引擎就绪';
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _status = '加载失败: $e';
      });
    }
  }

  Future<void> _importQuestions() async {
    setState(() {
      _isImporting = true;
      _status = '正在导入题库...';
    });

    await for (final progress in _importer.importWithProgress(questionBank)) {
      setState(() {
        _importProgress = progress.percentage;
        _status = progress.message;
      });
    }

    setState(() {
      _isImporting = false;
    });
  }

  String _formatFileSize(int bytes) {
    if (bytes < 1024) return '$bytes B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('易思培训助手'),
        centerTitle: true,
      ),
      body: _isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const CircularProgressIndicator(),
                  const SizedBox(height: 20),
                  Text(_status),
                ],
              ),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(
                                _questionCount > 0 ? Icons.check_circle : Icons.error,
                                color: _questionCount > 0 ? Colors.green : Colors.red,
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  '状态: $_status',
                                  style: const TextStyle(fontSize: 16),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text(
                            '题库数量: $_questionCount 道题',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          if (_databaseSize > 0)
                            Text(
                              '数据库大小: ${_formatFileSize(_databaseSize)}',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.grey[600],
                              ),
                            ),
                          if (_isImporting) ...[
                            const SizedBox(height: 12),
                            LinearProgressIndicator(value: _importProgress),
                            const SizedBox(height: 4),
                            Text(
                              '${(_importProgress * 100).toStringAsFixed(0)}%',
                              style: const TextStyle(fontSize: 12),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  const Text(
                    '⚡ 极速版特性：',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text('⚡ 100ms极速响应'),
                  const Text('⚡ 智能缓存加速'),
                  const Text('✅ 显示选项内容（不只是A/B/C/D）'),
                  const Text('✅ 反作弊检测保护'),
                  const Text('✅ 悬浮窗透明度调节'),
                  const Text('✅ 悬浮窗大小缩放'),
                  const Text('✅ 可拖动位置'),
                  const Text('✅ 可最小化/展开'),
                  const SizedBox(height: 20),
                  
                  const Text(
                    '使用说明：',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text('1. 开启无障碍服务权限'),
                  const Text('2. 开启悬浮窗权限'),
                  const Text('3. 打开"易思培训"APP开始考试'),
                  const Text('4. 悬浮窗显示答案和选项内容'),
                  const Text('5. 可调节透明度和大小'),
                  const SizedBox(height: 8),
                  const Text(
                    '支持版本: 易思培训 V35 / Android版',
                    style: TextStyle(color: Colors.blue, fontSize: 12),
                  ),
                  const SizedBox(height: 20),
                  
                  ElevatedButton.icon(
                    onPressed: _checkAccessibility,
                    icon: const Icon(Icons.accessibility),
                    label: const Text('检查无障碍权限'),
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 50),
                    ),
                  ),
                  const SizedBox(height: 12),
                  ElevatedButton.icon(
                    onPressed: _showFloatingWindow,
                    icon: const Icon(Icons.picture_in_picture),
                    label: const Text('显示悬浮窗'),
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 50),
                    ),
                  ),
                ],
              ),
            ),
    );
  }

  void _checkAccessibility() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('无障碍权限'),
        content: const Text(
          '请前往系统设置 -> 无障碍 -> 易思培训助手，开启无障碍服务权限。\n\n'
          '注意：本应用已添加反检测保护，正常使用不会被发现。',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('确定'),
          ),
        ],
      ),
    );
  }

  void _showFloatingWindow() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('悬浮窗权限'),
        content: const Text(
          '请前往系统设置 -> 应用管理 -> 易思培训助手 -> 权限管理，开启悬浮窗权限。\n\n'
          '悬浮窗功能：\n'
          '• 显示答案和选项内容\n'
          '• 可调节透明度（防发现）\n'
          '• 可调节大小\n'
          '• 可拖动位置\n'
          '• 可最小化',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('确定'),
          ),
        ],
      ),
    );
  }
}
