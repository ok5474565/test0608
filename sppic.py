import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

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
    
    return sorted_df, sorted_students, sorted_problems

# Function to plot S-curves
def plot_s_curves(df, sorted_students, sorted_problems):
    plt.figure(figsize=(10, 6))
    for i, student in enumerate(sorted_students):
        total_score = df.loc[student].sum()
        x = np.arange(len(sorted_problems))
        y = [total_score] * len(sorted_problems)
        plt.plot(x, y, color='b', linewidth=1)
        for j, problem in enumerate(sorted_problems):
            plt.plot([j, j+1], [total_score, total_score], color='b', linewidth=1)
    plt.title('S-curves')
    plt.xlabel('Problems')
    plt.ylabel('Total Score')
    st.pyplot()

# Function to plot P-curves
def plot_p_curves(df, sorted_students, sorted_problems):
    plt.figure(figsize=(10, 6))
    for j, problem in enumerate(sorted_problems):
        total_correct = df[problem].sum()
        x = [total_correct] * (len(sorted_students) + 1)
        y = np.arange(len(sorted_students) + 1)
        plt.plot(x, y, color='g', linewidth=1)
        for i, student in enumerate(sorted_students):
            plt.plot([total_correct, total_correct], [i, i+1], color='g', linewidth=1)
    plt.title('P-curves')
    plt.xlabel('Total Correct Answers')
    plt.ylabel('Students')
    st.pyplot()

# Streamlit app
st.title("S-P 表格生成器")

uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx"])

if uploaded_file is not None:
    st.write("上传成功！")
    sorted_df, sorted_students, sorted_problems = process_sp_chart(uploaded_file)
    
    st.write("生成的S-P表格：")
    st.dataframe(sorted_df)
    
    # Option to download the sorted S-P table
    st.write("下载S-P表格：")
    sorted_df.to_excel("sorted_sp_chart.xlsx", index=True)
    with open("sorted_sp_chart.xlsx", "rb") as file:
        btn = st.download_button(
            label="下载Excel文件",
            data=file,
            file_name="sorted_sp_chart.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Option to plot S-curves
    st.write("绘制S曲线：")
    plot_s_curves(sorted_df, sorted_students, sorted_problems)
    
    # Option to plot P-curves
    st.write("绘制P曲线：")
    plot_p_curves(sorted_df, sorted_students, sorted_problems)
