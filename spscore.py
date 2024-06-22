import streamlit as st
import pandas as pd
import numpy as np

def read_and_prepare_data(file_path):
    # 读取Excel文件，跳过第一行和第一列
    data = pd.read_excel(file_path)
    data = data.iloc[1:, 1:]
    return data

def calculate_totals(data):
    # 计算学生总分和问题总分
    student_totals = data.sum(axis=1)
    problem_totals = data.sum(axis=0)
    return student_totals, problem_totals

def sort_data_by_totals(data, student_totals, problem_totals):
    # 根据学生总分和问题总分进行排序
    sorted_data = data.loc[np.argsort(student_totals)[::-1]]
    sorted_data = sorted_data.iloc[:, np.argsort(problem_totals)[::-1]]
    return sorted_data

def calculate_covariance(student_totals, problem_totals):
    # 计算协方差，这里需要根据具体逻辑实现
    # 以下为协方差计算的示例代码，需要根据题目要求调整
    student_scores_matrix = data.values
    problem_scores_matrix = student_scores_matrix.T
    student_covariance = np.cov(student_scores_matrix, rowvar=False, bias=True)
    problem_covariance = np.cov(problem_scores_matrix, rowvar=False, bias=True)
    return student_covariance, problem_covariance

def sort_by_covariance(sorted_data, student_covariance, problem_covariance):
    # 根据协方差排序，这里需要根据具体逻辑实现
    # 以下为示例代码，需要根据题目要求调整
    # 通常需要对协方差矩阵进行进一步处理以确定排序逻辑
    pass

def add_titles(data, student_names, problem_names):
    # 添加标题行和列
    titles = pd.DataFrame(columns=[''] + list(data.columns))
    titles.iloc[0] = student_names + ['']  # 假设第一行是学生姓名
    titles = titles.transpose()  # 转置以匹配数据
    titles.iloc[0] = problem_names + ['']  # 假设第一列是问题名称
    sp_table = pd.concat([titles, sorted_data], axis=0)
    return sp_table

def main():
    st.title('S-P Table Generator')
    uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取和准备数据
        data = read_and_prepare_data(uploaded_file)
        student_totals, problem_totals = calculate_totals(data)
        sorted_data = sort_data_by_totals(data, student_totals, problem_totals)
        
        # 计算协方差
        student_covariance, problem_covariance = calculate_covariance(student_totals, problem_totals)
        
        # 根据协方差排序（需要根据具体逻辑实现）
        # sorted_data = sort_by_covariance(sorted_data, student_covariance, problem_covariance)
        
        # 添加标题
        student_names = pd.read_excel(uploaded_file, nrows=1, usecols=range(1, data.shape[1])).iloc[0]
        problem_names = pd.read_excel(uploaded_file, usecols=[0], skiprows=1).iloc[0]
        sp_table = add_titles(sorted_data, student_names, problem_names)
        
        # 显示S-P表
        st.write(sp_table)

if __name__ == "__main__":
    main()
