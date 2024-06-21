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
def read_file(uploaded_file, file_type, encoding='utf-8'):
    text = None
    common_encodings = ['utf-8', 'GBK', 'ISO-8859-1', 'Windows-1252', 'big5', 'latin1']
    
    for encoding in common_encodings:
        try:
            if file_type == '.csv':
                # 使用上传文件的read()方法读取内容，并尝试使用当前编码解析CSV
                content = uploaded_file.read()
                data = pd.read_csv(io.StringIO(content.decode(encoding)), header=None)
                text = ' '.join(str(row[0]).rstrip() for row in data.values)  # 假设我们只关心第一列
                break
            elif file_type == '.txt':
                # 使用上传文件的read()方法读取内容，并尝试使用当前编码解析TXT
                content = uploaded_file.read()
                text = ' '.join(line.decode(encoding).rstrip() for line in content.splitlines())
                break
        except UnicodeDecodeError:
            continue  # 如果解码错误，尝试下一个编码格式

    if text is None:
        st.error("无法读取文件，请检查文件格式或编码。")

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
        
        # 读取文件内容，自动尝试不同的编码格式
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


