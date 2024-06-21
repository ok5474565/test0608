import streamlit as st
import pandas as pd
import jieba
from collections import Counter
from wordcloud import WordCloud
from PIL import Image
import numpy as np

# 定义生成词云图的函数
def generate_wordcloud(text, font_path, max_words=200):
    # 使用jieba进行分词
    words = ' '.join(jieba.cut(text))
    
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=max_words,
        width=800,
        height=600
    ).generate(words)
    
    # 显示词云图
    image = wc.to_image()
    return image

# 主函数
def main():
    st.title("CSV文件词云图生成器")
    
    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
    
    if uploaded_file is not None:
        # 读取CSV文件内容
        data = pd.read_csv(uploaded_file, header=None)  # 假设没有列名
        
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
