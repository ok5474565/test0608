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

def main():
    st.title("评论文本分词与高频词统计")

    # 设置上传文件的按钮，接受CSV文件
    uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
    
    if uploaded_file is not None:
        # 读取CSV文件，假设第一列是评论文本
        data = pd.read_csv(uploaded_file, header=None, names=['comment'])
        
        # 使用jieba进行分词，合并所有评论文本
        all_comments = ' '.join(data['comment'].astype(str))
        words = jieba.lcut(all_comments)
        
        # 读取停用词典文件
        with open('stopwords.txt', 'encoding="utf-8"') as f:
            stopwords = f.read()
            stopwords_set = set(stopwords.splitlines())

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