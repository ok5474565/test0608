import streamlit as st
import pandas as pd
from collections import Counter
import jieba

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    return Counter(words).most_common(top_k)

# 定义读取文件内容的函数
def read_file(file, file_type, encoding):
    try:
        if file_type == 'csv':
            data = pd.read_csv(file, header=None, encoding=encoding)
            return [data.iloc[:, 0].tolist()]  # 假设CSV文件只有一列评论
        elif file_type == 'txt':
            with open(file, 'r', encoding=encoding) as f:
                text = f.read()
            return text.split()  # 假设TXT文件中的单词以空格分隔
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
        return None

def main():
    st.title("文本分词与高频词统计")

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

    encoding_type = st.selectbox(
        "请选择文件编码",
        encoding_options
    )

    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的文件", type=[file_type])

    if uploaded_file is not None:
        # 读取文件内容
        comments = read_file(uploaded_file, file_type, encoding_type)
        if comments is None:
            st.error("文件读取失败，请检查文件和编码格式。")
            return



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

        # 设置要统计的高频词数量
        top_k = st.sidebar.slider("选择要显示的高频词数量", 1, 100, 20)
        top_words = get_top_words(filtered_words, top_k)

        # 创建条形图的数据框
        top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])

        # 显示高频词
        st.write("高频词统计结果：")
        st.dataframe(top_words_df)

        # 生成条形图
        st.bar_chart(top_words_df.set_index('Word')['Frequency'])

if __name__ == '__main__':
    main()
