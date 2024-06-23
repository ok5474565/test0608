import streamlit as st
import pandas as pd
import numpy as np

def calculate_difficulty_index(df):
    # 计算差异系数（P指数），即每个题目的平均答对率
    return df.mean(axis=0)

def calculate_discrimination_index(df, num_top=27, num_bottom=27):
    # 计算每个学生的总分
    total_scores = df.sum(axis=0)
    
    # 根据总分排序以划分高分组和低分组
    sorted_student_scores = total_scores.sort_values(ascending=False)
    
    # 划分高分组和低分组的索引
    num_students = len(total_scores)
    top_index = int((num_students * num_top) / 100)
    bottom_index = int((num_students * num_bottom) / 100)
    top_student_indices = sorted_student_scores.index[-top_index:]
    bottom_student_indices = sorted_student_scores.index[:bottom_index]
    
    # 计算高分组和低分组的答对率
    top_group_mask = df.columns.isin(top_student_indices)
    bottom_group_mask = df.columns.isin(bottom_student_indices)
    
    top_group_correct_rate = df[top_group_mask].mean(axis=1)
    bottom_group_correct_rate = df[bottom_group_mask].mean(axis=1)
    
    # 计算D指数，即高分组答对率与低分组答对率的比值
    d_index = (top_group_correct_rate - bottom_group_correct_rate) / bottom_group_correct_rate
    
    # 避免除以零，只返回有效的D指数
    d_index = d_index.replace([np.inf, -np.inf], np.nan).dropna()
    
    return d_index

def main():
    st.title("S-P 表格分析工具")
    
    uploaded_file = st.file_uploader("上传一个 Excel 文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取 Excel 文件
        df = pd.read_excel(uploaded_file)
        
        # 去掉第一行（题目名称）和第一列（学生姓名）
        df = df.iloc[1:, 1:]
        
        # 转置 DataFrame，使其与原始上传的表格结构一致
        df = df.T
        
        # 计算难度系数（P指数）
        difficulty_index = calculate_difficulty_index(df)
        
        # 计算注意系数（D指数）
        discrimination_index = calculate_discrimination_index(df)
        
        # 显示结果
        st.subheader("分析结果")
        result_df = pd.DataFrame({
            '难度系数 (P指数)': difficulty_index,
            '注意系数 (D指数)': discrimination_index
        }, index=df.index)
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
