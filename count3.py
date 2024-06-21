import streamlit as st
import pandas as pd
from collections import Counter
import jieba
import os

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    counter = Counter(words)
    return counter.most_common(top_k)

# 定义读取文件内容的函数
def read_file(file, file_type, encodings=['utf-8', 'gbk', 'gb2312', 'big5', 'iso-8859-1']):
    text = None
    for encoding in encodings:
        try:
            if file_type == '.csv':
                data = pd.read_csv(file, header=None, encoding=encoding)
                texts = [str(row[0]).rstrip() for row in data.values]  # 假设只关心第一列
                text = ' '.join(texts)
            elif file_type == '.txt':
                with open(file.name, 'r', encoding=encoding) as f:
                    text = f.read()
            break  # 如果成功读取，跳出循环
        except UnicodeDecodeError:
            continue  # 如果编码错误，尝试下一个编码
        except Exception as e:
            st.error(f"读取文件时发生错误：{e}")
            return None
    return text

def main():
    st.title("评论文本分词与高频词统计")

    # 设置上传文件的按钮，接受CSV和TXT文件
    uploaded_file = st.file_uploader("请上传你的文件 (CSV或TXT)", type=["csv", "txt"])

    if uploaded_file is not None:
        file_type = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')  # 去除扩展名前的点

        # 读取文件内容
        text = read_file(uploaded_file, file_type)

        if text is not None:
            # 以下代码与原代码相同，处理文本、分词、统计高频词等
            words = []
            for line in text.splitlines():  # 按行处理文本
                line_stripped = line.strip()
                if line_stripped:  # 确保不处理空行
                    comment_words = jieba.lcut(line_stripped)
                    words.extend(comment_words)

            # 过滤掉空字符串和长度为1的单字符
            words = [word for word in words if word and len(word) > 1]

            # 尝试读取停用词典文件
            try:
                with open('stopwords.txt', 'r', encoding='utf-8') as f:
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
