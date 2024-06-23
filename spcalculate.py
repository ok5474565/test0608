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
        
        # 计算难度系数（P 指数）
        # 难度系数 P 由平均分数决定
        difficulty_index = df.mean(axis=1) / df.max(axis=1)
        
        # 计算注意系数（D 指数）
        # 排序每位学生的分数，分为高分组和低分组，取两组的平均值差作为D指数
        sorted_df = df.apply(lambda x: sorted(x, reverse=True))
        upper_group = sorted_df.iloc[:, :len(df.columns)//2]
        lower_group = sorted_df.iloc[:, len(df.columns)//2:]
        discrimination_index = upper_group.mean(axis=1) - lower_group.mean(axis=1)
        
        # 计算相关系数（使用 Pearson 相关系数）
        correlation_matrix = df.T.corr()
        correlation_with_total = correlation_matrix.mean(axis=1)
        
        # 计算同质性指数（标准化后的方差）
        homogeneity_index = df.var(axis=1) / df.mean(axis=1)
        
        # 显示结果
        st.subheader("分析结果")
        result_df = pd.DataFrame({
            '平均值': df.mean(axis=1),
            '标准差': df.std(axis=1),
            '难度系数 (P 指数)': difficulty_index,
            '注意系数 (D 指数)': discrimination_index,
            '相关系数': correlation_with_total,
            '同质性指数': homogeneity_index
        })
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
