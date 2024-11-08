import streamlit as st
import pandas as pd
from collections import Counter
import jieba
from wordcloud import WordCloud
import os

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    return Counter(words).most_common(top_k)

# 定义读取TXT文件内容的函数，尝试多种编码格式
def read_txt_file(uploaded_file):
    encodings = ['utf-8', 'ANSI', 'gbk', 'gb2312']
    for encoding in encodings:
        try:
            text = uploaded_file.read().decode(encoding)
            text = text.replace('\r\n', ' ').replace('\n', ' ')
            return text.split()
        except Exception as e:
            st.warning(f"尝试用编码 {encoding} 读取TXT文件失败：{e}")
    st.error("无法读取TXT文件，请检查文件编码格式。")
    return None

# 定义读取CSV文件内容的函数，尝试多种编码格式
def read_csv_file(uploaded_file):
    encodings = ['utf-8', 'gbk', 'ANSI', 'gb2312']
    for encoding in encodings:
        try:
            data = pd.read_csv(uploaded_file, encoding=encoding)
            return [str(cell) for cell in data.iloc[:, 0].tolist()]  # 假设CSV文件只有一列评论
        except Exception as e:
            st.warning(f"尝试用编码 {encoding} 读取CSV文件失败：{e}")
    st.error("无法读取CSV文件，请检查文件编码格式。")
    return None

# 定义读取XLSX文件内容的函数
def read_xlsx_file(uploaded_file):
    try:
        data = pd.read_excel(uploaded_file)
        return [str(cell) for cell in data.iloc[:, 0].tolist()]  # 假设XLSX文件只有一列评论
    except Exception as e:
        st.error(f"读取XLSX文件时发生错误：{e}")
        return None

def main():
    st.title("多编码在线文本分词与词云图生成")

    # 设置上传文件的按钮，支持txt、csv和xlsx文件
    uploaded_file = st.file_uploader("请上传你的文件", type=["txt", "csv", "xlsx"])

    words = []
    if uploaded_file is not None:
        file_type = uploaded_file.type.split('/')[1]
        # 根据文件类型读取文件内容
        if file_type == 'plain':
            comments = read_txt_file(uploaded_file)
        elif file_type == 'csv':
            comments = read_csv_file(uploaded_file)
        elif file_type == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            comments = read_xlsx_file(uploaded_file)
        else:
            st.error("不支持的文件类型。")
            return

        if comments is None:
            return  # 如果文件读取失败，不执行后续操作

        # 处理文本、分词
        for comment in comments:
            comment_stripped = comment.strip()  # 移除首尾空白字符
            if comment_stripped:  # 确保不处理空字符串
                comment_words = jieba.lcut(comment_stripped)
                words.extend(comment_words)

    # 过滤掉空字符串和长度为1的单字符（通常是标点符号或特殊字符）
    words = [word for word in words if len(word) > 1]

    # 尝试读取停用词典文件
    try:
        with open('stopwords.txt', encoding='utf-8') as f:
            stopwords = f.read()
            stopwords_set = set(stopwords.splitlines())
    except FileNotFoundError:
        st.error("停用词典文件 'stopwords.txt' 未找到，请确保文件存在于同一目录下。")
        return

    # 去除停用词
    filtered_words = remove_stopwords(words, stopwords_set)

    # 检查 filtered_words 是否为空
    if not filtered_words:
        st.error("没有有效的词可以生成词云。")
        return

    # 设置要显示的词云词数量
    min_frequency = 30  # 词频最低阈值
    max_frequency = 200  # 词频最高阈值
    default_top_k = 50  # 默认显示的词数
    top_k = st.sidebar.slider("选择要显示的词数量", min_frequency, max_frequency, default_top_k)
    top_words = get_top_words(filtered_words, top_k)

    # 创建词云
    wc = WordCloud(font_path='simhei.ttf', max_words=max_frequency, background_color='white', width=1200, height=800)
    word_freq = {word: freq for word, freq in top_words}
    wc.generate_from_frequencies(word_freq)

    # 将词云转换为PIL图像对象
    pil_image = wc.to_image()

    # 显示词云图
    st.write("生成的词云图：")
    st.image(pil_image, use_column_width=True, caption='词云图')

if __name__ == '__main__':
    main()
