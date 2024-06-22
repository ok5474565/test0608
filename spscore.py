import pandas as pd
import streamlit as st
import numpy as np

def read_and_process_xlsx(file):
    # 读取Excel文件，跳过第一行和第一列
    df = pd.read_excel(file, engine='openpyxl', header=1, skiprows=1)
    
    # 将DataFrame转换为布尔型，1代表True，0代表False
    df = df.replace({1: True, 0: False})
    
    return df

def calculate_totals(df):
    # 计算每个学生的总分
    student_totals = df.sum(axis=1)
    
    # 计算每个问题的总分
    problem_totals = df.sum(axis=0)
    
    return student_totals, problem_totals

def calculate_covariance(student_scores, problem_scores):
    # 计算协方差矩阵
    return np.cov(student_scores, problem_scores)

def sort_by_covariance(student_totals, problem_totals, df):
    # 计算协方差并排序
    covariance_matrix = calculate_covariance(student_totals, problem_totals)
    sorted_indices = (-covariance_matrix[0, 1:]).argsort()
    return sorted_indices

def main():
    st.title('学生成绩排序应用')
    
    # 让用户上传Excel文件
    uploaded_file = st.file_uploader("上传你的Excel文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取和处理数据
        df = read_and_process_xlsx(uploaded_file)
        
        # 计算总分
        student_totals, problem_totals = calculate_totals(df)
        
        # 根据总分和协方差排序学生
        sorted_students_index = sort_by_covariance(student_totals, problem_totals, df)
        
        # 根据问题总分排序问题
        sorted_problems_index = problem_totals.argsort(ascending=False)
        
        # 根据排序后的索引重新排列DataFrame
        sorted_df = df.iloc[sorted_students_index, sorted_problems_index]
        
        # 显示排序后的学生成绩表
        st.write("排序后的学生成绩表:")
        st.dataframe(sorted_df)
        
        # 显示问题总分
        st.write("问题总分:")
        problem_totals_series = pd.Series(problem_totals, name='问题总分')
        st.dataframe(problem_totals_series.reset_index().rename(columns={'index': '问题编号'}))

        # 显示学生总分
        st.write("学生总分:")
        student_totals_series = pd.Series(student_totals, name='学生总分')
        st.dataframe(student_totals_series.sort_values(ascending=False))

if __name__ == '__main__':
    main()
