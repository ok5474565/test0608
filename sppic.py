import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Function to calculate covariance for sorting
def calculate_covariance(student_scores, problem_scores):
    # 因为问题得分向量和学生得分向量是一维的，所以使用np.cov可能会出错
    # 这里我们直接计算两个向量的协方差
    return np.dot(student_scores, problem_scores) / len(student_scores)

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
    sorted_students = sorted(
        range(len(student_scores)), 
        key=lambda i: (-student_scores[i], calculate_covariance(df.iloc[:, i], problem_scores))
    )
    
    # Sorting problems by average score, then by covariance if scores are the same
    sorted_problems = sorted(
        range(len(problem_scores)), 
        key=lambda i: (-problem_scores[i], calculate_covariance(df.iloc[i, :], student_scores))
    )
    
    # Generating the sorted S-P table
    sorted_df = df.loc[sorted_students, sorted_problems]
    
    return sorted_df, student_names[sorted_students], problem_names[sorted_problems]

# Function to plot the S-P chart
def plot_sp_chart(sorted_df):
    # 为绘图设置图形大小
    plt.figure(figsize=(10, sorted_df.shape[0] / sorted_df.shape[1] * 10))
    
    # 使用seaborn的heatmap绘制S-P曲线
    sns.heatmap(sorted_df, annot=True, fmt="d", cmap="YlGnBu", cbar=False)
    
    # 设置标题和坐标轴标签
    plt.title('S-P Chart')
    plt.xlabel('Problems')
    plt.ylabel('Students')
    
    # 优化Y轴的标签显示，防止重叠
    plt.yticks(rotation=0)
    
    # 显示图形
    plt.show()

# Streamlit app
st.title("S-P Chart Generator")

uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    st.write("Upload successful!")
    sorted_df, sorted_students, sorted_problems = process_sp_chart(uploaded_file)
    
    st.write("Generated S-P Table:")
    st.dataframe(sorted_df)
    
    # Plot and display the S-P chart
    st.write("Plotting S-P Chart:")
    plot_sp_chart(sorted_df)
    
    # Option to download the sorted S-P table
    st.write("Download the S-P Table:")
    st.download_button(
        label="Download Excel file",
        data=pd.ExcelWriter("sorted_sp_chart.xlsx", engine='openpyxl'),
        file_name="sorted_sp_chart.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
