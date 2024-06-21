import streamlit as st
import pandas as pd
from wordcloud import WordCloud
from PIL import Image
import numpy as np

# 读取CSV文件并生成词云图的函数
def generate_wordcloud_from_csv(csv_file, font_path):
    # 读取CSV文件
    data = pd.read_csv(csv_file)
    
    # 假设CSV文件中有列名为'text'的列，包含我们要生成词云的文本
    text = ' '.join(str(v) for v in data['text'])
    
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=200,
        width=800,
        height=400
    ).generate(text)
    
    # 显示词云图
    image = wc.to_image()
    return image

# 主函数
def main():
    st.title("CSV文件词云图生成器")
    
    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的CSV文件", type=["csv"])
    
    if uploaded_file is not None:
        # 读取文件内容
        file_content = uploaded_file.read()
        
        # 将文件内容转换为Image对象
        image = generate_wordcloud_from_csv(file_content, 'simhei.ttf')
        
        # 显示词云图
        st.image(image, use_column_width=True)

if __name__ == '__main__':
    main()
