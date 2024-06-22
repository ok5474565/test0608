import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 上传文件
uploaded_file = st.file_uploader("上传 S-P 表格文件 (xlsx 或 csv)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # 读取文件
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)

    # 提取学生姓名和题目名称
    student_names = df.iloc[1:, 0].values
    question_titles = df.columns[1:].values

    # 提取答题数据
    data = df.iloc[1:, 1:].astype(int).values

    # 计算学生总分
    student_scores = data.sum(axis=1)

    # 计算每个问题的正答次数
    question_scores = data.sum(axis=0)

    # 绘制 S 曲线
    plt.figure(figsize=(12, 6))
    for i, score in enumerate(student_scores):
        plt.vlines(x=i, ymin=0, ymax=score, color='b')
        for j in range(len(question_titles)):
            if data[i, j] == 1:
                plt.hlines(y=student_scores[i], xmin=i, xmax=i+1, color='b')

    plt.title('S 曲线')
    plt.xlabel('学生')
    plt.ylabel('总分')
    plt.xticks(ticks=np.arange(len(student_names)), labels=student_names, rotation=90)
    st.pyplot(plt)

    # 绘制 P 曲线
    plt.figure(figsize=(12, 6))
    for i, score in enumerate(question_scores):
        plt.hlines(y=i, xmin=0, xmax=score, color='r')
        for j in range(len(student_names)):
            if data[j, i] == 1:
                plt.vlines(x=question_scores[i], ymin=i, ymax=i+1, color='r')

    plt.title('P 曲线')
    plt.xlabel('正答次数')
    plt.ylabel('题目')
    plt.yticks(ticks=np.arange(len(question_titles)), labels=question_titles, rotation=0)
    st.pyplot(plt)
