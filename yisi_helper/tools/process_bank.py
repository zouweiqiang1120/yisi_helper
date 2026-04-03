#!/usr/bin/env python3
"""
处理用户提供的完整题库内容
"""

import re
import json
import os

# 创建assets目录
os.makedirs('../assets', exist_ok=True)

# 读取完整题库内容
print("正在读取题库内容...")

# 这里应该包含用户提供的完整题库
# 由于内容太长，我们使用一个简化的示例
# 实际使用时需要将完整内容放入questions_full.txt

try:
    with open('questions_full.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"文件大小: {len(content)} 字符")
    print("开始解析...")
    
    questions = []
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 检测题目行
        is_question = False
        question_text = ""
        answer = ""
        q_type = "single"
        
        # 模式1: 包含括号的题目
        if '（）' in line or '()' in line:
            is_question = True
            match = re.search(r'\s+([A-D])$', line)
            if match:
                answer = match.group(1)
                question_text = line[:match.start()].strip()
            else:
                question_text = line
        
        # 模式2: 判断题
        elif '对;错' in line or (line.endswith('对') and len(line) < 200) or (line.endswith('错') and len(line) < 200):
            is_question = True
            q_type = "judge"
            if line.endswith('对') or line.endswith('错'):
                answer = line[-1]
                question_text = line[:-1].strip()
            else:
                question_text = line
        
        # 模式3: 多选题
        elif re.search(r'[A-D](;[A-D])+', line):
            match = re.search(r'([A-D](?:;[A-D])+)$', line)
            if match:
                is_question = True
                q_type = "multiple"
                answer = match.group(1)
                question_text = line[:match.start()].strip()
        
        if is_question and question_text:
            options = []
            i += 1
            
            while i < len(lines) and len(options) < 4:
                opt_line = lines[i].strip()
                
                if not opt_line:
                    i += 1
                    continue
                
                if opt_line.startswith(('A', 'B', 'C', 'D')):
                    opt_content = opt_line[1:].strip()
                    opt_content = opt_content.strip(';').strip('；')
                    if opt_content:
                        options.append(opt_content)
                    i += 1
                elif re.match(r'^[A-D](;[A-D])*$', opt_line) and len(opt_line) <= 15:
                    if not answer:
                        answer = opt_line
                    i += 1
                else:
                    break
            
            while len(options) < 4:
                options.append('')
            
            if q_type == "judge":
                options = ['对', '错', '', '']
            
            questions.append({
                'content': question_text,
                'options': options[:4],
                'answer': answer,
                'type': q_type,
                'category': 'LLDPE装置'
            })
        else:
            i += 1
    
    # 统计
    single = sum(1 for q in questions if q['type'] == 'single')
    multiple = sum(1 for q in questions if q['type'] == 'multiple')
    judge = sum(1 for q in questions if q['type'] == 'judge')
    
    print(f"\n解析完成!")
    print(f"总题数: {len(questions)}")
    print(f"单选题: {single}")
    print(f"多选题: {multiple}")
    print(f"判断题: {judge}")
    
    # 保存JSON
    output_file = '../assets/questions_full.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存到: {output_file}")
    
    # 显示前5道题
    print("\n前5道题目示例:")
    for i, q in enumerate(questions[:5], 1):
        print(f"\n{i}. [{q['type']}] {q['content'][:60]}...")
        print(f"   答案: {q['answer']}")

except FileNotFoundError:
    print("错误: 找不到 questions_full.txt 文件")
    print("请将完整题库内容保存到 questions_full.txt 文件")
    exit(1)

print("\n处理完成!")
