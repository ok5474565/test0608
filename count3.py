import streamlit as st
import pandas as pd
from collections import Counter
import jieba

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    counter = Counter(words)
    return counter.most_common(top_k)

# 定义读取TXT文件内容的函数
def read_txt_file(uploaded_file, encoding='utf-8'):
    try:
        with open(uploaded_file, 'r', encoding=encoding) as file:
            text = file.read()
            # 替换换行符为空白字符
            text = text.replace('\r\n', ' ').replace('\n', ' ')
    except Exception as e:
        st.error(f"读取TXT文件时发生错误：{e}")
        return None
    return text

# 修改main函数以增加对TXT文件的支持
def main():
    st.title("评论文本分词与高频词统计")

    # 设置上传文件的按钮，接受CSV和TXT文件
    file_type = st.selectbox(
        "请选择文件类型",
        ["csv", "txt"]
    )
    
    if file_type == "csv":
        uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
    elif file_type == "txt":
        uploaded_file = st.file_uploader("请上传你的TXT文件", type=["txt"])
    
    if uploaded_file is not None:
        if file_type == "csv":
            # 读取CSV文件，假设第一列是评论文本
            data = pd.read_csv(uploaded_file, header=None, encoding='gbk')
            comments = data.iloc[:, 0]  # 获取评论文本列
        elif file_type == "txt":
            # 读取TXT文件
            text = read_txt_file(uploaded_file)
            if text is None:  # 如果读取TXT文件失败，则不进行后续处理
                return
            comments = [text]  # 将整个文本文件视为一条评论

        # 以下代码与原代码相同，处理文本、分词、统计高频词等
        words = []
        for comment in comments:
            comment_stripped = comment.strip()  # 移除首尾空白字符
            comment_words = jieba.lcut(comment_stripped)
            words.extend(comment_words)

        # 过滤掉空字符串和长度为1的单字符（通常是标点符号或特殊字符）
        words = [word for word in words if word and len(word) > 1]

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
        top_k = 20
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
