import numpy as np
import jieba
import requests
import streamlit as st
from collections import Counter
import re
import string
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 定义一个用于文本清洗的函数
def clean_text(text):
    text = text.replace('\n', ' ')
    text = text.replace(' ', ' ')
    text = text.strip()
    return text

# 定义一个加载停用词的函数
def load_stopwords(filepath):
    stopwords = set()
    if filepath.is_file():
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                stopwords.add(line.strip())
    return stopwords

# 定义一个文本分词并去除停用词的函数
def segment(text, stopwords):
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords]
    return words

# 定义一个去除HTML标签的函数
def remove_html_tags(text):
    pattern = re.compile('<.*?>')  # 正则表达式匹配HTML标签
    return re.sub(pattern, '', text)

# 定义一个提取网页正文文本的函数
def extract_body_text(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('body').get_text()
    return text

# 定义一个生成词云的函数
def generate_wordcloud(word_counts, top_k, font_path):
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=top_k,
        max_font_size=80,  # 设置最大字体大小
        scale=5,  # 增加图像的清晰度，具体值可以根据结果调整
        random_state=42,
        width=1600,
        height=1200,
        colormap='viridis'
    ).generate_from_frequencies(word_counts)
    
    # 使用WordCloud的to_image方法获取高质量图像
    image = wc.to_image()

    return image

# 定义主函数
def run():
    st.title("输入链接爬取内容生成词云图")

    # 用户输入网址
    url = st.text_input('Enter URL:')

    # 从侧边栏添加滑块控件
    top_k = st.sidebar.slider("选择要显示的词数量", 10, 200, 50)

    if url:
        # 发送HTTP请求
        response = requests.get(url)
        response.encoding = 'utf-8'
        html_content = response.text

        # 清洗文本
        text = extract_body_text(html_content)
        text = remove_html_tags(text)
        text = clean_text(text)

        # 加载停用词
        stopwords_filepath = Path(__file__).parent / "stopwords.txt"
        stopwords = load_stopwords(stopwords_filepath)

        # 分词和统计词频
        words = segment(text, stopwords)
        word_counts = Counter(words)

        def update_wordcloud():
            plt.clf()  # 清除之前的图像
            # 重新生成词云图
            wc_image = WordCloud(
                font_path='simhei.ttf',  # 指定字体路径
                background_color='white',
                max_words=top_k,
                colormap='viridis'
            ).generate_from_frequencies(word_counts)

            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')

        # 初始生成词云图
        wc_image = generate_wordcloud(word_counts, top_k, font_path='simhei.ttf')

        # 用于显示词云图的占位符
        wordcloud_placeholder = st.empty()
        # 直接使用 st.image() 来显示图像
        wordcloud_placeholder.image(wc_image, use_column_width=True, caption='词云图')

if __name__ == "__main__":
    run()
