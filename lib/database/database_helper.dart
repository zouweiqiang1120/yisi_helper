import 'dart:io';
import 'package:flutter/services.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;
  
  // 数据库配置
  static const String _databaseName = 'questions.db';
  static const int _databaseVersion = 1;
  
  // 分批插入的大小
  static const int _batchSize = 500;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    // 获取应用文档目录
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final path = join(documentsDirectory.path, _databaseName);

    return await openDatabase(
      path,
      version: _databaseVersion,
      onCreate: _createDB,
      onUpgrade: _onUpgrade,
    );
  }

  Future _createDB(Database db, int version) async {
    // 创建题目表
    await db.execute('''
      CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        answer TEXT NOT NULL,
        type TEXT NOT NULL,
        category TEXT,
        keywords TEXT
      )
    ''');

    // 创建索引
    await db.execute('CREATE INDEX idx_content ON questions(content)');
    await db.execute('CREATE INDEX idx_keywords ON questions(keywords)');
    await db.execute('CREATE INDEX idx_category ON questions(category)');
    
    // 创建FTS虚拟表用于全文搜索
    await db.execute('''
      CREATE VIRTUAL TABLE questions_fts USING fts4(
        content,
        keywords
      )
    ''');
  }

  Future _onUpgrade(Database db, int oldVersion, int newVersion) async {
    // 数据库升级逻辑
    if (oldVersion < newVersion) {
      // 处理升级
    }
  }

  /// 批量插入题目（分批处理避免内存溢出）
  Future<void> batchInsertQuestions(List<Map<String, dynamic>> questions) async {
    final db = await database;
    
    await db.transaction((txn) async {
      final batch = txn.batch();
      
      for (int i = 0; i < questions.length; i++) {
        final q = questions[i];
        
        // 提取关键词用于搜索
        final keywords = _extractKeywords(q['content'] as String);
        
        batch.insert('questions', {
          'content': q['content'],
          'option_a': q['options'][0] ?? '',
          'option_b': q['options'][1] ?? '',
          'option_c': q['options'][2] ?? '',
          'option_d': q['options'][3] ?? '',
          'answer': q['answer'],
          'type': q['type'],
          'category': q['category'] ?? '通用',
          'keywords': keywords,
        });
        
        // 每_batchSize条执行一次
        if ((i + 1) % _batchSize == 0) {
          await batch.commit(noResult: true);
          batch.clear();
        }
      }
      
      // 提交剩余的数据
      await batch.commit(noResult: true);
    });
    
    // 同步到FTS表
    await _syncToFts();
  }

  /// 同步数据到FTS表
  Future<void> _syncToFts() async {
    final db = await database;
    await db.execute('DELETE FROM questions_fts');
    await db.execute('''
      INSERT INTO questions_fts (content, keywords)
      SELECT content, keywords FROM questions
    ''');
  }

  /// 提取关键词
  String _extractKeywords(String content) {
    // 移除标点符号和停用词
    final stopWords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'};
    
    String cleaned = content
        .replaceAll(RegExp(r'[\s\n\r（）()？?]'), '')
        .replaceAll(RegExp(r'[，。、；：""''！!]'), '');
    
    // 提取有意义的词（长度>=2）
    final words = <String>{};
    for (int i = 0; i < cleaned.length - 1; i++) {
      final char = cleaned[i];
      if (!stopWords.contains(char) && char.codeUnitAt(0) > 127) {
        // 尝试提取2-4字的词组
        for (int len = 2; len <= 4 && i + len <= cleaned.length; len++) {
          final word = cleaned.substring(i, i + len);
          if (word.length >= 2) {
            words.add(word);
          }
        }
      }
    }
    
    return words.join(' ');
  }

  /// 搜索题目（使用全文搜索）
  Future<List<Map<String, dynamic>>> searchQuestions(String query) async {
    final db = await database;
    
    // 清理查询文本
    final cleanQuery = query
        .replaceAll(RegExp(r'\s+'), '')
        .replaceAll(RegExp(r'[\n\r（）()？?]'), '');
    
    if (cleanQuery.isEmpty) return [];
    
    // 使用FTS全文搜索
    final ftsResults = await db.rawQuery('''
      SELECT q.* FROM questions q
      INNER JOIN questions_fts fts ON q.content = fts.content
      WHERE questions_fts MATCH ?
      LIMIT 20
    ''', [cleanQuery]);
    
    if (ftsResults.isNotEmpty) {
      return ftsResults;
    }
    
    // 如果FTS没有结果，使用LIKE模糊搜索
    return await db.query(
      'questions',
      where: 'content LIKE ? OR keywords LIKE ?',
      whereArgs: ['%$cleanQuery%', '%$cleanQuery%'],
      limit: 20,
    );
  }

  /// 智能搜索（支持相似度排序）
  Future<List<Map<String, dynamic>>> smartSearch(String query) async {
    final db = await database;
    
    // 获取候选题目
    final candidates = await searchQuestions(query);
    
    if (candidates.isEmpty) return [];
    
    // 计算相似度并排序
    final scoredResults = candidates.map((q) {
      final similarity = _calculateSimilarity(
        query,
        q['content'] as String,
      );
      return {
        ...q,
        'similarity': similarity,
      };
    }).toList();
    
    // 按相似度排序
    scoredResults.sort((a, b) => 
      (b['similarity'] as double).compareTo(a['similarity'] as double)
    );
    
    // 返回相似度>0.5的结果
    return scoredResults.where((q) => q['similarity'] > 0.5).toList();
  }

  /// 计算文本相似度（LCS算法）
  double _calculateSimilarity(String s1, String s2) {
    if (s1.isEmpty || s2.isEmpty) return 0.0;
    
    final cleanS1 = s1.replaceAll(RegExp(r'\s+'), '');
    final cleanS2 = s2.replaceAll(RegExp(r'\s+'), '');
    
    final lcs = _longestCommonSubsequence(cleanS1, cleanS2);
    return (2.0 * lcs) / (cleanS1.length + cleanS2.length);
  }

  int _longestCommonSubsequence(String s1, String s2) {
    if (s1.isEmpty || s2.isEmpty) return 0;
    
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
          curr[j] = curr[j - 1] > prev[j] ? curr[j - 1] : prev[j];
        }
      }
      // 交换数组
      final temp = prev;
      prev = curr;
      curr = temp;
    }
    
    return prev[n];
  }

  /// 获取题目总数
  Future<int> getQuestionCount() async {
    final db = await database;
    final result = await db.rawQuery('SELECT COUNT(*) as count FROM questions');
    return result.first['count'] as int;
  }

  /// 获取分类统计
  Future<Map<String, int>> getCategoryStats() async {
    final db = await database;
    final results = await db.rawQuery('''
      SELECT category, COUNT(*) as count 
      FROM questions 
      GROUP BY category
    ''');
    
    return Map.fromEntries(
      results.map((r) => MapEntry(
        r['category'] as String,
        r['count'] as int,
      ))
    );
  }

  /// 清空题库
  Future<void> clearQuestions() async {
    final db = await database;
    await db.delete('questions');
    await db.delete('questions_fts');
  }

  /// 检查数据库是否存在
  Future<bool> databaseExists() async {
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final path = join(documentsDirectory.path, _databaseName);
    return File(path).exists();
  }

  /// 获取数据库大小
  Future<int> getDatabaseSize() async {
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final path = join(documentsDirectory.path, _databaseName);
    final file = File(path);
    if (await file.exists()) {
      return await file.length();
    }
    return 0;
  }

  /// 关闭数据库
  Future<void> close() async {
    final db = await database;
    await db.close();
    _database = null;
  }

  /// 获取所有题目（用于匹配引擎）
  Future<List<Map<String, dynamic>>> getAllQuestionsForMatching() async {
    final db = await database;
    final results = await db.query('questions');
    
    return results.map((row) => {
      'content': row['content'],
      'options': [
        row['option_a'],
        row['option_b'],
        row['option_c'],
        row['option_d'],
      ],
      'answer': row['answer'],
      'type': row['type'],
      'category': row['category'],
    }).toList();
  }
}
