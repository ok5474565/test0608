import streamlit as st
import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import os
import chardet

# 定义加载停用词典的函数
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = set(word.strip() for word in file.readlines())
    return stopwords

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义生成词云图的函数
def generate_wordcloud(text, font_path):
    # 使用jieba进行分词
    words = jieba.lcut(text)
    # 加载停用词典
    stopwords = load_stopwords('stopwords.txt')
    # 去除停用词
    filtered_words = remove_stopwords(words, stopwords)
    # 将过滤后的词语重新组合成字符串
    filtered_text = ' '.join(filtered_words)
    
    # 创建词云对象，并生成词云图
    wc = WordCloud(font_path=font_path, background_color='white').generate(filtered_text)
    return wc.to_image()

# 读取文件内容的函数
def detect_and_read_csv(uploaded_file):
    # 读取文件的一定比例来检测编码
    chunk = uploaded_file.read(5000)  # 读取前5000字节作为样本
    detected_encoding = chardet.detect(chunk)['encoding']
    uploaded_file.seek(0)  # 重置文件指针到开始位置
    
    # 使用检测到的编码尝试读取CSV文件
    try:
        data = pd.read_csv(uploaded_file, header=None, encoding=detected_encoding)
    except UnicodeDecodeError:
        # 如果自动检测的编码失败，回退到尝试其他常见编码
        common_encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'iso-8859-1']
        for encoding in common_encodings:
            try:
                data = pd.read_csv(uploaded_file, header=None, encoding=encoding)
                break  # 如果读取成功，跳出循环
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("无法识别文件编码")
    
    # 假设只关心第一列数据
    text = ' '.join(str(row[0]).rstrip() for row in data.values if row[0] != '')
    return text

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    # 去除空白字符和换行符，并去除停用词
    return [word.strip() for word in words if word.strip() and word not in stopwords_set]

# 定义生成词频统计的函数
def generate_word_frequency(words, max_words=50):
    # 使用Counter计算词频
    word_counts = Counter(words)
    # 获取出现频率最高的max_words个词
    top_words = word_counts.most_common(max_words)
    return top_words

# 主函数
# 主函数
def main():
    st.title("自动编码检测的文本文件词云图生成器")
    uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
    if uploaded_file is not None:
        text = detect_and_read_csv(uploaded_file)
        # 显示生成的词云图
        image = generate_wordcloud(text, font_path)
        st.image(image, use_column_width=True)

if __name__ == '__main__':
    main()
