import 'dart:math';

/// 高级题目匹配器
/// 使用多种算法组合提高匹配准确率
class AdvancedQuestionMatcher {
  
  // 权重配置
  static const double _lcsWeight = 0.35;      // 最长公共子序列权重
  static const double _jaccardWeight = 0.25;  // Jaccard相似度权重
  static const double _levenshteinWeight = 0.25; // 编辑距离权重
  static const double _keywordWeight = 0.15;  // 关键词匹配权重
  
  // 相似度阈值
  static const double _matchThreshold = 0.75; // 匹配阈值
  static const double _candidateThreshold = 0.5; // 候选阈值
  
  List<Map<String, dynamic>> _questions = [];
  Map<String, List<int>> _keywordIndex = {};
  
  /// 加载题库并建立索引
  void loadQuestions(List<Map<String, dynamic>> questions) {
    _questions = questions;
    _buildKeywordIndex();
  }
  
  /// 建立关键词索引
  void _buildKeywordIndex() {
    _keywordIndex.clear();
    
    for (int i = 0; i < _questions.length; i++) {
      final keywords = _extractKeywords(_questions[i]['content'] as String);
      for (final keyword in keywords) {
        if (!_keywordIndex.containsKey(keyword)) {
          _keywordIndex[keyword] = [];
        }
        _keywordIndex[keyword]!.add(i);
      }
    }
  }
  
  /// 提取关键词
  Set<String> _extractKeywords(String text) {
    // 清理文本
    final cleaned = text
        .replaceAll(RegExp(r'[（）()？?，。、；：""''！!\s]'), '')
        .toLowerCase();
    
    // 停用词
    final stopWords = {
      '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', 
      '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', 
      '看', '好', '自己', '这', '那', '之', '与', '及', '或', '但', '而', '为',
      '以', '于', '则', '将', '被', '把', '给', '向', '从', '当', '对', '关于'
    };
    
    final keywords = <String>{};
    
    // 提取2-5字的关键词
    for (int len = 2; len <= 5 && len <= cleaned.length; len++) {
      for (int i = 0; i <= cleaned.length - len; i++) {
        final word = cleaned.substring(i, i + len);
        // 过滤纯数字和停用词
        if (!word.contains(RegExp(r'^\d+$')) && 
            !stopWords.contains(word) &&
            word.codeUnitAt(0) > 127) { // 只保留中文
          keywords.add(word);
        }
      }
    }
    
    return keywords;
  }
  
  /// 智能匹配 - 返回最佳匹配结果
  MatchResult? findBestMatch(String screenText) {
    if (screenText.isEmpty || _questions.isEmpty) return null;
    
    // 清理屏幕文本
    final cleanedScreen = _cleanText(screenText);
    
    // 快速筛选候选题目
    final candidates = _getCandidates(cleanedScreen);
    if (candidates.isEmpty) return null;
    
    // 计算综合相似度
    final scoredCandidates = candidates.map((index) {
      final question = _questions[index];
      final questionText = _cleanText(question['content'] as String);
      
      final score = _calculateCompositeScore(cleanedScreen, questionText);
      
      return ScoredQuestion(
        index: index,
        question: question,
        score: score,
      );
    }).toList();
    
    // 按分数排序
    scoredCandidates.sort((a, b) => b.score.compareTo(a.score));
    
    // 返回最佳匹配
    final best = scoredCandidates.first;
    if (best.score >= _matchThreshold) {
      return MatchResult(
        question: best.question,
        score: best.score,
        confidence: _getConfidenceLevel(best.score),
      );
    }
    
    // 如果没有达到阈值，返回最佳候选（低置信度）
    if (best.score >= _candidateThreshold) {
      return MatchResult(
        question: best.question,
        score: best.score,
        confidence: ConfidenceLevel.low,
      );
    }
    
    return null;
  }
  
  /// 获取候选题目（快速筛选）
  List<int> _getCandidates(String screenText) {
    final screenKeywords = _extractKeywords(screenText);
    final candidateScores = <int, int>{}; // index -> keyword match count
    
    // 通过关键词索引快速筛选
    for (final keyword in screenKeywords) {
      final indices = _keywordIndex[keyword];
      if (indices != null) {
        for (final index in indices) {
          candidateScores[index] = (candidateScores[index] ?? 0) + 1;
        }
      }
    }
    
    // 按关键词匹配数排序，取前20个
    final sortedCandidates = candidateScores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    
    return sortedCandidates.take(20).map((e) => e.key).toList();
  }
  
  /// 计算综合相似度分数
  double _calculateCompositeScore(String s1, String s2) {
    // 1. LCS相似度
    final lcsScore = _lcsSimilarity(s1, s2);
    
    // 2. Jaccard相似度（字符集合）
    final jaccardScore = _jaccardSimilarity(s1, s2);
    
    // 3. Levenshtein相似度（编辑距离）
    final levenshteinScore = _levenshteinSimilarity(s1, s2);
    
    // 4. 关键词匹配度
    final keywordScore = _keywordMatchScore(s1, s2);
    
    // 加权综合
    final compositeScore = 
        lcsScore * _lcsWeight +
        jaccardScore * _jaccardWeight +
        levenshteinScore * _levenshteinWeight +
        keywordScore * _keywordWeight;
    
    return compositeScore;
  }
  
  /// LCS相似度（最长公共子序列）
  double _lcsSimilarity(String s1, String s2) {
    if (s1.isEmpty || s2.isEmpty) return 0.0;
    
    final lcs = _longestCommonSubsequence(s1, s2);
    return (2.0 * lcs) / (s1.length + s2.length);
  }
  
