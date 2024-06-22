import pandas as pd
import streamlit as st
import numpy as np

def convert_to_numeric(df):
    # 尝试将DataFrame中的所有列转换为数值类型，如果失败则设置为NaN
    return df.apply(pd.to_numeric, errors='coerce')

def read_and_process_file(file):
    # 读取Excel文件
    df = pd.read_excel(file)
    
    # 确保所有数据都是数值类型
    df = convert_to_numeric(df)
    
    # 移除标题行
    df = df.drop(df.index[0])
    
    # 计算每个学生的总分
    student_totals = df.sum(axis=1)
    
    # 计算每个问题的总分
    problem_totals = df.sum(axis=0)
    
    # 根据总分对数据进行排序
    sorted_students = student_totals.sort_values(ascending=False)
    
    # 创建新的DataFrame
    new_df = pd.DataFrame(index=sorted_students.index, columns=df.columns).fillna(0)
    
    # 填充数据
    for student, total in sorted_students.items():
        new_df.loc[student] = df.loc[student]
    
    # 添加标题行
    new_df.index = [f"S{i+1}" for i in range(len(sorted_students))]
    
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
