import streamlit as st
import pandas as pd
from collections import Counter
import jieba
from wordcloud import WordCloud

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    return Counter(words).most_common(top_k)

# 定义读取TXT文件内容的函数
def read_txt_file(uploaded_file, encoding):
    try:
        text = uploaded_file.read().decode(encoding)
        text = text.replace('\r\n', ' ').replace('\n', ' ')
        return text.split()
    except Exception as e:
        st.error(f"读取TXT文件时发生错误：{e}")
        return None

# 定义读取CSV文件内容的函数
def read_csv_file(uploaded_file, encoding):
    try:
        data = pd.read_csv(uploaded_file, encoding=encoding)
        return [str(cell) for cell in data.iloc[:, 0].tolist()]  # 假设CSV文件只有一列评论
    except Exception as e:
        st.error(f"读取CSV文件时发生错误：{e}")
        return None

def main():
    st.title("文本分词与词云图生成")

    # 第一个下拉选项：选择文件类型
    file_type = st.selectbox(
        "请选择文件类型",
        ["txt", "csv"]
    )

    # 根据选择的文件类型，设置第二个下拉选项的选项内容
    if file_type == "txt":
        encoding_options = ["utf-8", "ANSI"]
    else:  # file_type == "csv"
        encoding_options = ["utf-8", "gbk"]

    selected_encoding = st.selectbox("请选择文件编码", encoding_options)

    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的文件", type=[file_type])

    if uploaded_file is not None:
        # 根据文件类型读取文件内容
        if file_type == 'txt':
            comments = read_txt_file(uploaded_file, selected_encoding)
        else:  # file_type == 'csv'
            comments = read_csv_file(uploaded_file, selected_encoding)

        if comments is None:
            return  # 如果文件读取失败，不执行后续操作


        # 以下代码与原代码相同，处理文本、分词、统计高频词等
        words = []
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

    # 确保 filtered_words 不是 None
    if filtered_words is None:
        st.error("处理文本时发生错误，未能生成词云。")
        return

    # 设置要显示的词云词数量
    min_frequency = 30  # 词频最低阈值
    max_frequency = 200  # 词频最高阈值
    default_top_k = 50  # 默认显示的词数
    top_k = st.sidebar.slider("选择要显示的词数量", min_frequency, max_frequency, default_top_k)
    top_words = get_top_words(filtered_words, top_k)

    # 过滤掉频率低于设定阈值的词
    filtered_words = [word for word, freq in top_words if freq >= min_frequency]

    # 创建词云
    wordcloud = WordCloud(font_path=font_path).generate_from_frequencies(dict(filtered_words))

    # 显示词云图
    st.write("生成的词云图：")
    st.image(wordcloud.to_image(), use_column_width=True)

if __name__ == '__main__':
    main()
