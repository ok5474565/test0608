import streamlit as st
import pandas as pd
import numpy as np

def calculate_discrimination_index(df):
    # 计算每个学生的总分
    total_scores = df.sum(axis=1)
    
    # 确定高分组和低分组的分界点
    num_students = len(total_scores)
    top_split = num_students * 0.27  # 假设高分组为前27%
    bottom_split = num_students * 0.73  # 假设低分组为后27%
    
    # 获取高分组和低分组的索引
    top_indices = total_scores.nlargest(int(top_split))..index
    bottom_indices = total_scores.nsmallest(int(bottom_split))..index
    
    # 计算高分组和低分组的答对率
    top_group = df.loc[total_scores >= total_scores[top_indices[-1]]]
    bottom_group = df.loc[total_scores <= total_scores[bottom_indices[0]]]
    
    top_correct_rate = (top_group.sum(axis=0) / len(top_indices)).values
    bottom_correct_rate = (bottom_group.sum(axis=0) / len(bottom_indices)).values
    
    # 计算D指数
    d_index = np.divide(top_correct_rate - bottom_correct_rate, bottom_correct_rate, out=np.zeros(len(df.columns)), where=bottom_correct_rate!=0)
    return d_index

def calculate_difficulty_index(df):
    # 计算每个题目的平均答对率
    return df.mean(axis=0)

def calculate_homogeneity_index(df):
    # 计算同质性指数，这里使用标准差与平均值的比值
    return df.std(axis=0) / df.mean(axis=0)

def main():
    st.title("S-P 表格分析工具")
    
    uploaded_file = st.file_uploader("上传 Excel 文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取 Excel 文件
        df = pd.read_excel(uploaded_file)
        
        # 去掉第一行（题目名称）和第一列（学生姓名）
        df = df.iloc[1:, 1:]
        
        # 转置 DataFrame，使其与原始上传的表格结构一致
        df = df.T
        
        # 计算统计量
        mean_values = df.mean(axis=1)
        std_values = df.std(axis=1)
        d_index = calculate_discrimination_index(df)
        p_index = calculate_difficulty_index(df)
        homogeneity_index = calculate_homogeneity_index(df)
        
        # 创建结果表格
        result_df = pd.DataFrame({
            '平均值': mean_values,
            '标准差': std_values,
            '注意系数 (D指数)': d_index,
            '差异系数 (P指数)': p_index,
            '同质性指数': homogeneity_index
        }, index=df.index)
        
        # 显示结果
        st.subheader("分析结果")
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
