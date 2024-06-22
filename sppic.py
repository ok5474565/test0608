import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(file):
    df = pd.read_excel(file, index_col=0)
    return df

def process_data(df):
    # 计算学生总分
    df['总分'] = df.sum(axis=1)
    # 按照总分排序学生
    df = df.sort_values(by='总分', ascending=False)
    
    # 计算每个题目的总分
    total_scores = df.drop(columns=['总分']).sum(axis=0)
    # 按照总分排序题目
    df = df[total_scores.sort_values(ascending=False).index]
    df = df.join(df.pop('总分'))
    
    return df

def plot_sp_curves(df):
    students = df.index
    problems = df.columns[:-1]
    student_scores = df['总分']
    
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    
    # 绘制S曲线
    for i, student in enumerate(students):
        score = student_scores[student]
        ax[0].vlines(i, 0, score, color='b')
        for j in range(score):
            ax[0].hlines(j, i, i+1, color='b')
    
    ax[0].set_title('S曲线')
    ax[0].set_xlabel('学生')
    ax[0].set_ylabel('得分')
    ax[0].set_xticks(range(len(students)))
    ax[0].set_xticklabels(students, rotation=90)
    
    # 绘制P曲线
    for i, problem in enumerate(problems):
        correct_answers = df[problem].sum()
        ax[1].hlines(i, 0, correct_answers, color='r')
        for j in range(correct_answers):
            ax[1].vlines(j, i, i+1, color='r')
    
    ax[1].set_title('P曲线')
    ax[1].set_xlabel('题目')
    ax[1].set_ylabel('正答次数')
    ax[1].set_yticks(range(len(problems)))
    ax[1].set_yticklabels(problems)
    
    st.pyplot(fig)

def main():
    st.title("S-P 表格及曲线生成器")
    
    uploaded_file = st.file_uploader("上传一个xlsx文件", type="xlsx")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.write("原始数据：")
        st.dataframe(df)
        
        processed_df = process_data(df)
        st.write("处理后的数据：")
        st.dataframe(processed_df)
        
        plot_sp_curves(processed_df)

if __name__ == "__main__":
    main()
