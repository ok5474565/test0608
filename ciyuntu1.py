import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import ImageFont
import jieba

def create_wordcloud(text, font_path, max_words=200):
    # 使用jieba进行中文分词
    cut_text = ' '.join(jieba.cut(text))
    
    # 创建词云图，指定中文字体和分辨率
    wordcloud = WordCloud(width=1600, height=800, background_color='white', max_words=max_words, font_path=font_path).generate(cut_text)
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
        
        # 指定中文字体路径，这里需要替换为你的字体文件路径
        font_path = 'path/to/your/chinese_font.ttf'
        
        # 创建词云图
        wordcloud = create_wordcloud(text_data, font_path)
        
        # 使用Streamlit的API显示词云图
        fig, ax = plt.subplots(figsize=(20, 10))  # 创建一个新的图形和轴，并设置大小
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')  # 不显示轴
        st.pyplot(fig)  # 将图形传递给Streamlit显示

if __name__ == "__main__":
    main()
