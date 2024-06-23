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

# 定义自动尝试多种编码格式读取文件的函数
def read_file_with_encodings(uploaded_file, read_function):
    encodings = ["utf-8", "ANSI", "gbk"]
    for encoding in encodings:
        try:
            return read_function(uploaded_file, encoding)
        except Exception as e:
            st.warning(f"尝试使用编码 {encoding} 读取文件失败：{e}")
    st.error("无法读取文件，请确认文件编码格式。")
    return None

# 定义读取TXT文件内容的函数
def read_txt_file(uploaded_file, encoding):
    text = uploaded_file.read().decode(encoding)
    text = text.replace('\r\n', ' ').replace('\n', ' ')
    return text.split()  # 假设TXT文件中的单词以空格分隔

# 定义读取CSV文件内容的函数
def read_csv_file(uploaded_file, encoding):
    data = pd.read_csv(uploaded_file, encoding=encoding)
    return [str(cell) for cell in data.iloc[:, 0].tolist()]  # 假设CSV文件只有一列评论

# 定义读取XLSX文件内容的函数
def read_xlsx_file(uploaded_file):
    data = pd.read_excel(uploaded_file)
    return [str(cell) for cell in data.iloc[:, 0].tolist()]  # 假设XLSX文件只有一列评论

def main():
    st.title("在线文本分词与高频词统计小程序")

    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的文件", type=["txt", "csv", "xlsx"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]

        # 根据文件类型读取文件内容
        if file_type == 'txt':
            comments = read_file_with_encodings(uploaded_file, read_txt_file)
        elif file_type == 'csv':
            comments = read_file_with_encodings(uploaded_file, read_csv_file)
        elif file_type == 'xlsx':
            comments = read_xlsx_file(uploaded_file)
        else:
            st.error("不支持的文件类型。")
            return

        if comments is None:
            return  # 如果文件读取失败，不执行后续操作

        # 处理文本、分词、统计高频词等
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
