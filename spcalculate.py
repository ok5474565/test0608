import streamlit as st
import pandas as pd
import numpy as np

def calculate_difficulty_index(df):
    # 计算差异系数（P指数），即每个题目的平均答对率
    return df.mean(axis=0)

def calculate_discrimination_index(df, num_top=27, num_bottom=27):
    # 计算每个学生的总分
    total_scores = df.sum(axis=1)
    
    # 根据总分排序以划分高分组和低分组
    sorted_student_indices = total_scores.sort_values(ascending=False).index
    top_index = int((len(total_scores) * num_top) / 100)
    bottom_index = int((len(total_scores) * num_bottom) / 100)
    
    # 选择高分组和低分组的学生
    top_group_mask = df.index.isin(sorted_student_indices[-top_index:])
    bottom_group_mask = df.index.isin(sorted_student_indices[:bottom_index])
    
    # 计算高分组和低分组的答对率
    top_group_scores = df.loc[top_group_mask]
    bottom_group_scores = df.loc[bottom_group_mask]
    
    top_group_correct_rate = top_group_scores.mean(axis=0)
    bottom_group_correct_rate = bottom_group_scores.mean(axis=0)
    
    # 注意系数 D 指数计算公式
    # 这里我们使用高分组和低分组的答对率的差值来表示区分度
    d_index = top_group_correct_rate - bottom_group_correct_rate
    
    # 为了避免除以零，我们只返回有有效数据的 D 指数
    valid_d_index = d_index[(d_index >= 0) & (bottom_group_correct_rate > 0)]
    
    return valid_d_index


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