  int _longestCommonSubsequence(String s1, String s2) {
    final m = s1.length;
    final n = s2.length;
    
    // 使用滚动数组优化内存
    var prev = List<int>.filled(n + 1, 0);
    var curr = List<int>.filled(n + 1, 0);
    
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        if (s1[i - 1] == s2[j - 1]) {
          curr[j] = prev[j - 1] + 1;
        } else {
          curr[j] = max(curr[j - 1], prev[j]);
        }
      }
      // 交换数组
      final temp = prev;
      prev = curr;
      curr = temp;
    }
    
    return prev[n];
  }
  
  /// Jaccard相似度（字符集合的交集/并集）
  double _jaccardSimilarity(String s1, String s2) {
    final set1 = s1.split('').toSet();
    final set2 = s2.split('').toSet();
    
    final intersection = set1.intersection(set2);
    final union = set1.union(set2);
    
    if (union.isEmpty) return 0.0;
    return intersection.length / union.length;
  }
  
  /// Levenshtein相似度（基于编辑距离）
  double _levenshteinSimilarity(String s1, String s2) {
    final distance = _levenshteinDistance(s1, s2);
    final maxLength = max(s1.length, s2.length);
    if (maxLength == 0) return 1.0;
    return 1.0 - (distance / maxLength);
  }
  
  int _levenshteinDistance(String s1, String s2) {
    final m = s1.length;
    final n = s2.length;
    
    if (m == 0) return n;
    if (n == 0) return m;
    
    // 使用滚动数组
    var prev = List<int>.filled(n + 1, 0);
    var curr = List<int>.filled(n + 1, 0);
    
    for (int j = 0; j <= n; j++) {
      prev[j] = j;
    }
    
    for (int i = 1; i <= m; i++) {
      curr[0] = i;
      for (int j = 1; j <= n; j++) {
        final cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
        curr[j] = min(
          min(curr[j - 1] + 1, prev[j] + 1),
          prev[j - 1] + cost,
        );
      }
      // 交换数组
      final temp = prev;
      prev = curr;
      curr = temp;
    }
    
    return prev[n];
  }
  
  /// 关键词匹配分数
  double _keywordMatchScore(String s1, String s2) {
    final keywords1 = _extractKeywords(s1);
    final keywords2 = _extractKeywords(s2);
    
    if (keywords1.isEmpty || keywords2.isEmpty) return 0.0;
    
    final intersection = keywords1.intersection(keywords2);
    final union = keywords1.union(keywords2);
    
    return intersection.length / union.length;
  }
  
  /// 清理文本
  String _cleanText(String text) {
    return text
        .replaceAll(RegExp(r'\s+'), '')
        .replaceAll(RegExp(r'[\n\r（）()？?，。、；：""''！!]'), '')
        .toLowerCase();
  }
  
  /// 获取置信度级别
  ConfidenceLevel _getConfidenceLevel(double score) {
    if (score >= 0.85) return ConfidenceLevel.high;
    if (score >= 0.75) return ConfidenceLevel.medium;
    return ConfidenceLevel.low;
  }
  
  /// 批量匹配（返回多个候选结果）
  List<MatchResult> findTopMatches(String screenText, {int topN = 3}) {
    if (screenText.isEmpty || _questions.isEmpty) return [];
    
    final cleanedScreen = _cleanText(screenText);
    final candidates = _getCandidates(cleanedScreen);
    
    final scoredCandidates = candidates.map((index) {
      final question = _questions[index];
      final questionText = _cleanText(question['content'] as String);
      final score = _calculateCompositeScore(cleanedScreen, questionText);
      
      return ScoredQuestion(
        index: index,
        question: question,
        score: score,
      );
    }).toList();
    
    scoredCandidates.sort((a, b) => b.score.compareTo(a.score));
    
    return scoredCandidates
        .take(topN)
        .where((s) => s.score >= _candidateThreshold)
        .map((s) => MatchResult(
              question: s.question,
              score: s.score,
              confidence: _getConfidenceLevel(s.score),
            ))
        .toList();
  }
}

/// 匹配结果
class MatchResult {
  final Map<String, dynamic> question;
  final double score;
  final ConfidenceLevel confidence;
  
  MatchResult({
    required this.question,
    required this.score,
    required this.confidence,
  });
  
  String get answer => question['answer'] as String;
  String get content => question['content'] as String;
  String get type => question['type'] as String;
  List<dynamic> get options => question['options'] as List<dynamic>;
  
  /// 获取答案的完整内容（而不仅是A/B/C/D）
  String get answerContent {
    final answerLabel = answer;
    final opts = options;
    
    // 判断题
    if (type == 'judge') {
      return answerLabel == 'A' || answerLabel == '对' ? '对' : '错';
    }
    
    // 单选题/多选题
    final index = answerLabel.codeUnitAt(0) - 'A'.codeUnitAt(0);
    if (index >= 0 && index < opts.length) {
      return opts[index] as String;
    }
    
    return answerLabel;
  }
  
  /// 获取答案标签和内容
  String get answerWithContent {
    return '$answer. $answerContent';
  }
  
  @override
  String toString() {
    return 'MatchResult(score: ${score.toStringAsFixed(3)}, confidence: $confidence, answer: $answerWithContent)';
  }
}

/// 置信度级别
enum ConfidenceLevel {
  high,    // 高置信度 (>=0.85)
  medium,  // 中置信度 (0.75-0.85)
  low,     // 低置信度 (0.5-0.75)
}

/// 带分数的题目
class ScoredQuestion {
  final int index;
  final Map<String, dynamic> question;
  final double score;
  
  ScoredQuestion({
    required this.index,
    required this.question,
    required this.score,
  });
}

/// 数学工具函数
int max(int a, int b) => a > b ? a : b;
int min(int a, int b) => a < b ? a : b;
