#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本摘要工具
支持: 提取关键句子、生成摘要、关键词提取
"""

import re
import os
from collections import Counter
import json


class TextSummarizer:
    """文本摘要器"""
    
    def __init__(self):
        self.stop_words = set([
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '这些', '那些', '这个', '那个', '之', '与', '及', '等', '或', '但', '而', '因为', '所以', '如果', '虽然', '这样', '那样', '这里', '那里', '什么', '怎么', '为什么', '如何', '谁', '哪', '个', '种', '类', '些', '者', '家', '员', '性', '化', '学', '中', '大', '小', '多', '少', '高', '低', '长', '短', '来', '过', '下', '前', '后', '内', '外', '里', '间', '边', '面', '头', '部', '身', '体', '心', '手', '眼', '口', '声', '地', '得', '着', '过', '但', '对', '将', '还', '把', '被', '让', '向', '从', '为', '以', '于', '则', '却', '并', '而', '且', '既', '又', '或', '因', '故', '若', '即', '使', '便', '就', '才', '乃', '均', '各', '每', '该', '此', '彼', '其', '另', '凡', '凡例', '有关', '相关', '关于', '对于', '由于', '根据', '按照', '通过', '经过', '随着', '为了', '为着', '除了', '除开', '除去', '有关', '相关'
        ])
    
    def split_sentences(self, text):
        """分句"""
        # 按句号、问号、感叹号分句
        sentences = re.split(r'[。！？\n]+', text)
        # 清理空句子和太短句子
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences
    
    def extract_keywords(self, text, top_k=10):
        """提取关键词"""
        # 提取中文词汇（简单版：2-4字词）
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        # 过滤停用词
        words = [w for w in words if w not in self.stop_words and len(w) > 1]
        # 统计词频
        word_freq = Counter(words)
        # 返回前k个
        return word_freq.most_common(top_k)
    
    def score_sentences(self, sentences, keywords):
        """给句子打分"""
        keyword_dict = dict(keywords)
        scores = []
        
        for i, sentence in enumerate(sentences):
            score = 0
            # 1. 关键词匹配得分
            words = re.findall(r'[\u4e00-\u9fa5]{2,4}', sentence)
            for word in words:
                if word in keyword_dict:
                    score += keyword_dict[word]
            
            # 2. 位置权重（开头和结尾的句子更重要）
            if i == 0 or i == len(sentences) - 1:
                score *= 1.5
            elif i < len(sentences) * 0.2 or i > len(sentences) * 0.8:
                score *= 1.2
            
            # 3. 句子长度惩罚（太长的句子减分）
            if len(sentence) > 100:
                score *= 0.8
            
            scores.append((i, sentence, score))
        
        return scores
    
    def summarize(self, text, ratio=0.3, min_sentences=3, max_sentences=10):
        """
        生成摘要
        
        Args:
            text: 原文本
            ratio: 摘要占原文比例
            min_sentences: 最少句子数
            max_sentences: 最多句子数
        """
        if not text or len(text) < 50:
            return text, []
        
        # 分句
        sentences = self.split_sentences(text)
        if len(sentences) <= min_sentences:
            return text, sentences
        
        # 提取关键词
        keywords = self.extract_keywords(text, top_k=20)
        
        # 句子打分
        scored_sentences = self.score_sentences(sentences, keywords)
        
        # 计算需要提取的句子数
        num_sentences = max(min_sentences, min(max_sentences, int(len(sentences) * ratio)))
        
        # 按分数排序，取前N个
        top_sentences = sorted(scored_sentences, key=lambda x: x[2], reverse=True)[:num_sentences]
        
        # 按原文顺序排列
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        # 生成摘要
        summary = '。'.join([s[1] for s in top_sentences]) + '。'
        
        return summary, [s[1] for s in top_sentences]
    
    def analyze_file(self, filepath):
        """分析文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"\n文件: {filepath}")
            print(f"原文长度: {len(text)} 字符")
            print(f"估计字数: {len(re.findall(r'[\u4e00-\u9fa5]', text))} 汉字")
            print("=" * 70)
            
            # 提取关键词
            keywords = self.extract_keywords(text, top_k=10)
            print("\n【关键词】")
            for word, freq in keywords:
                print(f"  {word}: {freq}次")
            
            # 生成摘要
            summary, key_sentences = self.summarize(text, ratio=0.2)
            
            print("\n【摘要】")
            print(summary)
            
            print("\n【关键句子】")
            for i, sentence in enumerate(key_sentences, 1):
                print(f"  {i}. {sentence}")
            
            # 保存结果
            output_file = filepath + '.summary.txt'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"原文文件: {filepath}\n")
                f.write(f"原文长度: {len(text)} 字符\n")
                f.write("=" * 70 + "\n\n")
                f.write("【关键词】\n")
                for word, freq in keywords:
                    f.write(f"  {word}: {freq}次\n")
                f.write("\n【摘要】\n")
                f.write(summary + "\n")
                f.write("\n【关键句子】\n")
                for i, sentence in enumerate(key_sentences, 1):
                    f.write(f"  {i}. {sentence}\n")
            
            print(f"\n结果已保存: {output_file}")
            return summary
            
        except Exception as e:
            print(f"错误: {e}")
            return None


def main():
    """主程序"""
    import sys
    
    print("=" * 70)
    print(" 文本摘要工具")
    print("=" * 70)
    
    summarizer = TextSummarizer()
    
    if len(sys.argv) > 1:
        # 从文件读取
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            summarizer.analyze_file(filepath)
        else:
            print(f"文件不存在: {filepath}")
    else:
        # 交互模式
        print("\n请输入文本（输入空行结束）:")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == '':
                    break
                lines.append(line)
            except EOFError:
                break
        
        text = '\n'.join(lines)
        
        if text.strip():
            print("\n" + "=" * 70)
            print("【关键词】")
            keywords = summarizer.extract_keywords(text, top_k=10)
            for word, freq in keywords:
                print(f"  {word}: {freq}次")
            
            print("\n【摘要】")
            summary, _ = summarizer.summarize(text)
            print(summary)
            print("=" * 70)
        else:
            print("未输入文本")


if __name__ == "__main__":
    main()
