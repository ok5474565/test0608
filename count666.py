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

# 读取文件内容的函数
def read_file(file, file_type, encoding='utf-8'):
    comments = None  # 确保初始化comments变量
    try:
        if file_type == '.csv':
            data = pd.read_csv(file, header=None, encoding=encoding)
            comments = data.iloc[:, 0]  # 假设我们只关心第一列
        elif file_type == '.txt':
            comments = file.read().decode(encoding)
    except Exception as e:
        st.error(f"读取文件时发生错误：{e}")
        return None  # 添加返回值以处理错误情况
    return comments

# 主函数
def main():
    st.title("评论文本分词与高频词统计")

    # 设置上传文件的按钮，接受CSV和TXT文件
    uploaded_file = st.file_uploader("请上传你的文件 (CSV或TXT)", type=["csv", "txt"])

    if uploaded_file is not None:
        # 获取文件扩展名
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # 根据文件类型设置编码
        encoding = 'GBK' if file_type == 'csv' else 'utf-8'
        
        # 读取文件内容
        comments = read_file(uploaded_file, file_type, encoding)
        
        if comments is not None:
            # 使用jieba进行分词
            words = []
            if file_type == '.csv':
                for comment in comments:
                    comment_words = jieba.lcut(comment.strip())
                    words.extend(comment_words)
            elif file_type == '.txt':
                comment_words = jieba.lcut(comments)
                words.extend(comment_words)

            # 过滤掉空字符串和长度为1的单字符
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
