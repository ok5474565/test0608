import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
from streamlit.logger import get_logger
import re
import string
from pathlib import Path
from bs4 import BeautifulSoup

# 获取日志器
LOGGER = get_logger(__name__)

def clean_text(text):
    text = text.replace('\n', '').replace(' ', '')
    text = ''.join(ch for ch in text if ch not in string.punctuation)
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
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords and len(word) > 1]
    return words

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_body_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('body').get_text()
    return text

def run():
    # 设置页面标题和图标（可选）
    st.set_page_config(page_title="文本分析工具", page_icon=":bar_chart:")

    # 页面标题
    st.title("输入链接爬取内容统计词频条形图")

    # 用户输入新闻链接
    url = st.text_input('输入新闻URL：')

    # 初始化条形图配置字典
    bar_chart_options = {
        "title": {"text": "词语条形图"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {"type": "category", "axisLabel": {"interval": 0, "rotate": 45}, "splitLine": {"show": False}},
        "yAxis": {"type": "value", "splitLine": {"show": False}},
        "series": [{"type": "bar"}],
    }

    # 添加滑块，允许用户选择 top N 个词语
    top_n = st.slider('选择要显示的 top N 个词语:', min_value=1, max_value=50, value=20)

    if url:
        try:
            # 发送请求获取网页内容
            response = requests.get(url)
            response.raise_for_status()  # 确保请求成功
            html_content = response.text

            # 提取正文文本并清理
            body_text = extract_body_text(html_content)
            text = remove_html_tags(body_text)
            text = clean_text(text)

            # 加载停用词
            stopwords_filepath = Path(__file__).parent / "stopwords.txt"
            stopwords = load_stopwords(stopwords_filepath)

            # 分词
            words = segment(text, stopwords)

            # 统计词频
            word_counts = Counter(words)

            # 获取 top N 个词语及其频率
            top_words = word_counts.most_common(top_n)

            # 更新条形图配置
            bar_chart_options["xAxis"]["data"] = [word for word, _ in top_words]
            bar_chart_options["series"][0]["data"] = [count for _, count in top_words]

            # 显示图表
            st_echarts(bar_chart_options, height='600px')

        except requests.RequestException as e:
            st.error(f"请求错误: {e}")
        except Exception as e:
            st.error(f"发生错误: {e}")

if __name__ == "__main__":
    run()
