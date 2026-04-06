import re
import json

def parse_questions_advanced(text):
    """高级题库解析器 - 处理复杂格式"""
    questions = []
    
    # 清理文本
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测题目模式：
        # 1. 包含"（）"或"()"的是选择题
        # 2. 以"对;错"结尾的是判断题
        # 3. 包含"？"或"?"的可能是题目
        
        is_question = False
        question_text = ""
        answer = ""
        q_type = "single"
        
        # 模式1: 标准选择题 "题目内容 答案"
        if '（）' in line or '()' in line:
            # 检查是否包含选项在同一行
            if ';' in line and any(c in line for c in ['A', 'B', 'C', 'D']):
                # 可能是选项和答案在同一行
                parts = line.rsplit(' ', 1)
                if len(parts) == 2 and parts[1] in ['A', 'B', 'C', 'D', '对', '错']:
                    question_text = parts[0]
                    answer = parts[1]
                    is_question = True
                else:
                    question_text = line
                    is_question = True
            else:
                # 检查行尾是否有答案
                match = re.search(r'([A-D])$', line)
                if match:
                    answer = match.group(1)
                    question_text = line[:match.start()].strip()
                else:
                    question_text = line
                is_question = True
        
        # 模式2: 判断题（包含"对;错"）
        elif '对;错' in line or line.endswith('对') or line.endswith('错'):
            if line.endswith('对') or line.endswith('错'):
                answer = line[-1]
                question_text = line[:-1].strip()
            else:
                question_text = line
            q_type = "judge"
            is_question = True
        
        # 模式3: 多选题（答案包含多个字母如"A;B;C"）
        elif re.search(r'[A-D](;[A-D])+', line):
            match = re.search(r'([A-D](?:;[A-D])+)$', line)
            if match:
                answer = match.group(1)
                question_text = line[:match.start()].strip()
                q_type = "multiple"
                is_question = True
        
        if is_question and question_text:
            # 读取选项
            options = []
            i += 1
            
            # 尝试读取下一行的选项
            while i < len(lines) and len(options) < 4:
                opt_line = lines[i]
                
                # 检测是否是选项行
                if opt_line.startswith('A') or opt_line.startswith('B') or \
                   opt_line.startswith('C') or opt_line.startswith('D'):
                    # 提取选项内容（去掉开头的字母和分隔符）
                    opt_content = opt_line[1:].strip()
                    opt_content = opt_content.strip(';').strip()
                    if opt_content:
                        options.append(opt_content)
                    i += 1
                # 检测是否是多选题的合并选项行（如"A;B;C;D"）
                elif re.match(r'^[A-D](;[A-D])*$', opt_line) and len(opt_line) <= 10:
                    # 这是答案行，不是选项
                    if not answer:
                        answer = opt_line
                    i += 1
                # 检测是否是以分号分隔的选项
                elif ';' in opt_line and len(options) == 0:
                    parts = opt_line.split('；')
                    if len(parts) == 0:
                        parts = opt_line.split(';')
                    for p in parts:
                        p = p.strip()
                        if p.startswith(('A', 'B', 'C', 'D')):
                            options.append(p[1:].strip())
                        elif p and len(options) < 4:
                            options.append(p)
                    i += 1
                else:
                    break
            
            # 补充选项到4个
            while len(options) < 4:
                options.append('')
            
            # 如果没有检测到答案，尝试从题目中提取
            if not answer:
                # 查找题目末尾的答案标记
                match = re.search(r'([A-D])$', question_text)
                if match:
                    answer = match.group(1)
                    question_text = question_text[:match.start()].strip()
            
            # 确定题型
            if q_type == "judge":
                options = ['对', '错', '', '']
            elif ';' in answer and len(answer) > 1:
                q_type = "multiple"
            elif answer in ['A', 'B', 'C', 'D']:
                q_type = "single"
            
            questions.append({
                'content': question_text,
                'options': options[:4],
                'answer': answer,
                'type': q_type
            })
        else:
            i += 1
    
    return questions

# 主程序
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python parse_full_questions.py <题库文件.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 读取题库文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("正在解析题库...")
    questions = parse_questions_advanced(content)
    
    # 保存为JSON
    output_file = input_file.replace('.txt', '.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n解析完成!")
    print(f"总题数: {len(questions)}")
    print(f"单选题: {sum(1 for q in questions if q['type'] == 'single')} 道")
    print(f"多选题: {sum(1 for q in questions if q['type'] == 'multiple')} 道")
    print(f"判断题: {sum(1 for q in questions if q['type'] == 'judge')} 道")
    print(f"\n已保存到: {output_file}")
    
    # 显示前5道题作为示例
    print("\n========== 前5道题目示例 ==========")
    for i, q in enumerate(questions[:5], 1):
        print(f"\n{i}. [{q['type']}] {q['content']}")
        print(f"   答案: {q['answer']}")
        if q['options'][0]:
            for j, opt in enumerate(q['options'], 1):
                if opt:
                    print(f"   {chr(64+j)}. {opt}")
