import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
from streamlit.logger import get_logger
import re
import string
from pathlib import Path
from wordcloud import WordCloud  # 导入wordcloud库
import matplotlib.pyplot as plt  # 用于显示词云图

#http://www.qstheory.cn/yaowen/2022-10/25/c_1129079926.htm

LOGGER = get_logger(__name__)

def clean_text(text):
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    text = text.strip()
    return text

def load_stopwords(filepath):
    stopwords = set()
    if filepath.is_file():
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                stopwords.add(line.strip())
    return stopwords

def segment(text, stopwords):
    punctuation = string.punctuation
    text = text.translate(str.maketrans('', '', punctuation))
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords]
    return words

def remove_html_tags(text):
    clean = re.compile('<.*?>')  # 正则表达式匹配HTML标签
    return re.sub(clean, '', text)

def extract_body_text(html):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('body').get_text()
    return text

def generate_wordcloud(words, max_words=100, max_font_size=200):
    # 创建词云对象
    wordcloud = WordCloud(
        font_path='simhei.ttf',  # 指定字体路径
        background_color='white',  # 背景颜色
        max_words=max_words,       # 显示的最大词数
        max_font_size=max_font_size,  # 字体最大大小
        random_state=42,            # 为了可重现性
        width=1600,                 # 宽度
        height=1200,                # 高度
        colormap='viridis'         # 颜色映射
    ).generate_from_frequencies(words)
    
    # 显示词云图
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.show()

def run():
    #st.set_page_config(
     #   page_title="Hello",
      #  page_icon="",
    #)

    #st.write("# 作业展示 ")

    url = st.text_input('Enter URL:')

    if url:
        r = requests.get(url)
        r.encoding = 'utf-8'
        text = r.text
        text = extract_body_text(text)
        
        text = remove_html_tags(text)
        text = clean_text(text)

        # 读取本地停用词文件
        stopwords_filepath = Path(__file__).parent / "stopwords.txt"
        stopwords = load_stopwords(stopwords_filepath)

        words = segment(text, stopwords)
        word_counts = Counter(words)
    
        # 生成词云图
        generate_wordcloud(word_counts)

        # ... 省略其他代码 ...

        # 显示词云图
        st.pyplot(plt)  # 使用st.pyplot来展示matplotlib生成的图表

        # ... 省略其他代码 ...

if __name__ == "__main__":
    run()
