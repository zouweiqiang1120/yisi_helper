#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易思培训题库转换工具
将原始题库文本转换为JSON格式
"""

import re
import json
import sys

def parse_questions(text):
    """解析题库文本"""
    questions = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测题目
        is_question = False
        question_text = ""
        answer = ""
        q_type = "single"
        
        # 模式1: 包含括号的题目
        if '（）' in line or '()' in line:
            is_question = True
            # 检查行尾是否有答案
            match = re.search(r'\s+([A-D])$', line)
            if match:
                answer = match.group(1)
                question_text = line[:match.start()].strip()
            else:
                question_text = line
        
        # 模式2: 判断题
        elif '对;错' in line or line.endswith('对') or line.endswith('错'):
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
            # 读取选项
            options = []
            i += 1
            
            while i < len(lines) and len(options) < 4:
                opt_line = lines[i]
                
                # 检测选项
                if opt_line.startswith(('A', 'B', 'C', 'D')):
                    opt_content = opt_line[1:].strip().strip(';')
                    if opt_content:
                        options.append(opt_content)
                    i += 1
                # 检测多选题答案
                elif re.match(r'^[A-D](;[A-D])*$', opt_line) and not answer:
                    answer = opt_line
                    i += 1
                else:
                    break
            
            # 补充选项
            while len(options) < 4:
                options.append('')
            
            # 判断题选项
            if q_type == "judge":
                options = ['对', '错', '', '']
            
            # 确定题型
            if ';' in answer and len(answer) > 1:
                q_type = "multiple"
            
            questions.append({
                'content': question_text,
                'options': options[:4],
                'answer': answer,
                'type': q_type,
                'category': 'LLDPE装置'
            })
        else:
            i += 1
    
    return questions

def main():
    if len(sys.argv) < 2:
        print("用法: python convert_questions.py <输入文件.txt> [输出文件.json]")
        print("示例: python convert_questions.py questions.txt questions.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.txt', '.json')
    
    print(f"正在读取文件: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)
    
    print("正在解析题目...")
    questions = parse_questions(content)
    
    print(f"\n解析完成!")
    print(f"总题数: {len(questions)}")
    print(f"单选题: {sum(1 for q in questions if q['type'] == 'single')} 道")
    print(f"多选题: {sum(1 for q in questions if q['type'] == 'multiple')} 道")
    print(f"判断题: {sum(1 for q in questions if q['type'] == 'judge')} 道")
    
    # 保存为JSON
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f"\n已保存到: {output_file}")
    except Exception as e:
        print(f"保存文件失败: {e}")
        sys.exit(1)
    
    # 显示前3道题作为示例
    print("\n========== 前3道题目示例 ==========")
    for i, q in enumerate(questions[:3], 1):
        print(f"\n{i}. [{q['type']}] {q['content']}")
        print(f"   答案: {q['answer']}")
        if q['options'][0]:
            for j, opt in enumerate(q['options'], 1):
                if opt:
                    print(f"   {chr(64+j)}. {opt}")

if __name__ == '__main__':
    main()
