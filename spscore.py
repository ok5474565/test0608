import pandas as pd
import numpy as np
import streamlit as st

# 定义协方差排序函数
def sort_by_covariance(df, primary_vec, is_student=True):
    cov_list = []
    for idx in range(df.shape[0] if is_student else df.shape[1]):
        vec = df.iloc[idx, :] if is_student else df.iloc[:, idx]
        cov = np.cov(vec, primary_vec)[0, 1]
        cov_list.append((idx, cov))
    cov_list.sort(key=lambda x: x[1], reverse=True)
    sorted_indices = [x[0] for x in cov_list]
    return sorted_indices

# Streamlit 接口
st.title('S-P 表格生成工具')
uploaded_file = st.file_uploader("上传Excel文件", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, index_col=0)
    
    # 提取题目名称和学生姓名
    students = df.index.tolist()
    problems = df.columns.tolist()
    
    # 计算总分
    student_scores = df.sum(axis=1)
    problem_scores = df.sum(axis=0)
    
    # 根据学生总分排序
    sorted_student_indices = student_scores.sort_values(ascending=False).index.tolist()
    
    # 对总分相同的学生，根据协方差排序
    for score in student_scores.unique():
        same_score_students = student_scores[student_scores == score].index.tolist()
        if len(same_score_students) > 1:
            primary_vec = problem_scores
            sorted_indices = sort_by_covariance(df.loc[same_score_students, :], primary_vec, is_student=True)
            sorted_student_indices = [i for i in sorted_student_indices if i not in same_score_students] + [same_score_students[i] for i in sorted_indices]
    
    # 根据问题总分排序
    sorted_problem_indices = problem_scores.sort_values(ascending=False).index.tolist()
    
    # 对正答率相同的问题，根据协方差排序
    for score in problem_scores.unique():
        same_score_problems = problem_scores[problem_scores == score].index.tolist()
        if len(same_score_problems) > 1:
            primary_vec = student_scores
            sorted_indices = sort_by_covariance(df.loc[:, same_score_problems], primary_vec, is_student=False)
            sorted_problem_indices = [i for i in sorted_problem_indices if i not in same_score_problems] + [same_score_problems[i] for i in sorted_indices]
    
    # 生成S-P表格
    sorted_df = df.loc[sorted_student_indices, sorted_problem_indices]
    
    # 添加学生姓名和题目名称
    sorted_df.index = [students[idx] for idx in sorted_student_indices]
    sorted_df.columns = [problems[idx] for idx in sorted_problem_indices]
    
    st.write("生成的S-P表格：")
    st.dataframe(sorted_df)
    
    # 提供下载链接
    def to_excel(df):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='S-P 表格')
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    
    download_link = st.download_button(label="下载S-P表格", data=to_excel(sorted_df), file_name="S-P表格.xlsx")

