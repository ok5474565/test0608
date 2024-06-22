import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 上传文件
uploaded_file = st.file_uploader("上传S-P表格", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 读取文件
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("原始数据表格：")
    st.dataframe(df)

    # 绘制S-P曲线
    st.write("S-P曲线：")
    fig, ax = plt.subplots()
    for index, row in df.iterrows():
        ax.plot(row, label=f"Student {index+1}")
    ax.set_xlabel('Problem Index')
    ax.set_ylabel('Score')
    ax.set_title('S-P Curve')
    ax.legend()
    st.pyplot(fig)

    # 计算差异系数
    student_mean_scores = df.mean(axis=1)
    total_mean_score = student_mean_scores.mean()
    total_sd = student_mean_scores.std()
    difference_coefficient = total_sd / total_mean_score
    st.write(f"差异系数：{difference_coefficient:.2f}")

    # 计算注意系数
    problem_mean_scores = df.mean(axis=0)
    total_problem_mean_score = problem_mean_scores.mean()
    total_problem_sd = problem_mean_scores.std()
    attention_coefficient = total_problem_sd / total_problem_mean_score
    st.write(f"注意系数：{attention_coefficient:.2f}")

