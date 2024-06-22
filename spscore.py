import streamlit as st
import pandas as pd
import numpy as np

def read_and_prepare_data(file_path):
    # 读取Excel文件
    data = pd.read_excel(file_path)
    
    # 忽略第一行的题目编号和第一列的学生姓名
    body_data = data.iloc[1:, 1:]
    student_names = data.iloc[0, 1:]  # 第一行的第2列到末尾作为学生姓名
    problem_ids = data.iloc[1:, 0]  # 第2列到末尾的第1列作为题目编号
    
    return body_data, student_names, problem_ids

def calculate_totals(body_data):
    # 计算学生总分和问题平均分
    student_totals = body_data.sum(axis=1)
    problem_averages = body_data.mean(axis=1)
    
    return student_totals, problem_averages

def sort_data(student_totals, problem_averages):
    # 根据学生总分排序
    sorted_index = student_totals.argsort()[::-1]  # 降序排序索引
    sorted_student_totals = student_totals[sorted_index]
    sorted_body_data = body_data.loc[sorted_index, :]
    
    # 根据问题平均分排序
    sorted_problem_index = problem_averages.argsort()  # 升序排序索引
    sorted_problem_averages = problem_averages[sorted_problem_index]
    sorted_body_data = sorted_body_data.iloc[:, sorted_problem_index]
    
    return sorted_body_data, sorted_student_totals, sorted_problem_averages

def add_titles(sorted_body_data, student_names, problem_ids):
    # 添加标题行和列
    sorted_data_with_titles = pd.concat([
        pd.DataFrame([problem_ids], columns=sorted_body_data.columns),
        sorted_body_data
    ], axis=0)
    sorted_data_with_titles.index = ['题目编号'] + student_names
    return sorted_data_with_titles

def main():
    st.title('S-P Table Generator')
    uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        file_path = st.text("File path: " + uploaded_file.name)
        
        # 读取和准备数据
        body_data, student_names, problem_ids = read_and_prepare_data(file_path)
        
        # 计算总分和平均分
        student_totals, problem_averages = calculate_totals(body_data)
        
        # 排序数据
        sorted_body_data, sorted_student_totals, sorted_problem_averages = sort_data(student_totals, problem_averages)
        
        # 添加标题
        sp_table = add_titles(sorted_body_data, student_names, problem_ids)
        
        # 显示S-P表
        st.write("Generated S-P Table:")
        st.dataframe(sp_table)

if __name__ == "__main__":
    main()
