import streamlit as st
import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import os
import re

# 洗洗
def clean_text(text):
    # 使用正则表达式去除非字母数字字符
    cleaned_text = ' '.join(re.findall(r'\b\w+\b', text))
    return cleaned_text

# 定义加载停用词典的函数
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = set(word.strip() for word in file.readlines())
    return stopwords

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义生成词云图的函数
def generate_wordcloud(text, font_path, max_words=200):
    # 使用jieba进行分词
    words = jieba.lcut(text)
    # 清洗
    text = clean_text(text)
    # 加载停用词典
    stopwords = load_stopwords('stopwords.txt')
    # 去除停用词
    filtered_words = remove_stopwords(words, stopwords)
    # 将过滤后的词语重新组合成字符串
    filtered_text = ' '.join(filtered_words)
    
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=max_words,
        width=800,
        height=600
    ).generate(filtered_text)
    
    # 显示词云图
    image = wc.to_image()
    return image


# 读取文件内容的函数
def read_file(file, file_type):
    text = None  # 初始化text变量
    try:
        if file_type == '.csv':
            encodings = ['utf-8', 'gbk', 'windows-1252', 'iso-8859-1', 'ascii', 'big5', 'euc-kr', 'shift_jis']
            for enc in encodings:
                try:
                    data = pd.read_csv(file, header=None, encoding=enc)
                    text = ' '.join(str(row[0]) for row in data.values)  # 假设我们只关心第一列
                    break  # 如果成功读取，跳出循环
                except UnicodeDecodeError:
                    continue
        elif file_type == '.txt':
            encodings = ['utf-8', 'gbk', 'windows-1252', 'iso-8859-1', 'ascii', 'big5', 'euc-kr', 'shift_jis']
            for enc in encodings:
                try:
                    file.seek(0)  # 重置文件指针到文件开头
                    text = file.read().decode(enc)
                    # 清洗文本
                    text = clean_text(text)
                    break  # 如果成功读取，跳出循环
                except (UnicodeDecodeError, LookupError):
                    continue
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
    return text

def clean_text(text):
    # 使用正则表达式去除非字母数字字符
    cleaned_text = ' '.join(re.findall(r'\b\w+\b', text))
    return cleaned_text

# 定义生成词频统计的函数
def generate_word_frequency(words, max_words=50):
    # 使用Counter计算词频
    word_counts = Counter(words)
    # 获取出现频率最高的max_words个词
    top_words = word_counts.most_common(max_words)
    return top_words

# 主函数
def main():
    st.title("文本文件词云图生成器")
    
    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的文件 (CSV或TXT)", type=["csv", "txt"])
    
    if uploaded_file is not None:
        # 获取文件扩展名
        file_type = os.path.splitext(uploaded_file.name)[1].lower()
        
        # 读取文件内容
        text = read_file(uploaded_file, file_type)
        
        if text is not None:
            # 清洗文本
            text = clean_text(text)
            
            # 设置中文字体路径
            font_path = 'simhei.ttf'  # 请确保这个路径是正确的
            
            # 使用jieba进行分词
            words = jieba.lcut(text)
            # 加载停用词典
            stopwords = load_stopwords('stopwords.txt')
            # 去除停用词
            filtered_words = remove_stopwords(words, stopwords)
            
            # 计算词频
            word_counts = generate_word_frequency(filtered_words, max_words=50)
            # 将词频数据转换为DataFrame
            top_words_df = pd.DataFrame(word_counts, columns=['Word', 'Frequency'])
            
            # 显示高频词统计表格
            st.write("高频词统计:")
            st.dataframe(top_words_df)
            
            # 生成词云图
            image = generate_wordcloud(text, font_path)
            
            # 显示词云图
            st.image(image, use_column_width=True)

# 确保主函数在脚本的最后调用
if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
