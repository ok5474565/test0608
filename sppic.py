import pandas as pd
import numpy as np
import streamlit as st

# Function to calculate covariance for sorting
def calculate_covariance(student_scores, problem_scores):
    return np.cov(student_scores, problem_scores)[0, 1]

# Function to load and process the data
def process_sp_chart(file):
    df = pd.read_excel(file, header=0, index_col=0)
    
    # Extracting student names and problem names
    student_names = df.index.tolist()
    problem_names = df.columns.tolist()
    
    # Calculating student scores and problem scores
    student_scores = df.sum(axis=1)
    problem_scores = df.sum(axis=0)
    
    # Sorting students by total score, then by covariance if scores are the same
    sorted_students = student_scores.sort_values(ascending=False).index.tolist()
    for i in range(len(sorted_students) - 1):
        for j in range(i + 1, len(sorted_students)):
            if student_scores[sorted_students[i]] == student_scores[sorted_students[j]]:
                cov_i = calculate_covariance(df.loc[sorted_students[i]], problem_scores)
                cov_j = calculate_covariance(df.loc[sorted_students[j]], problem_scores)
                if cov_i < cov_j:
                    sorted_students[i], sorted_students[j] = sorted_students[j], sorted_students[i]
    
    # Sorting problems by total score, then by covariance if scores are the same
    sorted_problems = problem_scores.sort_values(ascending=False).index.tolist()
    for i in range(len(sorted_problems) - 1):
        for j in range(i + 1, len(sorted_problems)):
            if problem_scores[sorted_problems[i]] == problem_scores[sorted_problems[j]]:
                cov_i = calculate_covariance(df[sorted_problems[i]], student_scores)
                cov_j = calculate_covariance(df[sorted_problems[j]], student_scores)
                if cov_i < cov_j:
                    sorted_problems[i], sorted_problems[j] = sorted_problems[j], sorted_problems[i]

    # Generating the sorted S-P table
    sorted_df = df.loc[sorted_students, sorted_problems]
    
    # Adding sorted student and problem names back to the table
    sorted_df.index.name = df.index.name
    sorted_df.columns.name = df.columns.name
    
    def plot_sp_curves(df):
        # 绘制S曲线
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        for index, row in df.iterrows():
            plt.step(df.columns, row, where='post')
        plt.title('S曲线 - 学生得分')
        plt.xlabel('学生')
        plt.ylabel('得分')
    
        # 绘制P曲线
        plt.subplot(1, 2, 2)
        for column in df.columns:
            plt.step(df.index, df[column], where='post')
        plt.title('P曲线 - 问题得分')
        plt.xlabel('问题')
        plt.ylabel('得分')
    
        plt.tight_layout()

    # ...（之前的代码不变）

    # 在这里调用绘制曲线的函数
    plot_sp_curves(sorted_df)

    return sorted_df, sorted_students, sorted_problems

# Streamlit app
st.title("S-P 表格生成器")

uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx"])

if uploaded_file is not None:
    st.write("上传成功！")
    sorted_df, sorted_students, sorted_problems = process_sp_chart(uploaded_file)
    
    st.write("生成的S-P表格：")
    st.dataframe(sorted_df)

    # 绘制并显示S-P曲线
    with st.spinner('绘制中...'):
        plot_sp_curves(sorted_df)
        st.pyplot()


    
    # Option to download the sorted S-P table
    st.write("下载S-P表格：")
    sorted_df.to_excel("sorted_sp_chart.xlsx")
    with open("sorted_sp_chart.xlsx", "rb") as file:
        btn = st.download_button(
            label="下载Excel文件",
            data=file,
            file_name="sorted_sp_chart.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
