import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Streamlit界面设置
def main():
    st.title('学生得分统计与分析')

    # 上传文件
    uploaded_file = st.file_uploader("请上传您的 Excel 文件", type=["xlsx"])
    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)

        # 去除列名中的空格
        data.columns = data.columns.str.strip()

        # 计算每个学生的总分
        student_totals = data.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = data.sum(axis=0)

        # 根据总分和协方差进行排序
        # 学生总分排序
        sorted_students = student_totals.sort_values(ascending=False)
        # 问题总分排序
        sorted_problems = problem_totals.sort_values(ascending=False)

        # 绘制S-P曲线
        plot_sp_curve(data, sorted_students.index)

        # 计算注意系数和差异系数
        attention_coefficients, difference_coefficients = calculate_coefficients(data, student_totals, problem_totals)

        # 显示排序后的学生列表
        st.write("学生得分排序：")
        st.write(sorted_students)

        # 显示排序后的问题列表
        st.write("问题得分排序：")
        st.write(sorted_problems)

        # 显示注意系数和差异系数
        st.write("注意系数：")
        st.write(attention_coefficients)
        st.write("差异系数：")
        st.write(difference_coefficients)

def plot_sp_curve(data, students):
    # 绘制S-P曲线
    plt.figure(figsize=(10, 6))
    for student in students:
        scores = data.loc[student]
        plt.plot(scores, label=student)
    plt.title('S-P Curve')
    plt.xlabel('问题编号')
    plt.ylabel('得分')
    plt.legend()
    st.pyplot(plt)

def calculate_coefficients(data, student_totals, problem_totals):
    # 计算注意系数和差异系数
    attention_coefficients = {}
    difference_coefficients = {}
    for student, total in student_totals.items():
        scores = data.loc[student]
        attention_coefficients[student] = pearsonr(scores, problem_totals)[0]
        difference_coefficients[student] = pearsonr(problem_totals, scores)[0]
    return attention_coefficients, difference_coefficients

if __name__ == '__main__':
    main()
