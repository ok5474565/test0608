import streamlit as st
import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import os

# 定义加载停用词典的函数
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = set(word.strip() for word in file.readlines())
    return stopwords

# 定义去停用词并统计词频的函数
def get_word_frequencies(text, stopwords_set):
    words = jieba.lcut(text)
    filtered_words = remove_stopwords(words, stopwords_set)
    word_freq = Counter(filtered_words)
    return word_freq

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义生成词云图的函数
def generate_wordcloud(word_freq, font_path, max_words=200):
    # 将Counter对象转换为字典，用于生成词云
    word_freq_dict = dict(word_freq)
    
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=max_words,
        width=800,
        height=600,
    ).generate_from_frequencies(word_freq_dict)
    
    # 显示词云图
    image = wc.to_image()
    
    # 获取高频词列表
    top_words = word_freq.most_common(max_words)
    
    return image, top_words

# 读取文件内容的函数
def read_file(file, file_type):
    text = None
    try:
        if file_type == '.csv':
            data = pd.read_csv(file, header=None, encoding='GBK')
            text = ' '.join(str(row[0]) for row in data.values)  # 假设只关心第一列
        elif file_type == '.txt':
            text = file.read().decode('utf-8')
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
    return text

# 主函数
def main():
    st.title("文本文件词云图及高频词统计")
    
    uploaded_file = st.file_uploader("请上传你的文件 (CSV或TXT)", type=["csv", "txt"])
    
    if uploaded_file is not None:
        file_type = os.path.splitext(uploaded_file.name)[1].lower()
        text = read_file(uploaded_file, file_type)
        
        if text:
            # 设置中文字体路径
            font_path = 'simhei.ttf'
            
            # 加载停用词典
            stopwords = load_stopwords('stopwords.txt')
            
            # 统计词频
            word_freq = get_word_frequencies(text, stopwords)
            
            # 生成词云图和高频词列表
            image, top_words = generate_wordcloud(word_freq, font_path)
            
            # 显示词云图
            st.image(image, use_column_width=True)
            
            # 显示高频词
            st.write("高频词统计:")
            top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_words_df)

if __name__ == '__main__':
    main()
