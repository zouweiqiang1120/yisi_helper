import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import '../database/database_helper.dart';

class QuestionImporter {
  static final QuestionImporter instance = QuestionImporter._init();
  
  QuestionImporter._init();

  /// 从JSON文件导入题库
  Future<ImportResult> importFromJsonFile(String filePath) async {
    try {
      final file = File(filePath);
      if (!await file.exists()) {
        return ImportResult(
          success: false,
          message: '文件不存在: $filePath',
        );
      }

      final jsonString = await file.readAsString();
      final List<dynamic> jsonList = json.decode(jsonString);
      
      return await importFromList(jsonList.cast<Map<String, dynamic>>());
    } catch (e) {
      return ImportResult(
        success: false,
        message: '导入失败: $e',
      );
    }
  }

  /// 从JSON字符串导入
  Future<ImportResult> importFromJsonString(String jsonString) async {
    try {
      final List<dynamic> jsonList = json.decode(jsonString);
      return await importFromList(jsonList.cast<Map<String, dynamic>>());
    } catch (e) {
      return ImportResult(
        success: false,
        message: '导入失败: $e',
      );
    }
  }

  /// 从列表导入
  Future<ImportResult> importFromList(List<Map<String, dynamic>> questions) async {
    try {
      final dbHelper = DatabaseHelper.instance;
      
      // 清空现有题库
      await dbHelper.clearQuestions();
      
      // 分批插入
      await dbHelper.batchInsertQuestions(questions);
      
      // 获取统计
      final count = await dbHelper.getQuestionCount();
      final size = await dbHelper.getDatabaseSize();
      
      return ImportResult(
        success: true,
        message: '导入成功',
        importedCount: count,
        databaseSize: size,
      );
    } catch (e) {
      return ImportResult(
        success: false,
        message: '导入失败: $e',
      );
    }
  }

  /// 从Assets导入（预置题库）
  Future<ImportResult> importFromAssets(BuildContext context, String assetPath) async {
    try {
      final jsonString = await DefaultAssetBundle.of(context).loadString(assetPath);
      return await importFromJsonString(jsonString);
    } catch (e) {
      return ImportResult(
        success: false,
        message: '从Assets导入失败: $e',
      );
    }
  }

  /// 检查是否需要导入
  Future<bool> needImport() async {
    final dbHelper = DatabaseHelper.instance;
    final count = await dbHelper.getQuestionCount();
    return count == 0;
  }

  /// 获取导入进度流
  Stream<ImportProgress> importWithProgress(List<Map<String, dynamic>> questions) async* {
    final total = questions.length;
    final batchSize = 100;
    final dbHelper = DatabaseHelper.instance;
    
    // 清空现有题库
    await dbHelper.clearQuestions();
    yield ImportProgress(
      current: 0,
      total: total,
      message: '正在清空旧数据...',
    );

    // 分批插入
    for (int i = 0; i < total; i += batchSize) {
      final end = (i + batchSize < total) ? i + batchSize : total;
      final batch = questions.sublist(i, end);
      
      await dbHelper.batchInsertQuestions(batch);
      
      yield ImportProgress(
        current: end,
        total: total,
        message: '已导入 $end / $total 道题',
      );
    }

    final count = await dbHelper.getQuestionCount();
    yield ImportProgress(
      current: total,
      total: total,
      message: '导入完成！共 $count 道题',
      isComplete: true,
    );
  }
}

/// 导入结果
class ImportResult {
  final bool success;
  final String message;
  final int? importedCount;
  final int? databaseSize;

  ImportResult({
    required this.success,
    required this.message,
    this.importedCount,
    this.databaseSize,
  });
}

/// 导入进度
class ImportProgress {
  final int current;
  final int total;
  final String message;
  final bool isComplete;

  ImportProgress({
    required this.current,
    required this.total,
    required this.message,
    this.isComplete = false,
  });

  double get percentage => total > 0 ? current / total : 0;
}
