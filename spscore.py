import pandas as pd
import streamlit as st
import numpy as np

def calculate_covariance(student_scores, problem_scores):
    # 将学生得分转换为二维数组形式
    student_scores_array = student_scores.values.reshape(-1, 1)
    # 计算协方差
    cov = np.cov(student_scores_array, problem_scores)
    return cov[0, 1]  # 返回协方差值

def read_and_process_file(file):
    # 读取Excel文件
    df = pd.read_excel(file, engine='openpyxl')
    
    # 移除标题行和列
    df = df.rename(columns=lambda x: x.strip())  # 去除可能的空白字符
    df = df.melt(var_name='Problem', value_name='Score')  # 将DataFrame转换为长格式
    first_row = df['Problem'].tolist()  # 保存问题名称作为标题行
    first_col = df['Score'].unique()  # 保存得分作为标题列

    # 计算每个学生的总分
    student_scores = df.groupby('Score')['Problem'].count()
    
    # 计算每个问题的总分
    problem_scores = df.groupby('Problem')['Score'].count() / len(df['Problem'].unique())

    # 计算每个学生得分向量与问题得分向量的协方差
    student_covariances = student_scores.apply(calculate_covariance, problem_scores=problem_scores)

    # 根据总分和协方差对数据进行排序
    sorted_students = student_scores.index.sort_values(by=-student_covariances)
    sorted_problems = problem_scores.index.sort_values(by=-problem_scores, key=lambda x: (-problem_scores[x], calculate_covariance(student_scores[x], problem_scores[x])))

    # 创建新的DataFrame
    new_df = pd.DataFrame(index=sorted_students, columns=sorted_problems).fillna(0)  # 使用0填充空值
    for student, problem in new_df.index:
        new_df.at[student, problem] = df[(df['Problem'] == problem) & (df['Score'] == 1)].shape[0]  # 填充正确答案的数量

    # 添加标题行和列
    new_df.index = [f'S{idx+1}' for idx in range(len(sorted_students))]  # 给学生编号
    new_df.columns = first_row[:len(sorted_problems)]  # 确保问题名称与排序后的问题对齐

    return new_df, first_col

def main():
    st.title("S-P Table Generator")
    
    # 文件上传
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取文件
        df, first_col = read_and_process_file(uploaded_file)
        
        # 显示结果
        st.write("Sorted S-P Table:")
        st.dataframe(df.style.set_properties(align="center", **{'border-color': 'black'}))

if __name__ == "__main__":
    main()
