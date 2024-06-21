import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_wordcloud(text):
    # 创建词云图
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def main():
    st.title('CSV to WordCloud App')
    
    # 文件上传
    file_uploader = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if file_uploader is not None:
        # 读取CSV文件，假设第一列是文本数据
        data = pd.read_csv(file_uploader, header=None)  # 没有列名，使用None
        
        # 提取第一列的文本数据
        text_data = ' '.join(str(v) for v in data.iloc[:, 0])
        
        # 创建词云图
        wordcloud = create_wordcloud(text_data)
        
        # 显示词云图
        st.write("Word Cloud:")
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

if __name__ == "__main__":
    main()
