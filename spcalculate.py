import streamlit as st
import pandas as pd
import numpy as np

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
        
        # 计算每个学生的总分
        df['total_score'] = df.sum(axis=1)
        
        # 将学生按总分排序
        df_sorted = df.sort_values(by='total_score', ascending=False)
        
        # 取前27%的学生作为高分组，后27%的学生作为低分组
        n_students = len(df_sorted)
        n_upper = int(n_students * 0.27)
        upper_group = df_sorted.iloc[:n_upper, :-1]
        lower_group = df_sorted.iloc[-n_upper:, :-1]
        
        # 计算每个题目的正确率（难度系数 P 指数）
        difficulty_index = df.mean(axis=0)
        
        # 计算每个题目的注意系数 D 指数
        upper_group_mean = upper_group.mean(axis=0)
        lower_group_mean = lower_group.mean(axis=0)
        discrimination_index = upper_group_mean - lower_group_mean
        
        # 去掉 total_score 列，重新计算平均值和标准差
        mean_values = df.iloc[:, :-1].mean(axis=1)
        std_values = df.iloc[:, :-1].std(axis=1)
        
        # 计算相关系数（使用 Pearson 相关系数）
        correlation_matrix = df.iloc[:, :-1].T.corr()
        correlation_with_total = correlation_matrix.mean(axis=1)
        
        # 计算同质性指数（标准化后的方差）
        homogeneity_index = df.iloc[:, :-1].var(axis=1) / df.iloc[:, :-1].mean(axis=1)
        
        # 显示结果
        st.subheader("分析结果")
        result_df = pd.DataFrame({
            '平均值': mean_values,
            '标准差': std_values,
            '难度系数 (P 指数)': difficulty_index,
            '注意系数 (D 指数)': discrimination_index,
            '相关系数': correlation_with_total,
            '同质性指数': homogeneity_index
        })
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
