import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def main():
    st.title('学生得分统计与分析')

    # 上传文件
    uploaded_file = st.file_uploader("请上传您的 Excel 文件", type=["xlsx"])
    if uploaded_file is not None:
        # 读取文件
        data = pd.read_excel(uploaded_file)

        # 去除列名中的空格
        data.columns = data.columns.str.strip()

        # 选择数值列进行求和
        numeric_data = data.select_dtypes(include=[np.number])
        student_totals = numeric_data.sum(axis=1)  # 学生总分

        # 计算每个问题的正答次数（假设第一行是题目编号）
        problem_totals = numeric_data.sum(axis=0)  # 问题总分

        # 根据学生总分排序
        sorted_students = student_totals.sort_values(ascending=False)

        # 根据问题总分排序
        sorted_problems = problem_totals.sort_values(ascending=False)

        # 绘制S-P曲线
        plot_sp_curve(numeric_data, sorted_problems.index)

        # 显示排序后的学生列表
        st.write("学生得分排序：")
        st.write(sorted_students)

        # 显示排序后的问题列表
        st.write("问题得分排序：")
        st.write(sorted_problems)

def plot_sp_curve(data, problems):
    plt.figure(figsize=(10, 6))
    for problem in problems:
        scores = data[data.index.str.contains(problem)]
        plt.plot(scores, label=problem)
    plt.title('S-P Curve')
    plt.xlabel('学生')
    plt.ylabel('正答次数')
    plt.legend()
    st.pyplot(plt)

if __name__ == '__main__':
    main()
