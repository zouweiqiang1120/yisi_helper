// 完整题库数据 - LLDPE装置操作工考试题库
// 从all_questions.dart导入完整题库

import 'all_questions.dart';

final List<Map<String, dynamic>> questionBank = allQuestions;

// 获取题库统计信息
Map<String, dynamic> getQuestionStats() {
  return getQuestionBankStats();
}
