import 'dart:collection';
import 'dart:math';

/// 极速版题目匹配器
/// 优化：快速响应 + 高准确率 + 缓存机制
class UltraFastMatcher {
  
  // 配置
  static const int _maxCacheSize = 100;
  static const double _highConfidenceThreshold = 0.85;
  static const double _matchThreshold = 0.70;
  
  // 数据
  List<Map<String, dynamic>> _questions = [];
  
  // 缓存：题目内容 -> 匹配结果
  final _cache = LinkedHashMap<String, MatchResult>();
  
  // 索引：关键词 -> 题目索引列表
  Map<String, List<int>> _keywordIndex = {};
  
  // 统计
  int _cacheHits = 0;
  int _totalQueries = 0;
  
  /// 加载题库并建立索引
  void loadQuestions(List<Map<String, dynamic>> questions) {
    _questions = questions;
    _buildFastIndex();
    print('极速匹配器已加载 ${questions.length} 道题');
  }
  
  /// 建立快速索引
  void _buildFastIndex() {
    _keywordIndex.clear();
    
    for (int i = 0; i < _questions.length; i++) {
      final keywords = _extractKeywordsFast(_questions[i]['content'] as String);
      for (final keyword in keywords) {
        _keywordIndex.putIfAbsent(keyword, () => []).add(i);
      }
    }
    
    print('索引建立完成，共 ${_keywordIndex.length} 个关键词');
  }
  
  /// 极速匹配
  MatchResult? match(String screenText) {
    _totalQueries++;
    
    if (screenText.isEmpty || _questions.isEmpty) return null;
    
    // 1. 检查缓存
    final cached = _checkCache(screenText);
    if (cached != null) {
      _cacheHits++;
      return cached;
    }
    
    // 2. 快速清理文本
    final cleaned = _fastClean(screenText);
    
    // 3. 快速筛选候选
    final candidates = _fastGetCandidates(cleaned);
    if (candidates.isEmpty) return null;
    
    // 4. 并行计算相似度（取前3个最像的）
    final results = _parallelMatch(cleaned, candidates, topN: 3);
    
    if (results.isEmpty) return null;
    
    // 5. 返回最佳结果
    final best = results.first;
    
    // 6. 缓存结果
    _addToCache(screenText, best);
    
    return best;
  }
  
  /// 检查缓存
  MatchResult? _checkCache(String text) {
    // 使用简化文本作为缓存键
    final key = _fastClean(text);
    return _cache[key];
  }
  
  /// 添加到缓存
  void _addToCache(String text, MatchResult result) {
    if (_cache.length >= _maxCacheSize) {
      _cache.remove(_cache.keys.first);
    }
    _cache[_fastClean(text)] = result;
  }
  
  /// 快速清理文本
  String _fastClean(String text) {
    final buffer = StringBuffer();
    for (final char in text.runes) {
      final c = String.fromCharCode(char);
      // 只保留中文、字母、数字
      if ((char >= 0x4E00 && char <= 0x9FFF) || // 中文
          (char >= 0x41 && char <= 0x5A) ||     // A-Z
          (char >= 0x61 && char <= 0x7A) ||     // a-z
          (char >= 0x30 && char <= 0x39)) {     // 0-9
        buffer.write(c);
      }
    }
    return buffer.toString().toLowerCase();
  }
  
  /// 快速提取关键词
  Set<String> _extractKeywordsFast(String text) {
    final cleaned = _fastClean(text);
    final keywords = <String>{};
    
    // 提取2-4字词组
    for (int len = 2; len <= 4 && len <= cleaned.length; len++) {
      for (int i = 0; i <= cleaned.length - len; i++) {
        keywords.add(cleaned.substring(i, i + len));
      }
    }
    
    return keywords;
  }
  
  /// 快速获取候选
  List<int> _fastGetCandidates(String cleaned) {
    final keywords = _extractKeywordsFast(cleaned);
    final scores = <int, int>{}; // index -> match count
    
    for (final kw in keywords) {
      final indices = _keywordIndex[kw];
      if (indices != null) {
        for (final idx in indices) {
          scores[idx] = (scores[idx] ?? 0) + 1;
        }
      }
    }
    
    // 按匹配数排序，取前15个
    final sorted = scores.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    
    return sorted.take(15).map((e) => e.key).toList();
  }
  
