import streamlit as st
import pandas as pd
from collections import Counter
import jieba
from streamlit.report_thread import get_report_ctx

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    return Counter(words).most_common(top_k)

# 定义读取文件内容的函数
def read_file(uploaded_file, file_type, encoding='utf-8'):
    comments = []
    try:
        if file_type == 'csv':
            # 为CSV文件指定正确的编码
            if encoding == 'gbk':
                data = pd.read_csv(uploaded_file, encoding='gbk')
            else:
                data = pd.read_csv(uploaded_file, encoding='utf-8')
            comments = data.iloc[:, 0].tolist()  # 假设第一列是评论文本
        elif file_type == 'txt':
            # 为TXT文件指定编码
            with open(uploaded_file, 'r', encoding=encoding) as f:
                text = f.read()
            comments = text.split()  # 假设文本中单词之间用空格分隔
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
    return comments

def main():
    st.title("文本分词与高频词统计")

    # 设置上传文件的按钮，接受CSV和TXT文件
    uploaded_file = st.file_uploader("请上传你的文件", type=["csv", "txt"])

    if uploaded_file is not None:
        # 确定文件类型
        file_type = uploaded_file.name.split('.')[-1]
        encoding = 'utf-8'  # 默认编码为utf-8

        # 读取文件内容
        comments = read_file(uploaded_file, file_type, encoding)

        if not comments:
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
