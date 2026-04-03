#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整题库处理工具
将原始题库文本转换为JSON格式
"""

import re
import json
import sys

def parse_full_questions(text):
    """解析完整题库"""
    questions = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 跳过空行和分隔线
        if not line or line.startswith('---') or line.startswith('==='):
            i += 1
            continue
        
        # 检测题目 - 包含括号的行
        if '（）' in line or '()' in line:
            # 提取题目和答案
            question_text = line
            answer = ""
            
            # 检查行尾是否有答案
            match = re.search(r'\s+([A-D])$', line)
            if match:
                answer = match.group(1)
                question_text = line[:match.start()].strip()
            
            # 读取选项
            options = []
            i += 1
            
            while i < len(lines) and len(options) < 4:
                opt_line = lines[i]
                
                # 检测选项行 (A/B/C/D开头)
                if opt_line.startswith(('A', 'B', 'C', 'D')):
                    # 去掉开头的字母和分隔符
                    opt_content = opt_line[1:].strip()
                    opt_content = opt_content.strip(';').strip('；')
                    if opt_content:
                        options.append(opt_content)
                    i += 1
                # 检测是否是答案行
                elif re.match(r'^[A-D](;[A-D])*$', opt_line) and len(opt_line) <= 10:
                    if not answer:
                        answer = opt_line
                    i += 1
                else:
                    break
            
            # 补充选项
            while len(options) < 4:
                options.append('')
            
            # 确定题型
            q_type = "single"
            if ';' in answer and len(answer) > 1:
                q_type = "multiple"
            
            if question_text:
                questions.append({
                    'content': question_text,
                    'options': options[:4],
                    'answer': answer,
                    'type': q_type,
                    'category': 'LLDPE装置'
                })
        
        # 检测判断题
        elif '对;错' in line or line.endswith('对') or line.endswith('错'):
            question_text = line
            answer = ""
            
            if line.endswith('对') or line.endswith('错'):
                answer = line[-1]
                question_text = line[:-1].strip()
            
            questions.append({
                'content': question_text,
                'options': ['对', '错', '', ''],
                'answer': answer,
                'type': 'judge',
                'category': 'LLDPE装置'
            })
            i += 1
        
        else:
            i += 1
    
    return questions

def main():
    print("=" * 60)
    print("易思培训题库转换工具")
    print("=" * 60)
    
    # 读取标准输入或文件
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print(f"\n正在读取文件: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("\n请粘贴题库内容，输入完成后按 Ctrl+D (Linux/Mac) 或 Ctrl+Z (Windows) 结束")
        content = sys.stdin.read()
    
    print("\n正在解析题目...")
    questions = parse_full_questions(content)
    
    # 统计
    single = sum(1 for q in questions if q['type'] == 'single')
    multiple = sum(1 for q in questions if q['type'] == 'multiple')
    judge = sum(1 for q in questions if q['type'] == 'judge')
    
    print(f"\n{'=' * 60}")
    print("解析结果")
    print(f"{'=' * 60}")
    print(f"总题数: {len(questions)} 道")
    print(f"  - 单选题: {single} 道")
    print(f"  - 多选题: {multiple} 道")
    print(f"  - 判断题: {judge} 道")
    
    # 保存JSON
    output_file = 'questions_full.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存到: {output_file}")
    
    # 显示示例
    print(f"\n{'=' * 60}")
    print("前3道题目示例")
    print(f"{'=' * 60}")
    for i, q in enumerate(questions[:3], 1):
        print(f"\n{i}. [{q['type']}] {q['content']}")
        print(f"   答案: {q['answer']}")
        if q['options'][0]:
            for j, opt in enumerate(q['options'], 1):
                if opt:
                    print(f"   {chr(64+j)}. {opt}")
    
    print(f"\n{'=' * 60}")
    print("处理完成！")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