  /// 并行匹配
  List<MatchResult> _parallelMatch(
    String query,
    List<int> candidates,
    {required int topN}
  ) {
    final results = <ScoredResult>[];
    
    for (final idx in candidates) {
      final q = _questions[idx];
      final qText = _fastClean(q['content'] as String);
      
      // 快速相似度计算
      final score = _ultraFastSimilarity(query, qText);
      
      if (score >= _matchThreshold) {
        results.add(ScoredResult(
          index: idx,
          question: q,
          score: score,
        ));
      }
    }
    
    // 排序并返回前N个
    results.sort((a, b) => b.score.compareTo(a.score));
    
    return results.take(topN).map((r) => MatchResult(
      question: r.question,
      score: r.score,
      confidence: _getConfidence(r.score),
    )).toList();
  }
  
  /// 极速相似度计算（简化版）
  double _ultraFastSimilarity(String s1, String s2) {
    if (s1.isEmpty || s2.isEmpty) return 0.0;
    
    // 1. 完全匹配
    if (s1 == s2) return 1.0;
    
    // 2. 包含关系
    if (s1.contains(s2) || s2.contains(s1)) {
      final ratio = s1.length < s2.length 
          ? s1.length / s2.length 
          : s2.length / s1.length;
      return 0.9 + ratio * 0.1;
    }
    
    // 3. 快速LCS（限制长度）
    final maxLen = 50; // 限制计算长度
    final t1 = s1.length > maxLen ? s1.substring(0, maxLen) : s1;
    final t2 = s2.length > maxLen ? s2.substring(0, maxLen) : s2;
    
    final lcs = _fastLCS(t1, t2);
    return (2.0 * lcs) / (t1.length + t2.length);
  }
  
  /// 快速LCS（优化版）
  int _fastLCS(String s1, String s2) {
    if (s1.length < s2.length) {
      return _fastLCS(s2, s1);
    }
    
    final m = s1.length;
    final n = s2.length;
    
    // 使用短数组
    var prev = List<int>.filled(n + 1, 0);
    var curr = List<int>.filled(n + 1, 0);
    
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        if (s1[i - 1] == s2[j - 1]) {
          curr[j] = prev[j - 1] + 1;
        } else {
          curr[j] = curr[j - 1] > prev[j] ? curr[j - 1] : prev[j];
        }
      }
      // 交换
      final tmp = prev;
      prev = curr;
      curr = tmp;
    }
    
    return prev[n];
  }
  
  /// 获取置信度
  Confidence _getConfidence(double score) {
    if (score >= _highConfidenceThreshold) return Confidence.high;
    if (score >= _matchThreshold) return Confidence.medium;
    return Confidence.low;
  }
  
  /// 获取统计
  Map<String, dynamic> getStats() {
    return {
      'totalQueries': _totalQueries,
      'cacheHits': _cacheHits,
      'cacheHitRate': _totalQueries > 0 
          ? '${(_cacheHits * 100 / _totalQueries).toStringAsFixed(1)}%' 
          : '0%',
      'cacheSize': _cache.length,
      'indexSize': _keywordIndex.length,
    };
  }
  
  /// 清空缓存
  void clearCache() {
    _cache.clear();
    _cacheHits = 0;
    _totalQueries = 0;
  }
}

/// 匹配结果
class MatchResult {
  final Map<String, dynamic> question;
  final double score;
  final Confidence confidence;
  
  MatchResult({
    required this.question,
    required this.score,
    required this.confidence,
  });
  
  String get answer => question['answer'] as String;
  String get content => question['content'] as String;
  List<dynamic> get options => question['options'] as List<dynamic>;
  
  /// 获取答案内容
  String get answerContent {
    final label = answer;
    if (label.length > 1) return label; // 多选题
    
    final idx = label.codeUnitAt(0) - 'A'.codeUnitAt(0);
    if (idx >= 0 && idx < options.length) {
      return options[idx] as String;
    }
    return label;
  }
  
  @override
  String toString() => 
      'MatchResult(score: ${score.toStringAsFixed(3)}, confidence: $confidence)';
}

/// 置信度
enum Confidence { high, medium, low }

/// 带分数的结果
class ScoredResult {
  final int index;
  final Map<String, dynamic> question;
  final double score;
  
  ScoredResult({
    required this.index,
    required this.question,
    required this.score,
  });
}
