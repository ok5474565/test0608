import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_totals(data):
    # 确保所有数据都是数值类型
    data = data.apply(pd.to_numeric, errors='coerce')
    
    # 替换非数值数据为0或1，这里使用0
    data = data.where(data.isna(), 0)
    
    # 计算学生总分
    student_totals = data.sum(axis=1)  
    # 计算问题总分
    problem_totals = data.sum(axis=0)  
    
    return student_totals, problem_totals

def sort_data_by_totals(data, student_totals, problem_totals):
    # 根据学生总分排序
    sorted_students_index = student_totals.sort_values(ascending=False).index
    # 根据问题总分排序
    sorted_problems_index = problem_totals.sort_values(ascending=False).index
    # 重新排序DataFrame
    sorted_data = data.loc[sorted_students_index, sorted_problems_index]
    return sorted_data

def plot_sp_curve(data):
    plt.figure(figsize=(12, 8))
    for column in data.columns:
        plt.plot(data[column], label=column)
    plt.title('S-P Curve')
    plt.xlabel('Students')
    plt.ylabel('Score')
    plt.legend()
    return plt

def calculate_coefficients(data):
    average = data.mean()
    std_dev = data.std()
    cv = std_dev / average  # 差异系数
    attention_coefficient = 1 - average  # 注意系数
    return average, std_dev, cv, attention_coefficient

def main():
    st.title('学生得分统计与分析')

    # 上传文件
    uploaded_file = st.file_uploader("请上传您的 Excel 文件", type=["xlsx"])
    if uploaded_file is not None:
        # 读取文件
        data = pd.read_excel(uploaded_file)

        # 计算总分
        student_totals, problem_totals = calculate_totals(data)

        # 根据总分排序
        sorted_data = sort_data_by_totals(data, student_totals, problem_totals)

        # 绘制S-P曲线
        sp_curve = plot_sp_curve(sorted_data)
        st.pyplot(sp_curve)

        # 计算差异系数和注意系数
        average, std_dev, cv, attention_coefficient = calculate_coefficients(sorted_data)
        st.write("平均值:", average)
        st.write("标准差:", std_dev)
        st.write("差异系数:", cv)
        st.write("注意系数:", attention_coefficient)

if __name__ == '__main__':
    main()
