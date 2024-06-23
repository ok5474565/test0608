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
        
        # 计算平均值和标准差
        mean_values = df.mean(axis=1)
        std_values = df.std(axis=1)
        
        # 计算差异系数（P 指数），这里 P 值越高表示题目越难
        difficulty_index = 1 - df.mean(axis=1)
        
        # 计算注意系数（D 指数）
        sorted_df = df.apply(lambda x: sorted(x, reverse=True), axis=1)
        upper_group = sorted_df.iloc[:, :len(df.columns)//2]
        lower_group = sorted_df.iloc[:, len(df.columns)//2:]
        discrimination_index = upper_group.mean(axis=1) - lower_group.mean(axis=1)
        
        # 计算相关系数（使用 Pearson 相关系数）
        total_score = df.sum(axis=0)
        correlation_with_total = df.apply(lambda x: x.corr(total_score), axis=1)
        
        # 计算同质性指数（标准化后的方差）
        homogeneity_index = df.var(axis=1) / df.mean(axis=1)
        
        # 显示结果
        st.subheader("分析结果")
        result_df = pd.DataFrame({
            '平均值': mean_values,
            '标准差': std_values,
            '差异系数 (P 指数)': difficulty_index,
            '注意系数 (D 指数)': discrimination_index,
            '相关系数': correlation_with_total,
            '同质性指数': homogeneity_index
        })
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
