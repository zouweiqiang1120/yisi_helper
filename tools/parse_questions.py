import re
import json

def parse_questions(text):
    """解析题库文本"""
    questions = []
    
    # 按行分割
    lines = text.strip().split('\n')
    
    current_question = None
    current_options = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是题目（以字母或数字开头，包含问号或括号）
        if re.match(r'^[A-Z]', line) or '（）' in line or '()' in line:
            # 保存上一题
            if current_question and current_options:
                questions.append({
                    'content': current_question,
                    'options': current_options[:4] if len(current_options) >= 4 else current_options + [''] * (4 - len(current_options)),
                    'answer': '',
                    'type': 'single' if len(current_options) == 4 else 'multiple'
                })
            
            # 新题目
            parts = line.rsplit(' ', 1)
            if len(parts) == 2 and parts[1] in 'ABCD':
                current_question = parts[0]
                answer = parts[1]
                current_options = []
            else:
                current_question = line
                current_options = []
        
        # 检查是否是选项
        elif line.startswith('A') or line.startswith('B') or line.startswith('C') or line.startswith('D'):
            # 提取选项内容
            option_text = line[1:].strip().strip(';')
            if option_text:
                current_options.append(option_text)
    
    # 保存最后一题
    if current_question and current_options:
        questions.append({
            'content': current_question,
            'options': current_options[:4] if len(current_options) >= 4 else current_options + [''] * (4 - len(current_options)),
            'answer': '',
            'type': 'single' if len(current_options) == 4 else 'multiple'
        })
    
    return questions

# 读取题库文件
with open('questions.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 解析题目
questions = parse_questions(content)

# 保存为JSON
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"共解析出 {len(questions)} 道题目")
print("\n前5道题目示例：")
for i, q in enumerate(questions[:5], 1):
    print(f"\n{i}. {q['content']}")
    for j, opt in enumerate(q['options'], 1):
        print(f"   {chr(64+j)}. {opt}")
