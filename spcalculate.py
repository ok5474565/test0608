import streamlit as st
import pandas as pd
import numpy as np

def calculate_difficulty_index(df):
    # 计算差异系数（P指数），即每个题目的平均答对率
    return df.mean(axis=0)

def calculate_discrimination_index(df, num_top=27, num_bottom=27):
    # 计算总分，并根据总分排序以划分高分组和低分组
    total_scores = df.sum(axis=0)  # 计算每个学生的总分
    sorted_total_scores = total_scores.sort_values(ascending=False)  # 总分降序排序
    sorted_df = df.loc[sorted_total_scores.index]  # 根据总分排序的原始数据

    # 划分高分组和低分组
    num_students = len(total_scores)
    top_index = int((num_students * num_top) / 100)
    bottom_index = int((num_students * num_bottom) / 100)
    
    top_group = sorted_df.iloc[-top_index:]  # 高分组
    bottom_group = sorted_df.iloc[:bottom_index]  # 低分组

    # 计算高分组和低分组的答对率
    top_group_correct_rate = top_group.mean(axis=1)
    bottom_group_correct_rate = bottom_group.mean(axis=1)
    
    # 计算D指数，即高分组答对率与低分组答对率的比值
    d_index = (top_group_correct_rate - bottom_group_correct_rate) / bottom_group_correct_rate
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
        }, index=df.columns)
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
