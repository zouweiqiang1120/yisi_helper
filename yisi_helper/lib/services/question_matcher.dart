import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class Question {
  final String content;
  final List<String> options;
  final String answer;
  final String type; // 'single', 'multiple', 'judge'

  Question({
    required this.content,
    required this.options,
    required this.answer,
    required this.type,
  });
}

class QuestionMatcher {
  List<Question> questions = [];

  void loadQuestions(List<Map<String, dynamic>> data) {
    questions = data.map((q) => Question(
      content: q['content'] ?? '',
      options: List<String>.from(q['options'] ?? []),
      answer: q['answer'] ?? '',
      type: q['type'] ?? 'single',
    )).toList();
  }

  Question? findMatch(String screenText) {
    if (screenText.isEmpty || questions.isEmpty) return null;
    
    // 清理屏幕文本
    String cleanText = screenText
        .replaceAll(RegExp(r'\s+'), '')
        .replaceAll(RegExp(r'[\n\r]'), '');
    
    Question? bestMatch;
    double maxSimilarity = 0.6; // 最小相似度阈值
    
    for (var q in questions) {
      String cleanQuestion = q.content
          .replaceAll(RegExp(r'\s+'), '')
          .replaceAll(RegExp(r'[\n\r]'), '');
      
      double similarity = _calculateSimilarity(cleanText, cleanQuestion);
      
      if (similarity > maxSimilarity) {
        maxSimilarity = similarity;
        bestMatch = q;
      }
    }
    
    return bestMatch;
  }

  double _calculateSimilarity(String s1, String s2) {
    if (s1.isEmpty || s2.isEmpty) return 0.0;
    
    // 使用最长公共子序列算法
    int lcs = _longestCommonSubsequence(s1, s2);
    return (2.0 * lcs) / (s1.length + s2.length);
  }

  int _longestCommonSubsequence(String s1, String s2) {
    List<List<int>> dp = List.generate(
      s1.length + 1,
      (_) => List.filled(s2.length + 1, 0),
    );
    
    for (int i = 1; i <= s1.length; i++) {
      for (int j = 1; j <= s2.length; j++) {
        if (s1[i - 1] == s2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1] + 1;
        } else {
          dp[i][j] = dp[i - 1][j] > dp[i][j - 1] ? dp[i - 1][j] : dp[i][j - 1];
        }
      }
    }
    
    return dp[s1.length][s2.length];
  }
}
