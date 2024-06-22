import pandas as pd
import streamlit as st
import numpy as np

def read_and_process_file(file):
    # 读取Excel文件
    df = pd.read_excel(file, header=None)
    
    # 移除第一行和第一列
    df = df.iloc[1:, 1:]
    
    # 计算每个学生的总分
    student_scores = df.sum(axis=1)
    
    # 计算每个问题的总分
    problem_scores = df.sum(axis=0)
    
    # 计算协方差矩阵
    cov_matrix = np.cov(df.T)
    
    # 根据总分和协方差对数据进行排序
    sorted_df = df.iloc[np.argsort(-student_scores)]  # 总分降序排序
    sorted_problem_scores = problem_scores.reindex(sorted_df.columns)
    
    # 构建新的DataFrame
    new_df = pd.DataFrame(index=sorted_df.index, columns=sorted_df.columns)
    
    # 填充数据
    for idx, row in sorted_df.iterrows():
        new_df.iloc[idx] = sorted_problem_scores[idx]
    
    # 添加第一行和第一列的内容
    first_row = df.iloc[0, 1:].copy()
    first_col = df.iloc[1:, 0].copy()
    
    new_df.index = first_row
    new_df.columns = first_col
    
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
