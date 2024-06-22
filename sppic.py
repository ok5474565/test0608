import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit应用标题
st.title("S-P 曲线生成器")

# 文件上传
uploaded_file = st.file_uploader("上传一个S-P表格文件 (xlsx格式)", type="xlsx")

if uploaded_file:
    # 读取Excel文件
    df = pd.read_excel(uploaded_file)

    # 显示数据表
    st.write("数据表格:", df)

    # 绘制S曲线
    fig, ax = plt.subplots()
    
    # S曲线
    for student in df.columns[1:]:
        total_score = df[student].sum()
        x = [student]*len(df)
        y = list(range(1, len(df) + 1))
        scores = df[student].values
        ax.plot(x, y, label=f'{student} (总分: {total_score})', drawstyle='steps-post')
    
    ax.set_xlabel('学生')
    ax.set_ylabel('问题编号')
    ax.set_title('S 曲线')
    ax.legend()
    
    st.pyplot(fig)

    # 绘制P曲线
    fig, ax = plt.subplots()
    
    # P曲线
    for question in df.index:
        correct_answers = df.loc[question].sum()
        y = [question]*len(df.columns[1:])
        x = list(range(1, len(df.columns)))
        answers = df.loc[question].values
        ax.plot(x, y, label=f'问题 {question} (正答次数: {correct_answers})', drawstyle='steps-post')

    ax.set_xlabel('学生编号')
    ax.set_ylabel('问题')
    ax.set_title('P 曲线')
    ax.legend()

    st.pyplot(fig)
