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
def read_file(file, file_type):
    text = None  # 初始化text变量
    common_encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'iso-8859-1']  # 常见的编码格式列表
    for encoding in common_encodings:
        try:
            if file_type == '.csv':
                data = pd.read_csv(file, header=None, encoding=encoding)
                texts = [str(row[0]).rstrip() for row in data.values]  # 假设我们只关心第一列
                text = ' '.join(texts)
            elif file_type == '.txt':
                with open(file, 'r', encoding=encoding) as f:
                    text = f.read()
            if text is not None:
                break  # 如果成功读取文件，则跳出循环
        except UnicodeDecodeError:
            continue  # 如果编码错误，继续尝试下一个编码
        except Exception as e:
            st.error(f"读取文件时发生错误：{e}")
            return None
    return text

def main():
    st.title("评论文本分词与高频词统计")
    
    # 设置上传文件的按钮，接受CSV和TXT文件
    uploaded_file = st.file_uploader("请上传你的文件 (CSV或TXT)", type=["csv", "txt"])
    
    if uploaded_file is not None:
        # 获取文件扩展名
        file_type = os.path.splitext(uploaded_file.name)[1].lower()
        
        # 读取文件内容
        text = read_file(uploaded_file, file_type)
        
        if text is not None:
            # 以下代码与原代码相同，处理文本、分词、统计高频词等
            # ...
            # 确保你将原始代码中的剩余部分放在这里，包括jieba分词、停用词过滤、高频词统计和可视化

if __name__ == '__main__':
    main()
