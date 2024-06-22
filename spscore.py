import pandas as pd
import streamlit as st
import numpy as np

# 计算单个学生得分向量与问题得分向量之间的协方差
def calculate_covariance(student_scores_series, problem_total):
    # 将学生得分转换为一维NumPy数组
    student_scores_array = student_scores_series.values
    # 问题得分向量与学生得分向量进行协方差计算
    cov = np.cov(student_scores_array, [problem_total])[0][1]
    return cov

def read_and_process_file(file):
    # 读取Excel文件
    df = pd.read_excel(file)
    
    # 移除标题行和列
    df = df.drop(df.index[0])  # 删除第一行
    df.columns = df.columns.str.lstrip()  # 去除列名可能的空白字符
    
    # 计算每个学生的总分
    student_totals = df.sum(axis=1)
    
    # 计算每个问题的总分
    problem_totals = df.sum(axis=0)
    
    # 计算每个学生得分向量与问题得分向量的协方差
    student_covariances = student_totals.apply(calculate_covariance, problem_total=problem_totals.sum())
    
    # 根据总分和协方差对数据进行排序
    sorted_index = student_totals.index[np.argsort(-student_totals)]
    sorted_students = student_totals.reindex(sorted_index).rank(ascending=0)
    
    # 创建新的DataFrame
    new_df = pd.DataFrame(index=sorted_students.index, columns=df.columns).fillna(0)
    
    # 填充数据
    for student in sorted_students.index:
        for problem in new_df.columns:
            new_df.at[student, problem] = df.at[student, problem]
    
    # 添加标题行和列
    new_df.index = [f"S{i+1}" for i in range(len(sorted_students.index))]
    new_df.columns = [f"P{i+1}" for i in range(len(new_df.columns))]
    
    return new_df

def main():
    st.title("S-P Table Generator")
    
    # 文件上传
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取文件
        df = read_and_process_file(uploaded_file)
        
        # 显示结果
        st.write("Sorted S-P Table:")
        st.dataframe(df)

if __name__ == "__main__":
    main()
