import pandas as pd
import streamlit as st
import numpy as np

def read_and_process_xlsx(file):
    # 读取Excel文件
    df = pd.read_excel(file, header=None)
    
    # 移除标题行和列
    df = df.iloc[1:, 1:]
    
    # 将DataFrame转换为布尔型，1代表True，0代表False
    df = df.replace({1: True, 0: False})
    
    return df

def calculate_totals(df):
    # 计算每个学生的总分
    student_totals = df.sum(axis=1)
    
    # 计算每个问题的总分
    problem_totals = df.sum(axis=0)
    
    return student_totals, problem_totals

def sort_students_by_totals(student_totals):
    # 根据总分排序学生
    sorted_students_index = student_totals.sort_values(ascending=False).index
    return sorted_students_index

def sort_problems_by_totals(problem_totals):
    # 根据总分排序问题
    sorted_problems_index = problem_totals.sort_values(ascending=False).index
    return sorted_problems_index

def main():
    st.title('学生成绩排序应用')
    
    # 让用户上传Excel文件
    uploaded_file = st.file_uploader("上传你的Excel文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取和处理数据
        df = read_and_process_xlsx(uploaded_file)
        
        # 计算总分
        student_totals, problem_totals = calculate_totals(df)
        
        # 排序学生和问题
        sorted_students_index = sort_students_by_totals(student_totals)
        sorted_problems_index = sort_problems_by_totals(problem_totals)
        
        # 根据排序后的索引重新排列DataFrame
        sorted_df = df.loc[sorted_students_index, sorted_problems_index]
        
        # 显示排序后的学生成绩表
        st.write("排序后的学生成绩表:")
        st.dataframe(sorted_df)
        
        # 显示问题总分
        st.write("问题总分:")
        st.dataframe(pd.DataFrame(problem_totals, index=['问题总分'], columns=df.columns))
        
        # 显示学生总分
        st.write("学生总分:")
        st.dataframe(pd.DataFrame(student_totals, index=['学生总分'], columns=sorted_students_index))

if __name__ == '__main__':
    main()
