import streamlit as st
import jieba
from collections import Counter
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import pandas as pd
import csv
import io


# 辅助函数，用于清理标题中的非法字符
def sanitize_word(word, illegal_chars):
    return ''.join([char for char in word if char not in illegal_chars])

# 定义去停用词的函数
def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

# 生成词云图
def generate_wordcloud(frequencies, font_path, width=800, height=600):
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=200,
        width=width,
        height=height
    ).generate_from_frequencies(frequencies)
    
    image = wc.to_image()
    st.image(image, use_column_width=True)

# 读取文件内容
def read_file(uploaded_file):
    text = ""
    if uploaded_file.type == 'text/plain':
        text = uploaded_file.read().decode('utf-8')
    elif uploaded_file.type == 'text/csv':
        # 使用io.StringIO将二进制内容转换为文件对象
        csv_content = io.StringIO(uploaded_file.read().decode('utf-8'))
        reader = csv.reader(csv_content)
        for row in reader:
            # 确保row是非空的
            if row:
                text += row[0] + "\n"
    return text

# 主函数
def main():
    st.title("文本分词、高频词统计与词云图生成")
    
    file_types = ["txt", "csv"]
    uploaded_file = st.file_uploader("请上传你的文本或CSV文件", type=file_types)
    
    if uploaded_file is not None:
        text = read_file(uploaded_file)
        
        words = jieba.lcut(text)
        
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = f.read().splitlines()
        
        illegal_chars = [':','"','|','/','\\\\','*','<','>','?']
        sanitized_words = [sanitize_word(word, illegal_chars) for word in words if word]
        filtered_words = remove_stopwords(sanitized_words, stopwords)
        
        word_freq = Counter(filtered_words)
        
        top_words = word_freq.most_common(50)
        
        wordcloud_freq = {word: freq for word, freq in top_words}
        
        font_path = 'simhei.ttf'  # 请确保这个路径是正确的
        
        generate_wordcloud(wordcloud_freq, font_path)
        
        st.write("高频词统计:")
        top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        st.dataframe(top_words_df)

if __name__ == '__main__':
    main()
