import streamlit as st
import pandas as pd
import numpy as np

def calculate_difficulty_index(df):
    # 计算每个题目的平均得分率，即差异系数（P指数）
    return df.mean(axis=1)

def calculate_discrimination_index(df, num_top=27, num_bottom=27):
    # 将数据分为高分组和低分组
    num_students = len(df)
    top_index = int((num_students * num_top) / 100)
    bottom_index = int((num_students * num_bottom) / 100)
    
    # 计算总分
    total_scores = df.sum(axis=1)
    # 根据总分排序
    sorted_indices = total_scores.sort_values(ascending=False).index
    
    # 分别获取高分组和低分组的题目得分
    top_group_scores = df.loc[sorted_indices[:top_index]]
    bottom_group_scores = df.loc[sorted_indices[-bottom_index:]]
    
    # 计算高分组和低分组的每个题目的答对率
    top_group_correct_rate = top_group_scores.mean(axis=0)
    bottom_group_correct_rate = bottom_group_scores.mean(axis=0)
    
    # 计算D指数
    d_index = top_group_correct_rate / (1 - bottom_group_correct_rate)
    return d_index

def main():
    st.title("S-P 表格分析工具")
    
    uploaded_file = st.file_uploader("上传一个 Excel 文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取 Excel 文件
        df = pd.read_excel(uploaded_file)
        
        # 去掉第一行（题目名称）和第一列（学生姓名）
        df = df.iloc[1:, 1:]  # 假设第一行和第一列是标题
        
        # 转置 DataFrame，使其与原始上传的表格结构一致
        df = df.T
        
        # 计算差异系数（P指数）
        difficulty_index = calculate_difficulty_index(df)
        
        # 计算注意系数（D指数）
        discrimination_index = calculate_discrimination_index(df)
        
        # 显示结果
        st.subheader("分析结果")
        result_df = pd.DataFrame({
            '差异系数 (P指数)': difficulty_index,
            '注意系数 (D指数)': discrimination_index
        })
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
