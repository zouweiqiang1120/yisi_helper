import re
import json

def clean_text(text):
    """清理文本"""
    return text.strip().replace('"', '\\"').replace('\n', ' ')

def parse_all_questions(text):
    """解析所有题目"""
    questions = []
    lines = text.split('\n')
    
    current_question = None
    current_options = []
    current_answer = ""
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # 检测题目
        is_new_question = False
        
        # 模式1: 包含括号的题目
        if '（）' in line or '()' in line:
            is_new_question = True
            # 检查行尾是否有答案
            match = re.search(r'\s+([A-D])$', line)
            if match:
                current_answer = match.group(1)
                current_question = line[:match.start()].strip()
            else:
                current_question = line
                current_answer = ""
        
        # 模式2: 判断题
        elif '对;错' in line or (line.endswith('对') and len(line) < 100) or (line.endswith('错') and len(line) < 100):
            is_new_question = True
            if line.endswith('对') or line.endswith('错'):
                current_answer = line[-1]
                current_question = line[:-1].strip()
            else:
                current_question = line
                current_answer = ""
        
        if is_new_question:
            # 保存上一题
            if current_question and i > 0:
                q_type = "single"
                if current_answer and (';' in current_answer or len(current_answer) > 1):
                    q_type = "multiple"
                elif '对' in current_question or '错' in current_question:
                    if not current_options or current_options == ['对', '错']:
                        q_type = "judge"
                        current_options = ['对', '错', '', '']
                
                if current_question:
                    questions.append({
                        'content': clean_text(current_question),
                        'options': current_options[:4] if current_options else ['', '', '', ''],
                        'answer': current_answer,
                        'type': q_type
                    })
            
            # 开始新题目
            current_options = []
            i += 1
            
            # 读取选项
            while i < len(lines):
                opt_line = lines[i].strip()
                if not opt_line:
                    i += 1
                    continue
                
                # 检测选项
                if opt_line.startswith(('A', 'B', 'C', 'D')):
                    opt_content = opt_line[1:].strip().strip(';')
                    current_options.append(opt_content)
                    i += 1
                # 检测多选题答案
                elif re.match(r'^[A-D](;[A-D])*$', opt_line):
                    current_answer = opt_line
                    i += 1
                else:
                    break
        else:
            i += 1
    
    # 保存最后一题
    if current_question:
        q_type = "single"
        if current_answer and (';' in current_answer or len(current_answer) > 1):
            q_type = "multiple"
        elif '对' in current_question or '错' in current_question:
            if not current_options or current_options == ['对', '错']:
                q_type = "judge"
                current_options = ['对', '错', '', '']
        
        questions.append({
            'content': clean_text(current_question),
            'options': current_options[:4] if current_options else ['', '', '', ''],
            'answer': current_answer,
            'type': q_type
        })
    
    return questions

def generate_dart_code(questions, output_file):
    """生成Dart代码文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('// 完整的LLDPE装置操作工考试题库\n')
        f.write('// 自动生成，共 {} 道题目\n\n'.format(len(questions)))
        f.write('const List<Map<String, dynamic>> allQuestions = [\n')
        
        for i, q in enumerate(questions):
            f.write('  {\n')
            f.write('    "content": "{}",\n'.format(q['content']))
            f.write('    "options": ["{}", "{}", "{}", "{}"],\n'.format(
                q['options'][0] if len(q['options']) > 0 else '',
                q['options'][1] if len(q['options']) > 1 else '',
                q['options'][2] if len(q['options']) > 2 else '',
                q['options'][3] if len(q['options']) > 3 else ''
            ))
            f.write('    "answer": "{}",\n'.format(q['answer']))
            f.write('    "type": "{}"\n'.format(q['type']))
            f.write('  }')
            if i < len(questions) - 1:
                f.write(',')
            f.write('\n')
        
        f.write('];\n\n')
        
        # 添加统计函数
        f.write('// 获取完整题库\n')
        f.write('List<Map<String, dynamic>> getAllQuestions() {\n')
        f.write('  return allQuestions;\n')
        f.write('}\n\n')
        
        f.write('// 获取题库统计\n')
        f.write('Map<String, dynamic> getQuestionBankStats() {\n')
        f.write('  int single = allQuestions.where((q) => q["type"] == "single").length;\n')
        f.write('  int multiple = allQuestions.where((q) => q["type"] == "multiple").length;\n')
        f.write('  int judge = allQuestions.where((q) => q["type"] == "judge").length;\n')
        f.write('  return {\n')
        f.write('    "total": allQuestions.length,\n')
        f.write('    "single": single,\n')
        f.write('    "multiple": multiple,\n')
        f.write('    "judge": judge,\n')
        f.write('  };\n')
        f.write('}\n')
    
    print(f"已生成Dart文件: {output_file}")

# 主程序
if __name__ == '__main__':
    import sys
    
    # 读取完整题库
    with open('questions_full.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("正在解析完整题库...")
    questions = parse_all_questions(content)
    
    print(f"\n解析完成!")
    print(f"总题数: {len(questions)}")
    print(f"单选题: {sum(1 for q in questions if q['type'] == 'single')} 道")
    print(f"多选题: {sum(1 for q in questions if q['type'] == 'multiple')} 道")
    print(f"判断题: {sum(1 for q in questions if q['type'] == 'judge')} 道")
    
    # 生成Dart代码
    generate_dart_code(questions, '../lib/data/all_questions.dart')
    
    # 同时保存JSON备份
    with open('questions_full.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print("\n文件已生成:")
    print("- ../lib/data/all_questions.dart (Dart代码)")
    print("- questions_full.json (JSON备份)")
