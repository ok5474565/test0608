import streamlit as st
import pandas as pd
from collections import Counter
import jieba
from io import TextIOWrapper

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    return Counter(words).most_common(top_k)

# 定义读取文件内容的函数，自动识别文件类型和尝试不同的编码
def read_file(uploaded_file, encoding='utf-8'):
    comments = None
    try:
        if uploaded_file.name.endswith('.csv'):
            # 使用TextIOWrapper来读取UploadedFile对象，并指定编码
            with TextIOWrapper(uploaded_file, encoding=encoding) as f:
                data = pd.read_csv(f)
                comments = data.iloc[:, 0]  # 假设第一列是评论文本
        elif uploaded_file.name.endswith('.txt'):
            # 使用指定编码读取TXT文件
            with open(uploaded_file, 'r', encoding=encoding) as file:
                text = file.read()
            comments = text.split()  # 假设每行是一个评论
    except UnicodeDecodeError:
        st.error(f"文件编码错误，请尝试使用其他编码重新上传文件。")
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
    return comments

def main():
    st.title("文本分词与高频词统计")

    # 设置上传文件的按钮，接受CSV和TXT文件
    uploaded_file = st.file_uploader("请上传你的文件", type=["csv", "txt"])

    if uploaded_file is not None:
        # 尝试使用utf-8编码读取文件
        comments_utf8 = read_file(uploaded_file, encoding='utf-8')
        # 如果utf-8读取失败，尝试使用GBK编码读取CSV文件，或ANSI编码读取TXT文件
        if comments_utf8 is None:
            if uploaded_file.name.endswith('.csv'):
                comments_gbk = read_file(uploaded_file, encoding='gbk')
            else:  # 文件名以.txt结尾
                comments_ansi = read_file(uploaded_file, encoding='ansi')
            # 根据文件类型选择正确的读取结果
            comments = comments_gbk if comments_gbk is not None else comments_ansi
        else:
            comments = comments_utf8

        if comments is None:
            st.error("文件读取失败，请确保文件格式正确且编码无误。")
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
