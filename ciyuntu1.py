import streamlit as st
import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
import numpy as np

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
    # 加载停用词典
    stopwords = load_stopwords('stopwords.txt')
    # 去除停用词
    words = remove_stopwords(words, stopwords)
    # 将过滤后的词语重新组合成字符串
    filtered_text = ' '.join(words)
    
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

# 主函数
def main():
    st.title("CSV文件词云图生成器")
    
    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # 尝试使用GBK编码读取文件
            data = pd.read_csv(uploaded_file, header=None, encoding='GBK')
        except Exception as e:
            # 如果发生错误，打印错误信息并返回
            st.error(f"读取文件时发生错误：{e}")
            return
        
        # 将所有行的数据合并为一个字符串
        all_text = ' '.join(str(row[0]) for row in data.values)  # 假设我们只关心第一列
        
        # 设置中文字体路径
        font_path = 'simhei.ttf'  # 请确保这个路径是正确的
        
        # 生成词云图
        image = generate_wordcloud(all_text, font_path)
        
        # 显示词云图
        st.image(image, use_column_width=True)

if __name__ == '__main__':
    main()
